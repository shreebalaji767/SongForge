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
 $('lyrics').addEventListener('input',()=>{if(current){current.lyrics=$('lyrics').value;$('words').textContent=countWords($('lyrics').value)+' words · Unsaved changes';queueDraft()}});
 $('title').addEventListener('input',()=>{if(current){current.title=$('title').value;$('heading').textContent=$('title').value||'Untitled Song';queueDraft()}});
 $('copy').onclick=()=>copy($('lyrics').value);
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
 const parody=$('parody').checked,angle=$('parodystyle').value,seed=hash(topic+genre+mood+Date.now()+Math.random()),sections=(structures[$('structure').value]||structures.standard).slice();
 if($('length').value==='short'){sections.splice(3);if(sections.length>3)sections.length=3}
 if($('length').value==='long')sections.splice(Math.max(2,sections.length-1),0,'[Verse 3]');
 const out=[],moodLines=phrases[mood]||phrases.Hopeful,topicPhrase=topic.replace(/[.!?]+$/,'').toLowerCase();
 sections.forEach((sec,i)=>{
  const lang=langs[i%langs.length],bank=lang.lines||data.languages[0].lines;
  out.push(sec+' — '+lang.name);
  const chorus=/chorus|hook/i.test(sec),n=chorus?4:2;
  for(let j=0;j<n;j++){
   let line;
   if(parody&&lang.id==='en'){const jokes=parodyLines[angle]||parodyLines['Anime / fandom obsession'];line=pick(jokes,seed+i*13+j*7)}
   else if(lang.id==='en'){
    line=pick(moodLines,seed+i*19+j*11);
    if(j===0&&!chorus)line='I turn '+topicPhrase+' into a song tonight';
    if(chorus&&j===0)line='This is our '+topicPhrase+', loud enough to light the sky';
    if(genre==='Rap'||genre==='Hip-Hop'||genre==='Trap'){const rapEnds=['— every setback turns to fuel','— I write my truth across the beat','— no borrowed crown, I make my lane','— one deep breath, then claim my name'];line+=' '+pick(rapEnds,seed+j+i)}
    if(genre==='Metal'||genre==='Rock')line=line.replace(/light|morning|quiet/gi,'fire').replace(/\.$/,'');
    if(genre==='Ballad'||genre==='Soul')line=line.replace(/city lights/g,'soft candlelight');
   }else{line=pick(bank,seed+i*19+j*11)}
   out.push(line);
  }
  out.push('');
 });
 const lyrics=out.join('\n').trim();
 current={id:(globalThis.crypto&&crypto.randomUUID)?crypto.randomUUID():String(Date.now())+'-'+seed,title:topicTitle(topic,seed)+(parody?' (Parody)':''),lyrics,topic,genre,mood,languages:langs.map(l=>l.name),languageIds:langs.map(l=>l.id),languageMode:document.querySelector('input[name=mode]:checked').value,length:$('length').value,structure:$('structure').value,parody,parodyAngle:angle,createdAt:new Date().toISOString(),favorite:false};
 showEditor();queueDraft();notify('Lyrics generated. Edit freely, then save to your library.');
}
function showEditor(){ $('empty').hidden=true;$('editor').hidden=false;$('heading').textContent=current.title;$('title').value=current.title;$('lyrics').value=current.lyrics;$('tags').innerHTML=[current.genre].concat(current.languages||[],[current.mood],current.parody?['Parody']:[]).map(t=>'<span>'+safe(t)+'</span>').join('');$('words').textContent=countWords(current.lyrics)+' words';$('save').textContent=getLib().some(s=>s.id===current.id)?'♥ Saved':'♡ Save'}
function countWords(s){return(s.match(/[\p{L}\p{N}]+/gu)||[]).length}
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
})();