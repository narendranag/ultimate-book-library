#!/usr/bin/env python3
"""Batch 24: More fresh authors - mystery, sci-fi, literary, non-fiction."""
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

# === MYSTERY/DETECTIVE - FRESH AUTHORS ===

# Tony Hillerman - Navajo mysteries
for title, year, pages in [
    ("The Blessing Way", 1970, 201), ("The Fly on the Wall", 1971, 220),
    ("Dance Hall of the Dead", 1973, 166), ("Listening Woman", 1978, 200),
    ("People of Darkness", 1980, 274), ("The Dark Wind", 1982, 214),
    ("The Ghostway", 1984, 213), ("Skinwalkers", 1986, 216),
    ("A Thief of Time", 1988, 209), ("Talking God", 1989, 239),
    ("Coyote Waits", 1990, 292), ("Sacred Clowns", 1993, 305),
    ("The Fallen Man", 1996, 294), ("The First Eagle", 1998, 278),
    ("Hunting Badger", 1999, 275), ("The Wailing Wind", 2002, 232),
    ("The Sinister Pig", 2003, 228), ("Skeleton Man", 2004, 230),
    ("The Shape Shifter", 2006, 276),
]:
    ALL_BOOKS.append(make_book(title, "Tony Hillerman", year, pages, ["Mystery", "Crime Fiction"]))

# Martha Grimes - Richard Jury series
for title, year, pages in [
    ("The Man with a Load of Mischief", 1981, 312), ("The Old Fox Deceiv'd", 1982, 299),
    ("The Anodyne Necklace", 1983, 250), ("The Dirty Duck", 1984, 262),
    ("Jerusalem Inn", 1984, 299), ("Help the Poor Struggler", 1985, 225),
    ("The Deer Leap", 1985, 282), ("I Am the Only Running Footman", 1986, 298),
    ("The Five Bells and Bladebone", 1987, 299), ("The Old Silent", 1989, 425),
    ("The Old Contemptibles", 1991, 344), ("The Horse You Came In On", 1993, 331),
    ("Rainbow's End", 1995, 368), ("The Case Has Altered", 1997, 371),
    ("The Stargazey", 1998, 337), ("The Lamorna Wink", 1999, 386),
    ("The Blue Last", 2001, 402), ("The Winds of Change", 2004, 384),
    ("The Old Wine Shades", 2006, 352), ("Dust", 2007, 391),
    ("The Black Cat", 2010, 384), ("Vertigo 42", 2014, 384),
]:
    ALL_BOOKS.append(make_book(title, "Martha Grimes", year, pages, ["Mystery", "Crime Fiction"]))

# Robert B. Parker - Spenser series
for title, year, pages in [
    ("The Godwulf Manuscript", 1973, 187), ("God Save the Child", 1974, 189),
    ("Mortal Stakes", 1975, 172), ("Promised Land", 1976, 181),
    ("The Judas Goat", 1978, 190), ("Looking for Rachel Wallace", 1980, 219),
    ("Early Autumn", 1981, 211), ("A Savage Place", 1981, 182),
    ("Ceremony", 1982, 183), ("The Widening Gyre", 1983, 183),
    ("Valediction", 1984, 211), ("A Catskill Eagle", 1985, 311),
    ("Taming a Sea-Horse", 1986, 198), ("Pale Kings and Princes", 1987, 211),
    ("Crimson Joy", 1988, 211), ("Playmates", 1989, 212),
    ("Stardust", 1990, 211), ("Pastime", 1991, 223),
    ("Double Deuce", 1992, 224), ("Paper Doll", 1993, 210),
    ("Walking Shadow", 1994, 269), ("Thin Air", 1995, 293),
    ("Chance", 1996, 312), ("Small Vices", 1997, 308),
    ("Sudden Mischief", 1998, 294), ("Hush Money", 1999, 309),
    ("Hugger Mugger", 2000, 307), ("Potshot", 2001, 294),
    ("Widow's Walk", 2002, 294), ("Back Story", 2003, 291),
]:
    ALL_BOOKS.append(make_book(title, "Robert B. Parker", year, pages, ["Mystery", "Crime Fiction"]))

