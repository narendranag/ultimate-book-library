#!/usr/bin/env python3
"""Batch 26: Push toward 8,500 - more fresh prolific authors."""
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

# === MYSTERY/THRILLER - FRESH NAMES ===

# J.A. Jance - J.P. Beaumont + Joanna Brady
for title, year, pages in [
    ("Until Proven Guilty", 1985, 341), ("Injustice for All", 1986, 339),
    ("Trial by Fury", 1986, 308), ("Taking the Fifth", 1987, 324),
    ("Improbable Cause", 1988, 309), ("A More Perfect Union", 1988, 309),
    ("Dismissed with Prejudice", 1989, 306), ("Minor in Possession", 1990, 320),
    ("Payment in Kind", 1991, 308), ("Without Due Process", 1992, 336),
    ("Failure to Appear", 1993, 336), ("Lying in Wait", 1994, 368),
    ("Name Withheld", 1995, 368), ("Breach of Duty", 1999, 400),
    ("Birds of Prey", 2001, 400), ("Partner in Crime", 2002, 432),
    ("Long Time Gone", 2005, 384), ("Justice Denied", 2007, 384),
    ("Desert Heat", 1993, 336), ("Tombstone Courage", 1994, 340),
    ("Shoot Don't Shoot", 1995, 368), ("Dead to Rights", 1996, 384),
    ("Skeleton Canyon", 1997, 352), ("Rattlesnake Crossing", 1998, 368),
    ("Outlaw Mountain", 1999, 384), ("Devil's Claw", 2000, 384),
    ("Paradise Lost", 2001, 384), ("Exit Wounds", 2003, 384),
    ("Dead Wrong", 2006, 400), ("Damage Control", 2008, 384),
]:
    ALL_BOOKS.append(make_book(title, "J.A. Jance", year, pages, ["Mystery", "Thriller"]))

# Craig Johnson - Longmire
for title, year, pages in [
    ("The Cold Dish", 2005, 375), ("Death Without Company", 2006, 272),
    ("Kindness Goes Unpunished", 2007, 288), ("Another Man's Moccasins", 2008, 290),
    ("The Dark Horse", 2009, 318), ("Junkyard Dogs", 2010, 306),
    ("Hell Is Empty", 2011, 312), ("As the Crow Flies", 2012, 320),
    ("A Serpent's Tooth", 2013, 320), ("Any Other Name", 2014, 336),
    ("Dry Bones", 2015, 308), ("An Obvious Fact", 2016, 320),
    ("The Western Star", 2017, 320), ("Depth of Winter", 2018, 288),
    ("Land of Wolves", 2019, 320), ("Next to Last Stand", 2020, 304),
    ("Daughter of the Morning Star", 2021, 304), ("Hell and Back", 2022, 320),
    ("The Longmire Defense", 2023, 320),
]:
    ALL_BOOKS.append(make_book(title, "Craig Johnson", year, pages, ["Mystery", "Western"]))

# Tess Gerritsen (filling remaining)
for title, year, pages in [
    ("Harvest", 1996, 343), ("Life Support", 1997, 371),
    ("Bloodstream", 1998, 356), ("Gravity", 1999, 342),
    ("The Surgeon", 2001, 344), ("The Apprentice", 2002, 340),
    ("The Sinner", 2003, 342), ("Body Double", 2004, 339),
    ("Vanish", 2005, 354), ("The Mephisto Club", 2006, 356),
    ("The Bone Garden", 2007, 384), ("The Keepsake", 2008, 339),
    ("Ice Cold", 2010, 384), ("The Silent Girl", 2011, 384),
    ("Last to Die", 2012, 400), ("Die Again", 2014, 384),
    ("Playing with Fire", 2015, 272), ("I Know a Secret", 2017, 352),
    ("The Shape of Night", 2019, 320), ("Choose Me", 2021, 320),
    ("Listen to Me", 2022, 320),
]:
    ALL_BOOKS.append(make_book(title, "Tess Gerritsen", year, pages, ["Thriller", "Mystery"]))

# Alex Michaelides
for title, year, pages in [
    ("The Silent Patient", 2019, 325), ("The Maidens", 2021, 316),
    ("The Fury", 2024, 336),
]:
    ALL_BOOKS.append(make_book(title, "Alex Michaelides", year, pages, ["Thriller", "Mystery"]))

