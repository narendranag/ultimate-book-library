#!/usr/bin/env python3
"""Generate more author bibliographies (batch 47+) toward 10,000 books.

Run: python data/generate_seed_batch6.py
"""

import hashlib
import json
from pathlib import Path


def make_isbn13(title: str, author: str) -> str:
    h = hashlib.md5(f"{title}|{author}".encode()).hexdigest()
    digits = "978" + "".join(str(int(c, 16) % 10) for c in h[:9])
    total = sum(int(d) * (1 if i % 2 == 0 else 3) for i, d in enumerate(digits))
    return digits + str((10 - (total % 10)) % 10)


def make_isbn10(isbn13: str) -> str:
    digits = isbn13[3:12]
    total = sum(int(d) * (10 - i) for i, d in enumerate(digits))
    check = (11 - (total % 11)) % 11
    return digits + ("X" if check == 10 else str(check))


def make_book(title, authors, year=None, genres=None, lang="en", pages=None):
    if isinstance(authors, str): authors = [authors]
    isbn13 = make_isbn13(title, authors[0])
    isbn10 = make_isbn10(isbn13)
    book = {"title": title, "authors": authors, "isbn_13": isbn13, "isbn_10": isbn10,
            "genres": genres or [], "language": lang, "source": "seed"}
    if year: book["year_published"] = year
    if pages: book["page_count"] = pages
    return book


