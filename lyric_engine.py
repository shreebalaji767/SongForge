#!/usr/bin/env python3
"""Free, deterministic Python lyric engine and static-data builder for SongForge.

The hosted site stays static: this module writes JSON at build time. No AI,
network calls, paid APIs, or runtime Python server are used.
"""
from __future__ import annotations
import argparse
import json
import random
import re
from pathlib import Path

PHRASES = {
 "Hopeful":["I turn the page and let the morning in","A thousand small beginnings start to shine","The road is long, but I can learn to fly","I plant a little courage in the light"],
 "Heartbroken":["Your echo lingers in the quiet room","I keep our old September in a song","The space you left is louder than the rain","I fold the memories and carry on"],
 "Dreamy":["The moon is painting silver on the street","We drift like paper planets through the blue","A secret constellation calls my name","The night is soft enough to hold a dream"],
 "Energetic":["We hit the ground like thunder in the night","No slowing down until the skyline glows","Turn every doubt into a battle cry","Our restless hearts are racing with the drums"],
 "Melancholic":["The evening leaves its blue upon my hands","Some goodbyes take the long way home","I hear the rain replaying yesterday","A faded photograph still knows my name"],
 "Romantic":["Your laughter makes a sunrise of the room","Two shadows dancing underneath the stars","I find my home in every word you say","The whole wide world gets quiet next to you"],
 "Angry":["I will not wear the chains you made for me","Let every locked door hear me break the silence","I turn the pressure into gasoline","You wrote the rules, now watch me rewrite them"],
 "Triumphant":["I climbed the walls that fear built in my way","The finish line is only one more start","Let every scar become a banner in the sky","I earned this sunrise one step at a time"],
 "Nostalgic":["Old summer streets still know the sound of us","A paper note can time-travel through the years","The radio brings back that golden afternoon","We were forever for a little while"],
 "Mysterious":["A hidden door is breathing in the wall","The midnight keeps a secret in its sleeve","Footsteps disappear beneath the fog","I follow little sparks where shadows weave"],
 "Playful":["My plans went left, my coffee went to space","The cat has filed a complaint against the moon","I brought a map; the map said good luck, pal","Today is just a blooper with a beat"],
 "Dark":["The city wears a crown of broken glass","A quiet thunder gathers underneath my skin","I shake hands with the ghosts that know my name","The stars look down like witnesses tonight"],
 "Peaceful":["The river takes the hurry from my mind","A slow breeze turns the leaves like pages","I let the silence settle in my chest","The world can wait beside this gentle light"],
 "Rebellious":["I paint my own horizon on the wall","No borrowed crown can tell me who to be","We make a little noise and call it freedom","I choose the road that nobody designed"],
 "Bittersweet":["We laughed so hard the tears became a song","Some endings leave a window open wide","I miss the days and love the way I grew","The sweetest things can sting a little too"]
}
PARODY = {
 "Anime / fandom obsession":[
  "One more episode, then sunrise (that is a lie)","My sleep schedule has entered a new arc","I came for one chapter, now birds are singing","The cliffhanger won; my alarm clock lost","I paused to get a snack and missed three plot twists","My watchlist needs its own apartment","The hero trained less than I refreshed the page","I said one episode; the season heard twenty","My blanket knows the opening theme by heart","The credits rolled; my bedtime filed a complaint","I memorized the lore but forgot my own lunch","My favorite character has more screen time in my head","The recap is short; my theories need a book","I bought one volume and adopted the whole shelf","My alarm said get up; the fandom said one more","I can explain the magic system, not my sleep debt","The plot twist hit harder than my morning coffee","I came for the art and stayed for the emotional damage","My tabs have formed a very niche committee","The finale ended; my imaginary sequel began","I called it research; my homework called it betrayal","My wallet fears every limited-edition release","I know the side characters better than my neighbors","The next arc starts after I pretend to be productive",
  "My watch history has more seasons than my life plan",
  "I know the opening song but not today's date",
  "The recap ended; my detective board began",
  "I called it a quick binge; the sun disagreed",
  "My fictional crush has better communication skills",
  "The manga shelf is now load-bearing architecture",
  "I skipped one page and invented three conspiracies",
  "My free time has been acquired by the next episode",
  "The subtitle delay created a brand-new plot twist",
  "I paused the finale to emotionally prepare for the finale",
  "My fan theory has footnotes and absolutely no evidence",
  "The merch arrived before my responsibilities did",
  "I speak fluent lore and beginner-level small talk",
  "My weekend schedule is just release dates in disguise",
  "I promised to sleep after the arc; the arc had sequels",
  "My browser tabs are a museum of unfinished cliffhangers"
 ],
 "Everyday-life chaos":[
  "My laundry pile just gained a final boss","I made a to-do list; it asked for a day off","The fridge light knows my midnight secrets","I lost my keys while holding them in my hand","My coffee got cold while I searched for my coffee","The dishes formed a union and elected a spokesperson","I cleaned one drawer; the whole room wants a sequel","My calendar sent a meeting invite to my nap","I bought a planner to organize my other planners","The grocery list said milk; I came home with snacks","My houseplants look disappointed in my life choices","I folded one shirt and called it personal growth","The vacuum ate a sock and denied everything","My alarm and I are no longer on speaking terms","I opened one email and unlocked seven new problems","The bin is full; apparently that is a future-me issue",
  "My clean laundry is living in the basket ecosystem",
  "I opened the fridge like it might have new content",
  "My budget saw the checkout total and logged off",
  "I cleaned for five minutes and needed a recovery episode",
  "The delivery tracker has become my main relationship",
  "I went shopping for one thing and adopted seventeen",
  "My phone is at one percent and so is my patience",
  "I put the important note somewhere very important",
  "The leftovers have outlived three meal plans",
  "My calendar is just apologies with timestamps",
  "I made a quick snack and used every pan I own",
  "The laundry timer and I have different definitions of done",
  "I arrived early, then spent ten minutes finding the room",
  "My plant is thriving out of pure spite",
  "I searched for my glasses while wearing them",
  "Future me has filed a complaint about present me"
 ],
 "Internet meme energy":[
  "The group chat says touch grass; I sent a meme","My last two brain cells are doing a dance","I went viral in a chat with three close friends","The algorithm knows my snack routine","I typed LOL with a completely neutral face","My screen-time report just called an intervention","I sent a voice note long enough to need chapters","The Wi-Fi blinked once; I saw my entire life flash","I opened one short video and lost a whole afternoon","My camera roll is ninety percent screenshots of jokes","I said quick reply, then wrote a small novel","The typing bubble vanished; now I need closure","I have twelve tabs open and no idea why","My password hint is now a philosophical question","I muted the group chat; the memes found another route","My digital detox sent me a push notification",
  "My draft folder is a graveyard of perfect comebacks",
  "I sent one sticker and the chat declared a holiday",
  "The algorithm served me my own personality back",
  "My focus mode is ignoring me with impressive consistency",
  "I opened the comments and lost faith in punctuation",
  "My online cart is practicing financial fiction",
  "I watched a tutorial to avoid doing the actual task",
  "The notification badge has achieved sentience",
  "I typed 'haha' while making the face of a tax auditor",
  "My feed refreshed and my plans evaporated",
  "I took a screen break to look at another screen",
  "The meme was niche but my commitment was global",
  "I left one unread message to preserve the mystery",
  "My digital footprint needs comfortable walking shoes",
  "I said log off, then checked one last thing",
  "My search history could host a very confusing quiz show"
 ],
 "Romance satire":[
  "You stole my hoodie and my streaming PIN","Our love language is what should we eat","You said be yourself; I sent twelve drafts","My heart said soulmate; my brain said terms apply","You asked where this is going; I opened a spreadsheet","We share one brain cell and a family streaming plan","You left me on read; I wrote a trilogy in my head","Our first date had more plot twists than a season finale","You said choose a movie; now the sun is coming up","I made a pros-and-cons list; your smile broke the chart","You sent a heart emoji; I checked its legal meaning","We flirt like two shy robots with a software update","You called me your person; I saved the screenshot twice","I practiced saying I love you and accidentally said Wi-Fi","You met my parents; my anxiety brought a PowerPoint","Our couple selfie took more takes than a feature film","You said we need space; I measured the living room","I wrote you a love song; autocorrect made it a breakup","Your goodnight text arrived; I analyzed every punctuation mark","We made a shared calendar for spontaneous romance","You stole one fry; I reconsidered our entire future","My love is unconditional, except when you eat my leftovers","I made a playlist; you shuffled past my emotional arc","You said trust your heart; mine requested two-factor login",
  "We split the bill and merged our streaming accounts",
  "You said 'I'm fine' and my spreadsheet turned red",
  "Our anniversary reminder arrived with a software update",
  "I flirted confidently, then waved at the wrong person",
  "You know my coffee order and my browser password hint",
  "We planned a quiet night; the group chat filed an appeal",
  "Your playlist skipped my song and I requested mediation",
  "I sent a voice note with director's commentary",
  "We define spontaneity as booking dinner without a poll",
  "You borrowed my charger and gained diplomatic immunity",
  "Our relationship status needs a terms-and-conditions page",
  "I said 'miss you' then checked your location in my memory",
  "You left a crumb in bed; romance entered arbitration",
  "We picked a wedding song before picking a restaurant",
  "My love notes have version history and tracked changes",
  "You said 'whatever you want' and the quest began again"
 ],
 "Genre exaggeration":[
  "One tiny feeling got a cinematic score","I stubbed my toe; the orchestra appeared","A dramatic wind machine followed me to work","My coffee has a character arc tonight","I missed one bus; the soundtrack turned tragic","A minor inconvenience got a twelve-part documentary","I dropped a spoon; the heavens issued a warning","My grocery trip needs a director's cut","I sent one text with the force of a thousand drums","The toaster popped; I heard the final boss theme","I lost one sock; the violins began to weep","A tiny plot twist summoned a choir from the clouds","My Monday got a budget bigger than a blockbuster","I spilled some tea; the narrator said previously on","One awkward wave deserved a slow-motion replay",
  "My tiny sigh came with a stadium reverb",
  "I made toast like the fate of kingdoms depended on it",
  "The door creaked and the brass section filed in",
  "I lost a pen and summoned a tragic backstory",
  "My commute received a full orchestral overture",
  "The microwave beeped like the end of civilization",
  "I tripped on air; the camera pulled back dramatically",
  "A minor typo triggered the director's commentary",
  "I opened a spreadsheet and the choir hit a high note",
  "The weather app announced rain like a prophecy",
  "My inbox filled up; the violins demanded hazard pay",
  "I missed a turn and the narrator whispered destiny",
  "The elevator stopped; the soundtrack entered act three",
  "I dropped a grape and the slow-motion budget doubled",
  "My lunch break ended with a season-finale cliffhanger",
  "The printer blinked and the villain theme began","The printer jammed; the soundtrack entered its villain era"
 ]
}
FANDOM = {
 "zh":["再看一集，天亮也没关系","我的睡眠时间开启了新篇章","只读一章，窗外鸟儿已经开唱","剧情反转赢了，闹钟彻底投降"],
 "ko":["한 편만 더, 해가 떠도 괜찮아","내 수면 시간표도 새 시즌 시작","한 화만 봤는데 새들이 노래해","반전은 이겼고 알람은 졌어"],
 "ja":["あと一話だけ、朝でもかまわない","睡眠時間にも新章が始まった","一話だけのはずが鳥まで歌ってる","伏線回収に勝てず目覚ましは敗北"],
 "hi":["बस एक एपिसोड और, सुबह हो तो होने दो","मेरी नींद ने भी नया आर्क शुरू कर दिया","एक चैप्टर पढ़ा, अब चिड़ियाँ गा रही हैं","क्लिफहैंगर जीता, अलार्म हार गया"],
 "es":["Un episodio más, que amanezca si quiere","Mi horario de sueño estrena otro arco","Vine por un capítulo y cantan los pájaros","Ganó el giro de trama, perdió mi alarma"],
 "fr":["Encore un épisode, que le soleil attende","Mon sommeil entame un nouvel arc narratif","Un chapitre de plus, les oiseaux chantent déjà","Le suspense a gagné, mon réveil a perdu"],
 "de":["Noch eine Folge, der Morgen kann warten","Mein Schlafrhythmus startet einen neuen Handlungsbogen","Ein Kapitel nur, jetzt singen schon die Vögel","Der Cliffhanger gewann, mein Wecker verlor"],
 "pt":["Só mais um episódio, que espere o amanhecer","Meu sono começou um novo arco","Vim por um capítulo e os pássaros já cantam","O suspense venceu, meu despertador perdeu"],
 "ar":["حلقة أخرى فقط، فلتنتظر الشمس قليلاً","جدول نومي بدأ موسماً جديداً","جئت لفصل واحد والطيور بدأت الغناء","فاز التشويق وخسر المنبّه"],
 "it":["Ancora un episodio, l’alba può aspettare","Il mio sonno inizia un nuovo arco narrativo","Un capitolo soltanto, e gli uccelli già cantano","Ha vinto il colpo di scena, ha perso la sveglia"],
 "ru":["Ещё одна серия — рассвет подождёт","Мой режим сна открыл новую сюжетную арку","Зашёл на главу, а птицы уже поют","Клиффхэнгер победил, будильник проиграл"]
}
ARCS = {
 "setup":["I turn {topic} into a story tonight","One small choice sets the whole thing in motion","I step inside before I know the rules"],
 "rise":["Then every easy answer turns into a maze","Each wrong turn becomes another plot twist","I lose the map but keep the reason why"],
 "bridge":["For one brief moment, even the stars go quiet","The truth arrives disguised as one more joke","I change the ending when the door is closed"],
 "resolve":["Now every scattered piece is finding place","The next new chapter waits beyond the light","We turn the last page but keep the world alive"]
}