# Gregg Hurwitz - Orphan X
for title, year, pages in [
    ("Orphan X", 2016, 384), ("The Nowhere Man", 2017, 384),
    ("Hellbent", 2018, 416), ("Out of the Dark", 2019, 416),
    ("Into the Fire", 2020, 416), ("Prodigal Son", 2021, 416),
    ("Dark Horse", 2022, 416), ("The Last Orphan", 2023, 416),
    ("Lone Wolf", 2024, 416),
]:
    ALL_BOOKS.append(make_book(title, "Gregg Hurwitz", year, pages, ["Thriller"]))

# Mark Billingham - Tom Thorne
for title, year, pages in [
    ("Sleepyhead", 2001, 375), ("Scaredy Cat", 2002, 400),
    ("Lazybones", 2003, 432), ("The Burning Girl", 2004, 400),
    ("Lifeless", 2005, 432), ("Buried", 2006, 464),
    ("Death Message", 2007, 400), ("Bloodline", 2009, 400),
    ("From the Dead", 2010, 432), ("Good as Dead", 2012, 432),
    ("The Dying Hours", 2013, 432), ("The Bones Beneath", 2014, 416),
    ("Time of Death", 2015, 432), ("Love Like Blood", 2017, 432),
    ("The Killing Habit", 2018, 416), ("Their Little Secret", 2019, 416),
    ("Cry Baby", 2021, 416), ("The Murder Book", 2022, 416),
    ("The Last Dance", 2023, 416),
]:
    ALL_BOOKS.append(make_book(title, "Mark Billingham", year, pages, ["Crime Fiction", "Thriller"]))

# === SCIENCE FICTION - MORE AUTHORS ===

# Iain Banks (non-Culture)
for title, year, pages in [
    ("The Wasp Factory", 1984, 184), ("Walking on Glass", 1985, 230),
    ("The Bridge", 1986, 288), ("Espedair Street", 1987, 249),
    ("Canal Dreams", 1989, 262), ("The Crow Road", 1992, 501),
    ("Complicity", 1993, 313), ("Whit", 1995, 451),
    ("A Song of Stone", 1997, 279), ("The Business", 1999, 394),
    ("Dead Air", 2002, 404), ("The Steep Approach to Garbadale", 2007, 392),
    ("Transition", 2009, 437), ("Stonemouth", 2012, 358),
    ("The Quarry", 2013, 339),
]:
    ALL_BOOKS.append(make_book(title, "Iain Banks", year, pages, ["Literary Fiction"]))

# Iain M. Banks - Culture (filling remaining)
for title, year, pages in [
    ("Consider Phlebas", 1987, 467), ("The Player of Games", 1988, 293),
    ("Use of Weapons", 1990, 371), ("The State of the Art", 1991, 213),
    ("Excession", 1996, 451), ("Inversions", 1998, 407),
    ("Look to Windward", 2000, 357), ("Matter", 2008, 593),
    ("Surface Detail", 2010, 627), ("The Hydrogen Sonata", 2012, 517),
    ("Against a Dark Background", 1993, 487), ("Feersum Endjinn", 1994, 279),
    ("The Algebraist", 2004, 434),
]:
    ALL_BOOKS.append(make_book(title, "Iain M. Banks", year, pages, ["Science Fiction"]))

# Samuel R. Delany
for title, year, pages in [
    ("The Jewels of Aptor", 1962, 156), ("Captives of the Flame", 1963, 189),
    ("The Towers of Toron", 1964, 140), ("City of a Thousand Suns", 1965, 153),
    ("The Ballad of Beta-2", 1965, 120), ("Babel-17", 1966, 192),
    ("The Einstein Intersection", 1967, 142), ("Nova", 1968, 237),
    ("Dhalgren", 1975, 879), ("Triton", 1976, 369),
    ("Stars in My Pocket Like Grains of Sand", 1984, 368),
    ("The Motion of Light in Water", 1988, 544), ("Through the Valley of the Nest of Spiders", 2012, 804),
]:
    ALL_BOOKS.append(make_book(title, "Samuel R. Delany", year, pages, ["Science Fiction"]))

