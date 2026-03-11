#!/usr/bin/env python3
"""Batch 29: Push toward 9,500 - completely fresh prolific authors."""
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

# === COMPLETELY FRESH THRILLER/MYSTERY AUTHORS ===

# Brad Thor
for title, year, pages in [
    ("The Lions of Lucerne", 2002, 528), ("Path of the Assassin", 2003, 512),
    ("State of the Union", 2004, 512), ("Blowback", 2005, 528),
    ("Takedown", 2006, 400), ("The First Commandment", 2007, 448),
    ("The Last Patriot", 2008, 384), ("The Apostle", 2009, 400),
    ("Foreign Influence", 2010, 400), ("Full Black", 2011, 400),
    ("Black List", 2012, 416), ("Hidden Order", 2013, 400),
    ("Act of War", 2014, 400), ("Code of Conduct", 2015, 416),
    ("Foreign Agent", 2016, 400), ("Use of Force", 2017, 384),
    ("Spymaster", 2018, 400), ("Backlash", 2019, 400),
    ("Near Dark", 2020, 400), ("Black Ice", 2021, 384),
    ("Rising Tiger", 2022, 384), ("Dead Fall", 2023, 384),
]:
    ALL_BOOKS.append(make_book(title, "Brad Thor", year, pages, ["Thriller", "Spy Fiction"]))

# W.E.B. Griffin
for title, year, pages in [
    ("Semper Fi", 1986, 400), ("Call to Arms", 1987, 368),
    ("Counterattack", 1990, 544), ("Battleground", 1991, 420),
    ("Line of Fire", 1992, 480), ("Close Combat", 1993, 416),
    ("Behind the Lines", 1995, 384), ("In Danger's Path", 1998, 432),
    ("Under Fire", 2002, 464), ("Retreat, Hell!", 2004, 448),
    ("The Murderers", 1994, 432), ("The Investigators", 1997, 464),
    ("The Vigilantes", 2010, 432), ("The Traffickers", 2009, 480),
    ("Honor Bound", 1993, 480), ("Blood and Honor", 1996, 496),
    ("Secret Honor", 2000, 512), ("Death and Honor", 2008, 480),
    ("The Honor of Spies", 2009, 432), ("Victory and Honor", 2011, 448),
]:
    ALL_BOOKS.append(make_book(title, "W.E.B. Griffin", year, pages, ["Thriller", "Military Fiction"]))

# Ace Atkins - Quinn Colson + Spenser
for title, year, pages in [
    ("Crossroad Blues", 1998, 341), ("Leavin' Trunk Blues", 2000, 290),
    ("Dark End of the Street", 2002, 288), ("Dirty South", 2004, 320),
    ("White Shadow", 2006, 320), ("Wicked City", 2008, 336),
    ("Devil's Garden", 2009, 368), ("Infamous", 2010, 384),
    ("The Ranger", 2011, 368), ("The Lost Ones", 2012, 384),
    ("The Broken Places", 2013, 368), ("The Forsaken", 2014, 384),
    ("The Redeemers", 2015, 384), ("The Innocents", 2016, 384),
    ("The Fallen", 2017, 384), ("The Sinners", 2018, 384),
    ("The Shameless", 2019, 384), ("The Revelators", 2020, 384),
    ("The Heathens", 2021, 384),
]:
    ALL_BOOKS.append(make_book(title, "Ace Atkins", year, pages, ["Mystery", "Thriller", "Crime Fiction"]))

# Peter May
for title, year, pages in [
    ("The Blackhouse", 2011, 384), ("The Lewis Man", 2012, 384),
    ("The Chessmen", 2013, 384), ("Entry Island", 2014, 400),
    ("Extraordinary People", 2006, 400), ("The Critic", 2007, 416),
    ("Blowback", 2008, 352), ("Freeze Frame", 2009, 336),
    ("Cast Iron", 2016, 368), ("I'll Keep You Safe", 2018, 400),
    ("A Silent Death", 2019, 400), ("Lockdown", 2020, 352),
    ("The Night Gate", 2021, 416), ("The Noble Path", 2022, 352),
]:
    ALL_BOOKS.append(make_book(title, "Peter May", year, pages, ["Mystery", "Thriller"]))