# Curated Simplified Chinese resources use native Mandarin idiom and short,
# singable phrases instead of translated English sentence templates.
LOCALIZED_PHRASES = {
 "zh": {
  "Hopeful": ["把明天写进今天的愿望", "跌倒几次，也要抬头看远方", "风再大，心里的灯也别关", "走慢一点，也能走到想去的地方"],
  "Heartbroken": ["你走以后，房间安静得不像话", "聊天记录还在，故事却停下", "我把没说完的话留给晚风回答", "原来最难删掉的，是习惯啊"],
  "Dreamy": ["月光把街角照成一片海", "晚风路过，把心事轻轻吹开", "闭上眼，银河就在窗外", "梦慢慢落下来，刚好被我接住"],
  "Energetic": ["鼓点一响，今天就别想拦我", "把烦恼甩开，跟着节奏跳", "心跳踩着拍子，热血刚刚好", "这一路再难，我也要跑到最闪耀"],
  "Melancholic": ["雨落在窗台，像旧事回来", "有些告别，连回声都走得很慢", "那首老歌还在，听的人换了心态", "天色暗下来，思念才敢摊开"],
  "Romantic": ["你一笑，整条街都变得可爱", "想把平常日子，和你慢慢过成花海", "人海那么大，我偏偏认得你的对白", "晚饭吃什么不重要，有你就很精彩"],
  "Angry": ["别拿你的规矩来替我安排", "我不欠谁一个乖乖听话的姿态", "把委屈攒成鼓点，今晚全都摊开", "我的路我自己走，不用谁来批改"],
  "Triumphant": ["走过的弯路，终于有了回响", "把每道伤疤，都唱成勋章", "曾经不敢想的，如今就在前方", "这一刻的光，配得上一路的倔强"],
  "Nostalgic": ["老街的风还记得那年夏天", "旧照片里，笑得比现在更坦然", "那首歌一响，青春就坐回身边", "有些日子走远了，还是舍不得说再见"],
  "Mysterious": ["午夜的风把答案藏进巷口", "路灯闪了三下，像有人点头", "门后那阵脚步，不肯说它要去哪走", "越是没有答案，越想追到最后"],
  "Playful": ["今天的计划，是先快乐再说", "奶茶少了珍珠，我的世界失落", "我说马上出门，结果还在找袜子", "人生像开盲盒，拆开全是小波折"],
  "Dark": ["城市把沉默藏进霓虹背后", "黑夜很深，我偏不低头", "影子跟着我，却猜不透我心头", "等风暴散场，我要亲手点亮宇宙"],
  "Peaceful": ["让风替我把急事慢慢带走", "云走得很慢，心也不必赶路", "把今天放轻，听树叶轻轻点头", "世界再忙，也留一刻给自己停留"],
  "Rebellious": ["不走别人画好的那条线", "把标签撕掉，我有自己的语言", "别替我写结局，我偏要改篇", "哪怕逆着风，也要唱出我的宣言"],
  "Bittersweet": ["笑着说再见，眼眶却先泄了密", "有些遗憾，后来也成了勇气", "甜的回忆里，总藏着一点可惜", "我们没走到最后，却认真爱过彼此"]
 }
}
LOCALIZED_PARODY = {
 "zh": {
  "Anime / fandom obsession": [
   "说好只追一集，抬头已经星期一", "番还没完结，我的黑眼圈先出圈",
   "本来只想补个番，结果直接补到天亮", "角色还在成长，我先被作业打败",
   "追番像修仙，睡眠全靠渡劫", "收藏夹越来越长，人生计划越来越短",
   "我说最后一集，弹幕说你想得美", "本命角色一登场，我的理智全退场",
   "别人追星要签名，我追番只想续命", "动漫教我热血，闹钟教我面对现实",
   "课本翻两页就困，漫画翻两百页精神", "更新提醒一响，我的意志力当场下线",
   "追到凌晨三点，早八像最终 Boss", "新角色刚登场，我的钱包先投降",
   "现实没有字幕，我只能靠脑补续命", "别人睡前数羊，我睡前数更新日",
   "主线还没通关，我先把周边买齐", "我不是不社交，只是番剧刚好更新",
   "二次元负责心动，三次元负责打卡", "我不是熬夜，是在和剧情交换人生"
  ],
  "Everyday-life chaos": [
   "我列了待办清单，清单让我先冷静", "衣服洗完没晾，直接开启第二轮人生",
   "进厨房只想煮面，最后洗了五口锅", "找手机找半天，原来一直拿在手里",
   "冰箱开了又关，像在等它刷新库存", "我说明天早起，明天表示不接受安排",
   "房间只收拾五分钟，休息却安排了半天", "外卖还在路上，我已经看完三集",
   "钱包说要自律，购物车说再等等", "闹钟响了八遍，我和现实还没和解",
   "我买了个收纳盒，专门收纳没收纳的东西", "拖延不是没计划，是计划明天再执行",
   "我把闹钟设得很早，起床时间另有安排", "本想省点钱，结果买了个省钱课程",
   "洗衣机转完一圈，我的人生还没转过弯", "我说马上开始，马上已经过了半小时",
   "今天只做一件事，先把待办写成十件事", "桌面清得很干净，文件全在下载文件夹", "我把休息排进日程，结果忙着安排休息", "我把事情拖到最后，最后开始催我自己"
  ],
  "Internet meme energy": [
   "群聊叫我去睡觉，我回了个表情包", "我发了个哈哈，脸上没有一点变化",
   "消息撤回得很快，尴尬加载得很慢", "已读不回四个字，够我脑补一整季",
   "刷视频说五分钟，抬头天都快亮了", "网速卡了一秒，我的人生开始走马灯",
   "朋友圈都在自律，我在给外卖写好评", "我开了专注模式，手机当场表示反对",
   "收藏的干货很多，真正学会的只有收藏", "我的表情包库存，比社交能力丰富",
   "本想戒网一天，结果先发了条动态", "通知红点不消失，我的强迫症不下班",
   "我把手机放远一点，手却自动导航过去", "网上冲浪两小时，现实里一句话没说",
   "打字删了又打，最后只发一个表情", "我说不看评论，手指已经滑到热评",
   "社恐在线很活跃，线下只会点头微笑", "我把生活发成动态，自己却忘了体验", "我以为自己隐身了，结果点赞暴露了行踪", "撤回的是消息，留下的是悬念"
  ],
  "Romance satire": [
   "你回了个句号，我开始复盘整个宇宙", "你说随便吃什么，我们走到店都没决定",
   "你穿走我的外套，还顺走我的会员", "你说做自己，我先发了十二版草稿",
   "我问我们算什么，你说先把饭吃了", "你说晚安，我研究标点到凌晨三点",
   "恋爱没有说明书，我却想找客服问问", "你说我想太多，我写了份报告反驳",
   "你拿走最后一块炸鸡，爱情进入冷静期", "你说马上到，我连下集预告都看完了",
   "我把心交给你，你把外卖地址发给我", "我想制造惊喜，先建了个投票群",
   "你说想吃点特别的，最后还是点了老三样", "我练习浪漫开场，结果问你医保交了没",
   "你把我置顶聊天，我把你置顶外卖", "恋爱最难的考试，是猜今晚吃什么",
   "你说想要仪式感，我给你做了预算表", "我本想说句情话，出口变成记得带伞", "你说听我的，我听完还是不知道吃什么", "你回了个表情，我的情绪开始股价波动"
  ],
  "Genre exaggeration": [
   "我摔了一跤，脑内响起史诗交响曲", "咖啡洒了一滴，命运突然开始铺垫",
   "电梯停了三秒，我以为大结局来了", "丢了一支笔，背景音乐立刻变悲情",
   "打印机卡了纸，反派主题曲自动播放", "外卖晚了十分钟，我的内心拍完连续剧",
   "打了个喷嚏，仿佛触发隐藏剧情", "表格打开那一刻，合唱团从天而降",
   "袜子少了一只，悬疑片正式开场", "手机只剩百分之一，末日感拉满",
   "周一刚上线，整座城市都像慢动作", "我只是叹口气，脑内已经开了演唱会",
   "门吱呀响了一声，导演说气氛到位", "忘带一把伞，剧情立刻进入暴雨篇",
   "打翻一杯水，慢镜头拍了三百遍", "老板发来一个问号，悬疑配乐立刻响起",
   "电量掉到百分五，末日字幕开始滚动", "只是迟到两分钟，内心演完谢幕曲",
   "我把小事说得像史诗，预算全花在鼓点里", "连喝口水都要配乐，我的人生制作费超支"
  ]
 }
}
LOCALIZED_RAP = {
 "zh": [
  "鼓点一落，废话全删，今天我来掌舵",
  "把烦恼押韵，顺手把坏心情没收",
  "嘴上说随缘，脚下每一步都算数",
  "不靠天降主角光环，我自己写字幕",
  "节奏踩稳，心气拉满，别叫我认输",
  "把不甘写进拍子，让沉默也有态度",
  "这一段不求满分，只求活得够酷",
  "现实爱出难题，我就现场改题目",
  "把冷眼当鼓掌，把逆风当伴奏",
  "我不等谁来救场，我自己就是主秀",
  "字字落地，句句有劲，别拿模板套我",
  "今天不当背景板，镜头现在归我",
  "先把气势开满，再把借口关掉",
  "不必人人点赞，我照样唱到破晓",
  "每次跌倒都采样，剪进下一段节奏",
  "我的人生不混音，主旋律由我掌控"
 ]
}