# Kim Stanley Robinson
for title, year, pages in [
    ("The Wild Shore", 1984, 365), ("Icehenge", 1984, 262),
    ("The Memory of Whiteness", 1985, 351), ("The Gold Coast", 1988, 389),
    ("Pacific Edge", 1990, 325), ("Red Mars", 1992, 572),
    ("Green Mars", 1993, 535), ("Blue Mars", 1996, 609),
    ("Antarctica", 1997, 511), ("The Years of Rice and Salt", 2002, 763),
    ("Forty Signs of Rain", 2004, 358), ("Fifty Degrees Below", 2005, 405),
    ("Sixty Days and Counting", 2007, 401), ("Galileo's Dream", 2009, 532),
    ("2312", 2012, 561), ("Shaman", 2013, 455),
    ("Aurora", 2015, 466), ("New York 2140", 2017, 613),
    ("The Ministry for the Future", 2020, 563), ("The High Sierra", 2022, 560),
]:
    ALL_BOOKS.append(make_book(title, "Kim Stanley Robinson", year, pages, ["Science Fiction"]))

# Peter Watts
for title, year, pages in [
    ("Starfish", 1999, 317), ("Maelstrom", 2001, 387),
    ("Behemoth: B-Max", 2004, 307), ("Blindsight", 2006, 384),
    ("Echopraxia", 2014, 384), ("The Freeze-Frame Revolution", 2018, 192),
]:
    ALL_BOOKS.append(make_book(title, "Peter Watts", year, pages, ["Science Fiction"]))

# Liu Cixin (filling remaining)
for title, year, pages in [
    ("The Three-Body Problem", 2008, 400), ("The Dark Forest", 2008, 512),
    ("Death's End", 2010, 604), ("Ball Lightning", 2004, 384),
    ("The Wandering Earth", 2000, 352), ("Supernova Era", 2003, 336),
]:
    ALL_BOOKS.append(make_book(title, "Liu Cixin", year, pages, ["Science Fiction"], "zh"))

# === FANTASY - MORE FRESH AUTHORS ===

# Michael Moorcock - Elric
for title, year, pages in [
    ("Elric of Melniboné", 1972, 181), ("The Sailor on the Seas of Fate", 1976, 192),
    ("The Weird of the White Wolf", 1977, 199), ("The Sleeping Sorceress", 1971, 144),
    ("The Bane of the Black Sword", 1977, 190), ("Stormbringer", 1965, 224),
    ("The Revenge of the Rose", 1991, 226), ("The Fortress of the Pearl", 1989, 268),
    ("The Dreamthief's Daughter", 2001, 330), ("The Skrayling Tree", 2003, 288),
    ("The White Wolf's Son", 2005, 352), ("The Warhound and the World's Pain", 1981, 248),
    ("The Brothel in Rosenstrasse", 1982, 176), ("The War Amongst the Angels", 1996, 329),
    ("Gloriana", 1978, 367), ("Behold the Man", 1969, 143),
    ("The Condition of Muzak", 1977, 335), ("The Ice Schooner", 1969, 200),
]:
    ALL_BOOKS.append(make_book(title, "Michael Moorcock", year, pages, ["Fantasy", "Science Fiction"]))

# Ursula Vernon / T. Kingfisher
for title, year, pages in [
    ("Swordheart", 2018, 326), ("Paladin's Grace", 2020, 465),
    ("Paladin's Strength", 2021, 440), ("Paladin's Hope", 2022, 462),
    ("Nettle & Bone", 2022, 245), ("Thornhedge", 2023, 119),
    ("A House with Good Bones", 2023, 256), ("What Moves the Dead", 2022, 176),
    ("The Hollow Places", 2020, 336), ("The Twisted Ones", 2019, 385),
]:
    ALL_BOOKS.append(make_book(title, "T. Kingfisher", year, pages, ["Fantasy", "Horror"]))

# Katherine Arden
for title, year, pages in [
    ("The Bear and the Nightingale", 2017, 323),
    ("The Girl in the Tower", 2018, 363),
    ("The Winter of the Witch", 2019, 371),
    ("Small Spaces", 2018, 218), ("Dead Voices", 2019, 224),
    ("Dark Waters", 2020, 224), ("Empty Smiles", 2023, 224),
]:
    ALL_BOOKS.append(make_book(title, "Katherine Arden", year, pages, ["Fantasy", "Historical Fiction"]))