# John Sandford - Prey series
for title, year, pages in [
    ("Rules of Prey", 1989, 316), ("Shadow Prey", 1990, 350),
    ("Eyes of Prey", 1991, 356), ("Silent Prey", 1992, 320),
    ("Winter Prey", 1993, 361), ("Night Prey", 1994, 339),
    ("Mind Prey", 1995, 323), ("Sudden Prey", 1996, 362),
    ("Secret Prey", 1998, 408), ("Certain Prey", 1999, 339),
    ("Easy Prey", 2000, 407), ("Chosen Prey", 2001, 407),
    ("Mortal Prey", 2002, 359), ("Naked Prey", 2003, 359),
    ("Hidden Prey", 2004, 393), ("Broken Prey", 2005, 390),
    ("Invisible Prey", 2007, 370), ("Phantom Prey", 2008, 372),
    ("Wicked Prey", 2009, 372), ("Storm Prey", 2010, 390),
    ("Buried Prey", 2011, 390), ("Stolen Prey", 2012, 406),
    ("Silken Prey", 2013, 406), ("Field of Prey", 2014, 390),
    ("Gathering Prey", 2015, 390), ("Extreme Prey", 2016, 390),
    ("Golden Prey", 2017, 400), ("Twisted Prey", 2018, 400),
    ("Neon Prey", 2019, 400), ("Masked Prey", 2020, 400),
]:
    ALL_BOOKS.append(make_book(title, "John Sandford", year, pages, ["Mystery", "Thriller", "Crime Fiction"]))

# Faye Kellerman - Peter Decker/Rina Lazarus
for title, year, pages in [
    ("The Ritual Bath", 1986, 293), ("Sacred and Profane", 1987, 326),
    ("Milk and Honey", 1990, 384), ("Day of Atonement", 1991, 359),
    ("False Prophet", 1992, 384), ("Grievous Sin", 1993, 384),
    ("Sanctuary", 1994, 400), ("Justice", 1995, 416),
    ("Prayers for the Dead", 1996, 406), ("Serpent's Tooth", 1997, 400),
    ("Jupiter's Bones", 1999, 384), ("Stalker", 2000, 384),
    ("The Forgotten", 2001, 384), ("Stone Kiss", 2002, 400),
    ("Street Dreams", 2003, 400), ("The Burnt House", 2007, 384),
    ("The Mercedes Coffin", 2008, 416), ("Blindman's Bluff", 2009, 384),
    ("Hangman", 2010, 384), ("Gun Games", 2012, 384),
    ("The Beast", 2013, 384), ("Murder 101", 2014, 384),
    ("The Theory of Death", 2015, 384), ("Bone Box", 2017, 352),
    ("Walking Shadows", 2018, 384), ("The Lost Boys", 2021, 384),
]:
    ALL_BOOKS.append(make_book(title, "Faye Kellerman", year, pages, ["Mystery", "Crime Fiction"]))

# Arnaldur Indriðason (filling remaining)
for title, year, pages in [
    ("Sons of Dust", 1997, 280), ("Silence of the Grave", 2001, 312),
    ("Voices", 2003, 320), ("The Draining Lake", 2004, 352),
    ("Arctic Chill", 2005, 320), ("Hypothermia", 2007, 320),
    ("Outrage", 2008, 288), ("Black Skies", 2009, 304),
    ("Strange Shores", 2010, 288), ("Reykjavik Nights", 2012, 288),
    ("The Shadow District", 2013, 320), ("The Shadow Killer", 2015, 352),
    ("The Darkness Knows", 2017, 320),
]:
    ALL_BOOKS.append(make_book(title, "Arnaldur Indriðason", year, pages, ["Crime Fiction", "Mystery"], "is"))

# === MORE SCIENCE FICTION ===