RHYME_DICTIONARY = {
  "ight": [
    "bright",
    "flight",
    "light",
    "night",
    "sight",
    "might",
    "right",
    "write",
    "fight",
    "height",
    "tonight",
    "ignite",
    "delight",
    "midnight",
    "starlight"
  ],
  "ay": [
    "away",
    "day",
    "gray",
    "play",
    "say",
    "stay",
    "way",
    "display",
    "betray",
    "decay",
    "delay",
    "array",
    "today",
    "okay",
    "sway"
  ],
  "ame": [
    "aim",
    "blame",
    "came",
    "claim",
    "flame",
    "game",
    "name",
    "same",
    "shame",
    "frame",
    "became",
    "rename",
    "tame",
    "fame"
  ],
  "art": [
    "art",
    "cart",
    "heart",
    "part",
    "start",
    "smart",
    "chart",
    "depart",
    "restart",
    "apart",
    "dart",
    "impart"
  ],
  "air": [
    "air",
    "care",
    "dare",
    "fair",
    "flare",
    "glare",
    "hair",
    "pair",
    "share",
    "stare",
    "there",
    "where",
    "aware",
    "repair",
    "compare"
  ],
  "ore": [
    "adore",
    "before",
    "door",
    "floor",
    "more",
    "shore",
    "score",
    "store",
    "roar",
    "explore",
    "restore",
    "ignore",
    "encore",
    "core"
  ],
  "own": [
    "alone",
    "known",
    "grown",
    "shown",
    "throne",
    "tone",
    "stone",
    "home",
    "roam",
    "chrome",
    "overgrown",
    "unknown"
  ],
  "ound": [
    "around",
    "bound",
    "found",
    "ground",
    "sound",
    "wound",
    "crowned",
    "down",
    "town",
    "renowned",
    "profound",
    "unbound"
  ],
  "ain": [
    "again",
    "brain",
    "chain",
    "crane",
    "gain",
    "lane",
    "pain",
    "rain",
    "remain",
    "train",
    "plain",
    "domain",
    "explain",
    "refrain"
  ],
  "ee": [
    "be",
    "free",
    "key",
    "me",
    "sea",
    "see",
    "tree",
    "three",
    "we",
    "agree",
    "believe",
    "release",
    "beneath",
    "dreamy"
  ],
  "ove": [
    "above",
    "glove",
    "love",
    "dove",
    "shove",
    "thereof",
    "enough",
    "rough",
    "tough",
    "stuff",
    "of"
  ],
  "ell": [
    "bell",
    "fell",
    "hell",
    "sell",
    "shell",
    "smell",
    "spell",
    "swell",
    "tell",
    "well",
    "compel",
    "farewell",
    "parallel"
  ],
  "end": [
    "bend",
    "blend",
    "end",
    "friend",
    "lend",
    "mend",
    "send",
    "spend",
    "trend",
    "weekend",
    "defend",
    "pretend",
    "transcend"
  ],
  "old": [
    "bold",
    "cold",
    "fold",
    "gold",
    "hold",
    "old",
    "sold",
    "told",
    "unfold",
    "behold",
    "threshold",
    "controlled"
  ],
  "ing": [
    "bring",
    "cling",
    "king",
    "ring",
    "sing",
    "spring",
    "swing",
    "thing",
    "wing",
    "string",
    "beginning",
    "everything",
    "awakening"
  ],
  "all": [
    "all",
    "call",
    "fall",
    "hall",
    "small",
    "wall",
    "crawl",
    "install",
    "recall",
    "overall",
    "waterfall",
    "freefall"
  ],
  "est": [
    "best",
    "chest",
    "guest",
    "jest",
    "quest",
    "rest",
    "test",
    "west",
    "confessed",
    "manifest",
    "protest",
    "request"
  ],
  "ime": [
    "chime",
    "climb",
    "crime",
    "dime",
    "lifetime",
    "rhyme",
    "time",
    "prime",
    "slime",
    "sublime",
    "paradigm"
  ],
  "ide": [
    "aside",
    "bride",
    "hide",
    "ride",
    "side",
    "slide",
    "stride",
    "tide",
    "wide",
    "provide",
    "inside",
    "collide"
  ],
  "ack": [
    "back",
    "black",
    "crack",
    "track",
    "stack",
    "snack",
    "pack",
    "attack",
    "comeback",
    "flashback",
    "unpack"
  ],
  "ush": [
    "blush",
    "brush",
    "crush",
    "flush",
    "hush",
    "rush",
    "slush",
    "trust",
    "just",
    "adjust",
    "discuss"
  ],
  "ow": [
    "allow",
    "brow",
    "how",
    "now",
    "plow",
    "pow",
    "vow",
    "wow",
    "somehow",
    "somehow",
    "endow"
  ],
  "ear": [
    "appear",
    "clear",
    "dear",
    "ear",
    "fear",
    "hear",
    "near",
    "year",
    "sincere",
    "disappear",
    "frontier"
  ],
  "ate": [
    "create",
    "fate",
    "gate",
    "late",
    "plate",
    "state",
    "wait",
    "celebrate",
    "elevate",
    "translate",
    "generate"
  ],
  "ore2": [
    "shore",
    "more",
    "core",
    "before",
    "explore",
    "restore",
    "encore",
    "roar",
    "door",
    "adore"
  ]
}

