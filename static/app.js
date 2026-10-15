(()=>{'use strict';
const $=id=>document.getElementById(id),KEY='songforge.library.v1',DRAFT='songforge.draft.v2',THEME='songforge.light';
let data={},current=null,toastTimer,draftTimer,deferredInstallPrompt=null,historyTimer,lyricHistory=[],lyricHistoryIndex=-1;
const structures={
 standard:['[Verse 1]','[Chorus]','[Verse 2]','[Bridge]','[Final Chorus]','[Outro]'],
 pop:['[Verse 1]','[Pre-Chorus]','[Chorus]','[Verse 2]','[Chorus]','[Bridge]','[Final Chorus]'],
 rap:['[Intro]','[Verse 1]','[Hook]','[Verse 2]','[Hook]','[Outro]'],
 short:['[Verse]','[Chorus]','[Outro]']
};
function safe(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function isSectionHeader(line){return /^\s*\[[^\]]+\](?:\s+[—–-]\s+.+)?\s*$/.test(String(line??''))}
function normalizeSong(s,fallbackId){if(!s||typeof s!=='object'||Array.isArray(s)||typeof s.title!=='string'||typeof s.lyrics!=='string')return null;const strings=v=>Array.isArray(v)?v.filter(x=>typeof x==='string').slice(0,100):[];return{...s,id:typeof s.id==='string'&&s.id.trim()?s.id.slice(0,160):fallbackId,title:s.title.slice(0,200),lyrics:s.lyrics.slice(0,200000),topic:typeof s.topic==='string'?s.topic.slice(0,2000):'',genre:typeof s.genre==='string'?s.genre.slice(0,80):'',mood:typeof s.mood==='string'?s.mood.slice(0,80):'',languages:strings(s.languages),languageIds:strings(s.languageIds),favorite:!!s.favorite,createdAt:typeof s.createdAt==='string'?s.createdAt:new Date().toISOString(),updatedAt:typeof s.updatedAt==='string'?s.updatedAt:undefined}}
function getLib(){try{const v=JSON.parse(localStorage.getItem(KEY)||'[]');return Array.isArray(v)?v.map((s,i)=>normalizeSong(s,'legacy-'+i)).filter(Boolean):[]}catch(e){return[]}}
function notify(s){$('toast').textContent=s;$('toast').classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').classList.remove('show'),2400)}
function setSelect(id,arr){$(id).innerHTML=arr.map(x=>'<option value="'+safe(typeof x==='string'?x:x.id)+'">'+safe(typeof x==='string'?x:x.name)+'</option>').join('')}
function selected(){if(document.querySelector('input[name=mode]:checked').value==='single')return[data.languages.find(x=>x.id===$('language').value)||data.languages[0]];return Array.from($('mixed').querySelectorAll('input:checked')).map(i=>data.languages.find(x=>x.id===i.value)).filter(Boolean)}
function loadJson(path,label){return fetch(path,{cache:'no-cache'}).then(response=>{if(!response.ok)throw Error(label+' returned HTTP '+response.status+' ('+path+')');return response.json()}).catch(error=>{console.error('[SongForge] '+label+' load failed:',error);throw error})}
function init(){Promise.all([loadJson('./content/catalog.json','Catalog'),loadJson('./content/lyric_engine.json','Lyric engine')]).then(([catalog,lyricEngine])=>{if(!Array.isArray(catalog.languages)||!catalog.languages.length||!Array.isArray(catalog.genres)||!Array.isArray(catalog.moods))throw Error('The catalog JSON is missing required data.');if(!lyricEngine.phrases||!lyricEngine.parodyLines||!lyricEngine.arcs||!lyricEngine.rhymeDictionary)throw Error('The lyric engine JSON is missing required data.');data={...catalog,lyricEngine};setSelect('genre',data.genres);setSelect('mood',data.moods);setSelect('language',data.languages);$('mixed').innerHTML=data.languages.map((l,i)=>'<label><input type="checkbox" value="'+safe(l.id)+'" '+(i<2?'checked':'')+'> '+safe(l.name)+'</label>').join('');$('mixed').querySelectorAll('input').forEach(i=>i.addEventListener('change',()=>{if(!$('mixed').querySelector('input:checked'))i.checked=true;queueDraft()}));bind();restoreDraft();updateCount();renderLibrary()}).catch(error=>notify('SongForge could not initialize: '+(error&&error.message?error.message:'check the catalog and lyric engine JSON files.')))}
function setupInstallPrompt(){
 const button=$('installPwa');if(!button)return;
 const standalone=()=>window.matchMedia('(display-mode: standalone)').matches||window.navigator.standalone===true;
 const refresh=()=>{button.textContent=standalone()?'✓ App Installed':'⇩ Install App';button.setAttribute('aria-label',standalone()?'SongForge is installed':'Install SongForge app')};
 refresh();
 window.addEventListener('beforeinstallprompt',event=>{event.preventDefault();deferredInstallPrompt=event;button.classList.add('install-ready');button.textContent='⇩ Install App'});
 window.addEventListener('appinstalled',()=>{deferredInstallPrompt=null;refresh();notify('SongForge installed successfully.')});
 button.addEventListener('click',async()=>{
  if(standalone()){notify('SongForge is already installed.');return}
  if(deferredInstallPrompt){
   deferredInstallPrompt.prompt();
   const choice=await deferredInstallPrompt.userChoice;
   deferredInstallPrompt=null;
   if(choice&&choice.outcome==='accepted')notify('SongForge installation accepted.');
   else notify('Installation was cancelled. You can install it later.');
   return;
  }
  const ios=/iphone|ipad|ipod/i.test(navigator.userAgent);
  if(ios)notify('To install: tap Share, then “Add to Home Screen”.');
  else if(!window.isSecureContext)notify('Install requires HTTPS. Open the GitHub Pages HTTPS website.');
  else notify('If your browser supports installation, use its menu and choose “Install app” or “Add to Home screen”.');
 });
}
function bind(){
 document.querySelectorAll('input[name=mode]').forEach(i=>i.addEventListener('change',()=>{const mix=document.querySelector('input[name=mode]:checked').value==='mixed';$('mixed').hidden=!mix;$('single').hidden=mix;queueDraft()}));
 ['topic','genre','mood','language','length','structure','verseLines','rhymeScheme','parody','parodystyle'].forEach(id=>$(id).addEventListener('change',queueDraft));$('topic').addEventListener('input',queueDraft);
 $('generate').onclick=generate;$('remix').onclick=generate;
 $('new').onclick=()=>{if(current&&!confirm('Start a new lyric draft? Your saved songs stay in the library.'))return;current=null;$('editor').hidden=true;$('empty').hidden=false;$('heading').textContent='Your blank canvas';$('save').textContent='♡ Save';clearDraft();};
 $('save').onclick=save;
 $('lyrics').addEventListener('input',()=>{if(current){current.lyrics=$('lyrics').value;$('words').textContent=countWords($('lyrics').value)+' words · Unsaved changes';updateCoach();queueLyricHistory($('lyrics').value);queueDraft()}});
 $('title').addEventListener('input',()=>{if(current){current.title=$('title').value;$('heading').textContent=$('title').value||'Untitled Song';queueDraft()}});
 $('undoLyrics').onclick=()=>moveLyricHistory(-1);$('redoLyrics').onclick=()=>moveLyricHistory(1);
 $('findRhymes').onclick=findRhymes;$('rhymeWord').addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault();findRhymes()}});setupInstallPrompt();
 $('copy').onclick=()=>copy($('lyrics').value);
 $('copyHook').onclick=()=>{
  const lines=$('lyrics').value.split(/\r?\n/);let active=false,found=false,out=[];
  for(const line of lines){
   if(isSectionHeader(line)){const header=(line.match(/^\s*\[([^\]]+)\]/)||[])[1]||'';active=/chorus|hook/i.test(header);if(active){found=true;out.push(line)}else if(found)break;continue}
   if(active)out.push(line);
  }
  const hook=out.join('\n').trim();if(hook)copy(hook);else notify('No [Chorus] or [Hook] section found.');
 };
 $('cleanLyrics').onclick=()=>{
  const before=$('lyrics').value;const cleaned=before.split(/\r?\n/).map(line=>line.trimEnd()).join('\n').replace(/^[ \t]+|[ \t]+$/gm,'').replace(/\n{3,}/g,'\n\n').replace(/^\n+|\n+$/g,'');
  clearTimeout(historyTimer);commitLyricHistory(before);$('lyrics').value=cleaned;commitLyricHistory(cleaned);if(current)current.lyrics=cleaned;
  $('words').textContent=countWords(cleaned)+' words · Formatting cleaned';updateCoach();queueDraft();notify('Whitespace cleaned; lyric wording preserved.');
 };
 $('download').onclick=()=>download(songText(),slug($('title').value||'song')+'.txt','text/plain;charset=utf-8');
 $('exportMd').onclick=()=>download('# '+($('title').value.trim()||'Untitled Song')+'\n\n'+$('lyrics').value,slug($('title').value||'song')+'.md','text/markdown;charset=utf-8');
 $('theme').onclick=()=>{document.body.classList.toggle('light');localStorage.setItem(THEME,document.body.classList.contains('light')?'1':'0')};
 document.querySelectorAll('[data-prompt]').forEach(b=>b.onclick=()=>{$('topic').value=b.dataset.prompt;generate()});
 document.querySelectorAll('[data-view]').forEach(b=>b.onclick=()=>view(b.dataset.view));
 $('search').oninput=renderLibrary;$('filterFavorites').onchange=renderLibrary;
 $('backup').onclick=()=>download(JSON.stringify({format:'songforge-backup',version:2,songs:getLib()},null,2),'songforge-backup.json','application/json');
 $('restore').onclick=()=>$('file').click();$('file').onchange=restore;
 document.addEventListener('keydown',e=>{if((e.ctrlKey||e.metaKey)&&e.key.toLowerCase()==='s'){e.preventDefault();save()}if((e.ctrlKey||e.metaKey)&&e.key==='Enter'&&$('studio').hidden===false){e.preventDefault();generate()}});
 if(localStorage.getItem(THEME)==='1')document.body.classList.add('light');
}
function findRhymes(){
 const input=$('rhymeWord'),out=$('rhymeResults'),word=(input.value||'').toLocaleLowerCase().trim().replace(/[^a-z'-]/g,'');
 if(!word){out.textContent='Enter an English word to search the offline rhyme dictionary.';return}
 const dict=(data.lyricEngine&&data.lyricEngine.rhymeDictionary)||{};
 let family=Object.entries(dict).find(([,words])=>words.some(w=>w.toLocaleLowerCase()===word));
 if(!family)family=Object.entries(dict).find(([key,words])=>!/\d/.test(key)&&word.endsWith(key)&&words.some(w=>w.toLocaleLowerCase()!==word));
 if(!family){const tail=word.slice(-2);family=Object.entries(dict).find(([,words])=>words.some(w=>w.toLocaleLowerCase().endsWith(tail)&&w.toLocaleLowerCase()!==word))}
 if(!family){out.textContent='No close match in the built-in dictionary. Try a common word or a different ending.';return}
 const matches=Array.from(new Set(family[1].filter(w=>w.toLocaleLowerCase()!==word))).slice(0,24);
 out.replaceChildren();
 const note=document.createElement('span');note.className='rhyme-family';note.textContent='Family: '+family[0]+' · '+matches.length+' suggestions';out.append(note);
 const chips=document.createElement('div');chips.className='rhyme-chips';
 matches.forEach(w=>{const b=document.createElement('button');b.type='button';b.className='rhyme-chip';b.textContent=w;b.title='Use '+w+' as the search word';b.onclick=()=>{input.value=w;findRhymes()};chips.append(b)});
 out.append(chips);
}
function hash(s){let h=2166136261;for(let i=0;i<s.length;i++)h=Math.imul(h^s.charCodeAt(i),16777619);return h>>>0}
function pick(a,n){return a[Math.abs(n)%a.length]}
function topicTitle(topic,seed){const words=topic.replace(/[^\p{L}\p{N}\s'-]/gu,' ').trim().split(/\s+/).filter(Boolean).slice(0,4);if(!words.length)return pick(['Neon Afterglow','Paper Moons','Electric Heart','Almost Tomorrow','Midnight Echoes','A Thousand Little Stars'],seed);return words.map(w=>w.charAt(0).toLocaleUpperCase()+w.slice(1)).join(' ')}
function generate(){
 if(!data.languages)return;
 const topic=$('topic').value.trim()||'following a dream through the night',genre=$('genre').value,mood=$('mood').value,langs=selected().filter(Boolean);
 if(!langs.length){notify('Select at least one language.');return}
 const parody=$('parody').checked,angle=$('parodystyle').value,seed=hash(topic+'|'+genre+'|'+mood+'|'+Date.now()+'|'+Math.random()),sections=(structures[$('structure').value]||structures.standard).slice();
 if($('length').value==='short'){
  const first=sections.find(x=>/intro|verse/i.test(x))||'[Verse]';
  const hook=sections.find(x=>/chorus|hook/i.test(x))||'[Chorus]';
  sections.splice(0,sections.length,first,hook,'[Outro]');
 }
 if($('length').value==='long'&&!sections.some(x=>/verse 3/i.test(x)))sections.splice(Math.max(2,sections.length-1),0,'[Verse 3]');
 const topicPhrase=topic.replace(/[.!?]+$/,'').replace(/\s+/g,' ').toLowerCase();
 const engine=data.lyricEngine,hookLang=langs.find(l=>l.id==='en')||langs[0],jokes=engine.parodyLines[angle]||engine.parodyLines['Anime / fandom obsession'];
 let hookLines=parody&&hookLang.id==='en'?jokes.slice():parody&&angle==='Anime / fandom obsession'&&engine.multilingualFandom[hookLang.id]?engine.multilingualFandom[hookLang.id].slice():[
  (hookLang.lines||data.languages[0].lines)[0],
  (hookLang.lines||data.languages[0].lines)[1],
  (hookLang.lines||data.languages[0].lines)[2],
  (hookLang.lines||data.languages[0].lines)[3]
 ];
 if(!parody&&hookLang.id==='en'&&engine.rhymeSchemes&&engine.rhymeSchemes[$('rhymeScheme').value]&&engine.rhymeSchemes[$('rhymeScheme').value].length){
  hookLines=engine.rhymeSchemes[$('rhymeScheme').value].map(line=>line.replace('{topic}',topicPhrase));
 }
 const arcs=engine.arcs;
 const out=[],used=new Set(),moodLines=engine.phrases[mood]||engine.phrases.Hopeful;
 function pickFresh(bank,key){const fresh=bank.map((v,i)=>({v,i})).filter(x=>!used.has(key+x.i));const pool=fresh.length?fresh:bank.map((v,i)=>({v,i}));const x=pool[Math.abs(seed+used.size*13)%pool.length];used.add(key+x.i);return x.v}
 sections.forEach((sec,i)=>{
  const isHook=/chorus|hook/i.test(sec),isBridge=/bridge/i.test(sec),isVerse=/verse/i.test(sec);
  const lang=isHook?hookLang:langs[i%langs.length],bank=lang.lines||data.languages[0].lines;
  out.push(sec+' — '+lang.name);
  let lines;
  if(isHook)lines=hookLines;
  else if(parody){
   if(lang.id==='en'){
    lines=[pickFresh(jokes,'joke'),pickFresh(jokes,'joke')];
    if(isVerse)lines[0]=i===0?'I opened '+topicPhrase+' for a minute or two':'The plot got more complicated than my plans';
   }else if(angle==='Anime / fandom obsession'&&engine.multilingualFandom[lang.id]){
    lines=[pickFresh(engine.multilingualFandom[lang.id],'localized'+lang.id),pickFresh(engine.multilingualFandom[lang.id],'localized'+lang.id)];
   }else{
    lines=[pickFresh(bank,'parody'+lang.id),pickFresh(bank,'parody'+lang.id)];
   }
  }else if(lang.id==='en'){
   const beat=isBridge?'bridge':i===0?'setup':isVerse?'rise':'resolve';
   lines=[pickFresh(arcs[beat],'arc'+beat).replace('{topic}',topicPhrase),pickFresh(moodLines,'mood'+mood)];
   if(genre==='Rap'||genre==='Hip-Hop'||genre==='Trap')lines=lines.map(line=>line+' — '+pickFresh(['every setback turns to fuel','I write my truth across the beat','no borrowed crown, I make my lane'],'rap'));
   if(genre==='Metal'||genre==='Rock')lines=lines.map(line=>line.replace(/light|morning|quiet/gi,'fire'));
  }else lines=[pickFresh(bank,'lang'+lang.id),pickFresh(bank,'lang'+lang.id)];
  if(isVerse&&!isHook){const target=Math.max(2,Math.min(8,Number($('verseLines').value)||4));while(lines.length<target){if(lang.id==='en'&&!parody)lines.push(pickFresh(moodLines,'verseExtraMood'+i));else if(parody&&lang.id==='en')lines.push(pickFresh(jokes,'verseExtraJoke'+i));else lines.push(pickFresh(bank,'verseExtraLang'+lang.id));}lines=lines.slice(0,target)}
  out.push(...lines,'');
 });
 const lyrics=out.join('\n').trim();
 current={id:(globalThis.crypto&&crypto.randomUUID)?crypto.randomUUID():String(Date.now())+'-'+seed,title:topicTitle(topic,seed)+(parody?' (Parody)':''),lyrics,topic,genre,mood,languages:langs.map(l=>l.name),languageIds:langs.map(l=>l.id),languageMode:document.querySelector('input[name=mode]:checked').value,length:$('length').value,structure:$('structure').value,rhymeScheme:$('rhymeScheme').value,verseLines:Number($('verseLines').value)||4,parody,parodyAngle:angle,createdAt:new Date().toISOString(),favorite:false};
 showEditor();queueDraft();notify('Lyrics generated locally with your selected rhyme pattern.');
}
function showEditor(){ $('empty').hidden=true;$('editor').hidden=false;$('heading').textContent=current.title;$('title').value=current.title;$('lyrics').value=current.lyrics;resetLyricHistory(current.lyrics);$('tags').innerHTML=[current.genre].concat(current.languages||[],[current.mood],current.parody?['Parody']:[]).map(t=>'<span>'+safe(t)+'</span>').join('');$('words').textContent=countWords(current.lyrics)+' words';$('save').textContent=getLib().some(s=>s.id===current.id)?'♥ Saved':'♡ Save';updateCoach()}
function ensureCoach(){
 let panel=$('lyricCoach');if(panel)return panel;
 panel=document.createElement('section');panel.id='lyricCoach';panel.className='lyric-coach';panel.setAttribute('aria-live','polite');
 const lyrics=$('lyrics');lyrics.insertAdjacentElement('afterend',panel);return panel;
}
function updateCoach(){
 if(!$('lyrics'))return;
 const raw=$('lyrics').value||'',lines=raw.split(/\r?\n/).map(x=>x.trim()).filter(Boolean),headers=lines.filter(isSectionHeader);
 let activeSection='';const entries=lines.map(line=>{if(isSectionHeader(line))activeSection=(line.match(/^\s*(\[[^\]]+\])/)||[])[1]||line;return{line,section:activeSection}}).filter(x=>!isSectionHeader(x.line));
 const body=entries.map(x=>x.line),norm=entries.filter(x=>!/chorus|hook/i.test(x.section)).map(x=>x.line.toLocaleLowerCase().replace(/[^\p{L}\p{N}]+/gu,' ').trim()).filter(Boolean);
 const seen=new Set(),dupes=[];norm.forEach(line=>{if(seen.has(line)&&!dupes.includes(line))dupes.push(line);seen.add(line)});
 const hasHook=headers.some(x=>/chorus|hook/i.test(x)),avg=body.length?body.reduce((n,x)=>n+countWords(x),0)/body.length:0;
 const english=current&&Array.isArray(current.languageIds)?current.languageIds.includes('en'):true;
 const verseLines=entries.filter(x=>!/chorus|hook/i.test(x.section)).map(x=>x.line);
 const rhymeGroups={};if(english)verseLines.forEach(line=>{const words=line.toLowerCase().match(/[a-z]+/g)||[];if(!words.length)return;const word=words[words.length-1],key=rhymeKey(word);if(key)(rhymeGroups[key]||(rhymeGroups[key]=[])).push(word)});
 const rhymePairs=Object.entries(rhymeGroups).filter(([,words])=>new Set(words).size>1);
 const syllables=english?verseLines.map(syllableCount).filter(n=>n>0):[];
 const syllableRange=syllables.length?Math.max(...syllables)-Math.min(...syllables):0;
 let score=100,tips=[];
 if(body.length<8){score-=20;tips.push('Add more lyric lines to develop the idea.')}
 if(!hasHook){score-=12;tips.push('Add a [Chorus] or [Hook] section to give listeners an anchor.')}
 if(dupes.length){score-=Math.min(30,dupes.length*15);tips.push('Review repeated lines outside an intentional chorus: '+dupes.slice(0,2).join(' / ')+'.')}
 if(headers.length<3){score-=10;tips.push('Try a clearer section arc: verse, hook, and bridge or outro.')}
 if(avg>0&&avg<4){score-=8;tips.push('Most lines are very short; try mixing short punches with longer phrases.')}
 if(avg>15){score-=8;tips.push('Several lines are long; split them to improve singability.')}
 const topic=(current&&current.topic||$('topic').value||'').toLocaleLowerCase().split(/[^\p{L}\p{N}]+/u).filter(w=>w.length>3);
 const found=topic.filter(w=>raw.toLocaleLowerCase().includes(w));
 if(topic.length&&!found.length){score-=8;tips.push('The topic wording is hard to spot; add a concrete image or phrase from your prompt.')}
 if(!tips.length)tips.push('No obvious structure or repetition issues detected. Read aloud to check natural rhythm and meaning.');
 score=Math.max(0,Math.min(100,score));
 const panel=ensureCoach();panel.replaceChildren();
 const head=document.createElement('div');head.className='coach-head';
 const title=document.createElement('strong');title.textContent='Lyric Coach · Draft checks';
 const grade=document.createElement('span');grade.className='coach-score';grade.textContent=score+'/100';
 head.append(title,grade);panel.append(head);
 const stats=document.createElement('p');stats.className='coach-stats';stats.textContent=headers.length+' sections · '+body.length+' lyric lines · '+dupes.length+' repeated line'+(dupes.length===1?'':'s')+' · '+Math.round(avg)+' words/line';panel.append(stats);
 const list=document.createElement('ul');tips.forEach(t=>{const li=document.createElement('li');li.textContent=t;list.append(li)});panel.append(list);
 const flow=document.createElement('p');flow.className='coach-stats';
 if(english){
  const rhymeText=rhymePairs.length?rhymePairs.slice(0,3).map(([key,words])=>key+': '+Array.from(new Set(words)).slice(0,4).join(' / ')).join(' · '):'No clear end-rhyme groups detected yet.';
  flow.textContent='Rhyme scan: '+rhymePairs.length+' possible rhyme group'+(rhymePairs.length===1?'':'s')+' · estimated syllables/line: '+(syllables.length?Math.round(syllables.reduce((a,b)=>a+b,0)/syllables.length):0)+' average · '+(syllableRange>7?'wide syllable spread—try reading lines aloud':'syllable spread looks manageable')+'. '+rhymeText;
 }else flow.textContent='Rhyme scan is available for English lines; read other languages aloud to check their natural rhythm.';
 panel.append(flow);
 const note=document.createElement('small');note.textContent='Heuristic checks only—not a judgment of artistic quality, rhyme accuracy, or translation quality.';panel.append(note);
}
function countWords(s){return(s.match(/[\p{L}\p{N}]+/gu)||[]).length}
function rhymeKey(word){
 const w=(word||'').toLocaleLowerCase().replace(/[^a-z]/g,'');
 if(w.length<3)return '';
 const endings=['ation','ition','ight','ound','ough','eart','air','are','ore','ower','ower','ame','ance','ence','ound','ound','ound','ain','ake','ate','ell','est','end','old','ost','ing','ong','uck','ush','ide','ove','ime','all','own','ay','ee','ow','oo','ue','ear','ire','ore','art','ent','ill','ink','ash','ack','ump'];
 const ending=endings.sort((a,b)=>b.length-a.length).find(x=>w.endsWith(x));
 return ending||w.slice(-3);
}
function syllableCount(line){
 const words=(line.toLowerCase().match(/[a-z]+/g)||[]);
 return words.reduce((sum,word)=>{
  if(word.length<=3)return sum+1;
  let w=word.replace(/(?:[^laeiouy]es|ed|[^laeiouy]e)$/,'').replace(/^y/,'');
  const groups=w.match(/[aeiouy]+/g);
  return sum+Math.max(1,groups?groups.length:1);
 },0);
}
function songText(){return($('title').value.trim()||'Untitled Song')+'\n\n'+$('lyrics').value}
function resetLyricHistory(value){clearTimeout(historyTimer);lyricHistory=[String(value??'')];lyricHistoryIndex=0;updateHistoryButtons()}
function commitLyricHistory(value){value=String(value??'');if(lyricHistory[lyricHistoryIndex]===value)return;lyricHistory=lyricHistory.slice(0,lyricHistoryIndex+1);lyricHistory.push(value);if(lyricHistory.length>100)lyricHistory.shift();lyricHistoryIndex=lyricHistory.length-1;updateHistoryButtons()}
function queueLyricHistory(value){clearTimeout(historyTimer);historyTimer=setTimeout(()=>commitLyricHistory(value),500)}
function updateHistoryButtons(){const undo=$('undoLyrics'),redo=$('redoLyrics');if(!undo||!redo)return;undo.disabled=lyricHistoryIndex<=0;redo.disabled=lyricHistoryIndex<0||lyricHistoryIndex>=lyricHistory.length-1}
function moveLyricHistory(step){clearTimeout(historyTimer);const value=$('lyrics').value;if(value!==lyricHistory[lyricHistoryIndex])commitLyricHistory(value);const next=lyricHistoryIndex+step;if(next<0||next>=lyricHistory.length){updateHistoryButtons();return}lyricHistoryIndex=next;$('lyrics').value=lyricHistory[lyricHistoryIndex];if(current)current.lyrics=$('lyrics').value;$('words').textContent=countWords($('lyrics').value)+' words · Unsaved changes';updateCoach();updateHistoryButtons();queueDraft()}
function save(){
 if(!current){notify('Generate lyrics first.');return}
 current.title=$('title').value.trim()||'Untitled Song';current.lyrics=$('lyrics').value;current.updatedAt=new Date().toISOString();
 const list=getLib(),idx=list.findIndex(s=>s.id===current.id);if(idx>=0)list[idx]=current;else list.unshift(current);
 try{localStorage.setItem(KEY,JSON.stringify(list));$('save').textContent='♥ Saved';notify('Saved in this browser.');updateCount();renderLibrary();queueDraft()}catch(e){notify('Browser storage is full. Export a backup first.')}
}
function queueDraft(){clearTimeout(draftTimer);draftTimer=setTimeout(persistDraft,180)}
function persistDraft(){try{const d={current:current?{...current,title:$('title').value,lyrics:$('lyrics').value}:null,controls:{topic:$('topic').value,genre:$('genre').value,mood:$('mood').value,language:$('language').value,length:$('length').value,structure:$('structure').value,verseLines:$('verseLines').value,rhymeScheme:$('rhymeScheme').value,parody:$('parody').checked,parodystyle:$('parodystyle').value,mode:document.querySelector('input[name=mode]:checked').value,mixed:Array.from($('mixed').querySelectorAll('input:checked')).map(i=>i.value)}};localStorage.setItem(DRAFT,JSON.stringify(d))}catch(e){}}
function restoreDraft(){try{const d=JSON.parse(localStorage.getItem(DRAFT)||'null');if(!d)return;const c=d.controls||{};for(const id of ['topic','genre','mood','language','length','structure','verseLines','rhymeScheme','parodystyle'])if(c[id]!==undefined){const el=$(id);if(el.tagName==='TEXTAREA'||Array.from(el.options||[]).some(o=>o.value===String(c[id])))el.value=c[id];}$('parody').checked=!!c.parody;if(c.mode){const radio=document.querySelector('input[name=mode][value="'+c.mode+'"]');if(radio)radio.checked=true}const mix=c.mode==='mixed';$('mixed').hidden=!mix;$('single').hidden=mix;if(Array.isArray(c.mixed))$('mixed').querySelectorAll('input').forEach(i=>i.checked=c.mixed.includes(i.value));if(d.current&&d.current.lyrics){current=d.current;showEditor();notify('Your last draft was restored.')}}catch(e){try{localStorage.removeItem(DRAFT)}catch(_){}}}
function clearDraft(){try{localStorage.removeItem(DRAFT)}catch(e){}}
function updateCount(){$('count').textContent=getLib().length}
function view(v){$('studio').hidden=v!=='studio';$('library').hidden=v!=='library';document.querySelectorAll('[data-view]').forEach(b=>b.classList.toggle('active',b.dataset.view===v));if(v==='library')renderLibrary();window.scrollTo(0,0)}
function renderLibrary(){
 if(!$('songs'))return;
 const q=$('search').value.toLowerCase(),fav=$('filterFavorites').value==='favorites';
 const list=getLib().filter(s=>(!fav||s.favorite)&&(s.title+' '+s.topic+' '+s.genre+' '+(s.languages||[]).join(' ')).toLowerCase().includes(q)).sort((a,b)=>new Date(b.updatedAt||b.createdAt||0)-new Date(a.updatedAt||a.createdAt||0));
 $('songs').innerHTML=list.map(s=>'<article class="songcard"><h3>'+safe(s.title)+'</h3><div class="meta">'+safe(s.genre||'')+' · '+safe((s.languages||[]).join(' + '))+(s.parody?' · Parody':'')+'</div><p>'+safe((s.lyrics||'').slice(0,220))+'</p><button data-action="open" data-id="'+safe(s.id)+'">Edit</button><button data-action="fav" data-id="'+safe(s.id)+'">'+(s.favorite?'♥ Favorite':'♡ Favorite')+'</button><button data-action="duplicate" data-id="'+safe(s.id)+'">Duplicate</button><button data-action="delete" data-id="'+safe(s.id)+'">Delete</button></article>').join('');
 $('libempty').hidden=list.length>0;$('songs').querySelectorAll('button').forEach(b=>b.onclick=()=>libraryAction(b.dataset.action,b.dataset.id));
}
function libraryAction(action,id){
 let list=getLib(),s=list.find(x=>x.id===id);if(!s)return;
 if(action==='delete'){if(!confirm('Delete this saved lyric?'))return;list=list.filter(x=>x.id!==id)}
 else if(action==='fav'){s.favorite=!s.favorite}
 else if(action==='duplicate'){const copySong={...s,id:String(Date.now())+'-'+Math.random().toString(36).slice(2,8),title:s.title+' (Copy)',createdAt:new Date().toISOString(),updatedAt:new Date().toISOString(),favorite:false};list.unshift(copySong);notify('A copy was added to your library.')}
 else{current={...s};$('topic').value=s.topic||'';$('genre').value=s.genre||data.genres[0];$('mood').value=s.mood||data.moods[0];$('parody').checked=!!s.parody;if(s.parodyAngle)$('parodystyle').value=s.parodyAngle;if(s.length)$('length').value=s.length;if(s.structure)$('structure').value=s.structure;if(s.verseLines)$('verseLines').value=String(s.verseLines);if(s.rhymeScheme)$('rhymeScheme').value=s.rhymeScheme;const ids=s.languageIds||[];if(ids.length){if(ids.length===1){document.querySelector('input[name=mode][value="single"]').checked=true;$('single').hidden=false;$('mixed').hidden=true;$('language').value=ids[0]}else{document.querySelector('input[name=mode][value="mixed"]').checked=true;$('single').hidden=true;$('mixed').hidden=false;$('mixed').querySelectorAll('input').forEach(i=>i.checked=ids.includes(i.value))}}showEditor();view('studio');queueDraft();return}
 try{localStorage.setItem(KEY,JSON.stringify(list));updateCount();renderLibrary()}catch(e){notify('Could not update library storage.')}
}
function slug(s){return(s||'song').toLowerCase().normalize('NFKD').replace(/[^\p{L}\p{N}]+/gu,'-').replace(/^-|-$/g,'').slice(0,80)||'song'}
function download(text,name,type){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([text],{type}));a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000)}
async function copy(text){try{await navigator.clipboard.writeText(text);notify('Lyrics copied')}catch(e){const ta=document.createElement('textarea');ta.value=text;document.body.append(ta);ta.select();const ok=document.execCommand('copy');ta.remove();notify(ok?'Lyrics copied':'Copy failed — select and copy the lyrics manually')}}
function restore(e){const f=e.target.files[0];if(!f)return;if(f.size>5*1024*1024){notify('Backup is too large (maximum 5 MB).');e.target.value='';return}const reader=new FileReader();reader.onload=()=>{try{const parsed=JSON.parse(reader.result),arr=Array.isArray(parsed)?parsed:parsed.songs;if(!Array.isArray(arr))throw Error('shape');const incoming=arr.map((s,i)=>normalizeSong(s,'restored-'+Date.now()+'-'+i)).filter(Boolean);if(!incoming.length)throw Error('empty');const map=new Map(getLib().map(s=>[s.id,s]));incoming.forEach(s=>map.set(s.id,s));localStorage.setItem(KEY,JSON.stringify(Array.from(map.values())));updateCount();renderLibrary();notify('Backup restored: '+incoming.length+' song'+(incoming.length===1?'':'s'))}catch(e){notify('Invalid backup or browser storage is full. No songs were imported.')}finally{e.target.value=''}};reader.onerror=()=>{notify('Could not read the selected backup file.');e.target.value=''};reader.readAsText(f)}
init();
if('serviceWorker' in navigator && location.protocol!=='file:'){
 window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(()=>{}));
}
})();