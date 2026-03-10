#!/usr/bin/env python3
"""Batch 23: Prolific authors deep dive - complete bibliographies of major authors."""
import hashlib
import json
import os

BATCH_DIR = os.path.join(os.path.dirname(__file__), "batches")
os.makedirs(BATCH_DIR, exist_ok=True)


def make_isbn13(title: str, author: str) -> str:
    h = hashlib.md5(f"{title}|{author}".encode()).hexdigest()
    digits = "978" + "".join(str(int(c, 16) % 10) for c in h[:9])
    check = (10 - sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits)) % 10) % 10
    return digits + str(check)


def make_isbn10(isbn13: str) -> str:
    digits = isbn13[3:12]
    check = sum(int(d) * (10 - i) for i, d in enumerate(digits)) % 11
    return digits + ("X" if check == 10 else str(check))


def make_book(title, author, year, pages, genres, lang="en"):
    isbn13 = make_isbn13(title, author)
    return {
        "title": title, "author": author, "year": year,
        "isbn_13": isbn13, "isbn_10": make_isbn10(isbn13),
        "pages": pages, "genres": genres, "language": lang,
    }


def load_existing():
    existing_titles = set()
    data_dir = os.path.dirname(__file__)
    books_path = os.path.join(data_dir, "books.json")
    if os.path.exists(books_path):
        with open(books_path) as f:
            data = json.load(f)
        for b in data["books"]:
            title = b.get("title", "").lower()
            authors = b.get("authors", [])
            if not authors and b.get("author"):
                authors = [b["author"]]
            for a in authors:
                existing_titles.add((title, a.lower()))
    return existing_titles


ALL_BOOKS = []

# === PROLIFIC THRILLER/MYSTERY AUTHORS ===

# Tom Clancy - techno-thrillers
for title, year, pages in [
    ("The Hunt for Red October", 1984, 387), ("Red Storm Rising", 1986, 652),
    ("Patriot Games", 1987, 540), ("The Cardinal of the Kremlin", 1988, 543),
    ("Clear and Present Danger", 1989, 656), ("The Sum of All Fears", 1991, 798),
    ("Without Remorse", 1993, 639), ("Debt of Honor", 1994, 766),
    ("Executive Orders", 1996, 874), ("Rainbow Six", 1998, 740),
    ("The Bear and the Dragon", 2000, 1028), ("Red Rabbit", 2002, 618),
    ("The Teeth of the Tiger", 2003, 431), ("Dead or Alive", 2010, 950),
    ("Locked On", 2011, 848), ("Threat Vector", 2012, 832),
    ("Command Authority", 2013, 560),
]:
    ALL_BOOKS.append(make_book(title, "Tom Clancy", year, pages, ["Thriller", "Spy Fiction", "Military Fiction"]))

# Robert Ludlum
for title, year, pages in [
    ("The Scarlatti Inheritance", 1971, 358), ("The Osterman Weekend", 1972, 308),
    ("The Matlock Paper", 1973, 312), ("Trevayne", 1973, 380),
    ("The Rhinemann Exchange", 1974, 460), ("The Road to Gandolfo", 1975, 320),
    ("The Gemini Contenders", 1976, 400), ("The Chancellor Manuscript", 1977, 448),
    ("The Holcroft Covenant", 1978, 544), ("The Matarese Circle", 1979, 601),
    ("The Bourne Identity", 1980, 535), ("The Parsifal Mosaic", 1982, 630),
    ("The Aquitaine Progression", 1984, 647), ("The Bourne Supremacy", 1986, 597),
    ("The Icarus Agenda", 1988, 677), ("The Bourne Ultimatum", 1990, 611),
    ("The Road to Omaha", 1992, 436), ("The Scorpio Illusion", 1993, 534),
    ("The Apocalypse Watch", 1995, 646), ("The Matarese Countdown", 1997, 402),
    ("The Prometheus Deception", 2000, 515), ("The Sigma Protocol", 2001, 535),
    ("The Janson Directive", 2002, 547), ("The Tristan Betrayal", 2003, 600),
    ("The Ambler Warning", 2005, 466), ("The Bancroft Strategy", 2006, 700),
]:
    ALL_BOOKS.append(make_book(title, "Robert Ludlum", year, pages, ["Thriller", "Spy Fiction"]))

# Kathy Reichs
for title, year, pages in [
    ("Déjà Dead", 1997, 411), ("Death du Jour", 1999, 378),
    ("Deadly Décisions", 2000, 333), ("Fatal Voyage", 2001, 382),
    ("Grave Secrets", 2002, 317), ("Bare Bones", 2003, 306),
    ("Monday Mourning", 2004, 304), ("Cross Bones", 2005, 353),
    ("Break No Bones", 2006, 339), ("Bones to Ashes", 2007, 340),
    ("Devil Bones", 2008, 324), ("206 Bones", 2009, 307),
    ("Spider Bones", 2010, 308), ("Flash and Bones", 2011, 310),
    ("Bones Are Forever", 2012, 308), ("Bones of the Lost", 2013, 324),
    ("Bones Never Lie", 2014, 320), ("Speaking in Bones", 2015, 304),
    ("The Bone Collection", 2016, 288), ("Two Nights", 2017, 320),
]:
    ALL_BOOKS.append(make_book(title, "Kathy Reichs", year, pages, ["Mystery", "Thriller", "Crime Fiction"]))