# Lois McMaster Bujold - Vorkosigan
for title, year, pages in [
    ("Shards of Honor", 1986, 253), ("The Warrior's Apprentice", 1986, 315),
    ("Ethan of Athos", 1986, 235), ("Falling Free", 1988, 307),
    ("Brothers in Arms", 1989, 338), ("Borders of Infinity", 1989, 311),
    ("The Vor Game", 1990, 345), ("Barrayar", 1991, 386),
    ("Mirror Dance", 1994, 387), ("Cetaganda", 1995, 302),
    ("Memory", 1996, 462), ("Komarr", 1998, 374),
    ("A Civil Campaign", 1999, 405), ("Diplomatic Immunity", 2002, 311),
    ("Cryoburn", 2010, 345), ("Captain Vorpatril's Alliance", 2012, 422),
    ("Gentleman Jole and the Red Queen", 2016, 354),
]:
    ALL_BOOKS.append(make_book(title, "Lois McMaster Bujold", year, pages, ["Science Fiction"]))

# David Weber - Honor Harrington
for title, year, pages in [
    ("On Basilisk Station", 1993, 422), ("The Honor of the Queen", 1993, 380),
    ("The Short Victorious War", 1994, 376), ("Field of Dishonor", 1994, 352),
    ("Flag in Exile", 1995, 416), ("Honor Among Enemies", 1996, 544),
    ("In Enemy Hands", 1997, 544), ("Echoes of Honor", 1998, 702),
    ("Ashes of Victory", 2000, 624), ("War of Honor", 2002, 877),
    ("At All Costs", 2005, 832), ("Mission of Honor", 2010, 688),
    ("A Rising Thunder", 2012, 464), ("Shadow of Freedom", 2013, 368),
    ("Uncompromising Honor", 2018, 752),
]:
    ALL_BOOKS.append(make_book(title, "David Weber", year, pages, ["Science Fiction", "Military Fiction"]))

# Jack Campbell / John G. Hemry - Lost Fleet
for title, year, pages in [
    ("Dauntless", 2006, 293), ("Fearless", 2007, 295),
    ("Courageous", 2007, 296), ("Valiant", 2008, 298),
    ("Relentless", 2009, 302), ("Victorious", 2010, 312),
    ("Dreadnaught", 2011, 354), ("Invincible", 2012, 354),
    ("Guardian", 2013, 354), ("Steadfast", 2014, 354),
    ("Leviathan", 2015, 370),
]:
    ALL_BOOKS.append(make_book(title, "Jack Campbell", year, pages, ["Science Fiction", "Military Fiction"]))

# Becky Chambers - Wayfarers
for title, year, pages in [
    ("The Long Way to a Small, Angry Planet", 2014, 518),
    ("A Closed and Common Orbit", 2016, 365),
    ("Record of a Spaceborn Few", 2018, 368),
    ("The Galaxy, and the Ground Within", 2021, 336),
    ("A Psalm for the Wild-Built", 2021, 160),
    ("A Prayer for the Crown-Shy", 2022, 152),
]:
    ALL_BOOKS.append(make_book(title, "Becky Chambers", year, pages, ["Science Fiction"]))

# Adrian Tchaikovsky
for title, year, pages in [
    ("Empire in Black and Gold", 2008, 612), ("Dragonfly Falling", 2009, 596),
    ("Blood of the Mantis", 2009, 437), ("Salute the Dark", 2010, 532),
    ("The Scarab Path", 2010, 580), ("The Sea Watch", 2011, 517),
    ("Heirs of the Blade", 2011, 437), ("The Air War", 2012, 567),
    ("War Master's Gate", 2013, 580), ("Seal of the Worm", 2014, 580),
    ("Children of Time", 2015, 609), ("Children of Ruin", 2019, 567),
    ("The Tiger and the Wolf", 2016, 592), ("The Bear and the Serpent", 2017, 608),
    ("The Hyena and the Hawk", 2018, 576), ("Shards of Earth", 2021, 560),
    ("Eyes of the Void", 2022, 560), ("Lords of Uncreation", 2023, 592),
    ("Children of Memory", 2022, 480), ("Elder Race", 2021, 208),
    ("Cage of Souls", 2019, 464), ("Dogs of War", 2017, 320),
]:
    ALL_BOOKS.append(make_book(title, "Adrian Tchaikovsky", year, pages, ["Science Fiction", "Fantasy"]))

