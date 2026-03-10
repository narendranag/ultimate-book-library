#!/usr/bin/env python3
"""Batch 10: Genre fiction deep dive - more sci-fi, fantasy, horror, romance (batches 69-75)."""
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


def make_book(title, author, year, pages, genres, lang="en", description=""):
    isbn13 = make_isbn13(title, author)
    isbn10 = make_isbn10(isbn13)
    return {
        "title": title,
        "author": author,
        "year": year,
        "isbn_13": isbn13,
        "isbn_10": isbn10,
        "pages": pages,
        "genres": genres,
        "language": lang,
        "description": description,
    }


AUTHORS = [
    # Sci-fi masters
    ("Iain M. Banks", "en", ["Science Fiction"], [
        ("Consider Phlebas", 1987, 471, []),
        ("The Player of Games", 1988, 293, []),
        ("Use of Weapons", 1990, 411, []),
        ("The State of the Art", 1991, 214, ["Short Stories"]),
        ("Excession", 1996, 455, []),
        ("Inversions", 1998, 343, []),
        ("Look to Windward", 2000, 357, []),
        ("Matter", 2008, 593, []),
        ("Surface Detail", 2010, 627, []),
        ("The Hydrogen Sonata", 2012, 517, []),
        ("Against a Dark Background", 1993, 487, []),
        ("Feersum Endjinn", 1994, 279, []),
        ("The Algebraist", 2004, 434, []),
    ]),
    ("Peter F. Hamilton", "en", ["Science Fiction", "Space Opera"], [
        ("The Reality Dysfunction", 1996, 1225, []),
        ("The Neutronium Alchemist", 1997, 1174, []),
        ("The Naked God", 1999, 1174, []),
        ("Pandora's Star", 2004, 988, []),
        ("Judas Unchained", 2005, 816, []),
        ("The Dreaming Void", 2007, 630, []),
        ("The Temporal Void", 2008, 720, []),
        ("The Evolutionary Void", 2010, 704, []),
        ("Great North Road", 2012, 984, ["Mystery"]),
        ("The Abyss Beyond Dreams", 2014, 618, []),
        ("Night Without Stars", 2016, 726, []),
        ("Salvation", 2018, 576, []),
        ("Salvation Lost", 2019, 528, []),
        ("The Saints of Salvation", 2020, 546, []),
    ]),
    ("Alastair Reynolds", "en", ["Science Fiction", "Space Opera"], [
        ("Revelation Space", 2000, 585, []),
        ("Chasm City", 2001, 695, []),
        ("Redemption Ark", 2002, 694, []),
        ("Absolution Gap", 2003, 565, []),
        ("Century Rain", 2004, 501, []),
        ("Pushing Ice", 2005, 458, []),
        ("The Prefect", 2007, 410, []),
        ("House of Suns", 2008, 479, []),
        ("Terminal World", 2010, 487, []),
        ("Blue Remembered Earth", 2012, 500, []),
        ("On the Steel Breeze", 2013, 480, []),
        ("Poseidon's Wake", 2015, 480, []),
        ("Elysium Fire", 2018, 399, []),
        ("Inhibitor Phase", 2021, 464, []),
    ]),
    ("N.K. Jemisin", "en", ["Science Fiction", "Fantasy"], [
        ("The Hundred Thousand Kingdoms", 2010, 427, []),
        ("The Broken Kingdoms", 2010, 384, []),
        ("The Kingdom of Gods", 2011, 567, []),
        ("The Killing Moon", 2012, 418, []),
        ("The Shadowed Sun", 2012, 411, []),
        ("The Fifth Season", 2015, 468, []),
        ("The Obelisk Gate", 2016, 410, []),
        ("The Stone Sky", 2017, 398, []),
        ("The City We Became", 2020, 434, []),
        ("The World We Make", 2022, 357, []),
    ]),
    ("Ann Leckie", "en", ["Science Fiction"], [
        ("Ancillary Justice", 2013, 386, []),
        ("Ancillary Sword", 2014, 356, []),
        ("Ancillary Mercy", 2015, 330, []),
        ("Provenance", 2017, 381, []),
        ("The Raven Tower", 2019, 416, ["Fantasy"]),
        ("Translation State", 2023, 390, []),
    ]),
    ("Becky Chambers", "en", ["Science Fiction"], [
        ("The Long Way to a Small, Angry Planet", 2014, 518, []),
        ("A Closed and Common Orbit", 2016, 364, []),
        ("Record of a Spaceborn Few", 2018, 359, []),
        ("The Galaxy, and the Ground Within", 2021, 325, []),
        ("A Psalm for the Wild-Built", 2021, 160, []),
        ("A Prayer for the Crown-Shy", 2022, 152, []),
    ]),
    # Fantasy deep dive
    ("Brandon Sanderson", "en", ["Fantasy"], [
        ("Elantris", 2005, 638, []),
        ("The Final Empire", 2006, 541, []),
        ("The Well of Ascension", 2007, 590, []),
        ("The Hero of Ages", 2008, 572, []),
        ("Warbreaker", 2009, 592, []),
        ("The Way of Kings", 2010, 1007, []),
        ("The Alloy of Law", 2011, 332, []),
        ("Words of Radiance", 2014, 1087, []),
        ("Shadows of Self", 2015, 383, []),
        ("The Bands of Mourning", 2016, 447, []),
        ("Oathbringer", 2017, 1248, []),
        ("Skyward", 2018, 513, ["Science Fiction"]),
        ("Starsight", 2019, 461, ["Science Fiction"]),
        ("Rhythm of War", 2020, 1232, []),
        ("Cytonic", 2021, 298, ["Science Fiction"]),
        ("The Lost Metal", 2022, 528, []),
        ("Tress of the Emerald Sea", 2023, 386, []),
        ("Yumi and the Nightmare Painter", 2023, 464, []),
        ("The Sunlit Man", 2023, 392, []),
        ("Wind and Truth", 2024, 1200, []),
    ]),
    ("Joe Abercrombie", "en", ["Fantasy", "Dark Fantasy"], [
        ("The Blade Itself", 2006, 515, []),
        ("Before They Are Hanged", 2007, 441, []),
        ("Last Argument of Kings", 2008, 536, []),
        ("Best Served Cold", 2009, 630, []),
        ("The Heroes", 2011, 531, []),
        ("Red Country", 2012, 451, []),
        ("Sharp Ends", 2016, 289, ["Short Stories"]),
        ("A Little Hatred", 2019, 480, []),
        ("The Trouble with Peace", 2020, 496, []),
        ("The Wisdom of Crowds", 2021, 512, []),
        ("The Devil You Know", 2023, 432, []),
    ]),
    ("Steven Erikson", "en", ["Fantasy", "Epic Fantasy"], [
        ("Gardens of the Moon", 1999, 496, []),
        ("Deadhouse Gates", 2000, 604, []),
        ("Memories of Ice", 2001, 780, []),
        ("House of Chains", 2002, 798, []),
        ("Midnight Tides", 2004, 860, []),
        ("The Bonehunters", 2006, 1199, []),
        ("Reaper's Gale", 2007, 902, []),
        ("Toll the Hounds", 2008, 1263, []),
        ("Dust of Dreams", 2009, 887, []),
        ("The Crippled God", 2011, 895, []),
        ("Forge of Darkness", 2012, 752, []),
        ("Fall of Light", 2016, 880, []),
        ("Walk in Shadow", 2024, 900, []),
    ]),
    ("Robin McKinley", "en", ["Fantasy"], [
        ("Beauty", 1978, 247, []),
        ("The Door in the Hedge", 1981, 232, ["Short Stories"]),
        ("The Blue Sword", 1982, 272, ["Adventure"]),
        ("The Hero and the Crown", 1984, 227, ["Adventure"]),
        ("The Outlaws of Sherwood", 1988, 282, ["Historical Fiction"]),
        ("Deerskin", 1993, 309, []),
        ("Rose Daughter", 1997, 306, []),
        ("Spindle's End", 2000, 354, []),
        ("Sunshine", 2003, 389, ["Horror"]),
        ("Dragonhaven", 2007, 342, []),
        ("Pegasus", 2010, 404, []),
        ("Chalice", 2008, 263, []),
    ]),
    # Horror masters
    ("Shirley Jackson", "en", ["Horror", "Literary Fiction"], [
        ("The Road Through the Wall", 1948, 254, []),
        ("Hangsaman", 1951, 218, []),
        ("The Bird's Nest", 1954, 276, []),
        ("The Sundial", 1958, 245, []),
        ("The Haunting of Hill House", 1959, 246, ["Classic"]),
        ("We Have Always Lived in the Castle", 1962, 214, ["Classic"]),
        ("Life Among the Savages", 1953, 241, ["Humor", "Memoir"]),
        ("Raising Demons", 1957, 302, ["Humor", "Memoir"]),
        ("The Lottery and Other Stories", 1949, 302, ["Short Stories", "Classic"]),
        ("Come Along with Me", 1968, 268, ["Short Stories"]),
    ]),
    ("Peter Straub", "en", ["Horror", "Thriller"], [
        ("Julia", 1975, 284, []),
        ("If You Could See Me Now", 1977, 286, []),
        ("Ghost Story", 1979, 567, []),
        ("Shadowland", 1980, 466, []),
        ("Floating Dragon", 1983, 515, []),
        ("The Talisman", 1984, 646, ["Fantasy"]),
        ("Koko", 1988, 562, ["Mystery"]),
        ("Mystery", 1990, 548, []),
        ("The Throat", 1993, 689, []),
        ("The Hellfire Club", 1996, 462, []),
        ("Mr. X", 1999, 482, []),
        ("lost boy lost girl", 2003, 281, []),
        ("In the Night Room", 2004, 243, []),
        ("A Dark Matter", 2010, 397, []),
        ("Black House", 2001, 625, ["Fantasy"]),
    ]),
    ("Clive Barker", "en", ["Horror", "Fantasy"], [
        ("The Damnation Game", 1985, 379, []),
        ("The Hellbound Heart", 1986, 163, []),
        ("Weaveworld", 1987, 722, []),
        ("Cabal", 1988, 264, []),
        ("The Great and Secret Show", 1989, 550, []),
        ("Imajica", 1991, 824, []),
        ("The Thief of Always", 1992, 230, []),
        ("Everville", 1994, 484, []),
        ("Sacrament", 1996, 550, []),
        ("Galilee", 1998, 560, []),
        ("Coldheart Canyon", 2001, 676, []),
        ("Mister B. Gone", 2007, 247, []),
        ("The Scarlet Gospels", 2015, 369, []),
        ("Books of Blood", 1984, 462, ["Short Stories"]),
    ]),
    # Romance heavy hitters
    ("Nora Roberts", "en", ["Romance"], [
        ("Irish Thoroughbred", 1981, 256, []),
        ("Untamed", 1983, 256, []),
        ("This Magic Moment", 1983, 256, []),
        ("Born in Fire", 1994, 400, []),
        ("Born in Ice", 1995, 387, []),
        ("Born in Shame", 1996, 384, []),
        ("The Reef", 1998, 448, ["Thriller"]),
        ("River's End", 1999, 419, ["Thriller"]),
        ("Carolina Moon", 2000, 437, ["Thriller"]),
        ("The Villa", 2001, 468, ["Thriller"]),
        ("Midnight Bayou", 2001, 352, []),
        ("Chesapeake Blue", 2002, 336, []),
        ("Three Fates", 2002, 454, []),
        ("Birthright", 2003, 451, []),
        ("Northern Lights", 2004, 500, []),
        ("Blue Smoke", 2005, 472, ["Thriller"]),
        ("Angels Fall", 2006, 422, ["Thriller"]),
        ("High Noon", 2007, 452, ["Thriller"]),
        ("Tribute", 2008, 452, []),
        ("Black Hills", 2009, 452, []),
        ("The Search", 2010, 480, ["Thriller"]),
        ("Chasing Fire", 2011, 472, []),
        ("The Witness", 2012, 488, ["Thriller"]),
        ("Whiskey Beach", 2013, 480, []),
        ("The Collector", 2014, 470, ["Thriller"]),
        ("The Liar", 2015, 496, ["Thriller"]),
        ("The Obsession", 2016, 453, ["Thriller"]),
        ("Come Sundown", 2017, 496, ["Thriller"]),
        ("Shelter in Place", 2018, 464, ["Thriller"]),
        ("Under Currents", 2019, 464, ["Thriller"]),
        ("Hideaway", 2020, 464, []),
        ("Legacy", 2021, 432, []),
    ]),
    ("Diana Gabaldon", "en", ["Romance", "Historical Fiction", "Fantasy"], [
        ("Outlander", 1991, 850, []),
        ("Dragonfly in Amber", 1992, 947, []),
        ("Voyager", 1993, 1059, []),
        ("Drums of Autumn", 1996, 880, []),
        ("The Fiery Cross", 2001, 979, []),
        ("A Breath of Snow and Ashes", 2005, 980, []),
        ("An Echo in the Bone", 2009, 820, []),
        ("Written in My Own Heart's Blood", 2014, 825, []),
        ("Go Tell the Bees That I Am Gone", 2021, 896, []),
    ]),
    ("Nicholas Sparks", "en", ["Romance"], [
        ("The Notebook", 1996, 214, []),
        ("Message in a Bottle", 1998, 322, []),
        ("A Walk to Remember", 1999, 240, []),
        ("The Rescue", 2000, 352, []),
        ("A Bend in the Road", 2001, 341, []),
        ("Nights in Rodanthe", 2002, 212, []),
        ("The Guardian", 2003, 389, ["Thriller"]),
        ("The Wedding", 2003, 258, []),
        ("True Believer", 2005, 352, []),
        ("At First Sight", 2005, 277, []),
        ("Dear John", 2006, 276, []),
        ("The Choice", 2007, 278, []),
        ("The Lucky One", 2008, 326, []),
        ("The Last Song", 2009, 390, []),
        ("Safe Haven", 2010, 348, ["Thriller"]),
        ("The Best of Me", 2011, 278, []),
        ("The Longest Ride", 2013, 386, []),
        ("See Me", 2015, 478, ["Thriller"]),
        ("Two by Two", 2016, 485, []),
        ("Every Breath", 2018, 302, []),
        ("The Return", 2020, 352, []),
        ("The Wish", 2021, 380, []),
    ]),
    # More thriller authors
    ("Karin Slaughter", "en", ["Thriller", "Mystery", "Crime Fiction"], [
        ("Blindsighted", 2001, 392, []),
        ("Kisscut", 2002, 429, []),
        ("A Faint Cold Fear", 2003, 400, []),
        ("Indelible", 2004, 423, []),
        ("Faithless", 2005, 419, []),
        ("Beyond Reach", 2007, 401, []),
        ("Fractured", 2008, 418, []),
        ("Undone", 2009, 401, []),
        ("Broken", 2010, 414, []),
        ("Fallen", 2011, 401, []),
        ("Criminal", 2012, 418, []),
        ("Unseen", 2013, 401, []),
        ("Cop Town", 2014, 401, ["Historical Fiction"]),
        ("Pretty Girls", 2015, 409, []),
        ("The Kept Woman", 2016, 401, []),
        ("The Good Daughter", 2017, 529, []),
        ("Pieces of Her", 2018, 480, []),
        ("The Last Widow", 2019, 418, []),
        ("The Silent Wife", 2020, 460, []),
        ("After That Night", 2023, 432, []),
    ]),
    ("Jeffery Deaver", "en", ["Thriller", "Mystery"], [
        ("Voodoo", 1988, 350, []),
        ("Manhattan Is My Beat", 1989, 268, []),
        ("Death of a Blue Movie Star", 1990, 337, []),
        ("A Maiden's Grave", 1995, 467, []),
        ("The Bone Collector", 1997, 421, []),
        ("The Coffin Dancer", 1998, 384, []),
        ("The Empty Chair", 2000, 423, []),
        ("The Stone Monkey", 2002, 423, []),
        ("The Vanished Man", 2003, 399, []),
        ("The Twelfth Card", 2005, 423, []),
        ("The Cold Moon", 2006, 432, []),
        ("The Sleeping Doll", 2007, 390, []),
        ("The Broken Window", 2008, 423, []),
        ("The Burning Wire", 2010, 423, []),
        ("The Kill Room", 2013, 421, []),
        ("The Skin Collector", 2014, 421, []),
        ("The Steel Kiss", 2016, 421, []),
        ("The Burial Hour", 2017, 421, []),
        ("The Cutting Edge", 2018, 421, []),
        ("The Midnight Lock", 2021, 405, []),
    ]),
    ("Tess Gerritsen", "en", ["Thriller", "Mystery"], [
        ("Harvest", 1996, 348, ["Medical Thriller"]),
        ("Life Support", 1997, 352, ["Medical Thriller"]),
        ("Bloodstream", 1998, 356, ["Medical Thriller"]),
        ("Gravity", 1999, 341, ["Science Fiction"]),
        ("The Surgeon", 2001, 341, []),
        ("The Apprentice", 2002, 341, []),
        ("The Sinner", 2003, 341, []),
        ("Body Double", 2004, 341, []),
        ("Vanish", 2005, 341, []),
        ("The Mephisto Club", 2006, 341, []),
        ("The Bone Garden", 2007, 341, ["Historical Fiction"]),
        ("The Keepsake", 2008, 341, []),
        ("Ice Cold", 2010, 341, []),
        ("The Silent Girl", 2011, 341, []),
        ("Last to Die", 2012, 341, []),
        ("Die Again", 2014, 341, []),
        ("Playing with Fire", 2015, 308, []),
        ("I Know a Secret", 2017, 289, []),
        ("The Shape of Night", 2019, 285, []),
        ("Choose Me", 2021, 336, []),
    ]),
]


def generate():
    batch_num = 69
    books_in_batch = []

    for author, lang, default_genres, works in AUTHORS:
        for title, year, pages, extra_genres in works:
            genres = list(default_genres) + extra_genres
            book = make_book(title, author, year, pages, genres, lang)
            books_in_batch.append(book)

            if len(books_in_batch) >= 100:
                fname = f"batch_{batch_num:02d}_authors_{batch_num - 41}.json"
                path = os.path.join(BATCH_DIR, fname)
                with open(path, "w") as f:
                    json.dump(books_in_batch, f, indent=2)
                print(f"  {fname}: {len(books_in_batch)} books")
                batch_num += 1
                books_in_batch = []

    if books_in_batch:
        fname = f"batch_{batch_num:02d}_authors_{batch_num - 41}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(books_in_batch, f, indent=2)
        print(f"  {fname}: {len(books_in_batch)} books")
        batch_num += 1

    total = sum(len(works) for _, _, _, works in AUTHORS)
    print(f"\nTotal new books: {total}")


if __name__ == "__main__":
    generate()