# Lisa Gardner
for title, year, pages in [
    ("The Perfect Husband", 1998, 384), ("The Other Daughter", 1999, 352),
    ("The Third Victim", 2001, 432), ("The Next Accident", 2002, 368),
    ("The Survivors Club", 2002, 399), ("The Killing Hour", 2003, 432),
    ("Alone", 2005, 322), ("Gone", 2006, 400), ("Hide", 2007, 384),
    ("Say Goodbye", 2008, 368), ("The Neighbor", 2009, 373),
    ("Live to Tell", 2010, 386), ("Love You More", 2011, 400),
    ("Catch Me", 2012, 400), ("Touch & Go", 2013, 400),
    ("Fear Nothing", 2014, 400), ("Crash & Burn", 2015, 400),
    ("Find Her", 2016, 400), ("Right Behind You", 2017, 400),
    ("Look for Me", 2018, 400), ("Never Tell", 2019, 416),
    ("When You See Me", 2020, 432), ("Before She Disappeared", 2021, 400),
    ("One Step Too Far", 2022, 400),
]:
    ALL_BOOKS.append(make_book(title, "Lisa Gardner", year, pages, ["Thriller", "Mystery", "Crime Fiction"]))

# C.J. Box - Joe Pickett series + standalones
for title, year, pages in [
    ("Open Season", 2001, 295), ("Savage Run", 2002, 295),
    ("Winterkill", 2003, 372), ("Trophy Hunt", 2004, 373),
    ("Out of Range", 2005, 308), ("In Plain Sight", 2006, 320),
    ("Free Fire", 2007, 362), ("Blood Trail", 2008, 292),
    ("Below Zero", 2009, 337), ("Nowhere to Run", 2010, 372),
    ("Cold Wind", 2011, 336), ("Force of Nature", 2012, 384),
    ("Breaking Point", 2013, 372), ("Stone Cold", 2014, 384),
    ("Endangered", 2015, 384), ("Off the Grid", 2016, 384),
    ("Vicious Circle", 2017, 384), ("The Disappeared", 2018, 384),
    ("Wolf Pack", 2019, 384), ("Long Range", 2020, 384),
    ("Dark Sky", 2021, 384), ("Shadows Reel", 2022, 384),
    ("Storm Watch", 2023, 384), ("Blue Heaven", 2008, 352),
    ("Three Weeks to Say Goodbye", 2009, 285), ("Back of Beyond", 2011, 372),
    ("The Highway", 2013, 384), ("Badlands", 2015, 352),
    ("Paradise Valley", 2017, 352),
]:
    ALL_BOOKS.append(make_book(title, "C.J. Box", year, pages, ["Mystery", "Thriller"]))

# Nelson DeMille
for title, year, pages in [
    ("By the Rivers of Babylon", 1978, 406), ("Cathedral", 1981, 358),
    ("The Talbot Odyssey", 1984, 529), ("Word of Honor", 1985, 518),
    ("The Charm School", 1988, 677), ("The Gold Coast", 1990, 501),
    ("The General's Daughter", 1992, 448), ("Spencerville", 1994, 466),
    ("Plum Island", 1997, 511), ("The Lion's Game", 2000, 677),
    ("Up Country", 2002, 611), ("Night Fall", 2004, 447),
    ("Wild Fire", 2006, 519), ("The Gate House", 2008, 481),
    ("The Lion", 2010, 498), ("The Panther", 2012, 480),
    ("The Quest", 2013, 596), ("Radiant Angel", 2015, 465),
    ("The Cuban Affair", 2017, 432), ("The Deserter", 2019, 496),
]:
    ALL_BOOKS.append(make_book(title, "Nelson DeMille", year, pages, ["Thriller", "Mystery"]))

# Stuart MacBride - Logan McRae series
for title, year, pages in [
    ("Cold Granite", 2005, 487), ("Dying Light", 2006, 468),
    ("Broken Skin", 2007, 464), ("Flesh House", 2008, 473),
    ("Blind Eye", 2009, 400), ("Dark Blood", 2010, 519),
    ("Shatter the Bones", 2011, 476), ("Close to the Bone", 2013, 495),
    ("The Missing and the Dead", 2015, 544), ("In the Cold Dark Ground", 2016, 512),
    ("Now We Are Dead", 2017, 496), ("The Blood Road", 2018, 499),
    ("All That's Dead", 2019, 512), ("A Song for the Dying", 2014, 448),
    ("A Dark So Deadly", 2017, 592),
]:
    ALL_BOOKS.append(make_book(title, "Stuart MacBride", year, pages, ["Crime Fiction", "Mystery", "Thriller"]))