# John Scalzi
for title, year, pages in [
    ("Old Man's War", 2005, 351), ("The Ghost Brigades", 2006, 343),
    ("The Android's Dream", 2006, 396), ("The Last Colony", 2007, 320),
    ("Zoe's Tale", 2008, 335), ("Agent to the Stars", 2005, 368),
    ("Fuzzy Nation", 2011, 304), ("Redshirts", 2012, 317),
    ("The Human Division", 2013, 432), ("Lock In", 2014, 336),
    ("The End of All Things", 2015, 384), ("The Collapsing Empire", 2017, 333),
    ("The Consuming Fire", 2018, 320), ("The Last Emperox", 2020, 320),
    ("The Kaiju Preservation Society", 2022, 264), ("Starter Villain", 2023, 272),
]:
    ALL_BOOKS.append(make_book(title, "John Scalzi", year, pages, ["Science Fiction"]))

# === LITERARY FICTION - FRESH AUTHORS ===

# Per Petterson
for title, year, pages in [
    ("To Siberia", 1996, 232), ("In the Wake", 2000, 208),
    ("Out Stealing Horses", 2003, 238), ("I Curse the River of Time", 2008, 233),
    ("I Refuse", 2012, 280), ("Men in My Situation", 2018, 320),
]:
    ALL_BOOKS.append(make_book(title, "Per Petterson", year, pages, ["Literary Fiction"], "no"))

# Jesmyn Ward
for title, year, pages in [
    ("Where the Line Bleeds", 2008, 256), ("Salvage the Bones", 2011, 261),
    ("Sing, Unburied, Sing", 2017, 289), ("Navigate Your Stars", 2020, 48),
    ("Let Us Descend", 2023, 304),
]:
    ALL_BOOKS.append(make_book(title, "Jesmyn Ward", year, pages, ["Literary Fiction"]))

# Chimamanda Ngozi Adichie (filling)
for title, year, pages in [
    ("Purple Hibiscus", 2003, 307), ("Half of a Yellow Sun", 2006, 433),
    ("The Thing Around Your Neck", 2009, 218), ("Americanah", 2013, 477),
    ("Dear Ijeawele", 2017, 63), ("Notes on Grief", 2021, 80),
]:
    ALL_BOOKS.append(make_book(title, "Chimamanda Ngozi Adichie", year, pages, ["Literary Fiction"]))

# Lauren Groff
for title, year, pages in [
    ("The Monsters of Templeton", 2008, 364), ("Arcadia", 2012, 289),
    ("Fates and Furies", 2015, 390), ("Florida", 2018, 275),
    ("Matrix", 2021, 258), ("The Vaster Wilds", 2023, 272),
]:
    ALL_BOOKS.append(make_book(title, "Lauren Groff", year, pages, ["Literary Fiction"]))

# Rachel Cusk
for title, year, pages in [
    ("Saving Agnes", 1993, 261), ("The Temporary", 1995, 240),
    ("The Country Life", 1997, 273), ("The Lucky Ones", 2003, 224),
    ("In the Fold", 2005, 256), ("Arlington Park", 2006, 256),
    ("The Bradshaw Variations", 2009, 240), ("Outline", 2014, 249),
    ("Transit", 2016, 260), ("Kudos", 2018, 240),
    ("Second Place", 2021, 192), ("Parade", 2024, 224),
]:
    ALL_BOOKS.append(make_book(title, "Rachel Cusk", year, pages, ["Literary Fiction"]))

