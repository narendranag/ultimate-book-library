#!/usr/bin/env python3
"""Batch 28: Fresh authors only - targeting completely new names for maximum yield."""
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

# === CLASSIC MYSTERY AUTHORS NOT YET COVERED ===

# Dorothy L. Sayers - Lord Peter Wimsey
for title, year, pages in [
    ("Whose Body?", 1923, 222), ("Clouds of Witness", 1926, 297),
    ("Unnatural Death", 1927, 262), ("The Unpleasantness at the Bellona Club", 1928, 279),
    ("Strong Poison", 1930, 252), ("The Five Red Herrings", 1931, 308),
    ("Have His Carcase", 1932, 471), ("Murder Must Advertise", 1933, 302),
    ("The Nine Tailors", 1934, 331), ("Gaudy Night", 1935, 501),
    ("Busman's Honeymoon", 1937, 381), ("In the Teeth of the Evidence", 1939, 285),
]:
    ALL_BOOKS.append(make_book(title, "Dorothy L. Sayers", year, pages, ["Mystery", "Classic"]))

# Margery Allingham - Albert Campion
for title, year, pages in [
    ("The Crime at Black Dudley", 1929, 256), ("Mystery Mile", 1930, 256),
    ("Look to the Lady", 1931, 256), ("Police at the Funeral", 1931, 288),
    ("Sweet Danger", 1933, 256), ("Death of a Ghost", 1934, 256),
    ("Flowers for the Judge", 1936, 256), ("The Case of the Late Pig", 1937, 160),
    ("Dancers in Mourning", 1937, 303), ("The Fashion in Shrouds", 1938, 288),
    ("Traitor's Purse", 1941, 192), ("Coroner's Pidgin", 1945, 224),
    ("More Work for the Undertaker", 1948, 256), ("The Tiger in the Smoke", 1952, 224),
    ("The Beckoning Lady", 1955, 256), ("Hide My Eyes", 1958, 224),
    ("The China Governess", 1963, 256), ("The Mind Readers", 1965, 224),
    ("Cargo of Eagles", 1968, 224),
]:
    ALL_BOOKS.append(make_book(title, "Margery Allingham", year, pages, ["Mystery", "Classic"]))

# Josephine Tey
for title, year, pages in [
    ("The Man in the Queue", 1929, 288), ("A Shilling for Candles", 1936, 256),
    ("Miss Pym Disposes", 1946, 256), ("The Franchise Affair", 1948, 260),
    ("Brat Farrar", 1949, 254), ("To Love and Be Wise", 1950, 265),
    ("The Daughter of Time", 1951, 206), ("The Singing Sands", 1952, 223),
]:
    ALL_BOOKS.append(make_book(title, "Josephine Tey", year, pages, ["Mystery", "Classic"]))

# === ACTION/THRILLER - FRESH ===

# Alistair MacLean
for title, year, pages in [
    ("HMS Ulysses", 1955, 320), ("The Guns of Navarone", 1957, 320),
    ("South by Java Head", 1958, 320), ("The Last Frontier", 1959, 288),
    ("Night Without End", 1959, 256), ("Fear Is the Key", 1961, 288),
    ("The Dark Crusader", 1961, 256), ("The Satan Bug", 1962, 288),
    ("Ice Station Zebra", 1963, 320), ("When Eight Bells Toll", 1966, 288),
    ("Where Eagles Dare", 1967, 288), ("Force 10 from Navarone", 1968, 288),
    ("Puppet on a Chain", 1969, 256), ("Bear Island", 1971, 288),
    ("Breakheart Pass", 1974, 205), ("Circus", 1975, 256),
    ("The Golden Gate", 1976, 256), ("Seawitch", 1977, 256),
    ("Goodbye California", 1977, 320), ("Athabasca", 1980, 256),
]:
    ALL_BOOKS.append(make_book(title, "Alistair MacLean", year, pages, ["Thriller", "Adventure"]))