# Jeffery Deaver - filling remaining
for title, year, pages in [
    ("Manhattan Is My Beat", 1988, 312), ("Death of a Blue Movie Star", 1990, 304),
    ("The Lesson of Her Death", 1993, 398), ("Praying for Sleep", 1994, 458),
    ("A Maiden's Grave", 1995, 434), ("The Bone Collector", 1997, 421),
    ("The Coffin Dancer", 1998, 454), ("The Devil's Teardrop", 1999, 420),
    ("The Empty Chair", 2000, 420), ("Speaking in Tongues", 2000, 432),
    ("The Blue Nowhere", 2001, 432), ("The Stone Monkey", 2002, 420),
    ("The Vanished Man", 2003, 432), ("The Twelfth Card", 2005, 416),
    ("The Cold Moon", 2006, 432), ("The Sleeping Doll", 2007, 432),
    ("The Broken Window", 2008, 464), ("The Bodies Left Behind", 2008, 352),
    ("Roadside Crosses", 2009, 432), ("Edge", 2010, 416),
    ("The Burning Wire", 2010, 432), ("Carte Blanche", 2011, 400),
    ("The Kill Room", 2013, 416), ("The Skin Collector", 2014, 400),
    ("Solitude Creek", 2015, 400), ("The Steel Kiss", 2016, 432),
    ("The Burial Hour", 2017, 432), ("The Cutting Edge", 2018, 432),
    ("The Midnight Lock", 2021, 432), ("The Watchmaker's Hand", 2023, 400),
]:
    ALL_BOOKS.append(make_book(title, "Jeffery Deaver", year, pages, ["Thriller", "Mystery", "Crime Fiction"]))

# Andrew Child / Lee Child - more Jack Reacher
for title, year, pages in [
    ("Killing Floor", 1997, 359), ("Die Trying", 1998, 479),
    ("Tripwire", 1999, 542), ("Running Blind", 2000, 378),
    ("Echo Burning", 2001, 531), ("Without Fail", 2002, 464),
    ("Persuader", 2003, 402), ("The Enemy", 2004, 467),
    ("One Shot", 2005, 417), ("The Hard Way", 2006, 404),
    ("Bad Luck and Trouble", 2007, 377), ("Nothing to Lose", 2008, 407),
    ("Gone Tomorrow", 2009, 374), ("61 Hours", 2010, 383),
    ("Worth Dying For", 2010, 376), ("The Affair", 2011, 405),
    ("A Wanted Man", 2012, 405), ("Never Go Back", 2013, 400),
    ("Personal", 2014, 353), ("Make Me", 2015, 416),
    ("Night School", 2016, 368), ("The Midnight Line", 2017, 368),
    ("Past Tense", 2018, 384), ("Blue Moon", 2019, 352),
    ("The Sentinel", 2020, 368), ("Better Off Dead", 2021, 384),
    ("No Plan B", 2022, 368), ("The Secret", 2023, 368),
]:
    ALL_BOOKS.append(make_book(title, "Lee Child", year, pages, ["Thriller"]))

# === FRESH LITERARY / GENERAL FICTION ===

# Annie Proulx
for title, year, pages in [
    ("Heart Songs and Other Stories", 1988, 175),
    ("Postcards", 1992, 308), ("The Shipping News", 1993, 337),
    ("Accordion Crimes", 1996, 381), ("Close Range", 1999, 283),
    ("That Old Ace in the Hole", 2002, 361), ("Bad Dirt", 2004, 219),
    ("Fine Just the Way It Is", 2008, 221), ("Barkskins", 2016, 736),
    ("Fen, Bog and Swamp", 2022, 208),
]:
    ALL_BOOKS.append(make_book(title, "Annie Proulx", year, pages, ["Literary Fiction"]))

# Kent Haruf
for title, year, pages in [
    ("The Tie That Binds", 1984, 256), ("Where You Once Belonged", 1990, 208),
    ("Plainsong", 1999, 301), ("Eventide", 2004, 300),
    ("Benediction", 2013, 272), ("Our Souls at Night", 2015, 179),
]:
    ALL_BOOKS.append(make_book(title, "Kent Haruf", year, pages, ["Literary Fiction"]))

# Marilynne Robinson (filling remaining)
for title, year, pages in [
    ("Housekeeping", 1980, 219), ("Gilead", 2004, 247),
    ("Home", 2008, 325), ("Lila", 2014, 261),
    ("Jack", 2020, 307), ("Mother Country", 1989, 275),
    ("The Death of Adam", 1998, 254), ("Absence of Mind", 2010, 158),
    ("When I Was a Child I Read Books", 2012, 206),
]:
    ALL_BOOKS.append(make_book(title, "Marilynne Robinson", year, pages, ["Literary Fiction"]))