# Paul Auster
for title, year, pages in [
    ("Squeeze Play", 1982, 254), ("The Invention of Solitude", 1982, 186),
    ("City of Glass", 1985, 203), ("Ghosts", 1986, 96),
    ("The Locked Room", 1986, 179), ("In the Country of Last Things", 1987, 188),
    ("Moon Palace", 1989, 307), ("The Music of Chance", 1990, 217),
    ("Leviathan", 1992, 275), ("Mr. Vertigo", 1994, 293),
    ("Timbuktu", 1999, 181), ("The Book of Illusions", 2002, 321),
    ("Oracle Night", 2003, 243), ("The Brooklyn Follies", 2005, 306),
    ("Travels in the Scriptorium", 2006, 145), ("Man in the Dark", 2008, 180),
    ("Invisible", 2009, 308), ("Sunset Park", 2010, 309),
    ("4 3 2 1", 2017, 866), ("Baumgartner", 2023, 208),
]:
    ALL_BOOKS.append(make_book(title, "Paul Auster", year, pages, ["Literary Fiction"]))

# Jenny Offill
for title, year, pages in [
    ("Last Things", 1999, 256), ("Dept. of Speculation", 2014, 177),
    ("Weather", 2020, 224),
]:
    ALL_BOOKS.append(make_book(title, "Jenny Offill", year, pages, ["Literary Fiction"]))

# Sigrid Undset
for title, year, pages in [
    ("Jenny", 1911, 367), ("Kristin Lavransdatter: The Wreath", 1920, 299),
    ("Kristin Lavransdatter: The Wife", 1921, 398),
    ("Kristin Lavransdatter: The Cross", 1922, 423),
    ("The Master of Hestviken: The Axe", 1925, 271),
    ("The Master of Hestviken: The Snake Pit", 1925, 299),
    ("The Master of Hestviken: In the Wilderness", 1927, 208),
    ("The Master of Hestviken: The Son Avenger", 1927, 267),
    ("Ida Elisabeth", 1932, 384), ("The Faithful Wife", 1936, 256),
]:
    ALL_BOOKS.append(make_book(title, "Sigrid Undset", year, pages, ["Literary Fiction", "Historical Fiction"], "no"))

# Halldór Laxness
for title, year, pages in [
    ("Salka Valka", 1931, 435), ("Independent People", 1934, 470),
    ("World Light", 1937, 538), ("Iceland's Bell", 1943, 517),
    ("The Atom Station", 1948, 179), ("The Happy Warriors", 1952, 225),
    ("The Fish Can Sing", 1957, 267), ("Paradise Reclaimed", 1960, 269),
    ("Christianity at Glacier", 1968, 184),
]:
    ALL_BOOKS.append(make_book(title, "Halldór Laxness", year, pages, ["Literary Fiction"], "is"))

# === HORROR ===

# Shirley Jackson (filling remaining)
for title, year, pages in [
    ("The Road Through the Wall", 1948, 215),
    ("Hangsaman", 1951, 218), ("The Bird's Nest", 1954, 276),
    ("The Sundial", 1958, 245),
    ("We Have Always Lived in the Castle", 1962, 214),
]:
    ALL_BOOKS.append(make_book(title, "Shirley Jackson", year, pages, ["Horror", "Literary Fiction"]))

# Paul Tremblay
for title, year, pages in [
    ("A Head Full of Ghosts", 2015, 286), ("Disappearance at Devil's Rock", 2016, 336),
    ("The Cabin at the End of the World", 2018, 272),
    ("Growing Things and Other Stories", 2019, 384),
    ("Survivor Song", 2020, 304), ("The Pallbearers Club", 2022, 272),
    ("Horror Movie", 2024, 288),
]:
    ALL_BOOKS.append(make_book(title, "Paul Tremblay", year, pages, ["Horror"]))

# Thomas Harris
for title, year, pages in [
    ("Black Sunday", 1975, 318), ("Red Dragon", 1981, 348),
    ("The Silence of the Lambs", 1988, 338), ("Hannibal", 1999, 484),
    ("Hannibal Rising", 2006, 323), ("Cari Mora", 2019, 307),
]:
    ALL_BOOKS.append(make_book(title, "Thomas Harris", year, pages, ["Thriller", "Horror"]))

# === NON-FICTION EXPANSION ===