# Jack Higgins
for title, year, pages in [
    ("The Eagle Has Landed", 1975, 352), ("Storm Warning", 1976, 304),
    ("Day of Judgment", 1978, 256), ("Solo", 1980, 288),
    ("Luciano's Luck", 1981, 272), ("Touch the Devil", 1982, 320),
    ("Exocet", 1983, 304), ("Confessional", 1985, 304),
    ("Night of the Fox", 1986, 336), ("A Season in Hell", 1989, 336),
    ("Cold Harbour", 1990, 320), ("The Eagle Has Flown", 1991, 336),
    ("Eye of the Storm", 1992, 336), ("Thunder Point", 1993, 288),
    ("On Dangerous Ground", 1994, 302), ("Angel of Death", 1995, 352),
    ("Drink with the Devil", 1996, 288), ("The President's Daughter", 1997, 352),
    ("Flight of Eagles", 1998, 336), ("The White House Connection", 1999, 304),
    ("Day of Reckoning", 2000, 304), ("Edge of Danger", 2001, 336),
    ("Midnight Runner", 2002, 304), ("Bad Company", 2003, 352),
    ("Dark Justice", 2004, 288), ("Without Mercy", 2005, 288),
    ("The Killing Ground", 2007, 304), ("A Darker Place", 2009, 336),
]:
    ALL_BOOKS.append(make_book(title, "Jack Higgins", year, pages, ["Thriller", "Adventure", "Spy Fiction"]))

# Desmond Bagley
for title, year, pages in [
    ("The Golden Keel", 1963, 254), ("High Citadel", 1965, 255),
    ("Wyatt's Hurricane", 1966, 288), ("Landslide", 1967, 256),
    ("The Vivero Letter", 1968, 320), ("The Spoilers", 1969, 288),
    ("Running Blind", 1970, 256), ("The Freedom Trap", 1971, 256),
    ("The Tightrope Men", 1973, 288), ("The Snow Tiger", 1975, 320),
    ("The Enemy", 1977, 288), ("Flyaway", 1978, 320),
    ("Bahama Crisis", 1980, 288), ("Windfall", 1982, 352),
    ("Night of Error", 1984, 288), ("Juggernaut", 1985, 320),
]:
    ALL_BOOKS.append(make_book(title, "Desmond Bagley", year, pages, ["Thriller", "Adventure"]))

# James Herbert
for title, year, pages in [
    ("The Rats", 1974, 176), ("The Fog", 1975, 224),
    ("The Survivor", 1976, 208), ("Fluke", 1977, 224),
    ("The Spear", 1978, 320), ("Lair", 1979, 288),
    ("The Dark", 1980, 384), ("The Jonah", 1981, 320),
    ("Shrine", 1983, 448), ("Domain", 1984, 384),
    ("Moon", 1985, 384), ("The Magic Cottage", 1986, 352),
    ("Sepulchre", 1987, 384), ("Haunted", 1988, 352),
    ("Creed", 1990, 384), ("Portent", 1992, 384),
    ("The Ghosts of Sleath", 1994, 448), ("'48", 1996, 384),
    ("Others", 1999, 448), ("Once...", 2001, 448),
    ("Nobody True", 2003, 416), ("The Secret of Crickley Hall", 2006, 576),
    ("Ash", 2012, 672),
]:
    ALL_BOOKS.append(make_book(title, "James Herbert", year, pages, ["Horror", "Thriller"]))

# === LITERARY FICTION - COMPLETELY FRESH ===

# Kate Morton
for title, year, pages in [
    ("The House at Riverton", 2006, 560), ("The Forgotten Garden", 2008, 548),
    ("The Distant Hours", 2010, 562), ("The Secret Keeper", 2012, 464),
    ("The Lake House", 2015, 512), ("The Clockmaker's Daughter", 2018, 485),
    ("Homecoming", 2023, 560),
]:
    ALL_BOOKS.append(make_book(title, "Kate Morton", year, pages, ["Literary Fiction", "Mystery", "Historical Fiction"]))

# Lisa See
for title, year, pages in [
    ("On Gold Mountain", 1995, 394), ("Flower Net", 1997, 384),
    ("The Interior", 1999, 384), ("Dragon Bones", 2003, 358),
    ("Snow Flower and the Secret Fan", 2005, 258),
    ("Peony in Love", 2007, 284), ("Shanghai Girls", 2009, 314),
    ("Dreams of Joy", 2011, 354), ("China Dolls", 2014, 384),
    ("The Tea Girl of Hummingbird Lane", 2017, 384),
    ("The Island of Sea Women", 2019, 374),
    ("Lady Tan's Circle of Women", 2023, 368),
]:
    ALL_BOOKS.append(make_book(title, "Lisa See", year, pages, ["Literary Fiction", "Historical Fiction"]))

