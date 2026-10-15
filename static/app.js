(()=>{'use strict';
const $=id=>document.getElementById(id),KEY='songforge.library.v1',DRAFT='songforge.draft.v2',THEME='songforge.light';
let data={},current=null,toastTimer,draftTimer;
const structures={
 standard:['[Verse 1]','[Chorus]','[Verse 2]','[Bridge]','[Final Chorus]','[Outro]'],
 pop:['[Verse 1]','[Pre-Chorus]','[Chorus]','[Verse 2]','[Chorus]','[Bridge]','[Final Chorus]'],
 rap:['[Intro]','[Verse 1]','[Hook]','[Verse 2]','[Hook]','[Outro]'],
 short:['[Verse]','[Chorus]','[Outro]']
};
const phrases={
 Hopeful:['I turn the page and let the morning in','A thousand small beginnings start to shine','The road is long, but I can learn to fly','I plant a little courage in the light'],
 Heartbroken:['Your echo lingers in the quiet room','I keep our old September in a song','The space you left is louder than the rain','I fold the memories and carry on'],
 Dreamy:['The moon is painting silver on the street','We drift like paper planets through the blue','A secret constellation calls my name','The night is soft enough to hold a dream'],
 Energetic:['We hit the ground like thunder in the night','No slowing down until the skyline glows','Turn every doubt into a battle cry','Our restless hearts are racing with the drums'],
 Melancholic:['The evening leaves its blue upon my hands','Some goodbyes take the long way home','I hear the rain replaying yesterday','A faded photograph still knows my name'],
 Romantic:['Your laughter makes a sunrise of the room','Two shadows dancing underneath the stars','I find my home in every word you say','The whole wide world gets quiet next to you'],
 Angry:['I will not wear the chains you made for me','Let every locked door hear me break the silence','I turn the pressure into gasoline','You wrote the rules, now watch me rewrite them'],
 Triumphant:['I climbed the walls that fear built in my way','The finish line is only one more start','Let every scar become a banner in the sky','I earned this sunrise one step at a time'],
 Nostalgic:['Old summer streets still know the sound of us','A paper note can time-travel through the years','The radio brings back that golden afternoon','We were forever for a little while'],
 Mysterious:['A hidden door is breathing in the wall','The midnight keeps a secret in its sleeve','Footsteps disappear beneath the fog','I follow little sparks where shadows weave'],
 Playful:['My plans went left, my coffee went to space','The cat has filed a complaint against the moon','I brought a map; the map said “good luck, pal”','Today is just a blooper with a beat'],
 Dark:['The city wears a crown of broken glass','A quiet thunder gathers underneath my skin','I shake hands with the ghosts that know my name','The stars look down like witnesses tonight'],
 Peaceful:['The river takes the hurry from my mind','A slow breeze turns the leaves like pages','I let the silence settle in my chest','The world can wait beside this gentle light'],
 Rebellious:['I paint my own horizon on the wall','No borrowed crown can tell me who to be','We make a little noise and call it freedom','I choose the road that nobody designed'],
 Bittersweet:['We laughed so hard the tears became a song','Some endings leave a window open wide','I miss the days and love the way I grew','The sweetest things can sting a little too']
};
const parodyLines={
 'Anime / fandom obsession':['One more episode, then sunrise (that is a lie)','My sleep schedule has entered a new arc','I came for one chapter, now birds are singing','The cliffhanger won; my alarm clock lost'],
 'Everyday-life chaos':['My laundry pile just gained a final boss','I made a to-do list; it asked for a day off','The fridge light knows my midnight secrets','I lost my keys while holding them in my hand'],
 'Internet meme energy':['The group chat says “touch grass”; I sent a meme','My last two brain cells are doing a dance','I went viral in a chat with three close friends','The algorithm knows my snack routine'],
 'Romance satire':['You stole my hoodie and my streaming PIN','Our love language is “what should we eat?”','You said “be yourself”; I sent twelve drafts','My heart said soulmate; my brain said “terms apply”'],
 'Genre exaggeration':['One tiny feeling got a cinematic score','I stubbed my toe; the orchestra appeared','A dramatic wind machine followed me to work','My coffee has a character arc tonight']
};
const multilingualFandom={
 zh:['再看一集，天亮也没关系','我的睡眠时间开启了新篇章','只读一章，窗外鸟儿已经开唱','剧情反转赢了，闹钟彻底投降'],
 ko:['한 편만 더, 해가 떠도 괜찮아','내 수면 시간표도 새 시즌 시작','한 화만 봤는데 새들이 노래해','반전은 이겼고 알람은 졌어'],
 ja:['あと一話だけ、朝でもかまわない','睡眠時間にも新章が始まった','一話だけのはずが鳥まで歌ってる','伏線回収に勝てず目覚ましは敗北'],
 hi:['बस एक एपिसोड और, सुबह हो तो होने दो','मेरी नींद ने भी नया आर्क शुरू कर दिया','एक चैप्टर पढ़ा, अब चिड़ियाँ गा रही हैं','क्लिफहैंगर जीता, अलार्म हार गया'],
 es:['Un episodio más, que amanezca si quiere','Mi horario de sueño estrena otro arco','Vine por un capítulo y cantan los pájaros','Ganó el giro de trama, perdió mi alarma'],
 fr:['Encore un épisode, que le soleil attende','Mon sommeil entame un nouvel arc narratif','Un chapitre de plus, les oiseaux chantent déjà','Le suspense a gagné, mon réveil a perdu'],
 de:['Noch eine Folge, der Morgen kann warten','Mein Schlafrhythmus startet einen neuen Handlungsbogen','Ein Kapitel nur, jetzt singen schon die Vögel','Der Cliffhanger gewann, mein Wecker verlor'],
 pt:['Só mais um episódio, que espere o amanhecer','Meu sono começou um novo arco','Vim por um capítulo e os pássaros já cantam','O suspense venceu, meu despertador perdeu'],
 ar:['حلقة أخرى فقط، فلتنتظر الشمس قليلاً','جدول نومي بدأ موسماً جديداً','جئت لفصل واحد والطيور بدأت الغناء','فاز التشويق وخسر المنبّه'],
 it:['Ancora un episodio, l’alba può aspettare','Il mio sonno inizia un nuovo arco narrativo','Un capitolo soltanto, e gli uccelli già cantano','Ha vinto il colpo di scena, ha perso la sveglia'],
 ru:['Ещё одна серия — рассвет подождёт','Мой режим сна открыл новую сюжетную арку','Зашёл на главу, а птицы уже поют','Клиффхэнгер победил, будильник проиграл']
};
function safe(s){return String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}
function getLib(){try{const v=JSON.parse(localStorage.getItem(KEY)||'[]');return Array.isArray(v)?v:[]}catch(e){return[]}}
function notify(s){$('toast').textContent=s;$('toast').classList.add('show');clearTimeout(toastTimer);toastTimer=setTimeout(()=>$('toast').classList.remove('show'),2400)}
function setSelect(id,arr){$(id).innerHTML=arr.map(x=>'<option value="'+safe(typeof x==='string'?x:x.id)+'">'+safe(typeof x==='string'?x:x.name)+'</option>').join('')}
function selected(){if(document.querySelector('input[name=mode]:checked').value==='single')return[data.languages.find(x=>x.id===$('language').value)||data.languages[0]];return Array.from($('mixed').querySelectorAll('input:checked')).map(i=>data.languages.find(x=>x.id===i.value)).filter(Boolean)}
function init(){fetch('./content/catalog.json').then(r=>{if(!r.ok)throw Error('catalog');return r.json()}).then(d=>{data=d;setSelect('genre',d.genres);setSelect('mood',d.moods);setSelect('language',d.languages);$('mixed').innerHTML=d.languages.map((l,i)=>'<label><input type="checkbox" value="'+safe(l.id)+'" '+(i<2?'checked':'')+'> '+safe(l.name)+'</label>').join('');$('mixed').querySelectorAll('input').forEach(i=>i.addEventListener('change',()=>{if(!$('mixed').querySelector('input:checked'))i.checked=true;queueDraft()}));bind();restoreDraft();updateCount();renderLibrary()}).catch(()=>notify('Could not load the lyric catalog. Open the deployed site or build it first.'))}
function bind(){
 document.querySelectorAll('input[name=mode]').forEach(i=>i.addEventListener('change',()=>{const mix=document.querySelector('input[name=mode]:checked').value==='mixed';$('mixed').hidden=!mix;$('single').hidden=mix;queueDraft()}));
 ['topic','genre','mood','language','length','structure','parody','parodystyle'].forEach(id=>$(id).addEventListener('change',queueDraft));$('topic').addEventListener('input',queueDraft);
 $('generate').onclick=generate;$('remix').onclick=generate;
 $('new').onclick=()=>{if(current&&!confirm('Start a new lyric draft? Your saved songs stay in the library.'))return;current=null;$('editor').hidden=true;$('empty').hidden=false;$('heading').textContent='Your blank canvas';$('save').textContent='♡ Save';clearDraft();};
 $('save').onclick=save;
 $('lyrics').addEventListener('input',()=>{if(current){current.lyrics=$('lyrics').value;$('words').textContent=countWords($('lyrics').value)+' words · Unsaved changes';updateCoach();queueDraft()}});
 $('title').addEventListener('input',()=>{if(current){current.title=$('title').value;$('heading').textContent=$('title').value||'Untitled Song';queueDraft()}});
 $('copy').onclick=()=>copy($('lyrics').value);
 $('copyHook').onclick=()=>{
  const lines=$('lyrics').value.split(/\r?\n/);let active=false,found=false,out=[];
  for(const line of lines){
   if(/^\s*\[.*\]\s*$/.test(line)){active=/chorus|hook/i.test(line);if(active){found=true;out.push(line)}else if(found)break;continue}
   if(active)out.push(line);
  }
  const hook=out.join('\n').trim();if(hook)copy(hook);else notify('No [Chorus] or [Hook] section found.');
 };
 $('cleanLyrics').onclick=()=>{
  const cleaned=$('lyrics').value.split(/\r?\n/).map(line=>line.trimEnd()).join('\n').replace(/^[ \t]+|[ \t]+$/gm,'').replace(/\n{3,}/g,'\n\n').replace(/\n*\s*(\[[^\]]+\])\s*\n*/g,'\n\n$1\n').replace(/^\n+|\n+$/g,'');
  $('lyrics').value=cleaned;if(current)current.lyrics=cleaned;
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
 const hookLang=langs.find(l=>l.id==='en')||langs[0],jokes=parodyLines[angle]||parodyLines['Anime / fandom obsession'];
 const hookLines=parody&&hookLang.id==='en'?jokes.slice():parody&&angle==='Anime / fandom obsession'&&multilingualFandom[hookLang.id]?multilingualFandom[hookLang.id].slice():[
  (hookLang.lines||data.languages[0].lines)[0],
  (hookLang.lines||data.languages[0].lines)[1],
  (hookLang.lines||data.languages[0].lines)[2],
  (hookLang.lines||data.languages[0].lines)[3]
 ];
 const arcs={
  setup:['I turn '+topicPhrase+' into a story tonight','One small choice sets the whole thing in motion','I step inside before I know the rules'],
  rise:['Then every easy answer turns into a maze','Each wrong turn becomes another plot twist','I lose the map but keep the reason why'],
  bridge:['For one brief moment, even the stars go quiet','The truth arrives disguised as one more joke','I change the ending when the door is closed'],
  resolve:['Now every scattered piece is finding place','The next new chapter waits beyond the light','We turn the last page but keep the world alive']
 };
 const out=[],used=new Set(),moodLines=phrases[mood]||phrases.Hopeful;
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
   }else if(angle==='Anime / fandom obsession'&&multilingualFandom[lang.id]){
    lines=[pickFresh(multilingualFandom[lang.id],'localized'+lang.id),pickFresh(multilingualFandom[lang.id],'localized'+lang.id)];
   }else{
    lines=[pickFresh(bank,'parody'+lang.id),pickFresh(bank,'parody'+lang.id)];
   }
  }else if(lang.id==='en'){
   const beat=isBridge?'bridge':i===0?'setup':isVerse?'rise':'resolve';
   lines=[pickFresh(arcs[beat],'arc'+beat),pickFresh(moodLines,'mood'+mood)];
   if(genre==='Rap'||genre==='Hip-Hop'||genre==='Trap')lines=lines.map(line=>line+' — '+pickFresh(['every setback turns to fuel','I write my truth across the beat','no borrowed crown, I make my lane'],'rap'));
   if(genre==='Metal'||genre==='Rock')lines=lines.map(line=>line.replace(/light|morning|quiet/gi,'fire'));
  }else lines=[pickFresh(bank,'lang'+lang.id),pickFresh(bank,'lang'+lang.id)];
  out.push(...lines,'');
 });
 const lyrics=out.join('\n').trim();
 current={id:(globalThis.crypto&&crypto.randomUUID)?crypto.randomUUID():String(Date.now())+'-'+seed,title:topicTitle(topic,seed)+(parody?' (Parody)':''),lyrics,topic,genre,mood,languages:langs.map(l=>l.name),languageIds:langs.map(l=>l.id),languageMode:document.querySelector('input[name=mode]:checked').value,length:$('length').value,structure:$('structure').value,parody,parodyAngle:angle,createdAt:new Date().toISOString(),favorite:false};
 showEditor();queueDraft();notify('Lyrics generated with a consistent repeating hook and connected verse progression.');
}
function showEditor(){ $('empty').hidden=true;$('editor').hidden=false;$('heading').textContent=current.title;$('title').value=current.title;$('lyrics').value=current.lyrics;$('tags').innerHTML=[current.genre].concat(current.languages||[],[current.mood],current.parody?['Parody']:[]).map(t=>'<span>'+safe(t)+'</span>').join('');$('words').textContent=countWords(current.lyrics)+' words';$('save').textContent=getLib().some(s=>s.id===current.id)?'♥ Saved':'♡ Save';updateCoach()}
function ensureCoach(){
 let panel=$('lyricCoach');if(panel)return panel;
 panel=document.createElement('section');panel.id='lyricCoach';panel.className='lyric-coach';panel.setAttribute('aria-live','polite');
 const lyrics=$('lyrics');lyrics.insertAdjacentElement('afterend',panel);return panel;
}
function updateCoach(){
 if(!$('lyrics'))return;
 const raw=$('lyrics').value||'',lines=raw.split(/\r?\n/).map(x=>x.trim()).filter(Boolean),headers=lines.filter(x=>/^\[.*\]$/.test(x));
 let activeSection='';const entries=lines.map(line=>{if(/^\[.*\]$/.test(line))activeSection=line;return{line,section:activeSection}}).filter(x=>!/^\[.*\]$/.test(x.line));
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
function save(){
 if(!current){notify('Generate lyrics first.');return}
 current.title=$('title').value.trim()||'Untitled Song';current.lyrics=$('lyrics').value;current.updatedAt=new Date().toISOString();
 const list=getLib(),idx=list.findIndex(s=>s.id===current.id);if(idx>=0)list[idx]=current;else list.unshift(current);
 try{localStorage.setItem(KEY,JSON.stringify(list));$('save').textContent='♥ Saved';notify('Saved in this browser.');updateCount();renderLibrary();queueDraft()}catch(e){notify('Browser storage is full. Export a backup first.')}
}
function queueDraft(){clearTimeout(draftTimer);draftTimer=setTimeout(persistDraft,180)}
function persistDraft(){try{const d={current:current?{...current,title:$('title').value,lyrics:$('lyrics').value}:null,controls:{topic:$('topic').value,genre:$('genre').value,mood:$('mood').value,language:$('language').value,length:$('length').value,structure:$('structure').value,parody:$('parody').checked,parodystyle:$('parodystyle').value,mode:document.querySelector('input[name=mode]:checked').value,mixed:Array.from($('mixed').querySelectorAll('input:checked')).map(i=>i.value)}};localStorage.setItem(DRAFT,JSON.stringify(d))}catch(e){}}
function restoreDraft(){try{const d=JSON.parse(localStorage.getItem(DRAFT)||'null');if(!d)return;const c=d.controls||{};for(const id of ['topic','genre','mood','language','length','structure','parodystyle'])if(c[id]!==undefined){const el=$(id);if(el.tagName==='TEXTAREA'||Array.from(el.options||[]).some(o=>o.value===String(c[id])))el.value=c[id];}$('parody').checked=!!c.parody;if(c.mode){const radio=document.querySelector('input[name=mode][value="'+c.mode+'"]');if(radio)radio.checked=true}const mix=c.mode==='mixed';$('mixed').hidden=!mix;$('single').hidden=mix;if(Array.isArray(c.mixed))$('mixed').querySelectorAll('input').forEach(i=>i.checked=c.mixed.includes(i.value));if(d.current&&d.current.lyrics){current=d.current;showEditor();notify('Your last draft was restored.')}}catch(e){localStorage.removeItem(DRAFT)}}
function clearDraft(){localStorage.removeItem(DRAFT)}
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
 else{current={...s};$('topic').value=s.topic||'';$('genre').value=s.genre||data.genres[0];$('mood').value=s.mood||data.moods[0];$('parody').checked=!!s.parody;if(s.parodyAngle)$('parodystyle').value=s.parodyAngle;if(s.length)$('length').value=s.length;if(s.structure)$('structure').value=s.structure;const ids=s.languageIds||[];if(ids.length){if(ids.length===1){document.querySelector('input[name=mode][value="single"]').checked=true;$('single').hidden=false;$('mixed').hidden=true;$('language').value=ids[0]}else{document.querySelector('input[name=mode][value="mixed"]').checked=true;$('single').hidden=true;$('mixed').hidden=false;$('mixed').querySelectorAll('input').forEach(i=>i.checked=ids.includes(i.value))}}showEditor();view('studio');queueDraft();return}
 try{localStorage.setItem(KEY,JSON.stringify(list));updateCount();renderLibrary()}catch(e){notify('Could not update library storage.')}
}
function slug(s){return(s||'song').toLowerCase().normalize('NFKD').replace(/[^\p{L}\p{N}]+/gu,'-').replace(/^-|-$/g,'').slice(0,80)||'song'}
function download(text,name,type){const a=document.createElement('a'),url=URL.createObjectURL(new Blob([text],{type}));a.href=url;a.download=name;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000)}
async function copy(text){try{await navigator.clipboard.writeText(text);notify('Lyrics copied')}catch(e){const ta=document.createElement('textarea');ta.value=text;document.body.append(ta);ta.select();const ok=document.execCommand('copy');ta.remove();notify(ok?'Lyrics copied':'Copy failed — select and copy the lyrics manually')}}
function restore(e){const f=e.target.files[0];if(!f)return;const reader=new FileReader();reader.onload=()=>{try{const parsed=JSON.parse(reader.result),arr=Array.isArray(parsed)?parsed:parsed.songs;if(!Array.isArray(arr))throw Error('shape');const map=new Map(getLib().map(s=>[s.id,s]));arr.forEach((s,i)=>{if(s&&typeof s.title==='string'&&typeof s.lyrics==='string')map.set(s.id||('restored-'+Date.now()+'-'+i),s)});localStorage.setItem(KEY,JSON.stringify(Array.from(map.values())));updateCount();renderLibrary();notify('Backup restored')}catch(e){notify('Invalid SongForge backup file')}e.target.value=''};reader.readAsText(f)}
init();
if('serviceWorker' in navigator && location.protocol!=='file:'){
 window.addEventListener('load',()=>navigator.serviceWorker.register('./sw.js').catch(()=>{}));
}
})();