# Yuval Noah Harari
for title, year, pages in [
    ("Sapiens", 2011, 443), ("Homo Deus", 2015, 449),
    ("21 Lessons for the 21st Century", 2018, 372),
    ("Unstoppable Us", 2022, 192), ("Nexus", 2024, 528),
]:
    ALL_BOOKS.append(make_book(title, "Yuval Noah Harari", year, pages, ["Non-Fiction", "History"]))

# Robert Caro
for title, year, pages in [
    ("The Power Broker", 1974, 1246), ("The Path to Power", 1982, 882),
    ("Means of Ascent", 1990, 506), ("Master of the Senate", 2002, 1167),
    ("The Passage of Power", 2012, 605), ("Working", 2019, 207),
]:
    ALL_BOOKS.append(make_book(title, "Robert Caro", year, pages, ["Non-Fiction", "History", "Biography"]))

# David McCullough
for title, year, pages in [
    ("The Johnstown Flood", 1968, 302), ("The Great Bridge", 1972, 636),
    ("The Path Between the Seas", 1977, 698), ("Mornings on Horseback", 1981, 445),
    ("Brave Companions", 1992, 240), ("Truman", 1992, 1117),
    ("John Adams", 2001, 751), ("1776", 2005, 386),
    ("The Greater Journey", 2011, 558), ("The Wright Brothers", 2015, 320),
    ("The Pioneers", 2019, 331),
]:
    ALL_BOOKS.append(make_book(title, "David McCullough", year, pages, ["Non-Fiction", "History", "Biography"]))

# Malcolm Gladwell
for title, year, pages in [
    ("The Tipping Point", 2000, 280), ("Blink", 2005, 277),
    ("Outliers", 2008, 309), ("What the Dog Saw", 2009, 410),
    ("David and Goliath", 2013, 305), ("Talking to Strangers", 2019, 400),
    ("The Bomber Mafia", 2021, 256), ("Revenge of the Tipping Point", 2024, 336),
]:
    ALL_BOOKS.append(make_book(title, "Malcolm Gladwell", year, pages, ["Non-Fiction"]))

# Rebecca Solnit
for title, year, pages in [
    ("Savage Dreams", 1994, 408), ("Wanderlust", 2000, 326),
    ("River of Shadows", 2003, 305), ("A Field Guide to Getting Lost", 2005, 206),
    ("A Paradise Built in Hell", 2009, 353), ("Infinite City", 2010, 165),
    ("The Faraway Nearby", 2013, 259), ("Men Explain Things to Me", 2014, 130),
    ("Hope in the Dark", 2016, 168), ("The Mother of All Questions", 2017, 176),
    ("Recollections of My Nonexistence", 2020, 240),
    ("Orwell's Roses", 2021, 320),
]:
    ALL_BOOKS.append(make_book(title, "Rebecca Solnit", year, pages, ["Non-Fiction"]))

# Ta-Nehisi Coates
for title, year, pages in [
    ("The Beautiful Struggle", 2008, 222),
    ("Between the World and Me", 2015, 152),
    ("We Were Eight Years in Power", 2017, 384),
    ("The Water Dancer", 2019, 403), ("The Message", 2024, 256),
]:
    ALL_BOOKS.append(make_book(title, "Ta-Nehisi Coates", year, pages, ["Non-Fiction", "Memoir"]))

# Roxane Gay
for title, year, pages in [
    ("An Untamed State", 2014, 368), ("Bad Feminist", 2014, 320),
    ("Difficult Women", 2017, 272), ("Hunger", 2017, 306),
    ("Not That Bad", 2018, 368), ("Opinions", 2024, 256),
]:
    ALL_BOOKS.append(make_book(title, "Roxane Gay", year, pages, ["Non-Fiction", "Memoir"]))

# Michael Lewis
for title, year, pages in [
    ("Liar's Poker", 1989, 249), ("The Money Culture", 1991, 288),
    ("Trail Fever", 1997, 316), ("The New New Thing", 1999, 268),
    ("Moneyball", 2003, 288), ("Coach", 2005, 95),
    ("The Blind Side", 2006, 299), ("Panic", 2008, 256),
    ("Home Game", 2009, 190), ("The Big Short", 2010, 291),
    ("Boomerang", 2011, 213), ("Flash Boys", 2014, 274),
    ("The Undoing Project", 2016, 362), ("The Fifth Risk", 2018, 219),
    ("The Premonition", 2021, 304), ("Going Infinite", 2023, 260),
]:
    ALL_BOOKS.append(make_book(title, "Michael Lewis", year, pages, ["Non-Fiction"]))