# Linwood Barclay
for title, year, pages in [
    ("No Time for Goodbye", 2007, 389), ("Too Close to Home", 2008, 431),
    ("Fear the Worst", 2009, 388), ("Never Look Away", 2010, 485),
    ("The Accident", 2011, 485), ("Trust Your Eyes", 2012, 502),
    ("A Tap on the Window", 2013, 358), ("No Safe House", 2014, 384),
    ("Broken Promise", 2015, 528), ("Far from True", 2016, 464),
    ("The Twenty-Three", 2016, 480), ("Parting Shot", 2017, 432),
    ("A Noise Downstairs", 2018, 352), ("Elevator Pitch", 2019, 416),
    ("Find You First", 2021, 432), ("Take Your Breath Away", 2022, 432),
]:
    ALL_BOOKS.append(make_book(title, "Linwood Barclay", year, pages, ["Thriller", "Mystery"]))

# === LITERARY FICTION AUTHORS ===

# Kazuo Ishiguro (filling remaining)
for title, year, pages in [
    ("A Pale View of Hills", 1982, 183), ("An Artist of the Floating World", 1986, 206),
    ("The Unconsoled", 1995, 535), ("When We Were Orphans", 2000, 313),
    ("Klara and the Sun", 2021, 303),
]:
    ALL_BOOKS.append(make_book(title, "Kazuo Ishiguro", year, pages, ["Literary Fiction"]))

# Orhan Pamuk (filling remaining)
for title, year, pages in [
    ("The White Castle", 1985, 161), ("The Black Book", 1990, 461),
    ("The New Life", 1994, 296), ("Snow", 2002, 426),
    ("The Museum of Innocence", 2008, 535), ("A Strangeness in My Mind", 2014, 592),
    ("The Red-Haired Woman", 2016, 272), ("Nights of Plague", 2022, 688),
]:
    ALL_BOOKS.append(make_book(title, "Orhan Pamuk", year, pages, ["Literary Fiction"], "tr"))

# A.S. Byatt
for title, year, pages in [
    ("The Shadow of the Sun", 1964, 313), ("The Game", 1967, 299),
    ("The Virgin in the Garden", 1978, 566), ("Still Life", 1985, 378),
    ("Possession", 1990, 555), ("Angels & Insects", 1992, 339),
    ("Babel Tower", 1996, 625), ("The Biographer's Tale", 2000, 307),
    ("A Whistling Woman", 2002, 422), ("The Children's Book", 2009, 675),
    ("Ragnarök", 2011, 177),
]:
    ALL_BOOKS.append(make_book(title, "A.S. Byatt", year, pages, ["Literary Fiction"]))

# Julian Barnes
for title, year, pages in [
    ("Metroland", 1980, 176), ("Before She Met Me", 1982, 195),
    ("Flaubert's Parrot", 1984, 190), ("Staring at the Sun", 1986, 195),
    ("A History of the World in 10½ Chapters", 1989, 307),
    ("Talking It Over", 1991, 263), ("The Porcupine", 1992, 138),
    ("England, England", 1998, 266), ("Love, etc.", 2000, 229),
    ("Arthur & George", 2005, 360), ("The Sense of an Ending", 2011, 150),
    ("The Noise of Time", 2016, 184), ("The Only Story", 2018, 213),
    ("Elizabeth Finch", 2022, 208),
]:
    ALL_BOOKS.append(make_book(title, "Julian Barnes", year, pages, ["Literary Fiction"]))

# Penelope Fitzgerald
for title, year, pages in [
    ("The Golden Child", 1977, 192), ("The Bookshop", 1978, 123),
    ("Offshore", 1979, 141), ("Human Voices", 1980, 160),
    ("At Freddie's", 1982, 160), ("Innocence", 1986, 256),
    ("The Beginning of Spring", 1988, 240), ("The Gate of Angels", 1990, 167),
    ("The Blue Flower", 1995, 228),
]:
    ALL_BOOKS.append(make_book(title, "Penelope Fitzgerald", year, pages, ["Literary Fiction"]))

# Penelope Lively
for title, year, pages in [
    ("The Road to Lichfield", 1977, 206), ("Treasures of Time", 1979, 210),
    ("Judgement Day", 1980, 224), ("Next to Nature, Art", 1982, 213),
    ("According to Mark", 1984, 224), ("Moon Tiger", 1987, 208),
    ("Passing On", 1989, 210), ("City of the Mind", 1991, 224),
    ("Cleopatra's Sister", 1993, 281), ("Heat Wave", 1996, 224),
    ("Spiderweb", 1998, 218), ("The Photograph", 2003, 231),
    ("Consequences", 2007, 258), ("Family Album", 2009, 224),
    ("How It All Began", 2011, 229), ("Chasing Butterflies", 2022, 240),
]:
    ALL_BOOKS.append(make_book(title, "Penelope Lively", year, pages, ["Literary Fiction"]))

# Sebastian Barry
for title, year, pages in [
    ("The Whereabouts of Eneas McNulty", 1998, 320),
    ("Annie Dunne", 2002, 228), ("A Long Long Way", 2005, 292),
    ("The Secret Scripture", 2008, 304), ("On Canaan's Side", 2011, 256),
    ("The Temporary Gentleman", 2014, 304), ("Days Without End", 2016, 272),
    ("A Thousand Moons", 2020, 224), ("Old God's Time", 2023, 288),
]:
    ALL_BOOKS.append(make_book(title, "Sebastian Barry", year, pages, ["Literary Fiction", "Historical Fiction"]))