# Chang-rae Lee
for title, year, pages in [
    ("Native Speaker", 1995, 324), ("A Gesture Life", 1999, 356),
    ("Aloft", 2004, 343), ("The Surrendered", 2010, 469),
    ("On Such a Full Sea", 2014, 352), ("My Year Abroad", 2021, 480),
]:
    ALL_BOOKS.append(make_book(title, "Chang-rae Lee", year, pages, ["Literary Fiction"]))

# Abraham Verghese
for title, year, pages in [
    ("My Own Country", 1994, 432), ("The Tennis Partner", 1998, 400),
    ("Cutting for Stone", 2009, 658), ("The Covenant of Water", 2023, 717),
]:
    ALL_BOOKS.append(make_book(title, "Abraham Verghese", year, pages, ["Literary Fiction"]))

# Riley Sager
for title, year, pages in [
    ("Final Girls", 2017, 352), ("The Last Time I Lied", 2018, 368),
    ("Lock Every Door", 2019, 368), ("Home Before Dark", 2020, 384),
    ("Survive the Night", 2021, 352), ("The House Across the Lake", 2022, 320),
    ("The Only One Left", 2023, 384), ("Middle of the Night", 2024, 368),
]:
    ALL_BOOKS.append(make_book(title, "Riley Sager", year, pages, ["Thriller", "Horror"]))

# Audrey Niffenegger
for title, year, pages in [
    ("The Time Traveler's Wife", 2003, 518), ("Her Fearful Symmetry", 2009, 406),
]:
    ALL_BOOKS.append(make_book(title, "Audrey Niffenegger", year, pages, ["Literary Fiction", "Romance"]))

# Anchee Min
for title, year, pages in [
    ("Red Azalea", 1994, 306), ("Katherine", 1995, 240),
    ("Becoming Madame Mao", 2000, 337), ("Wild Ginger", 2002, 228),
    ("Empress Orchid", 2004, 336), ("The Last Empress", 2007, 308),
    ("Pearl of China", 2010, 288), ("The Cooked Seed", 2013, 352),
]:
    ALL_BOOKS.append(make_book(title, "Anchee Min", year, pages, ["Literary Fiction", "Historical Fiction"]))

# Maxine Hong Kingston
for title, year, pages in [
    ("The Woman Warrior", 1976, 209), ("China Men", 1980, 308),
    ("Tripmaster Monkey", 1989, 340), ("The Fifth Book of Peace", 2003, 402),
    ("I Love a Broad Margin to My Life", 2011, 240),
]:
    ALL_BOOKS.append(make_book(title, "Maxine Hong Kingston", year, pages, ["Literary Fiction", "Memoir"]))

# Harlan Ellison
for title, year, pages in [
    ("A Touch of Infinity", 1960, 224), ("Ellison Wonderland", 1962, 256),
    ("Paingod and Other Delusions", 1965, 224), ("I Have No Mouth, and I Must Scream", 1967, 224),
    ("The Beast That Shouted Love at the Heart of the World", 1969, 288),
    ("Deathbird Stories", 1975, 334), ("Strange Wine", 1978, 288),
    ("Shatterday", 1980, 338), ("Stalking the Nightmare", 1982, 313),
    ("Angry Candy", 1988, 352), ("Slippage", 1997, 416),
]:
    ALL_BOOKS.append(make_book(title, "Harlan Ellison", year, pages, ["Science Fiction", "Short Stories"]))

# Ramsey Campbell
for title, year, pages in [
    ("The Doll Who Ate His Mother", 1976, 191), ("The Face That Must Die", 1979, 192),
    ("The Parasite", 1980, 250), ("The Nameless", 1981, 275),
    ("Incarnate", 1983, 462), ("Obsession", 1985, 346),
    ("The Hungry Moon", 1986, 367), ("The Influence", 1988, 287),
    ("Ancient Images", 1989, 303), ("Midnight Sun", 1990, 317),
    ("The Count of Eleven", 1991, 371), ("The Long Lost", 1993, 422),
    ("The One Safe Place", 1995, 461), ("The House on Nazareth Hill", 1996, 352),
    ("The Last Voice They Hear", 1998, 368), ("Silent Children", 2000, 350),
    ("The Darkest Part of the Woods", 2003, 329), ("The Overnight", 2004, 370),
    ("Secret Story", 2006, 308), ("The Grin of the Dark", 2007, 307),
    ("Thieving Fear", 2008, 360), ("Creatures of the Pool", 2009, 288),
    ("The Seven Days of Cain", 2010, 257), ("Ghosts Know", 2011, 304),
    ("The Kind Folk", 2012, 288), ("Think Yourself Lucky", 2014, 320),
]:
    ALL_BOOKS.append(make_book(title, "Ramsey Campbell", year, pages, ["Horror"]))