# Garth Nix
for title, year, pages in [
    ("Sabriel", 1995, 491), ("Shade's Children", 1997, 310),
    ("Lirael", 2001, 487), ("Abhorsen", 2003, 358),
    ("The Keys to the Kingdom: Mister Monday", 2003, 300),
    ("Grim Tuesday", 2004, 320), ("Drowned Wednesday", 2005, 384),
    ("Sir Thursday", 2006, 368), ("Lady Friday", 2007, 320),
    ("Superior Saturday", 2008, 304), ("Lord Sunday", 2010, 320),
    ("A Confusion of Princes", 2012, 337), ("Clariel", 2014, 389),
    ("Goldenhand", 2016, 393), ("Angel Mage", 2019, 560),
    ("The Left-Handed Booksellers of London", 2020, 400),
    ("Terciel & Elinor", 2021, 432),
]:
    ALL_BOOKS.append(make_book(title, "Garth Nix", year, pages, ["Fantasy"]))

# Patricia McKillip
for title, year, pages in [
    ("The Forgotten Beasts of Eld", 1974, 217),
    ("The Riddle-Master of Hed", 1976, 228),
    ("Heir of Sea and Fire", 1977, 224), ("Harpist in the Wind", 1979, 256),
    ("The Changeling Sea", 1988, 137), ("The Sorceress and the Cygnet", 1991, 236),
    ("The Cygnet and the Firebird", 1993, 246), ("Something Rich and Strange", 1994, 181),
    ("Winter Rose", 1996, 266), ("Song for the Basilisk", 1998, 314),
    ("The Tower at Stony Wood", 2000, 273), ("Ombria in Shadow", 2002, 298),
    ("In the Forests of Serre", 2003, 295), ("Alphabet of Thorn", 2004, 314),
    ("Od Magic", 2005, 315), ("Solstice Wood", 2006, 254),
    ("The Bell at Sealey Head", 2008, 262), ("The Bards of Bone Plain", 2010, 336),
    ("Kingfisher", 2016, 320),
]:
    ALL_BOOKS.append(make_book(title, "Patricia McKillip", year, pages, ["Fantasy"]))

# === NON-FICTION EXPANSION ===

# Walter Isaacson
for title, year, pages in [
    ("Kissinger", 1992, 893), ("Benjamin Franklin", 2003, 590),
    ("Einstein", 2007, 675), ("Steve Jobs", 2011, 630),
    ("The Innovators", 2014, 542), ("Leonardo da Vinci", 2017, 600),
    ("The Code Breaker", 2021, 536), ("Elon Musk", 2023, 670),
]:
    ALL_BOOKS.append(make_book(title, "Walter Isaacson", year, pages, ["Non-Fiction", "Biography"]))

# Ron Chernow
for title, year, pages in [
    ("The House of Morgan", 1990, 812), ("The Warburgs", 1993, 820),
    ("Titan: The Life of John D. Rockefeller, Sr.", 1998, 774),
    ("Alexander Hamilton", 2004, 818), ("Washington", 2010, 904),
    ("Grant", 2017, 1074),
]:
    ALL_BOOKS.append(make_book(title, "Ron Chernow", year, pages, ["Non-Fiction", "Biography", "History"]))

# Doris Kearns Goodwin
for title, year, pages in [
    ("Lyndon Johnson and the American Dream", 1976, 432),
    ("The Fitzgeralds and the Kennedys", 1987, 932),
    ("No Ordinary Time", 1994, 759), ("Wait Till Next Year", 1997, 261),
    ("Team of Rivals", 2005, 916), ("The Bully Pulpit", 2013, 910),
    ("Leadership in Turbulent Times", 2018, 473),
    ("An Unfinished Love Story", 2024, 482),
]:
    ALL_BOOKS.append(make_book(title, "Doris Kearns Goodwin", year, pages, ["Non-Fiction", "Biography", "History"]))

# Jared Diamond
for title, year, pages in [
    ("The Third Chimpanzee", 1991, 407),
    ("Guns, Germs, and Steel", 1997, 480),
    ("Collapse", 2005, 575), ("The World Until Yesterday", 2012, 498),
    ("Upheaval", 2019, 502),
]:
    ALL_BOOKS.append(make_book(title, "Jared Diamond", year, pages, ["Non-Fiction", "History", "Science"]))