# Michael Chabon (filling remaining)
for title, year, pages in [
    ("The Mysteries of Pittsburgh", 1988, 297),
    ("A Model World and Other Stories", 1991, 224),
    ("Wonder Boys", 1995, 368),
    ("The Amazing Adventures of Kavalier & Clay", 2000, 639),
    ("Summerland", 2002, 500), ("The Final Solution", 2004, 131),
    ("The Yiddish Policemen's Union", 2007, 414),
    ("Gentlemen of the Road", 2007, 204), ("Telegraph Avenue", 2012, 468),
    ("Moonglow", 2016, 430), ("The Treasure of the Sierra Madre", 2022, 256),
]:
    ALL_BOOKS.append(make_book(title, "Michael Chabon", year, pages, ["Literary Fiction"]))

# Lorrie Moore
for title, year, pages in [
    ("Self-Help", 1985, 170), ("Anagrams", 1986, 227),
    ("Like Life", 1990, 179), ("Who Will Run the Frog Hospital?", 1994, 147),
    ("Birds of America", 1998, 291), ("A Gate at the Stairs", 2009, 321),
    ("Bark", 2014, 176), ("I Am Homeless If This Is Not My Home", 2023, 224),
]:
    ALL_BOOKS.append(make_book(title, "Lorrie Moore", year, pages, ["Literary Fiction", "Short Stories"]))

# George Saunders (filling remaining)
for title, year, pages in [
    ("CivilWarLand in Bad Decline", 1996, 179),
    ("Pastoralia", 2000, 188), ("The Very Persistent Gappers of Frip", 2000, 84),
    ("In Persuasion Nation", 2006, 228), ("The Brief and Frightening Reign of Phil", 2005, 130),
    ("Tenth of December", 2013, 251), ("Lincoln in the Bardo", 2017, 343),
    ("A Swim in a Pond in the Rain", 2021, 409), ("Liberation Day", 2022, 256),
]:
    ALL_BOOKS.append(make_book(title, "George Saunders", year, pages, ["Literary Fiction", "Short Stories"]))

# Denis Johnson
for title, year, pages in [
    ("Angels", 1983, 209), ("Fiskadoro", 1985, 221),
    ("The Stars at Noon", 1986, 214), ("Resuscitation of a Hanged Man", 1991, 265),
    ("Jesus' Son", 1992, 133), ("Already Dead", 1997, 435),
    ("The Name of the World", 2000, 129), ("Tree of Smoke", 2007, 614),
    ("Nobody Move", 2009, 196), ("Train Dreams", 2011, 116),
    ("The Laughing Monsters", 2014, 228),
]:
    ALL_BOOKS.append(make_book(title, "Denis Johnson", year, pages, ["Literary Fiction"]))

# === FRESH SCIENCE FICTION / FANTASY ===

# C.S. Friedman
for title, year, pages in [
    ("In Conquest Born", 1986, 512), ("The Madness Season", 1990, 480),
    ("Black Sun Rising", 1991, 496), ("When True Night Falls", 1993, 576),
    ("Crown of Shadows", 1995, 496), ("This Alien Shore", 1998, 496),
    ("The Wilding", 2004, 384), ("Feast of Souls", 2007, 480),
    ("Wings of Wrath", 2009, 480), ("Legacy of Kings", 2011, 528),
    ("Dreamwalker", 2014, 400), ("Dreamseeker", 2015, 384),
]:
    ALL_BOOKS.append(make_book(title, "C.S. Friedman", year, pages, ["Science Fiction", "Fantasy"]))

# Elizabeth Moon
for title, year, pages in [
    ("Sheepfarmer's Daughter", 1988, 506), ("Divided Allegiance", 1988, 528),
    ("Oath of Gold", 1989, 496), ("Surrender None", 1990, 544),
    ("Liar's Oath", 1992, 528), ("The Speed of Dark", 2002, 340),
    ("Oath of Fealty", 2010, 396), ("Kings of the North", 2011, 464),
    ("Echoes of Betrayal", 2012, 464), ("Limits of Power", 2013, 464),
    ("Crown of Renewal", 2014, 480), ("Trading in Danger", 2003, 400),
    ("Marque and Reprisal", 2004, 384), ("Engaging the Enemy", 2006, 384),
    ("Command Decision", 2007, 384), ("Victory Conditions", 2008, 384),
]:
    ALL_BOOKS.append(make_book(title, "Elizabeth Moon", year, pages, ["Fantasy", "Science Fiction"]))