RHYME_SCHEMES = {
 "Free verse": [],
 "AABB": [
  "I turn {topic} into a spark tonight",
  "We chase that spark until it shines bright",
  "Each little step becomes a brand-new start",
  "We sing the next line straight from the heart"
 ],
 "ABAB": [
  "I carry {topic} into the night",
  "I find the courage deep within",
  "We turn the shadows into light",
  "And let a brand-new day begin"
 ]
}
ENGINE = {"version":7,"phrases":PHRASES,"parodyLines":PARODY,"multilingualFandom":FANDOM,"localizedPhrases":LOCALIZED_PHRASES,"localizedParody":LOCALIZED_PARODY,"localizedRap":LOCALIZED_RAP,"arcs":ARCS,"rhymeSchemes":RHYME_SCHEMES,"rhymeDictionary":RHYME_DICTIONARY}



def normalize_lyric_line(line: str) -> str:
    """Normalize a lyric line for duplicate detection without stripping Unicode letters."""
    return re.sub(r"[^\w]+", " ", line.casefold(), flags=re.UNICODE).strip()


def rhyme_key(word: str) -> str:
    """Return a conservative offline English rhyme family, preferring curated families."""
    word = re.sub(r"[^a-z]", "", (word or "").casefold())
    if len(word) < 2:
        return ""
    for family, words in RHYME_DICTIONARY.items():
        if word in {candidate.casefold() for candidate in words}:
            return family
    endings = sorted(
        (ending for ending in RHYME_DICTIONARY if not ending[-1:].isdigit()),
        key=len, reverse=True,
    )
    for ending in endings:
        if len(ending) >= 3 and word.endswith(ending):
            return ending
    return word[-2:] if len(word) >= 4 else ""