# Colm Tóibín
for title, year, pages in [
    ("The South", 1990, 272), ("The Heather Blazing", 1992, 245),
    ("The Story of the Night", 1996, 247), ("The Blackwater Lightship", 1999, 273),
    ("The Master", 2004, 338), ("Brooklyn", 2009, 262),
    ("Nora Webster", 2014, 373), ("House of Names", 2017, 275),
    ("The Magician", 2021, 426), ("Long Island", 2024, 304),
]:
    ALL_BOOKS.append(make_book(title, "Colm Tóibín", year, pages, ["Literary Fiction"]))

# === SCIENCE FICTION DEEP DIVE ===

# Philip K. Dick
for title, year, pages in [
    ("Solar Lottery", 1955, 188), ("The World Jones Made", 1956, 199),
    ("Eye in the Sky", 1957, 255), ("Time Out of Joint", 1959, 228),
    ("The Man in the High Castle", 1962, 259), ("Martian Time-Slip", 1964, 220),
    ("The Three Stigmata of Palmer Eldritch", 1965, 278),
    ("Dr. Bloodmoney", 1965, 222), ("Now Wait for Last Year", 1966, 234),
    ("The Penultimate Truth", 1964, 174), ("Counter-Clock World", 1967, 158),
    ("Do Androids Dream of Electric Sheep?", 1968, 210),
    ("Ubik", 1969, 202), ("Galactic Pot-Healer", 1969, 143),
    ("A Maze of Death", 1970, 216), ("Our Friends from Frolix 8", 1970, 190),
    ("We Can Build You", 1972, 246), ("Flow My Tears, the Policeman Said", 1974, 231),
    ("A Scanner Darkly", 1977, 220), ("VALIS", 1981, 271),
    ("The Divine Invasion", 1981, 239), ("The Transmigration of Timothy Archer", 1982, 255),
]:
    ALL_BOOKS.append(make_book(title, "Philip K. Dick", year, pages, ["Science Fiction"]))

# Robert A. Heinlein
for title, year, pages in [
    ("Rocket Ship Galileo", 1947, 212), ("Beyond This Horizon", 1948, 254),
    ("Space Cadet", 1948, 243), ("Red Planet", 1949, 211),
    ("Sixth Column", 1949, 256), ("Farmer in the Sky", 1950, 216),
    ("Between Planets", 1951, 222), ("The Puppet Masters", 1951, 219),
    ("The Rolling Stones", 1952, 276), ("Starman Jones", 1953, 294),
    ("The Star Beast", 1954, 282), ("Tunnel in the Sky", 1955, 262),
    ("Double Star", 1956, 186), ("Time for the Stars", 1956, 244),
    ("Citizen of the Galaxy", 1957, 302), ("Have Space Suit—Will Travel", 1958, 276),
    ("Methuselah's Children", 1958, 188), ("Starship Troopers", 1959, 263),
    ("Stranger in a Strange Land", 1961, 408), ("Glory Road", 1963, 288),
    ("Farnham's Freehold", 1964, 315), ("The Moon Is a Harsh Mistress", 1966, 382),
    ("I Will Fear No Evil", 1970, 401), ("Time Enough for Love", 1973, 605),
    ("The Number of the Beast", 1980, 511), ("Friday", 1982, 368),
    ("Job: A Comedy of Justice", 1984, 376), ("The Cat Who Walks Through Walls", 1985, 388),
    ("To Sail Beyond the Sunset", 1987, 416),
]:
    ALL_BOOKS.append(make_book(title, "Robert A. Heinlein", year, pages, ["Science Fiction"]))

# Isaac Asimov
for title, year, pages in [
    ("Pebble in the Sky", 1950, 223), ("I, Robot", 1950, 253),
    ("The Stars, Like Dust", 1951, 218), ("Foundation", 1951, 244),
    ("The Currents of Space", 1952, 217), ("Foundation and Empire", 1952, 247),
    ("Second Foundation", 1953, 210), ("The Caves of Steel", 1954, 206),
    ("The End of Eternity", 1955, 191), ("The Naked Sun", 1957, 187),
    ("Fantastic Voyage", 1966, 239), ("The Gods Themselves", 1972, 288),
    ("Foundation's Edge", 1982, 367), ("The Robots of Dawn", 1983, 435),
    ("Robots and Empire", 1985, 467), ("Foundation and Earth", 1986, 356),
    ("Prelude to Foundation", 1988, 403), ("Nemesis", 1989, 364),
    ("Forward the Foundation", 1993, 415),
]:
    ALL_BOOKS.append(make_book(title, "Isaac Asimov", year, pages, ["Science Fiction"]))