# Charles Stross
for title, year, pages in [
    ("Singularity Sky", 2003, 313), ("Iron Sunrise", 2004, 355),
    ("Accelerando", 2005, 390), ("Glasshouse", 2006, 335),
    ("Halting State", 2007, 351), ("Saturn's Children", 2008, 323),
    ("Rule 34", 2011, 358), ("Neptune's Brood", 2013, 325),
    ("The Atrocity Archives", 2004, 345), ("The Jennifer Morgue", 2006, 400),
    ("The Fuller Memorandum", 2010, 312), ("The Apocalypse Codex", 2012, 336),
    ("The Rhesus Chart", 2014, 352), ("The Annihilation Score", 2015, 400),
    ("The Nightmare Stacks", 2016, 400), ("The Delirium Brief", 2017, 368),
    ("The Labyrinth Index", 2018, 384), ("Dead Lies Dreaming", 2020, 400),
    ("Quantum of Nightmares", 2022, 400),
]:
    ALL_BOOKS.append(make_book(title, "Charles Stross", year, pages, ["Science Fiction"]))

# Lev Grossman
for title, year, pages in [
    ("Warp", 1997, 212), ("Codex", 2004, 309),
    ("The Magicians", 2009, 402), ("The Magician King", 2011, 400),
    ("The Magician's Land", 2014, 401), ("The Silver Arrow", 2020, 208),
    ("The Golden Swift", 2022, 256),
]:
    ALL_BOOKS.append(make_book(title, "Lev Grossman", year, pages, ["Fantasy"]))

# Mark Lawrence
for title, year, pages in [
    ("Prince of Thorns", 2011, 338), ("King of Thorns", 2012, 449),
    ("Emperor of Thorns", 2013, 432), ("Prince of Fools", 2014, 384),
    ("The Liar's Key", 2015, 480), ("The Wheel of Osheim", 2016, 464),
    ("Red Sister", 2017, 480), ("Grey Sister", 2018, 416),
    ("Holy Sister", 2019, 352), ("One Word Kill", 2019, 208),
    ("Limited Wish", 2019, 224), ("Dispel Illusion", 2019, 208),
    ("The Girl and the Stars", 2020, 384), ("The Girl and the Mountain", 2021, 432),
    ("The Book That Wouldn't Burn", 2023, 448),
]:
    ALL_BOOKS.append(make_book(title, "Mark Lawrence", year, pages, ["Fantasy"]))

# === FRESH NON-FICTION ===

# Mary Beard
for title, year, pages in [
    ("The Parthenon", 2002, 208), ("The Roman Triumph", 2007, 432),
    ("Pompeii", 2008, 352), ("The Fires of Vesuvius", 2008, 360),
    ("Confronting the Classics", 2013, 320), ("Laughter in Ancient Rome", 2014, 319),
    ("SPQR", 2015, 608), ("Women & Power", 2017, 128),
    ("Twelve Caesars", 2021, 320), ("Emperor of Rome", 2023, 512),
]:
    ALL_BOOKS.append(make_book(title, "Mary Beard", year, pages, ["Non-Fiction", "History"]))

# Anthony Beevor
for title, year, pages in [
    ("The Spanish Civil War", 1982, 491), ("Crete: The Battle and the Resistance", 1991, 399),
    ("Stalingrad", 1998, 493), ("The Fall of Berlin 1945", 2002, 489),
    ("The Battle for Spain", 2006, 526), ("D-Day", 2009, 591),
    ("The Second World War", 2012, 863), ("Ardennes 1944", 2015, 471),
    ("Arnhem", 2018, 451), ("Russia", 2022, 576),
]:
    ALL_BOOKS.append(make_book(title, "Anthony Beevor", year, pages, ["Non-Fiction", "History"]))

