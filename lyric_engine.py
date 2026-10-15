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
 "Anime / fandom obsession":["One more episode, then sunrise (that is a lie)","My sleep schedule has entered a new arc","I came for one chapter, now birds are singing","The cliffhanger won; my alarm clock lost"],
 "Everyday-life chaos":["My laundry pile just gained a final boss","I made a to-do list; it asked for a day off","The fridge light knows my midnight secrets","I lost my keys while holding them in my hand"],
 "Internet meme energy":["The group chat says touch grass; I sent a meme","My last two brain cells are doing a dance","I went viral in a chat with three close friends","The algorithm knows my snack routine"],
 "Romance satire":["You stole my hoodie and my streaming PIN","Our love language is what should we eat","You said be yourself; I sent twelve drafts","My heart said soulmate; my brain said terms apply"],
 "Genre exaggeration":["One tiny feeling got a cinematic score","I stubbed my toe; the orchestra appeared","A dramatic wind machine followed me to work","My coffee has a character arc tonight"]
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
ENGINE = {"version":1,"phrases":PHRASES,"parodyLines":PARODY,"multilingualFandom":FANDOM,"arcs":ARCS}

def build_static_data(destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(json.dumps(ENGINE, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

def generate_lyrics(topic: str, mood: str="Hopeful", genre: str="Pop", parody: bool=False, seed: int|None=None) -> str:
    """Generate a complete short lyric draft locally using Python templates."""
    rng = random.Random(seed)
    topic = re.sub(r"\s+", " ", topic.strip()).rstrip(".!?") or "following a dream through the night"
    mood_lines = PHRASES.get(mood, PHRASES["Hopeful"])
    if parody:
        bank = PARODY["Anime / fandom obsession"]
        lines = rng.sample(bank, k=len(bank))
    else:
        lines = [ARCS["setup"][0].format(topic=topic), rng.choice(mood_lines),
                 rng.choice(ARCS["rise"]), rng.choice(mood_lines),
                 rng.choice(ARCS["bridge"]), rng.choice(mood_lines),
                 rng.choice(ARCS["resolve"]), rng.choice(mood_lines)]
    if genre.lower() in {"rap", "hip-hop", "trap"} and not parody:
        lines = [line + " — I write my truth across the beat" for line in lines]
    return "[Verse 1]\n" + "\n".join(lines[:2]) + "\n\n[Chorus]\n" + "\n".join(lines[2:4]) + "\n\n[Verse 2]\n" + "\n".join(lines[4:6]) + "\n\n[Outro]\n" + "\n".join(lines[6:8])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate original template-based SongForge lyrics locally.")
    parser.add_argument("--topic", default="following a dream through the night")
    parser.add_argument("--mood", default="Hopeful", choices=sorted(PHRASES))
    parser.add_argument("--genre", default="Pop")
    parser.add_argument("--parody", action="store_true")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--build-data", action="store_true", help="Write the static JSON bank used by the website")
    parser.add_argument("--output", default=None, help="Optional path for generated lyric text")
    args = parser.parse_args()
    if args.build_data:
        build_static_data(Path(args.output or "content/lyric_engine.json"))
    else:
        lyric = generate_lyrics(args.topic, args.mood, args.genre, args.parody, args.seed)
        if args.output:
            Path(args.output).write_text(lyric + "\n", encoding="utf-8")
        else:
            print(lyric)