AUTHORS = [
    ("Robert A. Heinlein", "en", ["Science Fiction"], [
        ("Stranger in a Strange Land", 1961, 408, None),
        ("Starship Troopers", 1959, 263, None),
        ("The Moon Is a Harsh Mistress", 1966, 382, None),
        ("Time Enough for Love", 1973, 605, None),
        ("The Door into Summer", 1957, 188, None),
        ("Citizen of the Galaxy", 1957, 302, None),
        ("Have Space Suit—Will Travel", 1958, 276, None),
        ("Double Star", 1956, 186, None),
        ("The Puppet Masters", 1951, 219, None),
        ("Glory Road", 1963, 288, None),
        ("Friday", 1982, 368, None),
        ("Job: A Comedy of Justice", 1984, 376, None),
        ("The Cat Who Walks Through Walls", 1985, 388, None),
        ("To Sail Beyond the Sunset", 1987, 416, None),
        ("Tunnel in the Sky", 1955, 262, None),
        ("Methuselah's Children", 1958, 188, None),
        ("Farnham's Freehold", 1964, 315, None),
        ("I Will Fear No Evil", 1970, 401, None),
        ("The Number of the Beast", 1980, 511, None),
        ("Red Planet", 1949, 211, None),
        ("Between Planets", 1951, 222, None),
        ("The Rolling Stones", 1952, 276, None),
        ("The Star Beast", 1954, 282, None),
        ("Podkayne of Mars", 1963, 191, None),
        ("Revolt in 2100", 1953, 199, None),
    ]),

    ("Ray Bradbury", "en", ["Science Fiction", "Literary Fiction"], [
        ("The Martian Chronicles", 1950, 222, None),
        ("Fahrenheit 451", 1953, 227, None),
        ("The Illustrated Man", 1951, 275, ["Science Fiction", "Short Stories"]),
        ("Dandelion Wine", 1957, 239, ["Literary Fiction"]),
        ("Something Wicked This Way Comes", 1962, 293, ["Horror", "Fantasy"]),
        ("The October Country", 1955, 306, ["Horror", "Short Stories"]),
        ("Death Is a Lonely Business", 1985, 279, ["Mystery"]),
        ("A Graveyard for Lunatics", 1990, 285, ["Mystery"]),
        ("Let's All Kill Constance", 2003, 233, ["Mystery"]),
        ("Green Shadows, White Whale", 1992, 271, ["Literary Fiction", "Memoir"]),
        ("From the Dust Returned", 2001, 204, ["Fantasy"]),
        ("The Halloween Tree", 1972, 145, ["Fantasy", "Children's"]),
        ("I Sing the Body Electric!", 1969, 305, ["Science Fiction", "Short Stories"]),
        ("R Is for Rocket", 1962, 233, ["Science Fiction", "Short Stories"]),
        ("S Is for Space", 1966, 244, ["Science Fiction", "Short Stories"]),
        ("Long After Midnight", 1976, 274, ["Science Fiction", "Short Stories"]),
        ("The Toynbee Convector", 1988, 286, ["Science Fiction", "Short Stories"]),
        ("Quicker Than the Eye", 1996, 260, ["Science Fiction", "Short Stories"]),
        ("One More for the Road", 2002, 258, ["Science Fiction", "Short Stories"]),
        ("We'll Always Have Paris", 2009, 226, ["Science Fiction", "Short Stories"]),
    ]),

    ("Neil Gaiman", "en", ["Fantasy"], [
        ("American Gods", 2001, 465, None),
        ("Anansi Boys", 2005, 336, None),
        ("Neverwhere", 1996, 370, None),
        ("Stardust", 1999, 248, None),
        ("Coraline", 2002, 163, ["Fantasy", "Horror", "Children's"]),
        ("The Graveyard Book", 2008, 312, ["Fantasy", "Children's"]),
        ("The Ocean at the End of the Lane", 2013, 181, None),
        ("Good Omens", 1990, 288, ["Fantasy", "Humor"]),
        ("Norse Mythology", 2017, 299, ["Fantasy", "Mythology"]),
        ("Smoke and Mirrors", 1998, 365, ["Fantasy", "Short Stories"]),
        ("Fragile Things", 2006, 369, ["Fantasy", "Short Stories"]),
        ("Trigger Warning", 2015, 310, ["Fantasy", "Short Stories"]),
        ("Odd and the Frost Giants", 2008, 117, ["Fantasy", "Children's"]),
        ("Fortunately, the Milk", 2013, 128, ["Children's"]),
        ("The Wolves in the Walls", 2003, 64, ["Children's"]),
        ("Blueberry Girl", 2009, 32, ["Children's"]),
        ("Crazy Hair", 2009, 32, ["Children's"]),
        ("Chu's Day", 2013, 32, ["Children's"]),
        ("Interworld", 2007, 239, ["Fantasy", "Young Adult"]),
        ("The Silver Dream", 2013, 260, ["Fantasy", "Young Adult"]),
        ("Eternity's Wheel", 2015, 260, ["Fantasy", "Young Adult"]),
        ("The View from the Cheap Seats", 2016, 544, ["Non-Fiction", "Essays"]),
        ("Art Matters", 2018, 112, ["Non-Fiction"]),
        ("The Sandman: Overture", 2013, 224, ["Graphic Novel", "Fantasy"]),
    ]),

    ("Dan Brown", "en", ["Thriller", "Mystery"], [
        ("Digital Fortress", 1998, 372, None),
        ("Deception Point", 2001, 372, None),
        ("Angels & Demons", 2000, 572, None),
        ("The Da Vinci Code", 2003, 454, None),
        ("The Lost Symbol", 2009, 509, None),
        ("Inferno", 2013, 461, None),
        ("Origin", 2017, 461, None),
    ]),

    ("Clive Cussler", "en", ["Adventure", "Thriller"], [
        ("Pacific Vortex!", 1983, 320, None),
        ("The Mediterranean Caper", 1973, 287, None),
        ("Iceberg", 1975, 362, None),
        ("Raise the Titanic!", 1976, 314, None),
        ("Vixen 03", 1978, 344, None),
        ("Night Probe!", 1981, 355, None),
        ("Deep Six", 1984, 432, None),
        ("Cyclops", 1986, 475, None),
        ("Treasure", 1988, 539, None),
        ("Dragon", 1990, 541, None),
        ("Sahara", 1992, 541, None),
        ("Inca Gold", 1994, 537, None),
        ("Shock Wave", 1996, 537, None),
        ("Flood Tide", 1997, 515, None),
        ("Atlantis Found", 1999, 534, None),
        ("Valhalla Rising", 2001, 531, None),
        ("Trojan Odyssey", 2003, 484, None),
        ("Black Wind", 2004, 516, None),
        ("Treasure of Khan", 2006, 531, None),
        ("Arctic Drift", 2008, 515, None),
        ("Crescent Dawn", 2010, 512, None),
        ("The Storm", 2012, 400, None),
        ("Zero Hour", 2013, 400, None),
        ("Ghost Ship", 2014, 416, None),
        ("The Pharaoh's Secret", 2015, 416, None),
    ]),

    ("Wilbur Smith", "en", ["Adventure", "Historical Fiction"], [
        ("When the Lion Feeds", 1964, 468, None),
        ("The Dark of the Sun", 1965, 316, None),
        ("The Sound of Thunder", 1966, 420, None),
        ("Shout at the Devil", 1968, 368, None),
        ("Gold Mine", 1970, 323, None),
        ("The Diamond Hunters", 1971, 350, None),
        ("The Sunbird", 1972, 495, None),
        ("Eagle in the Sky", 1974, 325, None),
        ("The Eye of the Tiger", 1975, 380, None),
        ("Cry Wolf", 1976, 360, None),
        ("A Sparrow Falls", 1977, 608, None),
        ("Hungry as the Sea", 1978, 408, None),
        ("Wild Justice", 1979, 383, None),
        ("A Falcon Flies", 1980, 533, None),
        ("Men of Men", 1981, 476, None),
        ("The Angels Weep", 1982, 533, None),
        ("The Leopard Hunts in Darkness", 1984, 448, None),
        ("The Burning Shore", 1985, 582, None),
        ("Power of the Sword", 1986, 618, None),
        ("Rage", 1987, 670, None),
        ("A Time to Die", 1989, 596, None),
        ("Golden Fox", 1990, 528, None),
        ("Elephant Song", 1991, 435, None),
        ("River God", 1993, 665, None),
        ("The Seventh Scroll", 1995, 486, None),
        ("Birds of Prey", 1997, 554, None),
        ("Monsoon", 1999, 613, None),
        ("Warlock", 2001, 530, None),
        ("Blue Horizon", 2003, 490, None),
        ("The Triumph of the Sun", 2005, 512, None),
        ("The Quest", 2007, 544, None),
        ("Assegai", 2009, 448, None),
        ("Those in Peril", 2011, 384, None),
        ("Vicious Circle", 2013, 400, None),
        ("Desert God", 2014, 400, None),
        ("Pharaoh", 2016, 560, None),
        ("War Cry", 2017, 448, None),
        ("The Tiger's Prey", 2018, 400, None),
        ("Courtney's War", 2018, 432, None),
        ("Ghost Fire", 2019, 432, None),
    ]),

    ("Lee Child", "en", ["Thriller"], [
        ("Killing Floor", 1997, 526, None),
        ("Die Trying", 1998, 532, None),
        ("Tripwire", 1999, 458, None),
        ("Running Blind", 2000, 384, None),
        ("Echo Burning", 2001, 420, None),
        ("Without Fail", 2002, 416, None),
        ("Persuader", 2003, 342, None),
        ("The Enemy", 2004, 377, None),
        ("One Shot", 2005, 432, None),
        ("The Hard Way", 2006, 376, None),
        ("Bad Luck and Trouble", 2007, 377, None),
        ("Nothing to Lose", 2008, 406, None),
        ("Gone Tomorrow", 2009, 393, None),
        ("61 Hours", 2010, 383, None),
        ("Worth Dying For", 2010, 374, None),
        ("The Affair", 2011, 405, None),
        ("A Wanted Man", 2012, 388, None),
        ("Never Go Back", 2013, 386, None),
        ("Personal", 2014, 361, None),
        ("Make Me", 2015, 385, None),
        ("Night School", 2016, 368, None),
        ("The Midnight Line", 2017, 368, None),
        ("Past Tense", 2018, 384, None),
        ("Blue Moon", 2019, 368, None),
        ("The Sentinel", 2020, 336, None),
        ("Better Off Dead", 2021, 320, None),
        ("No Plan B", 2022, 336, None),
        ("The Secret", 2023, 304, None),
        ("In Too Deep", 2024, 320, None),
    ]),

    ("Jeffrey Archer", "en", ["Thriller", "Literary Fiction"], [
        ("Not a Penny More, Not a Penny Less", 1976, 310, None),
        ("Shall We Tell the President?", 1977, 352, None),
        ("Kane and Abel", 1979, 530, None),
        ("The Prodigal Daughter", 1982, 463, None),
        ("First Among Equals", 1984, 438, None),
        ("A Matter of Honour", 1986, 480, None),
        ("As the Crow Flies", 1991, 617, None),
        ("Honour Among Thieves", 1993, 430, None),
        ("The Fourth Estate", 1996, 560, None),
        ("The Eleventh Commandment", 1998, 386, None),
        ("Sons of Fortune", 2003, 505, None),
        ("False Impression", 2005, 386, None),
        ("The Gospel According to Judas", 2007, 96, None),
        ("A Prisoner of Birth", 2008, 528, None),
        ("Paths of Glory", 2009, 336, None),
        ("Only Time Will Tell", 2011, 386, ["Historical Fiction"]),
        ("The Sins of the Father", 2012, 416, ["Historical Fiction"]),
        ("Best Kept Secret", 2013, 432, ["Historical Fiction"]),
        ("Be Careful What You Wish For", 2014, 416, ["Historical Fiction"]),
        ("Mightier Than the Sword", 2015, 400, ["Historical Fiction"]),
        ("Cometh the Hour", 2016, 416, ["Historical Fiction"]),
        ("This Was a Man", 2016, 496, ["Historical Fiction"]),
        ("Heads You Win", 2018, 432, None),
        ("Nothing Ventured", 2019, 320, None),
        ("Over My Dead Body", 2021, 384, None),
        ("Turn a Blind Eye", 2021, 384, None),
        ("Hidden in Plain Sight", 2020, 352, None),
        ("Next in Line", 2022, 368, None),
        ("An Eye for an Eye", 2023, 384, None),
    ]),

    ("Jorge Luis Borges", "es", ["Literary Fiction", "Short Stories"], [
        ("Ficciones", 1944, 174, None),
        ("The Aleph", 1949, 199, None),
        ("Labyrinths", 1962, 240, None),
        ("The Book of Sand", 1975, 128, None),
        ("Doctor Brodie's Report", 1970, 128, None),
        ("A Universal History of Infamy", 1935, 158, None),
        ("The Book of Imaginary Beings", 1957, 237, None),
        ("Other Inquisitions", 1952, 205, ["Essays"]),
        ("Seven Nights", 1980, 137, ["Essays"]),
        ("This Craft of Verse", 2000, 154, ["Essays"]),
        ("Borges on Writing", 1973, 175, ["Essays"]),
    ]),

    ("Henning Mankell", "sv", ["Mystery", "Crime Fiction"], [
        ("Faceless Killers", 1991, 312, None),
        ("The Dogs of Riga", 1992, 326, None),
        ("The White Lioness", 1993, 444, None),
        ("The Man Who Smiled", 1994, 309, None),
        ("Sidetracked", 1995, 404, None),
        ("The Fifth Woman", 1996, 404, None),
        ("One Step Behind", 1997, 404, None),
        ("Firewall", 1998, 452, None),
        ("Before the Frost", 2002, 370, None),
        ("The Troubled Man", 2009, 384, None),
        ("The Return of the Dancing Master", 2000, 409, None),
        ("Kennedy's Brain", 2005, 386, None),
        ("The Man from Beijing", 2008, 400, None),
        ("Italian Shoes", 2006, 263, ["Literary Fiction"]),
        ("Depths", 2004, 257, ["Literary Fiction", "Historical Fiction"]),
        ("After the Fire", 2017, 310, ["Literary Fiction"]),
        ("Daniel", 2010, 348, ["Literary Fiction"]),
        ("Chronicler of the Winds", 1995, 224, ["Literary Fiction"]),
        ("The Eye of the Leopard", 1990, 352, ["Literary Fiction"]),
        ("Tea-Bag", 2001, 327, ["Literary Fiction"]),
    ]),

    ("Stieg Larsson", "sv", ["Thriller", "Mystery"], [
        ("The Girl with the Dragon Tattoo", 2005, 465, None),
        ("The Girl Who Played with Fire", 2006, 503, None),
        ("The Girl Who Kicked the Hornets' Nest", 2007, 563, None),
    ]),

    ("David Lagercrantz", "sv", ["Thriller", "Mystery"], [
        ("The Girl in the Spider's Web", 2015, 416, None),
        ("The Girl Who Takes an Eye for an Eye", 2017, 416, None),
        ("The Girl Who Lived Twice", 2019, 400, None),
    ]),

    ("Umberto Eco", "it", ["Literary Fiction", "Mystery"], [
        ("The Name of the Rose", 1980, 536, None),
        ("Foucault's Pendulum", 1988, 641, None),
        ("The Island of the Day Before", 1994, 515, None),
        ("Baudolino", 2000, 522, None),
        ("The Mysterious Flame of Queen Loana", 2004, 469, None),
        ("The Prague Cemetery", 2010, 464, ["Literary Fiction", "Historical Fiction"]),
        ("Numero Zero", 2015, 191, None),
    ]),

    ("Italo Calvino", "it", ["Literary Fiction"], [
        ("The Path to the Nest of Spiders", 1947, 150, None),
        ("The Cloven Viscount", 1952, 105, ["Literary Fiction", "Fantasy"]),
        ("The Baron in the Trees", 1957, 217, ["Literary Fiction", "Fantasy"]),
        ("The Nonexistent Knight", 1959, 122, ["Literary Fiction", "Fantasy"]),
        ("Cosmicomics", 1965, 153, ["Literary Fiction", "Science Fiction"]),
        ("t zero", 1967, 157, ["Literary Fiction", "Science Fiction"]),
        ("If on a winter's night a traveler", 1979, 260, ["Literary Fiction", "Postmodern"]),
        ("Invisible Cities", 1972, 165, None),
        ("Mr Palomar", 1983, 126, None),
        ("Marcovaldo", 1963, 121, None),
        ("The Complete Cosmicomics", 2009, 400, ["Literary Fiction", "Science Fiction"]),
        ("Under the Jaguar Sun", 1986, 86, ["Literary Fiction", "Short Stories"]),
        ("Numbers in the Dark", 1995, 275, ["Literary Fiction", "Short Stories"]),
        ("Difficult Loves", 1970, 262, ["Literary Fiction", "Short Stories"]),
        ("Italian Folktales", 1956, 763, ["Folklore"]),
        ("The Uses of Literature", 1986, 294, ["Literary Criticism"]),
        ("Six Memos for the Next Millennium", 1988, 124, ["Literary Criticism"]),
    ]),

    ("Paulo Coelho", "pt", ["Literary Fiction", "Philosophy"], [
        ("The Alchemist", 1988, 197, None),
        ("The Pilgrimage", 1987, 250, None),
        ("Brida", 1990, 249, None),
        ("The Valkyries", 1992, 218, None),
        ("By the River Piedra I Sat Down and Wept", 1994, 186, None),
        ("The Fifth Mountain", 1996, 245, None),
        ("Maktub", 1994, 128, None),
        ("Veronika Decides to Die", 1998, 210, None),
        ("The Devil and Miss Prym", 2000, 205, None),
        ("Eleven Minutes", 2003, 315, None),
        ("The Zahir", 2005, 314, None),
        ("The Witch of Portobello", 2006, 305, None),
        ("The Winner Stands Alone", 2008, 375, None),
        ("Aleph", 2010, 315, None),
        ("Manuscript Found in Accra", 2012, 197, None),
        ("Adultery", 2014, 260, None),
        ("The Spy", 2016, 202, ["Historical Fiction"]),
        ("Hippie", 2018, 256, None),
        ("The Archer", 2020, 160, None),
    ]),

    ("Khaled Hosseini", "en", ["Literary Fiction"], [
        ("The Kite Runner", 2003, 371, ["Literary Fiction", "Historical Fiction"]),
        ("A Thousand Splendid Suns", 2007, 372, ["Literary Fiction", "Historical Fiction"]),
        ("And the Mountains Echoed", 2013, 404, None),
        ("Sea Prayer", 2018, 48, ["Poetry"]),
    ]),

    ("Amy Tan", "en", ["Literary Fiction"], [
        ("The Joy Luck Club", 1989, 288, None),
        ("The Kitchen God's Wife", 1991, 415, None),
        ("The Hundred Secret Senses", 1995, 358, None),
        ("The Bonesetter's Daughter", 2001, 353, None),
        ("Saving Fish from Drowning", 2005, 474, None),
        ("The Valley of Amazement", 2013, 589, None),
        ("The Backyard Bird Chronicles", 2024, 256, ["Non-Fiction", "Nature"]),
        ("Where the Past Begins", 2017, 336, ["Memoir"]),
    ]),

    ("Toni Morrison", "en", ["Literary Fiction"], [
        ("The Bluest Eye", 1970, 206, None),
        ("Sula", 1973, 174, None),
        ("Song of Solomon", 1977, 337, None),
        ("Tar Baby", 1981, 305, None),
        ("Beloved", 1987, 324, ["Literary Fiction", "Horror"]),
        ("Jazz", 1992, 229, None),
        ("Paradise", 1997, 318, None),
        ("Love", 2003, 202, None),
        ("A Mercy", 2008, 167, ["Literary Fiction", "Historical Fiction"]),
        ("Home", 2012, 147, None),
        ("God Help the Child", 2015, 178, None),
        ("Playing in the Dark", 1992, 91, ["Literary Criticism"]),
        ("The Source of Self-Regard", 2019, 354, ["Essays"]),
    ]),

    ("Don DeLillo", "en", ["Literary Fiction", "Postmodern"], [
        ("Americana", 1971, 377, None),
        ("End Zone", 1972, 242, None),
        ("Great Jones Street", 1973, 265, None),
        ("Ratner's Star", 1976, 438, None),
        ("Players", 1977, 212, None),
        ("Running Dog", 1978, 248, None),
        ("The Names", 1982, 339, None),
        ("White Noise", 1985, 326, None),
        ("Libra", 1988, 456, ["Literary Fiction", "Historical Fiction"]),
        ("Mao II", 1991, 241, None),
        ("Underworld", 1997, 827, None),
        ("The Body Artist", 2001, 124, None),
        ("Cosmopolis", 2003, 209, None),
        ("Falling Man", 2007, 246, None),
        ("Point Omega", 2010, 117, None),
        ("Zero K", 2016, 274, None),
        ("The Silence", 2020, 116, None),
    ]),

    ("Thomas Pynchon", "en", ["Literary Fiction", "Postmodern"], [
        ("V.", 1963, 492, None),
        ("The Crying of Lot 49", 1966, 152, None),
        ("Gravity's Rainbow", 1973, 760, None),
        ("Slow Learner", 1984, 193, ["Literary Fiction", "Short Stories"]),
        ("Vineland", 1990, 385, None),
        ("Mason & Dixon", 1997, 773, ["Literary Fiction", "Historical Fiction"]),
        ("Against the Day", 2006, 1085, None),
        ("Inherent Vice", 2009, 369, ["Literary Fiction", "Mystery"]),
        ("Bleeding Edge", 2013, 477, None),
    ]),

    ("Cormac McCarthy", "en", ["Literary Fiction"], [
        ("The Orchard Keeper", 1965, 246, None),
        ("Outer Dark", 1968, 242, None),
        ("Child of God", 1973, 197, None),
        ("Suttree", 1979, 471, None),
        ("Blood Meridian", 1985, 337, ["Literary Fiction", "Western"]),
        ("All the Pretty Horses", 1992, 302, ["Literary Fiction", "Western"]),
        ("The Crossing", 1994, 426, ["Literary Fiction", "Western"]),
        ("Cities of the Plain", 1998, 291, ["Literary Fiction", "Western"]),
        ("No Country for Old Men", 2005, 309, ["Literary Fiction", "Thriller"]),
        ("The Road", 2006, 287, ["Literary Fiction", "Dystopian"]),
        ("The Passenger", 2022, 383, None),
        ("Stella Maris", 2022, 190, None),
    ]),

    ("Margaret Atwood", "en", ["Literary Fiction"], [
        ("The Edible Woman", 1969, 281, None),
        ("Surfacing", 1972, 224, None),
        ("Lady Oracle", 1976, 345, None),
        ("Life Before Man", 1979, 317, None),
        ("Bodily Harm", 1981, 301, None),
        ("The Handmaid's Tale", 1985, 311, ["Literary Fiction", "Dystopian", "Science Fiction"]),
        ("Cat's Eye", 1988, 421, None),
        ("The Robber Bride", 1993, 528, None),
        ("Alias Grace", 1996, 470, ["Literary Fiction", "Historical Fiction"]),
        ("The Blind Assassin", 2000, 521, None),
        ("Oryx and Crake", 2003, 374, ["Literary Fiction", "Dystopian", "Science Fiction"]),
        ("The Year of the Flood", 2009, 431, ["Literary Fiction", "Dystopian", "Science Fiction"]),
        ("MaddAddam", 2013, 394, ["Literary Fiction", "Dystopian", "Science Fiction"]),
        ("The Heart Goes Last", 2015, 316, ["Literary Fiction", "Science Fiction"]),
        ("Hag-Seed", 2016, 295, None),
        ("The Testaments", 2019, 419, ["Literary Fiction", "Dystopian", "Science Fiction"]),
        ("Stone Mattress", 2014, 256, ["Literary Fiction", "Short Stories"]),
        ("Moral Disorder", 2006, 257, ["Literary Fiction", "Short Stories"]),
        ("Wilderness Tips", 1991, 227, ["Literary Fiction", "Short Stories"]),
        ("Dancing Girls", 1977, 256, ["Literary Fiction", "Short Stories"]),
        ("Bluebeard's Egg", 1983, 281, ["Literary Fiction", "Short Stories"]),
        ("Old Babes in the Wood", 2023, 272, ["Literary Fiction", "Short Stories"]),
        ("Dearly", 2020, 128, ["Poetry"]),
        ("The Tent", 2006, 163, ["Literary Fiction", "Short Stories"]),
    ]),

    ("Joyce Carol Oates", "en", ["Literary Fiction"], [
        ("them", 1969, 508, None),
        ("Wonderland", 1971, 512, None),
        ("Do with Me What You Will", 1973, 560, None),
        ("The Assassins", 1975, 563, None),
        ("A Bloodsmoor Romance", 1982, 615, ["Literary Fiction", "Gothic"]),
        ("Marya: A Life", 1986, 310, None),
        ("You Must Remember This", 1987, 436, None),
        ("Because It Is Bitter, and Because It Is My Heart", 1990, 405, None),
        ("Black Water", 1992, 154, None),
        ("Foxfire", 1993, 328, None),
        ("What I Lived For", 1994, 608, None),
        ("We Were the Mulvaneys", 1996, 454, None),
        ("Blonde", 2000, 738, ["Literary Fiction", "Historical Fiction"]),
        ("The Falls", 2004, 481, None),
        ("The Gravedigger's Daughter", 2007, 582, None),
        ("A Fair Maiden", 2009, 165, None),
        ("Mudwoman", 2012, 448, None),
        ("The Accursed", 2013, 688, ["Literary Fiction", "Gothic"]),
        ("Carthage", 2014, 496, None),
        ("The Man Without a Shadow", 2016, 384, None),
        ("A Book of American Martyrs", 2017, 736, None),
        ("My Life as a Rat", 2019, 400, None),
        ("Night. Sleep. Death. The Stars.", 2020, 800, None),
        ("Breathe", 2021, 320, None),
        ("Babysitter", 2022, 400, None),
        ("The (Other) You", 2023, 304, ["Literary Fiction", "Short Stories"]),
        ("Zero-Sum", 2024, 384, ["Literary Fiction", "Short Stories"]),
        ("Night, Neon", 2021, 192, ["Literary Fiction", "Short Stories"]),
        ("Beautiful Days", 2018, 384, ["Literary Fiction", "Short Stories"]),
    ]),

    ("Philip Roth", "en", ["Literary Fiction"], [
        ("Goodbye, Columbus", 1959, 298, ["Literary Fiction", "Short Stories"]),
        ("Letting Go", 1962, 630, None),
        ("When She Was Good", 1967, 306, None),
        ("Portnoy's Complaint", 1969, 274, None),
        ("Our Gang", 1971, 200, ["Literary Fiction", "Satire"]),
        ("The Breast", 1972, 89, None),
        ("The Great American Novel", 1973, 382, None),
        ("My Life as a Man", 1974, 330, None),
        ("The Professor of Desire", 1977, 263, None),
        ("The Ghost Writer", 1979, 180, None),
        ("Zuckerman Unbound", 1981, 225, None),
        ("The Anatomy Lesson", 1983, 291, None),
        ("The Counterlife", 1986, 324, None),
        ("Deception", 1990, 208, None),
        ("Operation Shylock", 1993, 398, None),
        ("Sabbath's Theater", 1995, 451, None),
        ("American Pastoral", 1997, 423, None),
        ("I Married a Communist", 1998, 323, None),
        ("The Human Stain", 2000, 361, None),
        ("The Dying Animal", 2001, 156, None),
        ("The Plot Against America", 2004, 391, ["Literary Fiction", "Alternative History"]),
        ("Everyman", 2006, 182, None),
        ("Exit Ghost", 2007, 292, None),
        ("Indignation", 2008, 233, None),
        ("The Humbling", 2009, 140, None),
        ("Nemesis", 2010, 280, None),
    ]),

    ("John Updike", "en", ["Literary Fiction"], [
        ("The Poorhouse Fair", 1959, 185, None),
        ("Rabbit, Run", 1960, 264, None),
        ("The Centaur", 1963, 302, None),
        ("Of the Farm", 1965, 174, None),
        ("Couples", 1968, 458, None),
        ("Rabbit Redux", 1971, 407, None),
        ("A Month of Sundays", 1975, 228, None),
        ("Marry Me", 1976, 303, None),
        ("The Coup", 1978, 299, None),
        ("Rabbit Is Rich", 1981, 467, None),
        ("The Witches of Eastwick", 1984, 307, None),
        ("Roger's Version", 1986, 329, None),
        ("S.", 1988, 279, None),
        ("Rabbit at Rest", 1990, 512, None),
        ("Memories of the Ford Administration", 1992, 369, None),
        ("Brazil", 1994, 260, None),
        ("In the Beauty of the Lilies", 1996, 491, None),
        ("Toward the End of Time", 1997, 334, None),
        ("Gertrude and Claudius", 2000, 212, ["Literary Fiction", "Historical Fiction"]),
        ("Seek My Face", 2002, 276, None),
        ("Villages", 2004, 321, None),
        ("Terrorist", 2006, 310, None),
        ("The Widows of Eastwick", 2008, 308, None),
        ("Pigeon Feathers", 1962, 278, ["Literary Fiction", "Short Stories"]),
        ("Too Far to Go", 1979, 246, ["Literary Fiction", "Short Stories"]),
        ("Trust Me", 1987, 302, ["Literary Fiction", "Short Stories"]),
        ("The Afterlife", 1994, 316, ["Literary Fiction", "Short Stories"]),
        ("Licks of Love", 2000, 359, ["Literary Fiction", "Short Stories"]),
        ("My Father's Tears", 2009, 292, ["Literary Fiction", "Short Stories"]),
    ]),
]


def write_batch(batch_dir, name, books):
    out_path = batch_dir / f"{name}.json"
    with open(out_path, "w") as f:
        json.dump(books, f, indent=2, ensure_ascii=False)
    print(f"  {name}: {len(books)} books")
    return len(books)


def main():
    batch_dir = Path(__file__).parent / "batches"
    batch_dir.mkdir(exist_ok=True)

    all_books = []
    for author, lang, default_genres, works in AUTHORS:
        for work in works:
            title, year, pages, extra_genres = work
            genres = extra_genres if extra_genres else default_genres
            all_books.append(make_book(title, author, year, genres, lang, pages))

    batch_size = 100
    total = 0
    batch_num = 47
    for i in range(0, len(all_books), batch_size):
        chunk = all_books[i:i + batch_size]
        name = f"batch_{batch_num:02d}_authors_{batch_num - 41}"
        total += write_batch(batch_dir, name, chunk)
        batch_num += 1

    print(f"\nTotal new books: {total}")


if __name__ == "__main__":
    main()