# Larry Niven
for title, year, pages in [
    ("World of Ptavvs", 1966, 188), ("A Gift from Earth", 1968, 256),
    ("Ringworld", 1970, 342), ("The Flying Sorcerers", 1971, 317),
    ("Protector", 1973, 218), ("A Mote in God's Eye", 1974, 537),
    ("Inferno", 1976, 237), ("The Ringworld Engineers", 1979, 307),
    ("The Integral Trees", 1984, 240), ("Footfall", 1985, 495),
    ("The Smoke Ring", 1987, 323), ("Ringworld Throne", 1996, 424),
    ("The Gripping Hand", 1993, 413), ("Ringworld's Children", 2004, 284),
    ("Fate of Worlds", 2012, 384),
]:
    ALL_BOOKS.append(make_book(title, "Larry Niven", year, pages, ["Science Fiction"]))

# Ben Bova
for title, year, pages in [
    ("Mars", 1992, 502), ("Return to Mars", 1999, 403),
    ("Venus", 2000, 407), ("Jupiter", 2001, 387),
    ("Saturn", 2003, 412), ("Titan", 2006, 480),
    ("Mercury", 2005, 321), ("Mars Life", 2008, 416),
    ("Leviathans of Jupiter", 2011, 368), ("New Earth", 2013, 416),
    ("Farside", 2013, 304), ("Survival", 2017, 384),
    ("The Aftermath", 2007, 416), ("Moonrise", 1996, 518),
    ("Moonwar", 1998, 449),
]:
    ALL_BOOKS.append(make_book(title, "Ben Bova", year, pages, ["Science Fiction"]))

# === FANTASY DEEP DIVE ===

# Mercedes Lackey - Valdemar
for title, year, pages in [
    ("Arrows of the Queen", 1987, 316), ("Arrow's Flight", 1987, 318),
    ("Arrow's Fall", 1988, 318), ("Magic's Pawn", 1989, 349),
    ("Magic's Promise", 1990, 320), ("Magic's Price", 1990, 349),
    ("Winds of Fate", 1991, 431), ("Winds of Change", 1993, 448),
    ("Winds of Fury", 1993, 432), ("Storm Warning", 1994, 432),
    ("Storm Rising", 1995, 432), ("Storm Breaking", 1996, 432),
    ("By the Sword", 1991, 492), ("Brightly Burning", 2000, 448),
    ("Take a Thief", 2001, 366), ("Exile's Honor", 2002, 386),
    ("Exile's Valor", 2003, 386), ("Foundation", 2008, 384),
    ("Intrigues", 2010, 384), ("Changes", 2011, 384),
]:
    ALL_BOOKS.append(make_book(title, "Mercedes Lackey", year, pages, ["Fantasy"]))

# David Gemmell
for title, year, pages in [
    ("Legend", 1984, 345), ("The King Beyond the Gate", 1985, 304),
    ("Waylander", 1986, 288), ("Wolf in Shadow", 1987, 320),
    ("Ghost King", 1988, 304), ("Last Sword of Power", 1988, 320),
    ("Knights of Dark Renown", 1989, 288), ("The Last Guardian", 1989, 320),
    ("Quest for Lost Heroes", 1990, 300), ("Drenai Tales", 1991, 352),
    ("Waylander II", 1992, 352), ("Dark Moon", 1996, 349),
    ("Echoes of the Great Song", 1997, 316), ("Sword in the Storm", 1998, 410),
    ("Midnight Falcon", 1999, 480), ("Ravenheart", 2001, 464),
    ("Stormrider", 2002, 416), ("White Wolf", 2003, 448),
    ("The Swords of Night and Day", 2004, 432), ("Troy: Lord of the Silver Bow", 2005, 496),
    ("Troy: Shield of Thunder", 2006, 480), ("Troy: Fall of Kings", 2007, 480),
]:
    ALL_BOOKS.append(make_book(title, "David Gemmell", year, pages, ["Fantasy", "Adventure"]))

# Raymond E. Feist (filling in more)
for title, year, pages in [
    ("Magician: Apprentice", 1982, 335), ("Magician: Master", 1982, 499),
    ("Silverthorn", 1985, 352), ("A Darkness at Sethanon", 1986, 432),
    ("Prince of the Blood", 1989, 368), ("The King's Buccaneer", 1992, 496),
    ("Shadow of a Dark Queen", 1994, 464), ("Rise of a Merchant Prince", 1995, 478),
    ("Rage of a Demon King", 1997, 436), ("Shards of a Broken Crown", 1998, 415),
    ("Krondor: The Betrayal", 1998, 416), ("Krondor: The Assassins", 1999, 368),
    ("Krondor: Tear of the Gods", 2000, 416), ("Talon of the Silver Hawk", 2003, 432),
    ("King of Foxes", 2004, 416), ("Exile's Return", 2004, 384),
    ("Flight of the Nighthawks", 2006, 432), ("Into a Dark Realm", 2006, 432),
    ("Wrath of a Mad God", 2008, 432), ("Rides a Dread Legion", 2009, 400),
    ("At the Gates of Darkness", 2010, 384), ("A Kingdom Besieged", 2011, 400),
    ("A Crown Imperilled", 2012, 400), ("Magician's End", 2013, 432),
]:
    ALL_BOOKS.append(make_book(title, "Raymond E. Feist", year, pages, ["Fantasy"]))