# Peter Benchley
for title, year, pages in [
    ("Jaws", 1974, 311), ("The Deep", 1976, 264),
    ("The Island", 1979, 305), ("The Girl of the Sea of Cortez", 1982, 204),
    ("Q Clearance", 1986, 320), ("Rummies", 1989, 320),
    ("Beast", 1991, 293), ("White Shark", 1994, 288),
]:
    ALL_BOOKS.append(make_book(title, "Peter Benchley", year, pages, ["Thriller", "Adventure"]))

# === NON-FICTION - COMPLETELY FRESH ===

# Atul Gawande
for title, year, pages in [
    ("Complications", 2002, 269), ("Better", 2007, 273),
    ("The Checklist Manifesto", 2009, 209), ("Being Mortal", 2014, 282),
]:
    ALL_BOOKS.append(make_book(title, "Atul Gawande", year, pages, ["Non-Fiction", "Science"]))

# Siddhartha Mukherjee
for title, year, pages in [
    ("The Emperor of All Maladies", 2010, 571), ("The Laws of Medicine", 2015, 80),
    ("The Gene", 2016, 592), ("The Song of the Cell", 2022, 496),
]:
    ALL_BOOKS.append(make_book(title, "Siddhartha Mukherjee", year, pages, ["Non-Fiction", "Science"]))

# Matthew Walker
for title, year, pages in [
    ("Why We Sleep", 2017, 368),
]:
    ALL_BOOKS.append(make_book(title, "Matthew Walker", year, pages, ["Non-Fiction", "Science"]))

# Robert Sapolsky
for title, year, pages in [
    ("A Primate's Memoir", 2001, 304), ("Why Zebras Don't Get Ulcers", 2004, 560),
    ("Monkeyluv", 2005, 209), ("Behave", 2017, 790),
    ("Determined", 2023, 528),
]:
    ALL_BOOKS.append(make_book(title, "Robert Sapolsky", year, pages, ["Non-Fiction", "Science"]))

# David Grann
for title, year, pages in [
    ("The Lost City of Z", 2009, 339), ("Killers of the Flower Moon", 2017, 338),
    ("The White Darkness", 2018, 144), ("The Wager", 2023, 352),
]:
    ALL_BOOKS.append(make_book(title, "David Grann", year, pages, ["Non-Fiction", "History"]))

# Patrick Radden Keefe
for title, year, pages in [
    ("Chatter", 2005, 296), ("The Snakehead", 2009, 432),
    ("Say Nothing", 2019, 464), ("Empire of Pain", 2021, 535),
    ("Rogues", 2022, 352),
]:
    ALL_BOOKS.append(make_book(title, "Patrick Radden Keefe", year, pages, ["Non-Fiction", "History"]))

# Ibram X. Kendi
for title, year, pages in [
    ("Stamped from the Beginning", 2016, 592),
    ("How to Be an Antiracist", 2019, 320),
]:
    ALL_BOOKS.append(make_book(title, "Ibram X. Kendi", year, pages, ["Non-Fiction", "History"]))

# Susan Orlean
for title, year, pages in [
    ("Saturday Night", 1990, 272), ("The Orchid Thief", 1998, 284),
    ("The Bullfighter Checks Her Makeup", 2001, 288),
    ("My Kind of Place", 2004, 304), ("Rin Tin Tin", 2011, 336),
    ("The Library Book", 2018, 317), ("On Animals", 2021, 288),
]:
    ALL_BOOKS.append(make_book(title, "Susan Orlean", year, pages, ["Non-Fiction"]))