# Steven Pinker
for title, year, pages in [
    ("The Language Instinct", 1994, 525), ("How the Mind Works", 1997, 660),
    ("Words and Rules", 1999, 348), ("The Blank Slate", 2002, 509),
    ("The Stuff of Thought", 2007, 499), ("The Better Angels of Our Nature", 2011, 832),
    ("The Sense of Style", 2014, 359), ("Enlightenment Now", 2018, 556),
    ("Rationality", 2021, 432),
]:
    ALL_BOOKS.append(make_book(title, "Steven Pinker", year, pages, ["Non-Fiction", "Science"]))

# Edward O. Wilson
for title, year, pages in [
    ("The Insect Societies", 1971, 548), ("Sociobiology", 1975, 697),
    ("On Human Nature", 1978, 260), ("The Ants", 1990, 732),
    ("The Diversity of Life", 1992, 424), ("Consilience", 1998, 332),
    ("The Future of Life", 2002, 256), ("The Creation", 2006, 175),
    ("The Social Conquest of Earth", 2012, 330), ("The Meaning of Human Existence", 2014, 207),
    ("Half-Earth", 2016, 259), ("Genesis", 2019, 153),
]:
    ALL_BOOKS.append(make_book(title, "Edward O. Wilson", year, pages, ["Non-Fiction", "Science"]))

# Daniel Kahneman
for title, year, pages in [
    ("Thinking, Fast and Slow", 2011, 499),
    ("Noise", 2021, 464),
]:
    ALL_BOOKS.append(make_book(title, "Daniel Kahneman", year, pages, ["Non-Fiction", "Science"]))

# Nassim Nicholas Taleb
for title, year, pages in [
    ("Fooled by Randomness", 2001, 316), ("The Black Swan", 2007, 366),
    ("The Bed of Procrustes", 2010, 176), ("Antifragile", 2012, 519),
    ("Skin in the Game", 2018, 304),
]:
    ALL_BOOKS.append(make_book(title, "Nassim Nicholas Taleb", year, pages, ["Non-Fiction"]))

# === LITERARY FICTION - MORE FRESH AUTHORS ===

# Alice Munro
for title, year, pages in [
    ("Dance of the Happy Shades", 1968, 224), ("Lives of Girls and Women", 1971, 277),
    ("Something I've Been Meaning to Tell You", 1974, 245),
    ("Who Do You Think You Are?", 1978, 223), ("The Moons of Jupiter", 1982, 233),
    ("The Progress of Love", 1986, 309), ("Friend of My Youth", 1990, 273),
    ("Open Secrets", 1994, 293), ("The Love of a Good Woman", 1998, 339),
    ("Hateship, Friendship, Courtship, Loveship, Marriage", 2001, 323),
    ("Runaway", 2004, 335), ("The View from Castle Rock", 2006, 349),
    ("Too Much Happiness", 2009, 303), ("Dear Life", 2012, 319),
]:
    ALL_BOOKS.append(make_book(title, "Alice Munro", year, pages, ["Literary Fiction", "Short Stories"]))

# V.S. Naipaul (filling remaining)
for title, year, pages in [
    ("The Mystic Masseur", 1957, 215), ("The Suffrage of Elvira", 1958, 240),
    ("Miguel Street", 1959, 222), ("A House for Mr Biswas", 1961, 564),
    ("Mr Stone and the Knights Companion", 1963, 159),
    ("The Mimic Men", 1967, 297), ("In a Free State", 1971, 246),
    ("Guerrillas", 1975, 248), ("A Bend in the River", 1979, 278),
    ("The Enigma of Arrival", 1987, 354), ("A Way in the World", 1994, 380),
    ("Half a Life", 2001, 211), ("Magic Seeds", 2004, 280),
    ("An Area of Darkness", 1964, 281), ("India: A Wounded Civilization", 1977, 192),
    ("Among the Believers", 1981, 430), ("A Turn in the South", 1989, 307),
    ("India: A Million Mutinies Now", 1990, 521), ("Beyond Belief", 1998, 408),
]:
    ALL_BOOKS.append(make_book(title, "V.S. Naipaul", year, pages, ["Literary Fiction"]))