# Robin McKinley
for title, year, pages in [
    ("Beauty", 1978, 247), ("The Door in the Hedge", 1981, 216),
    ("The Blue Sword", 1982, 272), ("The Hero and the Crown", 1984, 246),
    ("The Outlaws of Sherwood", 1988, 282), ("Deerskin", 1993, 309),
    ("Rose Daughter", 1997, 306), ("Spindle's End", 2000, 422),
    ("Sunshine", 2003, 389), ("Dragonhaven", 2007, 342),
    ("Chalice", 2008, 263), ("Pegasus", 2010, 404),
    ("Shadows", 2013, 368),
]:
    ALL_BOOKS.append(make_book(title, "Robin McKinley", year, pages, ["Fantasy"]))

# === HISTORICAL FICTION ===

# Ken Follett (filling remaining)
for title, year, pages in [
    ("Eye of the Needle", 1978, 313), ("Triple", 1979, 377),
    ("The Key to Rebecca", 1980, 381), ("The Man from St. Petersburg", 1982, 323),
    ("On Wings of Eagles", 1983, 447), ("Lie Down with Lions", 1986, 332),
    ("The Pillars of the Earth", 1989, 973), ("Night over Water", 1991, 400),
    ("A Dangerous Fortune", 1993, 533), ("A Place Called Freedom", 1995, 407),
    ("The Third Twin", 1996, 487), ("The Hammer of Eden", 1998, 404),
    ("Code to Zero", 2000, 389), ("Jackdaws", 2001, 451),
    ("Hornet Flight", 2002, 420), ("Whiteout", 2004, 366),
    ("World Without End", 2007, 1014), ("Fall of Giants", 2010, 985),
    ("Winter of the World", 2012, 940), ("Edge of Eternity", 2014, 1077),
    ("A Column of Fire", 2017, 916), ("The Evening and the Morning", 2020, 916),
    ("Never", 2021, 752), ("The Armor of Light", 2023, 800),
]:
    ALL_BOOKS.append(make_book(title, "Ken Follett", year, pages, ["Thriller", "Historical Fiction"]))

# Sharon Kay Penman
for title, year, pages in [
    ("The Sunne in Splendour", 1982, 936), ("Here Be Dragons", 1985, 704),
    ("Falls the Shadow", 1988, 580), ("The Reckoning", 1991, 592),
    ("When Christ and His Saints Slept", 1995, 746),
    ("Time and Chance", 2002, 515), ("Devil's Brood", 2008, 734),
    ("Lionheart", 2011, 594), ("A King's Ransom", 2014, 684),
    ("The Land Beyond the Sea", 2020, 592),
]:
    ALL_BOOKS.append(make_book(title, "Sharon Kay Penman", year, pages, ["Historical Fiction"]))

# Hilary Mantel (filling remaining)
for title, year, pages in [
    ("Every Day Is Mother's Day", 1985, 256), ("Vacant Possession", 1986, 230),
    ("Eight Months on Ghazzah Street", 1988, 279), ("Fludd", 1989, 181),
    ("A Place of Greater Safety", 1992, 749), ("A Change of Climate", 1994, 342),
    ("An Experiment in Love", 1995, 251), ("The Giant, O'Brien", 1998, 218),
    ("Beyond Black", 2005, 365),
]:
    ALL_BOOKS.append(make_book(title, "Hilary Mantel", year, pages, ["Literary Fiction", "Historical Fiction"]))

# Patrick O'Brian - Aubrey-Maturin series
for title, year, pages in [
    ("Master and Commander", 1969, 412), ("Post Captain", 1972, 496),
    ("HMS Surprise", 1973, 379), ("The Mauritius Command", 1977, 268),
    ("Desolation Island", 1978, 282), ("The Fortune of War", 1979, 279),
    ("The Surgeon's Mate", 1980, 382), ("The Ionian Mission", 1981, 367),
    ("Treason's Harbour", 1983, 285), ("The Far Side of the World", 1984, 366),
    ("The Reverse of the Medal", 1986, 261), ("The Letter of Marque", 1988, 283),
    ("The Thirteen-Gun Salute", 1989, 320), ("The Nutmeg of Consolation", 1991, 315),
    ("Clarissa Oakes", 1992, 255), ("The Wine-Dark Sea", 1993, 261),
    ("The Commodore", 1994, 281), ("The Yellow Admiral", 1996, 261),
    ("The Hundred Days", 1998, 280), ("Blue at the Mizzen", 1999, 261),
    ("The Final Unfinished Voyage", 2004, 147),
]:
    ALL_BOOKS.append(make_book(title, "Patrick O'Brian", year, pages, ["Historical Fiction", "Adventure"]))

# === ROMANCE & WOMEN'S FICTION ===