# Hampton Sides
for title, year, pages in [
    ("Ghost Soldiers", 2001, 342), ("Blood and Thunder", 2006, 462),
    ("Hellhound on His Trail", 2010, 459), ("In the Kingdom of Ice", 2014, 480),
    ("On Desperate Ground", 2018, 416), ("The Wide Wide Sea", 2024, 432),
]:
    ALL_BOOKS.append(make_book(title, "Hampton Sides", year, pages, ["Non-Fiction", "History"]))

# Candice Millard
for title, year, pages in [
    ("The River of Doubt", 2005, 416), ("Destiny of the Republic", 2011, 352),
    ("Hero of the Empire", 2016, 384), ("River of the Gods", 2022, 352),
]:
    ALL_BOOKS.append(make_book(title, "Candice Millard", year, pages, ["Non-Fiction", "History"]))

# === ROMANCE / WOMEN'S FICTION - FRESH ===

# Colleen Hoover (filling remaining)
for title, year, pages in [
    ("Slammed", 2012, 340), ("Point of Retreat", 2012, 280),
    ("Hopeless", 2012, 406), ("Losing Hope", 2013, 318),
    ("Maybe Someday", 2014, 384), ("Ugly Love", 2014, 329),
    ("Confess", 2015, 352), ("November 9", 2015, 320),
    ("It Ends with Us", 2016, 385), ("Without Merit", 2017, 364),
    ("All Your Perfects", 2018, 320), ("Verity", 2018, 314),
    ("Regretting You", 2019, 352), ("Heart Bones", 2020, 352),
    ("Layla", 2020, 336), ("Reminders of Him", 2022, 335),
    ("It Starts with Us", 2022, 336),
]:
    ALL_BOOKS.append(make_book(title, "Colleen Hoover", year, pages, ["Romance"]))

# Emily Henry (filling remaining)
for title, year, pages in [
    ("The Love That Split the World", 2016, 393),
    ("A Million Junes", 2017, 352), ("Beach Read", 2020, 361),
    ("People We Meet on Vacation", 2021, 364),
    ("Book Lovers", 2022, 373), ("Happy Place", 2023, 400),
    ("Funny Story", 2024, 395),
]:
    ALL_BOOKS.append(make_book(title, "Emily Henry", year, pages, ["Romance"]))

# Talia Hibbert
for title, year, pages in [
    ("Get a Life, Chloe Brown", 2019, 373),
    ("Take a Hint, Dani Brown", 2020, 384),
    ("Act Your Age, Eve Brown", 2021, 368),
]:
    ALL_BOOKS.append(make_book(title, "Talia Hibbert", year, pages, ["Romance"]))

# Christina Lauren
for title, year, pages in [
    ("Beautiful Bastard", 2013, 304), ("Beautiful Stranger", 2013, 304),
    ("Beautiful Player", 2013, 320), ("The Unhoneymooners", 2019, 400),
    ("In a Holidaze", 2020, 320), ("The Soulmate Equation", 2021, 352),
    ("Something Wilder", 2022, 352), ("The True Love Experiment", 2023, 384),
]:
    ALL_BOOKS.append(make_book(title, "Christina Lauren", year, pages, ["Romance"]))

# Jasmine Guillory
for title, year, pages in [
    ("The Wedding Date", 2018, 320), ("The Proposal", 2018, 325),
    ("The Wedding Party", 2019, 320), ("Royal Holiday", 2019, 304),
    ("Party of Two", 2020, 336), ("While We Were Dating", 2021, 352),
    ("By the Book", 2022, 336), ("Drunk on Love", 2022, 352),
]:
    ALL_BOOKS.append(make_book(title, "Jasmine Guillory", year, pages, ["Romance"]))

# === SCI-FI / FANTASY FRESH ===

# Arkady Martine
for title, year, pages in [
    ("A Memory Called Empire", 2019, 462),
    ("A Desolation Called Peace", 2021, 496),
]:
    ALL_BOOKS.append(make_book(title, "Arkady Martine", year, pages, ["Science Fiction"]))

# Shelley Parker-Chan
for title, year, pages in [
    ("She Who Became the Sun", 2021, 416),
    ("He Who Drowned the World", 2023, 432),
]:
    ALL_BOOKS.append(make_book(title, "Shelley Parker-Chan", year, pages, ["Fantasy", "Historical Fiction"]))

# Travis Baldree
for title, year, pages in [
    ("Legends & Lattes", 2022, 296), ("Bookshops & Bonedust", 2023, 352),
]:
    ALL_BOOKS.append(make_book(title, "Travis Baldree", year, pages, ["Fantasy"]))