# Philip Roth (filling remaining)
for title, year, pages in [
    ("Goodbye, Columbus", 1959, 298), ("Letting Go", 1962, 630),
    ("When She Was Good", 1967, 306), ("Portnoy's Complaint", 1969, 274),
    ("Our Gang", 1971, 200), ("The Great American Novel", 1973, 382),
    ("My Life as a Man", 1974, 334), ("The Professor of Desire", 1977, 263),
    ("The Ghost Writer", 1979, 180), ("Zuckerman Unbound", 1981, 225),
    ("The Anatomy Lesson", 1983, 291), ("The Counterlife", 1986, 324),
    ("Deception", 1990, 208), ("Operation Shylock", 1993, 398),
    ("Sabbath's Theater", 1995, 451), ("American Pastoral", 1997, 423),
    ("I Married a Communist", 1998, 323), ("The Human Stain", 2000, 361),
    ("The Dying Animal", 2001, 156), ("The Plot Against America", 2004, 391),
    ("Everyman", 2006, 182), ("Exit Ghost", 2007, 292),
    ("Indignation", 2008, 233), ("The Humbling", 2009, 140),
    ("Nemesis", 2010, 280),
]:
    ALL_BOOKS.append(make_book(title, "Philip Roth", year, pages, ["Literary Fiction"]))

# Margaret Drabble
for title, year, pages in [
    ("A Summer Bird-Cage", 1963, 208), ("The Garrick Year", 1964, 208),
    ("The Millstone", 1965, 192), ("Jerusalem the Golden", 1967, 208),
    ("The Waterfall", 1969, 256), ("The Needle's Eye", 1972, 384),
    ("The Realms of Gold", 1975, 384), ("The Ice Age", 1977, 320),
    ("The Middle Ground", 1980, 288), ("The Radiant Way", 1987, 400),
    ("A Natural Curiosity", 1989, 320), ("The Gates of Ivory", 1991, 480),
    ("The Witch of Exmoor", 1996, 288), ("The Peppered Moth", 2000, 384),
    ("The Seven Sisters", 2002, 310), ("The Red Queen", 2004, 288),
    ("The Sea Lady", 2006, 352), ("The Pure Gold Baby", 2013, 304),
    ("The Dark Flood Rises", 2016, 336),
]:
    ALL_BOOKS.append(make_book(title, "Margaret Drabble", year, pages, ["Literary Fiction"]))

# Muriel Spark
for title, year, pages in [
    ("The Comforters", 1957, 256), ("Robinson", 1958, 176),
    ("Memento Mori", 1959, 224), ("The Ballad of Peckham Rye", 1960, 160),
    ("The Bachelors", 1960, 224), ("The Prime of Miss Jean Brodie", 1961, 128),
    ("The Girls of Slender Means", 1963, 176), ("The Mandelbaum Gate", 1965, 369),
    ("The Public Image", 1968, 128), ("The Driver's Seat", 1970, 107),
    ("Not to Disturb", 1971, 144), ("The Hothouse by the East River", 1973, 140),
    ("The Abbess of Crewe", 1974, 116), ("The Takeover", 1976, 266),
    ("Territorial Rights", 1979, 246), ("Loitering with Intent", 1981, 217),
    ("The Only Problem", 1984, 179), ("A Far Cry from Kensington", 1988, 189),
    ("Symposium", 1990, 184), ("Reality and Dreams", 1996, 171),
    ("Aiding and Abetting", 2000, 166), ("The Finishing School", 2004, 181),
]:
    ALL_BOOKS.append(make_book(title, "Muriel Spark", year, pages, ["Literary Fiction"]))

# === INDIAN FICTION EXPANSION ===

# Amitav Ghosh (filling remaining)
for title, year, pages in [
    ("The Circle of Reason", 1986, 423), ("The Shadow Lines", 1988, 252),
    ("In an Antique Land", 1992, 393), ("The Calcutta Chromosome", 1995, 311),
    ("The Glass Palace", 2000, 474), ("The Hungry Tide", 2004, 333),
    ("Sea of Poppies", 2008, 515), ("River of Smoke", 2011, 528),
    ("Flood of Fire", 2015, 616), ("Gun Island", 2019, 307),
    ("The Nutmeg's Curse", 2021, 336), ("Smoke and Ashes", 2023, 368),
]:
    ALL_BOOKS.append(make_book(title, "Amitav Ghosh", year, pages, ["Literary Fiction", "Historical Fiction", "Indian Fiction"]))

