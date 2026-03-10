#!/usr/bin/env python3
"""Batch 17: More authors across mystery, sci-fi, literary fiction, historical fiction."""
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


AUTHORS = [
    ("Alexander McCall Smith", "en", ["Mystery", "Literary Fiction"], [
        ("The No. 1 Ladies' Detective Agency", 1998, 235, []),
        ("Tears of the Giraffe", 2000, 227, []),
        ("Morality for Beautiful Girls", 2001, 227, []),
        ("The Kalahari Typing School for Men", 2002, 198, []),
        ("The Full Cupboard of Life", 2003, 218, []),
        ("In the Company of Cheerful Ladies", 2004, 233, []),
        ("Blue Shoes and Happiness", 2006, 227, []),
        ("The Good Husband of Zebra Drive", 2007, 213, []),
        ("The Miracle at Speedy Motors", 2008, 229, []),
        ("Tea Time for the Traditionally Built", 2009, 212, []),
        ("The Double Comfort Safari Club", 2010, 211, []),
        ("The Saturday Big Tent Wedding Party", 2011, 213, []),
        ("The Limpopo Academy of Private Detection", 2012, 242, []),
        ("44 Scotland Street", 2005, 261, []),
        ("Espresso Tales", 2005, 322, []),
        ("Love Over Scotland", 2006, 352, []),
        ("The World According to Bertie", 2007, 319, []),
        ("The Unbearable Lightness of Scones", 2008, 304, []),
        ("The Sunday Philosophy Club", 2004, 304, ["Philosophy"]),
        ("Friends, Lovers, Chocolate", 2005, 260, []),
        ("The Right Attitude to Rain", 2006, 272, []),
        ("The Careful Use of Compliments", 2007, 260, []),
        ("The Comfort of Saturdays", 2008, 260, []),
        ("Portuguese Irregular Verbs", 2003, 128, ["Humor"]),
        ("The Finer Points of Sausage Dogs", 2003, 138, ["Humor"]),
        ("At the Villa of Reduced Circumstances", 2003, 148, ["Humor"]),
    ]),
    ("Henning Mankell", "sv", ["Mystery", "Crime Fiction"], [
        ("Chronicler of the Winds", 1995, 237, ["Literary Fiction"]),
        ("Depths", 2004, 312, []),
        ("The Man from Beijing", 2008, 390, ["Thriller"]),
        ("After the Fire", 2017, 315, ["Literary Fiction"]),
    ]),
    ("Fred Vargas", "fr", ["Mystery", "Crime Fiction"], [
        ("The Chalk Circle Man", 1991, 263, []),
        ("Have Mercy on Us All", 2001, 288, []),
        ("Seeking Whom He May Devour", 1999, 288, []),
        ("Wash This Blood Clean from My Hand", 2004, 400, []),
        ("This Night's Foul Work", 2006, 316, []),
        ("An Uncertain Place", 2008, 395, []),
        ("The Ghost Riders of Ordebec", 2011, 400, []),
        ("A Climate of Fear", 2015, 384, []),
    ]),
    ("Andrea Camilleri", "it", ["Mystery", "Crime Fiction"], [
        ("The Shape of Water", 1994, 224, []),
        ("The Terra-Cotta Dog", 1996, 279, []),
        ("The Snack Thief", 1996, 268, []),
        ("Voice of the Violin", 1997, 230, []),
        ("Excursion to Tindari", 2000, 280, []),
        ("The Smell of the Night", 2001, 220, []),
        ("Rounding the Mark", 2003, 284, []),
        ("The Patience of the Spider", 2004, 256, []),
        ("The Paper Moon", 2005, 272, []),
        ("August Heat", 2006, 288, []),
        ("The Wings of the Sphinx", 2006, 280, []),
        ("The Track of Sand", 2007, 290, []),
        ("The Potter's Field", 2008, 268, []),
        ("The Age of Doubt", 2008, 274, []),
        ("The Dance of the Seagull", 2009, 272, []),
        ("Angelica's Smile", 2010, 264, []),
        ("Game of Mirrors", 2011, 256, []),
        ("A Beam of Light", 2012, 272, []),
        ("A Voice in the Night", 2012, 264, []),
        ("A Nest of Vipers", 2013, 272, []),
    ]),
    ("Donna Leon", "en", ["Mystery", "Crime Fiction"], [
        ("Death at La Fenice", 1992, 263, []),
        ("Death in a Strange Country", 1993, 273, []),
        ("Dressed for Death", 1994, 270, []),
        ("Death and Judgment", 1995, 277, []),
        ("Acqua Alta", 1996, 267, []),
        ("Quietly in Their Sleep", 1997, 270, []),
        ("A Noble Radiance", 1998, 260, []),
        ("Fatal Remedies", 1999, 278, []),
        ("Friends in High Places", 2000, 250, []),
        ("A Sea of Troubles", 2001, 253, []),
        ("Willful Behavior", 2002, 278, []),
        ("Uniform Justice", 2003, 259, []),
        ("Doctored Evidence", 2004, 282, []),
        ("Blood from a Stone", 2005, 276, []),
        ("Through a Glass, Darkly", 2006, 280, []),
        ("Suffer the Little Children", 2007, 278, []),
        ("The Girl of His Dreams", 2008, 277, []),
        ("About Face", 2009, 262, []),
        ("A Question of Belief", 2010, 267, []),
        ("Drawing Conclusions", 2011, 260, []),
        ("Beastly Things", 2012, 256, []),
        ("The Golden Egg", 2013, 256, []),
        ("By Its Cover", 2014, 262, []),
        ("Falling in Love", 2015, 267, []),
        ("The Waters of Eternal Youth", 2016, 256, []),
        ("Earthly Remains", 2017, 260, []),
        ("The Temptation of Forgiveness", 2018, 290, []),
        ("Unto Us a Son Is Given", 2019, 256, []),
        ("Trace Elements", 2020, 260, []),
        ("Transient Desires", 2021, 302, []),
    ]),
    # Historical fiction
    ("Hilary Mantel", "en", ["Literary Fiction", "Historical Fiction"], [
        ("A Place of Greater Safety", 1992, 749, []),
    ]),
    ("Bernard Cornwell", "en", ["Historical Fiction", "Adventure"], [
        ("Sharpe's Tiger", 1997, 382, []),
        ("Sharpe's Triumph", 1998, 382, []),
        ("Sharpe's Fortress", 1999, 382, []),
        ("Sharpe's Trafalgar", 2000, 382, []),
        ("Sharpe's Prey", 2001, 352, []),
        ("Sharpe's Rifles", 1988, 304, []),
        ("Sharpe's Havoc", 2003, 383, []),
        ("Sharpe's Eagle", 1981, 270, []),
        ("Sharpe's Gold", 1981, 286, []),
        ("Sharpe's Escape", 2004, 383, []),
        ("Sharpe's Fury", 2006, 383, []),
        ("Sharpe's Battle", 1995, 352, []),
        ("Sharpe's Company", 1982, 280, []),
        ("Sharpe's Sword", 1983, 319, []),
        ("Sharpe's Enemy", 1984, 346, []),
        ("Sharpe's Honour", 1985, 320, []),
        ("Sharpe's Regiment", 1986, 304, []),
        ("Sharpe's Siege", 1987, 319, []),
        ("Sharpe's Revenge", 1989, 349, []),
        ("Sharpe's Waterloo", 1990, 378, []),
        ("Sharpe's Devil", 1992, 283, []),
        ("The Last Kingdom", 2004, 333, []),
        ("The Pale Horseman", 2005, 349, []),
        ("The Lords of the North", 2006, 328, []),
        ("Sword Song", 2007, 343, []),
        ("The Burning Land", 2009, 337, []),
        ("Death of Kings", 2011, 333, []),
        ("The Pagan Lord", 2013, 338, []),
        ("The Empty Throne", 2014, 310, []),
        ("Warriors of the Storm", 2015, 310, []),
        ("The Flame Bearer", 2016, 301, []),
        ("War of the Wolf", 2018, 336, []),
        ("Sword of Kings", 2019, 336, []),
        ("War Lord", 2020, 336, []),
    ]),
    ("C.J. Sansom", "en", ["Historical Fiction", "Mystery"], [
        ("Dissolution", 2003, 416, []),
        ("Dark Fire", 2004, 512, []),
        ("Sovereign", 2006, 583, []),
        ("Revelation", 2008, 545, []),
        ("Heartstone", 2010, 650, []),
        ("Lamentation", 2014, 640, []),
        ("Tombland", 2018, 880, []),
        ("Winter in Madrid", 2006, 537, ["Thriller"]),
        ("Dominion", 2012, 592, ["Alternate History"]),
    ]),
    ("Philippa Gregory", "en", ["Historical Fiction", "Romance"], [
        ("The Other Boleyn Girl", 2001, 530, []),
        ("The Queen's Fool", 2003, 529, []),
        ("The Virgin's Lover", 2004, 444, []),
        ("The Constant Princess", 2005, 393, []),
        ("The Boleyn Inheritance", 2006, 518, []),
        ("The Other Queen", 2008, 440, []),
        ("The White Queen", 2009, 437, []),
        ("The Red Queen", 2010, 382, []),
        ("The Lady of the Rivers", 2011, 448, []),
        ("The Kingmaker's Daughter", 2012, 416, []),
        ("The White Princess", 2013, 544, []),
        ("The King's Curse", 2014, 549, []),
        ("Three Sisters, Three Queens", 2016, 593, []),
        ("The Last Tudor", 2017, 529, []),
        ("The Other Boleyn Girl: A Novel", 2001, 661, []),
        ("Tidelands", 2019, 448, []),
        ("Dark Tides", 2020, 448, []),
        ("Dawnlands", 2022, 448, []),
    ]),
    ("Edward Rutherfurd", "en", ["Historical Fiction"], [
        ("Sarum", 1987, 897, []),
        ("Russka", 1991, 945, []),
        ("London", 1997, 829, []),
        ("The Forest", 2000, 598, []),
        ("Dublin: Foundation", 2004, 784, []),
        ("New York", 2009, 862, []),
        ("Paris", 2013, 844, []),
        ("China", 2021, 795, []),
    ]),
    ("James Clavell", "en", ["Historical Fiction", "Adventure"], [
        ("King Rat", 1962, 400, ["War"]),
        ("Tai-Pan", 1966, 732, []),
        ("Shōgun", 1975, 1152, ["Classic"]),
        ("Noble House", 1981, 1206, ["Thriller"]),
        ("Whirlwind", 1986, 1147, []),
        ("Gai-Jin", 1993, 1038, []),
    ]),
    ("Conn Iggulden", "en", ["Historical Fiction", "Adventure"], [
        ("Emperor: The Gates of Rome", 2003, 453, []),
        ("Emperor: The Death of Kings", 2004, 453, []),
        ("Emperor: The Field of Swords", 2005, 413, []),
        ("Emperor: The Gods of War", 2006, 416, []),
        ("Genghis: Birth of an Empire", 2007, 434, []),
        ("Genghis: Lords of the Bow", 2008, 434, []),
        ("Genghis: Bones of the Hills", 2008, 434, []),
        ("Khan: Empire of Silver", 2010, 434, []),
        ("Conqueror", 2011, 464, []),
        ("Wars of the Roses: Stormbird", 2014, 448, []),
        ("Wars of the Roses: Trinity", 2014, 400, []),
        ("Wars of the Roses: Bloodline", 2015, 400, []),
        ("Wars of the Roses: Ravenspur", 2016, 416, []),
        ("Dunstan", 2017, 448, []),
        ("The Gates of Athens", 2020, 384, []),
        ("Protector", 2021, 384, []),
        ("The Gates of Sparta", 2022, 400, []),
    ]),
    # More sci-fi
    ("Vernor Vinge", "en", ["Science Fiction"], [
        ("Tatja Grimm's World", 1987, 230, []),
        ("A Fire Upon the Deep", 1992, 613, []),
        ("A Deepness in the Sky", 1999, 606, []),
        ("Rainbows End", 2006, 364, []),
        ("The Children of the Sky", 2011, 444, []),
        ("True Names", 1981, 126, ["Short Stories"]),
    ]),
    ("Greg Bear", "en", ["Science Fiction"], [
        ("Hegira", 1979, 224, []),
        ("The Forge of God", 1987, 474, []),
        ("Anvil of Stars", 1992, 434, []),
        ("Blood Music", 1985, 263, []),
        ("Eon", 1985, 504, []),
        ("Eternity", 1988, 389, []),
        ("Queen of Angels", 1990, 420, []),
        ("Moving Mars", 1993, 385, []),
        ("Darwin's Radio", 1999, 440, []),
        ("Darwin's Children", 2003, 368, []),
        ("Vitals", 2002, 368, ["Thriller"]),
        ("Quantico", 2005, 357, ["Thriller"]),
        ("City at the End of Time", 2008, 476, []),
        ("Hull Zero Three", 2010, 320, []),
    ]),
    ("David Brin", "en", ["Science Fiction"], [
        ("Sundiver", 1980, 340, []),
        ("Startide Rising", 1983, 462, []),
        ("The Uplift War", 1987, 636, []),
        ("The Postman", 1985, 294, []),
        ("Heart of the Comet", 1986, 468, []),
        ("Earth", 1990, 601, []),
        ("Glory Season", 1993, 564, []),
        ("Brightness Reef", 1995, 580, []),
        ("Infinity's Shore", 1996, 528, []),
        ("Heaven's Reach", 1998, 448, []),
        ("Kiln People", 2002, 458, []),
        ("Existence", 2012, 556, []),
    ]),
    ("C.J. Cherryh", "en", ["Science Fiction", "Fantasy"], [
        ("Gate of Ivrel", 1976, 191, ["Fantasy"]),
        ("Brothers of Earth", 1976, 319, []),
        ("The Faded Sun: Kesrith", 1978, 312, []),
        ("The Faded Sun: Shon'jir", 1978, 238, []),
        ("The Faded Sun: Kutath", 1979, 299, []),
        ("Downbelow Station", 1981, 432, []),
        ("Merchanter's Luck", 1982, 215, []),
        ("The Pride of Chanur", 1981, 224, []),
        ("Chanur's Venture", 1984, 279, []),
        ("The Kif Strike Back", 1985, 281, []),
        ("Chanur's Homecoming", 1986, 313, []),
        ("Cyteen", 1988, 680, []),
        ("Rimrunners", 1989, 277, []),
        ("Heavy Time", 1991, 284, []),
        ("Hellburner", 1992, 326, []),
        ("Foreigner", 1994, 378, []),
        ("Invader", 1995, 399, []),
        ("Inheritor", 1996, 397, []),
        ("Precursor", 1999, 389, []),
        ("Defender", 2001, 392, []),
        ("Explorer", 2002, 416, []),
        ("Destroyer", 2005, 376, []),
        ("Pretender", 2006, 344, []),
        ("Deliverer", 2007, 356, []),
        ("Conspirator", 2009, 311, []),
        ("Deceiver", 2010, 340, []),
        ("Betrayer", 2011, 360, []),
    ]),
    ("Jack McDevitt", "en", ["Science Fiction"], [
        ("The Hercules Text", 1986, 336, []),
        ("A Talent for War", 1989, 310, []),
        ("The Engines of God", 1994, 419, []),
        ("Ancient Shores", 1996, 358, []),
        ("Eternity Road", 1997, 350, []),
        ("Moonfall", 1998, 526, []),
        ("Infinity Beach", 2000, 435, []),
        ("Deepsix", 2001, 432, []),
        ("Chindi", 2002, 511, []),
        ("Omega", 2003, 434, []),
        ("Polaris", 2004, 369, []),
        ("Seeker", 2005, 369, []),
        ("Odyssey", 2006, 403, []),
        ("Cauldron", 2007, 395, []),
        ("The Devil's Eye", 2008, 340, []),
        ("Time Travelers Never Die", 2009, 340, []),
        ("Echo", 2010, 369, []),
        ("Firebird", 2011, 369, []),
        ("Starhawk", 2013, 369, []),
        ("Coming Home", 2014, 375, []),
        ("Thunderbird", 2015, 369, []),
        ("The Long Sunset", 2018, 384, []),
        ("Octavia Gone", 2019, 384, []),
        ("Village in the Sky", 2023, 384, []),
    ]),
    # More literary fiction
    ("Richard Powers", "en", ["Literary Fiction"], [
        ("Three Farmers on Their Way to a Dance", 1985, 352, []),
        ("Prisoner's Dilemma", 1988, 348, []),
        ("The Gold Bug Variations", 1991, 639, []),
        ("Operation Wandering Soul", 1993, 352, []),
        ("Galatea 2.2", 1995, 329, []),
        ("Gain", 1998, 355, []),
        ("Plowing the Dark", 2000, 415, []),
        ("The Time of Our Singing", 2003, 631, []),
        ("The Echo Maker", 2006, 451, []),
        ("Generosity", 2009, 296, []),
        ("Orfeo", 2014, 369, []),
        ("The Overstory", 2018, 502, ["Classic"]),
        ("Bewilderment", 2021, 278, []),
        ("Playground", 2024, 384, []),
    ]),
    ("George Saunders", "en", ["Literary Fiction", "Short Stories"], [
        ("CivilWarLand in Bad Decline", 1996, 179, []),
        ("Pastoralia", 2000, 188, []),
        ("The Brief and Frightening Reign of Phil", 2005, 130, []),
        ("In Persuasion Nation", 2006, 228, []),
        ("Tenth of December", 2013, 251, []),
        ("Lincoln in the Bardo", 2017, 343, []),
        ("A Swim in a Pond in the Rain", 2021, 411, ["Non-Fiction"]),
        ("Liberation Day", 2022, 252, []),
    ]),
    ("Chimamanda Ngozi Adichie", "en", ["Literary Fiction"], [
        ("We Should All Be Feminists", 2014, 48, ["Non-Fiction"]),
        ("Dear Ijeawele", 2017, 63, ["Non-Fiction"]),
    ]),
    ("Ocean Vuong", "en", ["Literary Fiction", "Poetry"], [
        ("Night Sky with Exit Wounds", 2016, 89, ["Poetry"]),
        ("On Earth We're Briefly Gorgeous", 2019, 256, []),
        ("Time Is a Mother", 2022, 116, ["Poetry"]),
    ]),
    ("Hanya Yanagihara", "en", ["Literary Fiction"], [
        ("The People in the Trees", 2013, 369, []),
        ("A Little Life", 2015, 720, []),
        ("To Paradise", 2022, 708, []),
    ]),
    ("Sally Rooney", "en", ["Literary Fiction"], [
        ("Conversations with Friends", 2017, 321, []),
        ("Normal People", 2018, 266, []),
        ("Beautiful World, Where Are You", 2021, 356, []),
        ("Intermezzo", 2024, 448, []),
    ]),
    ("Rachel Kushner", "en", ["Literary Fiction"], [
        ("Telex from Cuba", 2008, 369, ["Historical Fiction"]),
        ("The Flamethrowers", 2013, 383, []),
        ("The Mars Room", 2018, 338, []),
        ("Creation Lake", 2024, 416, []),
    ]),
    ("Ottessa Moshfegh", "en", ["Literary Fiction"], [
        ("Eileen", 2015, 259, []),
        ("My Year of Rest and Relaxation", 2018, 289, []),
        ("Death in Her Hands", 2020, 272, ["Mystery"]),
        ("Lapvona", 2022, 272, []),
        ("Homesick for Another World", 2017, 289, ["Short Stories"]),
    ]),
]


def generate():
    batch_num = 101
    books_in_batch = []

    for author, lang, default_genres, works in AUTHORS:
        for title, year, pages, extra_genres in works:
            genres = list(default_genres) + extra_genres
            book = make_book(title, author, year, pages, genres, lang)
            books_in_batch.append(book)

            if len(books_in_batch) >= 100:
                fname = f"batch_{batch_num:03d}_batch17_{batch_num - 100}.json"
                path = os.path.join(BATCH_DIR, fname)
                with open(path, "w") as f:
                    json.dump(books_in_batch, f, indent=2)
                print(f"  {fname}: {len(books_in_batch)} books")
                batch_num += 1
                books_in_batch = []

    if books_in_batch:
        fname = f"batch_{batch_num:03d}_batch17_{batch_num - 100}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(books_in_batch, f, indent=2)
        print(f"  {fname}: {len(books_in_batch)} books")
        batch_num += 1

    total = sum(len(works) for _, _, _, works in AUTHORS)
    print(f"\nTotal new books: {total}")


if __name__ == "__main__":
    generate()