def end_rhyme_pairs(lines: list[str]) -> list[tuple[str, str]]:
    """Return distinct end-word pairs sharing a curated rhyme family."""
    groups: dict[str, list[str]] = {}
    for line in lines:
        words = re.findall(r"[A-Za-z']+", line)
        if words:
            word = words[-1].strip("'")
            key = rhyme_key(word)
            if key:
                groups.setdefault(key, []).append(word.casefold())
    return [
        (key, " / ".join(dict.fromkeys(words)))
        for key, words in groups.items()
        if len(set(words)) > 1
    ]


def _quality_fallbacks(language: str) -> list[str]:
    """Pool unused local lines to repair accidental repeats without network calls."""
    if language == "zh":
        pools = list(LOCALIZED_PHRASES.get("zh", {}).values())
        lines = [line for bank in pools for line in bank]
        lines += list(LOCALIZED_RAP.get("zh", []))
        lines += [line for bank in LOCALIZED_PARODY.get("zh", {}).values() for line in bank]
        return lines
    lines = [line for bank in PHRASES.values() for line in bank]
    lines += [line for bank in ARCS.values() for line in bank]
    lines += [line for bank in PARODY.values() for line in bank]
    lines += [line for bank in LOCALIZED_RAP.values() for line in bank]
    return lines