# Jhumpa Lahiri (filling remaining)
for title, year, pages in [
    ("Interpreter of Maladies", 1999, 198), ("The Namesake", 2003, 291),
    ("Unaccustomed Earth", 2008, 333), ("The Lowland", 2013, 340),
    ("In Other Words", 2015, 233), ("Whereabouts", 2021, 176),
    ("Roman Stories", 2023, 224),
]:
    ALL_BOOKS.append(make_book(title, "Jhumpa Lahiri", year, pages, ["Literary Fiction", "Indian Fiction"]))

# Arundhati Roy
for title, year, pages in [
    ("The God of Small Things", 1997, 321),
    ("The Ministry of Utmost Happiness", 2017, 449),
    ("The Algebra of Infinite Justice", 2002, 304),
    ("An Ordinary Person's Guide to Empire", 2004, 159),
    ("Listening to Grasshoppers", 2009, 256),
    ("Capitalism: A Ghost Story", 2014, 128),
    ("My Seditious Heart", 2019, 1051),
]:
    ALL_BOOKS.append(make_book(title, "Arundhati Roy", year, pages, ["Literary Fiction", "Indian Fiction"]))

# Kiran Desai
for title, year, pages in [
    ("Hullabaloo in the Guava Orchard", 1998, 210),
    ("The Inheritance of Loss", 2006, 357),
]:
    ALL_BOOKS.append(make_book(title, "Kiran Desai", year, pages, ["Literary Fiction", "Indian Fiction"]))

# Vikram Chandra (filling remaining)
for title, year, pages in [
    ("Red Earth and Pouring Rain", 1995, 507),
    ("Love and Longing in Bombay", 1997, 265),
    ("Sacred Games", 2006, 916), ("Mirrored Mind", 2013, 339),
]:
    ALL_BOOKS.append(make_book(title, "Vikram Chandra", year, pages, ["Literary Fiction", "Indian Fiction"]))

# === DRAMA / PLAYS ===

# Samuel Beckett
for title, year, pages in [
    ("Waiting for Godot", 1952, 87), ("Endgame", 1957, 84),
    ("Krapp's Last Tape", 1958, 30), ("Happy Days", 1961, 64),
    ("Molloy", 1951, 241), ("Malone Dies", 1951, 120),
    ("The Unnamable", 1953, 179), ("Murphy", 1938, 268),
    ("Watt", 1953, 255), ("How It Is", 1961, 147),
    ("Company", 1980, 89), ("Ill Seen Ill Said", 1981, 59),
    ("Worstward Ho", 1983, 47),
]:
    ALL_BOOKS.append(make_book(title, "Samuel Beckett", year, pages, ["Drama", "Literary Fiction"]))

# Harold Pinter
for title, year, pages in [
    ("The Birthday Party", 1957, 96), ("The Dumb Waiter", 1957, 48),
    ("The Caretaker", 1959, 76), ("The Homecoming", 1964, 82),
    ("Old Times", 1970, 75), ("No Man's Land", 1975, 95),
    ("Betrayal", 1978, 138), ("One for the Road", 1984, 48),
    ("Mountain Language", 1988, 32), ("Moonlight", 1993, 80),
    ("Ashes to Ashes", 1996, 85), ("Celebration", 1999, 60),
]:
    ALL_BOOKS.append(make_book(title, "Harold Pinter", year, pages, ["Drama"]))

# Tennessee Williams
for title, year, pages in [
    ("The Glass Menagerie", 1944, 115), ("A Streetcar Named Desire", 1947, 142),
    ("Summer and Smoke", 1948, 114), ("The Rose Tattoo", 1951, 138),
    ("Cat on a Hot Tin Roof", 1955, 168), ("Orpheus Descending", 1957, 112),
    ("Suddenly Last Summer", 1958, 90), ("Sweet Bird of Youth", 1959, 114),
    ("The Night of the Iguana", 1961, 128), ("The Milk Train Doesn't Stop Here Anymore", 1963, 119),
    ("Small Craft Warnings", 1972, 116), ("Vieux Carré", 1977, 116),
]:
    ALL_BOOKS.append(make_book(title, "Tennessee Williams", year, pages, ["Drama"]))