# Naomi Klein
for title, year, pages in [
    ("No Logo", 1999, 490), ("Fences and Windows", 2002, 268),
    ("The Shock Doctrine", 2007, 558), ("This Changes Everything", 2014, 576),
    ("No Is Not Enough", 2017, 273), ("The Battle for Paradise", 2018, 96),
    ("On Fire", 2019, 310), ("Doppelganger", 2023, 416),
]:
    ALL_BOOKS.append(make_book(title, "Naomi Klein", year, pages, ["Non-Fiction"]))

# === POETRY COLLECTIONS ===

# Seamus Heaney
for title, year, pages in [
    ("Death of a Naturalist", 1966, 57), ("Door into the Dark", 1969, 56),
    ("Wintering Out", 1972, 80), ("North", 1975, 78),
    ("Field Work", 1979, 60), ("Station Island", 1984, 123),
    ("The Haw Lantern", 1987, 52), ("Seeing Things", 1991, 107),
    ("The Spirit Level", 1996, 70), ("Electric Light", 2001, 81),
    ("District and Circle", 2006, 78), ("Human Chain", 2010, 85),
]:
    ALL_BOOKS.append(make_book(title, "Seamus Heaney", year, pages, ["Poetry"]))

# Derek Walcott
for title, year, pages in [
    ("In a Green Night", 1962, 80), ("The Castaway", 1965, 60),
    ("The Gulf", 1969, 72), ("Another Life", 1973, 144),
    ("Sea Grapes", 1976, 80), ("The Star-Apple Kingdom", 1979, 57),
    ("The Fortunate Traveller", 1981, 98), ("Midsummer", 1984, 54),
    ("The Arkansas Testament", 1987, 117), ("Omeros", 1990, 325),
    ("The Bounty", 1997, 79), ("Tiepolo's Hound", 2000, 164),
    ("The Prodigal", 2004, 105), ("White Egrets", 2010, 96),
]:
    ALL_BOOKS.append(make_book(title, "Derek Walcott", year, pages, ["Poetry"]))

# Mary Oliver
for title, year, pages in [
    ("No Voyage and Other Poems", 1963, 64), ("The River Styx, Ohio", 1972, 63),
    ("Twelve Moons", 1979, 60), ("American Primitive", 1983, 78),
    ("Dream Work", 1986, 70), ("House of Light", 1990, 64),
    ("New and Selected Poems", 1992, 255), ("White Pine", 1994, 67),
    ("West Wind", 1997, 63), ("The Leaf and the Cloud", 2000, 55),
    ("What Do We Know", 2002, 70), ("Why I Wake Early", 2004, 64),
    ("Thirst", 2006, 71), ("Red Bird", 2008, 95),
    ("A Thousand Mornings", 2012, 79), ("Devotions", 2017, 461),
    ("Felicity", 2015, 46),
]:
    ALL_BOOKS.append(make_book(title, "Mary Oliver", year, pages, ["Poetry"]))

# === ADDITIONAL FRESH AUTHORS ===

# Kate Atkinson - Jackson Brodie series + literary
for title, year, pages in [
    ("Behind the Scenes at the Museum", 1995, 382),
    ("Human Croquet", 1997, 342), ("Emotionally Weird", 2000, 342),
    ("Not the End of the World", 2002, 244), ("Case Histories", 2004, 312),
    ("One Good Turn", 2006, 415), ("When Will There Be Good News?", 2008, 388),
    ("Started Early, Took My Dog", 2010, 371), ("Life After Life", 2013, 529),
    ("A God in Ruins", 2015, 400), ("Transcription", 2018, 352),
    ("Big Sky", 2019, 400), ("Shrines of Gaiety", 2022, 432),
    ("Normal Rules Don't Apply", 2023, 192),
]:
    ALL_BOOKS.append(make_book(title, "Kate Atkinson", year, pages, ["Literary Fiction", "Mystery"]))

