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
  "I find the nerve to begin again",
  "We turn the shadows into light",
  "And let the morning wash away the rain"
 ]
}
ENGINE = {"version":5,"phrases":PHRASES,"parodyLines":PARODY,"multilingualFandom":FANDOM,"arcs":ARCS,"rhymeSchemes":RHYME_SCHEMES,"rhymeDictionary":RHYME_DICTIONARY}

def build_static_data(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(ENGINE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def generate_lyrics(topic: str, mood: str="Hopeful", genre: str="Pop", parody: bool=False, seed: int|None=None, rhyme_scheme: str="Free verse", verse_lines: int=4) -> str:
    """Generate a complete short lyric draft locally using Python templates."""
    rng = random.Random(seed)
    topic = re.sub(r"\s+", " ", topic.strip()).rstrip(".!?") or "following a dream through the night"
    verse_lines = max(2, min(8, int(verse_lines)))
    mood_lines = PHRASES.get(mood, PHRASES["Hopeful"])
    if parody:
        bank = list(PARODY["Anime / fandom obsession"])
        chorus_lines = [bank[2], bank[3], "One more page becomes a whole new season", "My alarm clock deserves a redemption arc"]
        available = [line for line in bank if line not in chorus_lines]
        verse1 = rng.sample(available, k=verse_lines)
        remaining = [line for line in available if line not in verse1]
        verse2 = rng.sample(remaining, k=verse_lines)
    else:
        verse1 = [ARCS["setup"][0].format(topic=topic), rng.choice(mood_lines)]
        verse2 = [rng.choice(ARCS["rise"]), rng.choice(mood_lines)]
        chorus_lines = [rng.choice(mood_lines), rng.choice(ARCS["resolve"])]
        if rhyme_scheme in RHYME_SCHEMES and RHYME_SCHEMES[rhyme_scheme]:
            chorus_lines = [line.format(topic=topic) for line in RHYME_SCHEMES[rhyme_scheme]]
    while len(verse1) < verse_lines:
        verse1.append(rng.choice(mood_lines if not parody else PARODY["Anime / fandom obsession"]))
    while len(verse2) < verse_lines:
        verse2.append(rng.choice(mood_lines if not parody else PARODY["Anime / fandom obsession"]))
    if genre.lower() in {"rap", "hip-hop", "trap"} and not parody:
        verse1 = [line + " — I write my truth across the beat" for line in verse1]
        verse2 = [line + " — I write my truth across the beat" for line in verse2]
    return (
        "[Verse 1]\n" + "\n".join(verse1)
        + "\n\n[Chorus]\n" + "\n".join(chorus_lines)
        + "\n\n[Verse 2]\n" + "\n".join(verse2)
        + "\n\n[Outro]\n" + "\n".join([rng.choice(mood_lines), rng.choice(ARCS["resolve"])])
    )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate original template-based SongForge lyrics locally.")
    parser.add_argument("--topic", default="following a dream through the night")
    parser.add_argument("--mood", default="Hopeful", choices=sorted(PHRASES))
    parser.add_argument("--genre", default="Pop")
    parser.add_argument("--parody", action="store_true")
    parser.add_argument("--rhyme-scheme", choices=sorted(RHYME_SCHEMES), default="Free verse", help="Optional offline chorus rhyme pattern")
    parser.add_argument("--verse-lines", type=int, choices=[2, 4, 6, 8], default=4, help="Lines per verse (2, 4, 6, or 8)")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--build-data", action="store_true", help="Write the static JSON bank used by the website")
    parser.add_argument("--output", default=None, help="Optional path for generated lyric text")
    args = parser.parse_args()
    if args.build_data:
        build_static_data(Path(args.output or "content/lyric_engine.json"))
    else:
        lyric = generate_lyrics(args.topic, args.mood, args.genre, args.parody, args.seed, args.rhyme_scheme, args.verse_lines)
        if args.output:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(lyric + "\n", encoding="utf-8")
        else:
            print(lyric)