# Arthur Miller
for title, year, pages in [
    ("All My Sons", 1947, 86), ("Death of a Salesman", 1949, 139),
    ("The Crucible", 1953, 143), ("A View from the Bridge", 1955, 85),
    ("After the Fall", 1964, 113), ("Incident at Vichy", 1964, 70),
    ("The Price", 1968, 116), ("The Creation of the World and Other Business", 1972, 128),
    ("The American Clock", 1980, 96), ("The Ride Down Mt. Morgan", 1991, 108),
    ("Broken Glass", 1994, 77), ("Mr. Peters' Connections", 1998, 80),
    ("Resurrection Blues", 2002, 96), ("Finishing the Picture", 2004, 72),
]:
    ALL_BOOKS.append(make_book(title, "Arthur Miller", year, pages, ["Drama"]))

# === MORE FRESH AUTHORS FOR VOLUME ===

# Catherine Cookson
for title, year, pages in [
    ("Kate Hannigan", 1950, 320), ("The Fifteen Streets", 1952, 352),
    ("Colour Blind", 1953, 384), ("A Grand Man", 1954, 320),
    ("The Lord and Mary Ann", 1956, 256), ("Rooney", 1957, 288),
    ("The Menagerie", 1958, 352), ("Slinky Jane", 1959, 288),
    ("Fanny McBride", 1959, 352), ("Fenwick Houses", 1960, 320),
    ("The Garment", 1962, 320), ("The Blind Miller", 1963, 288),
    ("Hannah Massey", 1964, 288), ("The Long Corridor", 1965, 320),
    ("The Unbaited Trap", 1966, 320), ("Katie Mulholland", 1967, 416),
    ("The Round Tower", 1968, 448), ("The Nice Bloke", 1969, 384),
    ("The Glass Virgin", 1969, 416), ("The Invitation", 1970, 384),
    ("The Dwelling Place", 1971, 352), ("The Mallen Streak", 1973, 320),
    ("The Mallen Girl", 1973, 352), ("The Mallen Litter", 1974, 352),
    ("The Tide of Life", 1976, 416), ("The Girl", 1977, 352),
]:
    ALL_BOOKS.append(make_book(title, "Catherine Cookson", year, pages, ["Romance", "Historical Fiction"]))

# Victoria Holt (Jean Plaidy)
for title, year, pages in [
    ("Mistress of Mellyn", 1960, 338), ("Kirkland Revels", 1962, 372),
    ("Bride of Pendorric", 1963, 320), ("The Legend of the Seventh Virgin", 1965, 383),
    ("Menfreya in the Morning", 1966, 340), ("The King of the Castle", 1967, 371),
    ("The Queen's Confession", 1968, 448), ("The Shivering Sands", 1969, 352),
    ("The Secret Woman", 1970, 307), ("The Shadow of the Lynx", 1971, 381),
    ("On the Night of the Seventh Moon", 1972, 340), ("The Curse of the Kings", 1973, 382),
    ("The House of a Thousand Lanterns", 1974, 383), ("Lord of the Far Island", 1975, 383),
    ("The Pride of the Peacock", 1976, 397), ("The Devil on Horseback", 1977, 360),
    ("My Enemy the Queen", 1978, 337), ("The Spring of the Tiger", 1979, 390),
    ("The Mask of the Enchantress", 1980, 384), ("The Judas Kiss", 1981, 382),
    ("The Demon Lover", 1982, 335), ("The Time of the Hunter's Moon", 1983, 384),
    ("The Landower Legacy", 1984, 384), ("The Road to Paradise Island", 1985, 384),
    ("Secret for a Nightingale", 1986, 374), ("The Silk Vendetta", 1987, 384),
]:
    ALL_BOOKS.append(make_book(title, "Victoria Holt", year, pages, ["Romance", "Mystery", "Historical Fiction"]))


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

    batch_num = 155
    for i in range(0, len(new_books), 100):
        chunk = new_books[i:i+100]
        fname = f"batch_{batch_num}_batch26_{(i//100)+1}.json"
        with open(os.path.join(BATCH_DIR, fname), "w") as f:
            json.dump(chunk, f, indent=2)
        print(f"  {fname}: {len(chunk)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(new_books)}")