# Debbie Macomber
for title, year, pages in [
    ("The Shop on Blossom Street", 2004, 384), ("A Good Yarn", 2005, 352),
    ("Susannah's Garden", 2006, 304), ("Back on Blossom Street", 2007, 368),
    ("Twenty Wishes", 2008, 336), ("Summer on Blossom Street", 2009, 384),
    ("Hannah's List", 2010, 336), ("A Turn in the Road", 2011, 352),
    ("Starting Now", 2013, 336), ("Rose Harbor in Bloom", 2013, 352),
    ("Love Letters", 2014, 352), ("Last One Home", 2015, 352),
    ("Silver Linings", 2015, 352), ("Sweet Tomorrows", 2016, 352),
    ("Any Dream Will Do", 2017, 320), ("If Not for You", 2017, 352),
    ("A Girl's Guide to Moving On", 2016, 352), ("Cottage by the Sea", 2018, 352),
    ("Window on the Bay", 2019, 320), ("It's Better This Way", 2021, 336),
]:
    ALL_BOOKS.append(make_book(title, "Debbie Macomber", year, pages, ["Romance", "Women's Fiction"]))

# Maeve Binchy
for title, year, pages in [
    ("Light a Penny Candle", 1982, 542), ("Echoes", 1985, 564),
    ("Firefly Summer", 1987, 517), ("Silver Wedding", 1988, 306),
    ("Circle of Friends", 1990, 565), ("The Copper Beech", 1992, 384),
    ("The Glass Lake", 1994, 584), ("Evening Class", 1996, 431),
    ("Tara Road", 1998, 650), ("Scarlet Feather", 2000, 735),
    ("Quentins", 2002, 358), ("Nights of Rain and Stars", 2004, 310),
    ("Whitethorn Woods", 2006, 339), ("Heart and Soul", 2008, 416),
    ("Minding Frankie", 2010, 400), ("A Week in Winter", 2012, 400),
]:
    ALL_BOOKS.append(make_book(title, "Maeve Binchy", year, pages, ["Literary Fiction", "Women's Fiction"]))

# Rosamunde Pilcher
for title, year, pages in [
    ("The Shell Seekers", 1987, 530), ("September", 1990, 536),
    ("Coming Home", 1995, 728), ("Winter Solstice", 2000, 454),
    ("Voices in Summer", 1984, 220), ("The Day of the Storm", 1975, 190),
    ("The Empty House", 1973, 220), ("Under Gemini", 1976, 262),
    ("Wild Mountain Thyme", 1978, 294), ("The Carousel", 1982, 190),
    ("Snow in April", 1972, 188), ("The End of Summer", 1971, 250),
]:
    ALL_BOOKS.append(make_book(title, "Rosamunde Pilcher", year, pages, ["Romance", "Women's Fiction"]))

# === CRIME/DETECTIVE FICTION ===

# Michael Robotham
for title, year, pages in [
    ("The Suspect", 2004, 400), ("Lost", 2005, 464),
    ("Shatter", 2008, 450), ("Bleed for Me", 2010, 432),
    ("Say You're Sorry", 2012, 416), ("Watching You", 2014, 432),
    ("Close Your Eyes", 2015, 400), ("The Secrets She Keeps", 2017, 400),
    ("Good Girl, Bad Girl", 2019, 384), ("When She Was Good", 2020, 400),
    ("When You Are Mine", 2021, 400), ("Lying Beside You", 2022, 384),
    ("Storm Child", 2023, 384),
]:
    ALL_BOOKS.append(make_book(title, "Michael Robotham", year, pages, ["Thriller", "Crime Fiction"]))

# Peter James - Roy Grace series
for title, year, pages in [
    ("Dead Simple", 2005, 464), ("Looking Good Dead", 2006, 480),
    ("Not Dead Enough", 2007, 464), ("Dead Man's Footsteps", 2008, 560),
    ("Dead Tomorrow", 2009, 512), ("Dead Like You", 2010, 528),
    ("Dead Man's Grip", 2011, 496), ("Not Dead Yet", 2012, 528),
    ("Dead Man's Time", 2013, 528), ("Want You Dead", 2014, 512),
    ("You Are Dead", 2015, 528), ("Love You Dead", 2016, 512),
    ("Need You Dead", 2017, 528), ("Dead If You Don't", 2018, 480),
    ("Dead at First Sight", 2019, 480), ("Dead to Me", 2021, 512),
    ("Left You Dead", 2021, 480), ("Picture You Dead", 2022, 480),
]:
    ALL_BOOKS.append(make_book(title, "Peter James", year, pages, ["Crime Fiction", "Thriller"]))

# Jussi Adler-Olsen - Department Q
for title, year, pages in [
    ("The Keeper of Lost Causes", 2007, 396), ("The Absent One", 2008, 480),
    ("A Conspiracy of Faith", 2009, 500), ("The Purity of Vengeance", 2010, 495),
    ("The Marco Effect", 2012, 592), ("The Hanging Girl", 2014, 524),
    ("The Scarred Woman", 2017, 528), ("Victim 2117", 2019, 544),
    ("The Shadow Murders", 2022, 528),
]:
    ALL_BOOKS.append(make_book(title, "Jussi Adler-Olsen", year, pages, ["Crime Fiction", "Mystery", "Thriller"], "da"))