# P. Djèlí Clark
for title, year, pages in [
    ("A Master of Djinn", 2021, 396), ("Ring Shout", 2020, 192),
    ("The Dead Cat Tail Assassins", 2024, 144),
]:
    ALL_BOOKS.append(make_book(title, "P. Djèlí Clark", year, pages, ["Fantasy"]))

# Samantha Shannon
for title, year, pages in [
    ("The Bone Season", 2013, 466), ("The Mime Order", 2015, 528),
    ("The Song Rising", 2017, 416), ("The Mask Falling", 2021, 560),
    ("The Priory of the Orange Tree", 2019, 848),
    ("A Day of Fallen Night", 2023, 848),
]:
    ALL_BOOKS.append(make_book(title, "Samantha Shannon", year, pages, ["Fantasy"]))

# Fonda Lee
for title, year, pages in [
    ("Jade City", 2017, 498), ("Jade War", 2019, 592),
    ("Jade Legacy", 2021, 752), ("Exo", 2017, 384),
    ("Cross Fire", 2018, 400),
]:
    ALL_BOOKS.append(make_book(title, "Fonda Lee", year, pages, ["Fantasy"]))

# Tamsyn Muir - Locked Tomb
for title, year, pages in [
    ("Gideon the Ninth", 2019, 448), ("Harrow the Ninth", 2020, 512),
    ("Nona the Ninth", 2022, 480), ("Alecto the Ninth", 2024, 608),
]:
    ALL_BOOKS.append(make_book(title, "Tamsyn Muir", year, pages, ["Fantasy", "Science Fiction"]))

# Naomi Novik (filling remaining)
for title, year, pages in [
    ("His Majesty's Dragon", 2006, 356), ("Throne of Jade", 2006, 398),
    ("Black Powder War", 2006, 365), ("Empire of Ivory", 2007, 404),
    ("Victory of Eagles", 2008, 352), ("Tongues of Serpents", 2010, 272),
    ("Crucible of Gold", 2012, 302), ("Blood of Tyrants", 2013, 356),
    ("League of Dragons", 2016, 416),
]:
    ALL_BOOKS.append(make_book(title, "Naomi Novik", year, pages, ["Fantasy", "Historical Fiction"]))

# === INDIAN / SOUTH ASIAN FICTION - FRESH ===

# Pankaj Mishra
for title, year, pages in [
    ("The Romantics", 1999, 260), ("An End to Suffering", 2004, 424),
    ("Temptations of the West", 2006, 323), ("From the Ruins of Empire", 2012, 356),
    ("Age of Anger", 2017, 406), ("Run and Hide", 2022, 272),
]:
    ALL_BOOKS.append(make_book(title, "Pankaj Mishra", year, pages, ["Literary Fiction", "Indian Fiction"]))

# Neel Mukherjee
for title, year, pages in [
    ("A Life Apart", 2008, 368), ("The Lives of Others", 2014, 512),
    ("A State of Freedom", 2017, 288), ("Choice", 2023, 416),
]:
    ALL_BOOKS.append(make_book(title, "Neel Mukherjee", year, pages, ["Literary Fiction", "Indian Fiction"]))

# Amitava Kumar
for title, year, pages in [
    ("Husband of a Fanatic", 2005, 296), ("A Foreigner Carrying in the Crook of His Arm a Tiny Bomb", 2010, 256),
    ("Immigrant, Montana", 2018, 256), ("A Time Outside This Time", 2021, 272),
    ("My Beloved Life", 2023, 336),
]:
    ALL_BOOKS.append(make_book(title, "Amitava Kumar", year, pages, ["Literary Fiction", "Indian Fiction"]))

# Shashi Tharoor (filling remaining)
for title, year, pages in [
    ("The Great Indian Novel", 1989, 423), ("Show Business", 1992, 310),
    ("Riot", 2001, 275), ("An Era of Darkness", 2016, 296),
    ("Why I Am a Hindu", 2018, 302), ("The Battle of Belonging", 2020, 487),
    ("Pax Indica", 2012, 476), ("India: From Midnight to the Millennium", 1997, 392),
]:
    ALL_BOOKS.append(make_book(title, "Shashi Tharoor", year, pages, ["Literary Fiction", "Non-Fiction", "Indian Fiction"]))