# David Lodge
for title, year, pages in [
    ("The Picturegoers", 1960, 256), ("Ginger, You're Barmy", 1962, 224),
    ("The British Museum Is Falling Down", 1965, 192),
    ("Out of the Shelter", 1970, 288), ("Changing Places", 1975, 251),
    ("How Far Can You Go?", 1980, 244), ("Small World", 1984, 339),
    ("Nice Work", 1988, 277), ("Paradise News", 1991, 293),
    ("Therapy", 1995, 321), ("Home Truths", 1999, 344),
    ("Thinks...", 2001, 341), ("Author, Author", 2004, 389),
    ("Deaf Sentence", 2008, 294), ("A Man of Parts", 2011, 544),
    ("Quite a Good Time to Be Born", 2015, 342),
]:
    ALL_BOOKS.append(make_book(title, "David Lodge", year, pages, ["Literary Fiction", "Humor"]))

# Donna Tartt
for title, year, pages in [
    ("The Secret History", 1992, 559), ("The Little Friend", 2002, 555),
    ("The Goldfinch", 2013, 771),
]:
    ALL_BOOKS.append(make_book(title, "Donna Tartt", year, pages, ["Literary Fiction"]))

# Zadie Smith (filling)
for title, year, pages in [
    ("White Teeth", 2000, 448), ("The Autograph Man", 2002, 347),
    ("On Beauty", 2005, 445), ("NW", 2012, 294),
    ("Swing Time", 2016, 453), ("Grand Union", 2019, 247),
    ("The Fraud", 2023, 464),
]:
    ALL_BOOKS.append(make_book(title, "Zadie Smith", year, pages, ["Literary Fiction"]))

# Mohsin Hamid
for title, year, pages in [
    ("Moth Smoke", 2000, 247), ("The Reluctant Fundamentalist", 2007, 184),
    ("How to Get Filthy Rich in Rising Asia", 2013, 228),
    ("Exit West", 2017, 231), ("The Last White Man", 2022, 192),
]:
    ALL_BOOKS.append(make_book(title, "Mohsin Hamid", year, pages, ["Literary Fiction"]))

# Yoko Ogawa (filling)
for title, year, pages in [
    ("The Memory Police", 1994, 274), ("The Housekeeper and the Professor", 2003, 180),
    ("The Diving Pool", 1990, 171), ("Hotel Iris", 1996, 179),
    ("Revenge", 1998, 166), ("The Museum of Silence", 2000, 312),
]:
    ALL_BOOKS.append(make_book(title, "Yoko Ogawa", year, pages, ["Literary Fiction"], "ja"))

# Haruki Murakami (filling remaining)
for title, year, pages in [
    ("Hear the Wind Sing", 1979, 130), ("Pinball, 1973", 1980, 164),
    ("A Wild Sheep Chase", 1982, 299), ("Hard-Boiled Wonderland and the End of the World", 1985, 400),
    ("South of the Border, West of the Sun", 1992, 213),
    ("The Wind-Up Bird Chronicle", 1994, 607), ("Sputnik Sweetheart", 1999, 210),
    ("After Dark", 2004, 191), ("Colorless Tsukuru Tazaki", 2013, 386),
    ("Killing Commendatore", 2017, 704), ("The City and Its Uncertain Walls", 2023, 464),
]:
    ALL_BOOKS.append(make_book(title, "Haruki Murakami", year, pages, ["Literary Fiction"], "ja"))


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

    batch_num = 140
    for i in range(0, len(new_books), 100):
        chunk = new_books[i:i+100]
        fname = f"batch_{batch_num}_batch24_{(i//100)+1}.json"
        with open(os.path.join(BATCH_DIR, fname), "w") as f:
            json.dump(chunk, f, indent=2)
        print(f"  {fname}: {len(chunk)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(new_books)}")