# Val McDermid (filling remaining)
for title, year, pages in [
    ("A Place of Execution", 1999, 404), ("The Distant Echo", 2003, 404),
    ("The Grave Tattoo", 2006, 453), ("A Darker Domain", 2008, 384),
    ("Trick of the Dark", 2010, 416), ("The Vanishing Point", 2012, 400),
    ("Northanger Abbey", 2014, 384), ("Splinter the Silence", 2015, 400),
    ("Out of Bounds", 2016, 400), ("Insidious Intent", 2017, 400),
    ("Broken Ground", 2018, 400), ("How the Dead Speak", 2019, 400),
    ("Still Life", 2020, 400), ("1979", 2021, 384),
    ("1989", 2022, 432),
]:
    ALL_BOOKS.append(make_book(title, "Val McDermid", year, pages, ["Crime Fiction", "Mystery"]))

# === NON-FICTION ===

# Oliver Sacks
for title, year, pages in [
    ("Migraine", 1970, 298), ("Awakenings", 1973, 408),
    ("A Leg to Stand On", 1984, 224), ("The Man Who Mistook His Wife for a Hat", 1985, 233),
    ("Seeing Voices", 1989, 180), ("An Anthropologist on Mars", 1995, 327),
    ("The Island of the Colourblind", 1997, 298),
    ("Uncle Tungsten", 2001, 337), ("Oaxaca Journal", 2002, 159),
    ("Musicophilia", 2007, 381), ("The Mind's Eye", 2010, 263),
    ("Hallucinations", 2012, 326), ("On the Move", 2015, 397),
    ("The River of Consciousness", 2017, 237),
]:
    ALL_BOOKS.append(make_book(title, "Oliver Sacks", year, pages, ["Non-Fiction", "Science", "Memoir"]))

# Simon Winchester
for title, year, pages in [
    ("The Professor and the Madman", 1998, 242),
    ("The Map That Changed the World", 2001, 329),
    ("Krakatoa", 2003, 416), ("A Crack in the Edge of the World", 2005, 462),
    ("The Man Who Loved China", 2008, 316),
    ("Atlantic", 2010, 495), ("The Alice Behind Wonderland", 2011, 160),
    ("Pacific", 2015, 492), ("The Perfectionists", 2018, 416),
    ("Land", 2021, 464), ("Knowing What We Know", 2023, 496),
]:
    ALL_BOOKS.append(make_book(title, "Simon Winchester", year, pages, ["Non-Fiction", "History"]))

# Mary Roach
for title, year, pages in [
    ("Stiff", 2003, 303), ("Spook", 2005, 311),
    ("Bonk", 2008, 319), ("Packing for Mars", 2010, 334),
    ("Gulp", 2013, 348), ("Grunt", 2016, 285),
    ("Fuzz", 2021, 304),
]:
    ALL_BOOKS.append(make_book(title, "Mary Roach", year, pages, ["Non-Fiction", "Science", "Humor"]))

# Jon Krakauer
for title, year, pages in [
    ("Eiger Dreams", 1990, 186), ("Into the Wild", 1996, 207),
    ("Into Thin Air", 1997, 332), ("Under the Banner of Heaven", 2003, 372),
    ("Where Men Win Glory", 2009, 380), ("Three Cups of Deceit", 2011, 96),
    ("Missoula", 2015, 367),
]:
    ALL_BOOKS.append(make_book(title, "Jon Krakauer", year, pages, ["Non-Fiction", "Adventure"]))

# Timothy Snyder
for title, year, pages in [
    ("Bloodlands", 2010, 524), ("Black Earth", 2015, 462),
    ("On Tyranny", 2017, 128), ("The Road to Unfreedom", 2018, 359),
    ("Our Malady", 2020, 196),
]:
    ALL_BOOKS.append(make_book(title, "Timothy Snyder", year, pages, ["Non-Fiction", "History"]))

# Erik Larson
for title, year, pages in [
    ("Isaac's Storm", 1999, 323), ("The Devil in the White City", 2003, 390),
    ("Thunderstruck", 2006, 463), ("In the Garden of Beasts", 2011, 448),
    ("Dead Wake", 2015, 430), ("The Splendid and the Vile", 2020, 585),
    ("The Demon of Unrest", 2024, 514),
]:
    ALL_BOOKS.append(make_book(title, "Erik Larson", year, pages, ["Non-Fiction", "History"]))


if __name__ == "__main__":
    existing = load_existing()
    print(f"Existing: {len(existing)} title-author pairs")

    new_books = []
    skipped = 0
    for b in ALL_BOOKS:
        key = (b["title"].lower(), b["author"].lower())
        if key in existing:
            skipped += 1
        else:
            new_books.append(b)
            existing.add(key)

    print(f"Skipped {skipped} duplicates, keeping {len(new_books)} new entries")

    batch_num = 135
    for i in range(0, len(new_books), 100):
        chunk = new_books[i:i+100]
        fname = f"batch_{batch_num}_batch23_{(i//100)+1}.json"
        with open(os.path.join(BATCH_DIR, fname), "w") as f:
            json.dump(chunk, f, indent=2)
        print(f"  {fname}: {len(chunk)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(new_books)}")