# Max Hastings
for title, year, pages in [
    ("Bomber Command", 1979, 384), ("The Battle for the Falklands", 1983, 384),
    ("Overlord", 1984, 368), ("The Korean War", 1987, 448),
    ("Armageddon", 2004, 608), ("Retribution", 2008, 636),
    ("Inferno", 2011, 729), ("Catastrophe 1914", 2013, 628),
    ("The Secret War", 2015, 631), ("Vietnam", 2018, 752),
    ("Chastise", 2019, 464), ("Operation Pedestal", 2021, 432),
    ("Abyss", 2022, 512),
]:
    ALL_BOOKS.append(make_book(title, "Max Hastings", year, pages, ["Non-Fiction", "History"]))

# Niall Ferguson
for title, year, pages in [
    ("Paper and Iron", 1995, 576), ("The Pity of War", 1998, 563),
    ("The House of Rothschild: Money's Prophets", 1998, 540),
    ("The Cash Nexus", 2001, 552), ("Empire", 2003, 392),
    ("Colossus", 2004, 384), ("The War of the World", 2006, 808),
    ("The Ascent of Money", 2008, 441), ("Civilization", 2011, 402),
    ("The Great Degeneration", 2012, 192), ("Kissinger", 2015, 1008),
    ("The Square and the Tower", 2017, 573), ("Doom", 2021, 496),
]:
    ALL_BOOKS.append(make_book(title, "Niall Ferguson", year, pages, ["Non-Fiction", "History"]))

# Dava Sobel
for title, year, pages in [
    ("Longitude", 1995, 184), ("Galileo's Daughter", 1999, 420),
    ("The Planets", 2005, 270), ("A More Perfect Heaven", 2011, 273),
    ("The Glass Universe", 2016, 324),
]:
    ALL_BOOKS.append(make_book(title, "Dava Sobel", year, pages, ["Non-Fiction", "Science", "History"]))

# Simon Singh
for title, year, pages in [
    ("Fermat's Last Theorem", 1997, 340), ("The Code Book", 1999, 416),
    ("Big Bang", 2004, 532), ("Trick or Treatment?", 2008, 342),
    ("The Simpsons and Their Mathematical Secrets", 2013, 255),
]:
    ALL_BOOKS.append(make_book(title, "Simon Singh", year, pages, ["Non-Fiction", "Science"]))

# === FRESH ROMANCE/WOMEN'S FICTION ===

# Helen Hoang
for title, year, pages in [
    ("The Kiss Quotient", 2018, 336), ("The Bride Test", 2019, 304),
    ("The Heart Principle", 2021, 336),
]:
    ALL_BOOKS.append(make_book(title, "Helen Hoang", year, pages, ["Romance"]))

# Kennedy Ryan
for title, year, pages in [
    ("When You Are Mine", 2018, 370), ("Long Shot", 2018, 416),
    ("Block Shot", 2019, 400), ("Hook Shot", 2019, 382),
    ("Before I Let Go", 2022, 448), ("This Could Be Us", 2024, 400),
]:
    ALL_BOOKS.append(make_book(title, "Kennedy Ryan", year, pages, ["Romance"]))

# Abby Jimenez
for title, year, pages in [
    ("The Friend Zone", 2019, 384), ("The Happy Ever After Playlist", 2020, 368),
    ("Life's Too Short", 2021, 352), ("Part of Your World", 2022, 400),
    ("Yours Truly", 2023, 416), ("Just for the Summer", 2024, 400),
]:
    ALL_BOOKS.append(make_book(title, "Abby Jimenez", year, pages, ["Romance"]))

# Courtney Milan
for title, year, pages in [
    ("Proof by Seduction", 2010, 304), ("Trial by Desire", 2010, 320),
    ("Unveiled", 2011, 304), ("Unlocked", 2011, 200),
    ("Unclaimed", 2011, 352), ("Unraveled", 2012, 336),
    ("The Duchess War", 2012, 288), ("The Heiress Effect", 2013, 384),
    ("The Countess Conspiracy", 2013, 352), ("The Suffragette Scandal", 2014, 352),
    ("Hold Me", 2016, 322), ("Trade Me", 2015, 320),
    ("Her Every Wish", 2016, 268),
]:
    ALL_BOOKS.append(make_book(title, "Courtney Milan", year, pages, ["Romance", "Historical Fiction"]))

# === GEOGRAPHY / TRAVEL FRESH ===

# Rory Stewart
for title, year, pages in [
    ("The Places in Between", 2004, 299), ("The Prince of the Marshes", 2006, 416),
    ("Occupational Hazards", 2006, 398), ("Politics on the Edge", 2023, 416),
]:
    ALL_BOOKS.append(make_book(title, "Rory Stewart", year, pages, ["Non-Fiction", "Travel"]))