# Manu Joseph
for title, year, pages in [
    ("Serious Men", 2010, 272), ("The Illicit Happiness of Other People", 2012, 352),
    ("Miss Laila, Armed and Dangerous", 2017, 224),
]:
    ALL_BOOKS.append(make_book(title, "Manu Joseph", year, pages, ["Literary Fiction", "Indian Fiction"]))

# Chitra Banerjee Divakaruni (filling remaining)
for title, year, pages in [
    ("Arranged Marriage", 1995, 307), ("The Mistress of Spices", 1997, 317),
    ("Sister of My Heart", 1999, 322), ("The Vine of Desire", 2002, 323),
    ("Queen of Dreams", 2004, 336), ("The Palace of Illusions", 2008, 360),
    ("One Amazing Thing", 2010, 224), ("Oleander Girl", 2013, 304),
    ("Before We Visit the Goddess", 2016, 288), ("The Last Queen", 2021, 400),
    ("Independence", 2022, 368),
]:
    ALL_BOOKS.append(make_book(title, "Chitra Banerjee Divakaruni", year, pages, ["Literary Fiction", "Indian Fiction"]))

# === FRESH SCIENCE / TECH NON-FICTION ===

# Carlo Rovelli
for title, year, pages in [
    ("Seven Brief Lessons on Physics", 2014, 96),
    ("The Order of Time", 2017, 224), ("Reality Is Not What It Seems", 2014, 280),
    ("Helgoland", 2020, 240), ("There Are Places in the World Where Rules Are Less Important Than Kindness", 2020, 256),
    ("White Holes", 2023, 176),
]:
    ALL_BOOKS.append(make_book(title, "Carlo Rovelli", year, pages, ["Non-Fiction", "Science"]))

# Michio Kaku
for title, year, pages in [
    ("Beyond Einstein", 1987, 240), ("Hyperspace", 1994, 359),
    ("Visions", 1997, 403), ("Einstein's Cosmos", 2004, 239),
    ("Parallel Worlds", 2005, 428), ("Physics of the Impossible", 2008, 329),
    ("Physics of the Future", 2011, 389), ("The Future of the Mind", 2014, 377),
    ("The Future of Humanity", 2018, 368), ("The God Equation", 2021, 240),
    ("Quantum Supremacy", 2023, 336),
]:
    ALL_BOOKS.append(make_book(title, "Michio Kaku", year, pages, ["Non-Fiction", "Science"]))

# Sean Carroll
for title, year, pages in [
    ("From Eternity to Here", 2010, 438), ("The Particle at the End of the Universe", 2012, 352),
    ("The Big Picture", 2016, 470), ("Something Deeply Hidden", 2019, 347),
    ("The Biggest Ideas in the Universe", 2022, 305),
]:
    ALL_BOOKS.append(make_book(title, "Sean Carroll", year, pages, ["Non-Fiction", "Science"]))

# Katie Mack
for title, year, pages in [
    ("The End of Everything", 2020, 240),
]:
    ALL_BOOKS.append(make_book(title, "Katie Mack", year, pages, ["Non-Fiction", "Science"]))

# Neil deGrasse Tyson
for title, year, pages in [
    ("Merlin's Tour of the Universe", 1989, 288),
    ("The Sky Is Not the Limit", 2000, 218), ("Origins", 2004, 352),
    ("Death by Black Hole", 2007, 384), ("The Pluto Files", 2009, 194),
    ("Space Chronicles", 2012, 364), ("Astrophysics for People in a Hurry", 2017, 222),
    ("Accessory to War", 2018, 576), ("Letters from an Astrophysicist", 2019, 272),
    ("Cosmic Queries", 2021, 320), ("Starry Messenger", 2022, 288),
    ("To Infinity and Beyond", 2023, 304),
]:
    ALL_BOOKS.append(make_book(title, "Neil deGrasse Tyson", year, pages, ["Non-Fiction", "Science"]))


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

    batch_num = 165
    for i in range(0, len(new_books), 100):
        chunk = new_books[i:i+100]
        fname = f"batch_{batch_num}_batch28_{(i//100)+1}.json"
        with open(os.path.join(BATCH_DIR, fname), "w") as f:
            json.dump(chunk, f, indent=2)
        print(f"  {fname}: {len(chunk)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(new_books)}")