def avoid_duplicate_lines(lyrics: str, language: str = "en", seed: int | None = None) -> str:
    """Replace accidental repeated lyric lines; section labels and repeated hooks are exempt."""
    rng = random.Random(seed)
    fallback = list(dict.fromkeys(_quality_fallbacks(language)))
    rng.shuffle(fallback)
    used: set[str] = set()
    section = ""
    output: list[str] = []
    for line in lyrics.splitlines():
        if line.startswith("[") and "]" in line:
            section = line[1:line.index("]")].casefold()
            output.append(line)
            continue
        if not line.strip():
            output.append(line)
            continue
        key = normalize_lyric_line(line)
        intentional_hook = "chorus" in section or "hook" in section
        if key and key in used and not intentional_hook:
            replacement = next(
                (candidate for candidate in fallback
                 if normalize_lyric_line(candidate) not in used
                 and normalize_lyric_line(candidate) != key),
                None,
            )
            if replacement:
                line = replacement
                key = normalize_lyric_line(line)
        if key:
            used.add(key)
        output.append(line)
    return "\n".join(output)


def build_static_data(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(ENGINE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def generate_lyrics(topic: str, mood: str="Hopeful", genre: str="Pop", parody: bool=False, seed: int|None=None, rhyme_scheme: str="Free verse", verse_lines: int=4, language: str="en", parody_angle: str="Anime / fandom obsession") -> str:
    """Generate a complete lyric draft locally; zh uses curated native-Mandarin banks."""
    rng = random.Random(seed)
    topic = re.sub(r"\s+", " ", topic.strip()).rstrip(".!?") or "following a dream through the night"
    verse_lines = max(2, min(8, int(verse_lines)))
    mood_lines = PHRASES.get(mood, PHRASES["Hopeful"])

    if language == "zh":
        zh_topic = topic if re.search(r"[\u4e00-\u9fff]", topic) else "今晚的心事"
        zh_moods = LOCALIZED_PHRASES["zh"]
        zh_lines = zh_moods.get(mood, zh_moods["Hopeful"])
        if parody:
            bank = list(LOCALIZED_PARODY["zh"].get(parody_angle, LOCALIZED_PARODY["zh"]["Anime / fandom obsession"]))
            chorus_lines = bank[:4]
            available = [line for line in bank if line not in chorus_lines]
            verse1 = rng.sample(available, k=verse_lines)
            remaining = [line for line in available if line not in verse1]
            verse2 = rng.sample(remaining, k=verse_lines)
        else:
            topic_lines = [f"今晚这首歌，就唱给{zh_topic}听", f"把{zh_topic}写进今晚的副歌", f"关于{zh_topic}，我还有话没说完"]
            verse1 = [rng.choice(topic_lines), rng.choice(zh_lines)]
            verse2 = [rng.choice(zh_lines), rng.choice(zh_lines)]
            chorus_lines = rng.sample(zh_lines, k=2)
            if genre.lower() in {"rap", "hip-hop", "trap", "嘻哈", "说唱"}:
                rap = LOCALIZED_RAP["zh"]
                verse1 = [f"这一段，就从{zh_topic}唱起", rng.choice(rap)]
                verse2 = [rng.choice(rap), rng.choice(zh_lines)]
                chorus_lines = rng.sample(rap, k=2)
        while len(verse1) < verse_lines:
            bank_for_extra = LOCALIZED_PARODY["zh"].get(parody_angle, LOCALIZED_PARODY["zh"]["Anime / fandom obsession"]) if parody else (LOCALIZED_RAP["zh"] if genre.lower() in {"rap", "hip-hop", "trap", "嘻哈", "说唱"} else zh_lines)
            verse1.append(rng.choice(bank_for_extra))
        while len(verse2) < verse_lines:
            bank_for_extra = LOCALIZED_PARODY["zh"].get(parody_angle, LOCALIZED_PARODY["zh"]["Anime / fandom obsession"]) if parody else (LOCALIZED_RAP["zh"] if genre.lower() in {"rap", "hip-hop", "trap", "嘻哈", "说唱"} else zh_lines)
            verse2.append(rng.choice(bank_for_extra))
        outro_lines = [rng.choice(zh_lines), rng.choice(LOCALIZED_RAP["zh"] if genre.lower() in {"rap", "hip-hop", "trap", "嘻哈", "说唱"} else zh_lines)]
    elif parody:
        bank = list(PARODY.get(parody_angle, PARODY["Anime / fandom obsession"]))
        chorus_lines = [bank[2], bank[3], "One more page becomes a whole new season", "My alarm clock deserves a redemption arc"]
        available = [line for line in bank if line not in chorus_lines]
        verse1 = rng.sample(available, k=verse_lines)
        remaining = [line for line in available if line not in verse1]
        verse2 = rng.sample(remaining, k=verse_lines)
        outro_lines = [rng.choice(bank), rng.choice(bank)]
    else:
        verse1 = [ARCS["setup"][0].format(topic=topic), rng.choice(mood_lines)]
        verse2 = [rng.choice(ARCS["rise"]), rng.choice(mood_lines)]
        chorus_lines = [rng.choice(mood_lines), rng.choice(ARCS["resolve"])]
        if rhyme_scheme in RHYME_SCHEMES and RHYME_SCHEMES[rhyme_scheme]:
            chorus_lines = [line.format(topic=topic) for line in RHYME_SCHEMES[rhyme_scheme]]
        outro_lines = [rng.choice(mood_lines), rng.choice(ARCS["resolve"])]

    if language != "zh":
        while len(verse1) < verse_lines:
            verse1.append(rng.choice(mood_lines if not parody else PARODY.get(parody_angle, PARODY["Anime / fandom obsession"])))
        while len(verse2) < verse_lines:
            verse2.append(rng.choice(mood_lines if not parody else PARODY.get(parody_angle, PARODY["Anime / fandom obsession"])))
        if genre.lower() in {"rap", "hip-hop", "trap"} and not parody:
            verse1 = [line + " — I write my truth across the beat" for line in verse1]
            verse2 = [line + " — I write my truth across the beat" for line in verse2]

    lyrics = (
        "[Verse 1]\n" + "\n".join(verse1[:verse_lines])
        + "\n\n[Chorus]\n" + "\n".join(chorus_lines)
        + "\n\n[Verse 2]\n" + "\n".join(verse2[:verse_lines])
        + "\n\n[Outro]\n" + "\n".join(outro_lines)
    )
    return avoid_duplicate_lines(lyrics, language=language, seed=seed)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate original template-based SongForge lyrics locally.")
    parser.add_argument("--topic", default="following a dream through the night")
    parser.add_argument("--mood", default="Hopeful", choices=sorted(PHRASES))
    parser.add_argument("--genre", default="Pop")
    parser.add_argument("--parody", action="store_true")
    parser.add_argument("--language", choices=["en", "zh"], default="en", help="Lyrics language: English or Simplified Chinese")
    parser.add_argument("--parody-angle", choices=sorted(PARODY), default="Anime / fandom obsession", help="Comedy angle used by parody mode")
    parser.add_argument("--rhyme-scheme", choices=sorted(RHYME_SCHEMES), default="Free verse", help="Optional offline chorus rhyme pattern")
    parser.add_argument("--verse-lines", type=int, choices=[2, 4, 6, 8], default=4, help="Lines per verse (2, 4, 6, or 8)")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--build-data", action="store_true", help="Write the static JSON bank used by the website")
    parser.add_argument("--output", default=None, help="Optional path for generated lyric text")
    args = parser.parse_args()
    if args.build_data:
        build_static_data(Path(args.output or "content/lyric_engine.json"))
    else:
        lyric = generate_lyrics(args.topic, args.mood, args.genre, args.parody, args.seed, args.rhyme_scheme, args.verse_lines, args.language, args.parody_angle)
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(lyric + "\n", encoding="utf-8")
        else:
            print(lyric)