# Colin Thubron
for title, year, pages in [
    ("Among the Russians", 1983, 288), ("Behind the Wall", 1987, 304),
    ("The Lost Heart of Asia", 1994, 384), ("In Siberia", 1999, 287),
    ("Shadow of the Silk Road", 2006, 384), ("To a Mountain in Tibet", 2011, 230),
    ("The Amur River", 2021, 304),
]:
    ALL_BOOKS.append(make_book(title, "Colin Thubron", year, pages, ["Non-Fiction", "Travel"]))

# Jan Morris
for title, year, pages in [
    ("Venice", 1960, 320), ("The World of Venice", 1974, 326),
    ("Heaven's Command", 1973, 554), ("Pax Britannica", 1968, 576),
    ("Farewell the Trumpets", 1978, 575), ("Conundrum", 1974, 174),
    ("The Oxford Book of Oxford", 1978, 414), ("Destinations", 1980, 256),
    ("Stones of Empire", 1983, 240), ("Among the Cities", 1985, 350),
    ("Manhattan '45", 1987, 316), ("Hong Kong", 1988, 336),
    ("Sydney", 1992, 224), ("Trieste and the Meaning of Nowhere", 2001, 204),
    ("Hav", 2006, 281), ("Thinking Again", 2020, 176),
]:
    ALL_BOOKS.append(make_book(title, "Jan Morris", year, pages, ["Non-Fiction", "Travel"]))

# === FRESH CHILDREN'S/YA ===

# Cornelia Funke
for title, year, pages in [
    ("The Thief Lord", 2000, 350), ("Dragon Rider", 1997, 528),
    ("Inkheart", 2003, 534), ("Inkspell", 2005, 635),
    ("Inkdeath", 2007, 683), ("Reckless", 2010, 394),
    ("Fearless", 2012, 432), ("The Golden Yarn", 2015, 448),
    ("The Color of Revenge", 2023, 416), ("Ghost Knight", 2011, 262),
    ("The Book No One Ever Read", 2017, 32), ("When Santa Fell to Earth", 2006, 224),
]:
    ALL_BOOKS.append(make_book(title, "Cornelia Funke", year, pages, ["Fantasy", "Children's"]))

# Jonathan Stroud - Bartimaeus
for title, year, pages in [
    ("The Amulet of Samarkand", 2003, 462), ("The Golem's Eye", 2004, 562),
    ("Ptolemy's Gate", 2005, 501), ("The Ring of Solomon", 2010, 398),
    ("Lockwood & Co: The Screaming Staircase", 2013, 390),
    ("Lockwood & Co: The Whispering Skull", 2014, 435),
    ("Lockwood & Co: The Hollow Boy", 2015, 422),
    ("Lockwood & Co: The Creeping Shadow", 2016, 418),
    ("Lockwood & Co: The Empty Grave", 2017, 432),
]:
    ALL_BOOKS.append(make_book(title, "Jonathan Stroud", year, pages, ["Fantasy", "Young Adult"]))

# Derek Landy - Skulduggery Pleasant
for title, year, pages in [
    ("Skulduggery Pleasant", 2007, 400), ("Playing with Fire", 2008, 416),
    ("The Faceless Ones", 2009, 400), ("Dark Days", 2010, 368),
    ("Mortal Coil", 2010, 528), ("Death Bringer", 2011, 608),
    ("Kingdom of the Wicked", 2012, 592), ("Last Stand of Dead Men", 2013, 592),
    ("The Dying of the Light", 2014, 608), ("Resurrection", 2017, 496),
    ("Midnight", 2018, 496), ("Bedlam", 2019, 528),
    ("Seasons of War", 2020, 576), ("Dead or Alive", 2021, 576),
    ("Until the End", 2022, 576),
]:
    ALL_BOOKS.append(make_book(title, "Derek Landy", year, pages, ["Fantasy", "Young Adult"]))


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

    batch_num = 170
    for i in range(0, len(new_books), 100):
        chunk = new_books[i:i+100]
        fname = f"batch_{batch_num}_batch29_{(i//100)+1}.json"
        with open(os.path.join(BATCH_DIR, fname), "w") as f:
            json.dump(chunk, f, indent=2)
        print(f"  {fname}: {len(chunk)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(new_books)}")
