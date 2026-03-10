#!/usr/bin/env python3
"""Generate a very large batch of books using author-centric generation.

Each author gets their complete/near-complete bibliography.
This is more efficient than genre-based generation for hitting 10K.

Run: python data/generate_seed_batch5.py
"""

import hashlib
import json
from pathlib import Path


def make_isbn13(title: str, author: str) -> str:
    h = hashlib.md5(f"{title}|{author}".encode()).hexdigest()
    digits = "978" + "".join(str(int(c, 16) % 10) for c in h[:9])
    total = 0
    for i, d in enumerate(digits):
        total += int(d) * (1 if i % 2 == 0 else 3)
    check = (10 - (total % 10)) % 10
    return digits + str(check)


def make_isbn10(isbn13: str) -> str:
    digits = isbn13[3:12]
    total = sum(int(d) * (10 - i) for i, d in enumerate(digits))
    check = (11 - (total % 11)) % 11
    return digits + ("X" if check == 10 else str(check))


def make_book(title, authors, year=None, genres=None, lang="en", pages=None):
    if isinstance(authors, str):
        authors = [authors]
    isbn13 = make_isbn13(title, authors[0])
    isbn10 = make_isbn10(isbn13)
    book = {
        "title": title, "authors": authors, "isbn_13": isbn13, "isbn_10": isbn10,
        "genres": genres or [], "language": lang, "source": "seed",
    }
    if year: book["year_published"] = year
    if pages: book["page_count"] = pages
    return book


# Format: (author, lang, default_genres, [(title, year, pages, extra_genres), ...])
# extra_genres override default_genres if provided

AUTHORS = [
    # ─── AGATHA CHRISTIE (complete detective novels) ─────────────────
    ("Agatha Christie", "en", ["Mystery"], [
        ("The Secret Adversary", 1922, 282, None),
        ("The Man in the Brown Suit", 1924, 312, None),
        ("The Secret of Chimneys", 1925, 290, None),
        ("The Murder at the Vicarage", 1930, 288, None),
        ("The Thirteen Problems", 1932, 288, ["Mystery", "Short Stories"]),
        ("Why Didn't They Ask Evans?", 1934, 256, None),
        ("Three Act Tragedy", 1935, 256, None),
        ("Cards on the Table", 1936, 240, None),
        ("Dumb Witness", 1937, 320, None),
        ("Appointment with Death", 1938, 256, None),
        ("Hercule Poirot's Christmas", 1938, 256, None),
        ("Sad Cypress", 1940, 224, None),
        ("One, Two, Buckle My Shoe", 1940, 256, None),
        ("N or M?", 1941, 224, None),
        ("The Body in the Library", 1942, 218, None),
        ("Death Comes as the End", 1944, 223, None),
        ("Sparkling Cyanide", 1945, 227, None),
        ("The Hollow", 1946, 290, None),
        ("Taken at the Flood", 1948, 240, None),
        ("They Came to Baghdad", 1951, 224, None),
        ("Mrs McGinty's Dead", 1952, 243, None),
        ("They Do It with Mirrors", 1952, 199, None),
        ("A Pocket Full of Rye", 1953, 222, None),
        ("Destination Unknown", 1954, 192, None),
        ("Hickory Dickory Dock", 1955, 248, None),
        ("Dead Man's Folly", 1956, 256, None),
        ("Cat Among the Pigeons", 1959, 224, None),
        ("The Pale Horse", 1961, 256, None),
        ("The Mirror Crack'd from Side to Side", 1962, 256, None),
        ("The Clocks", 1963, 256, None),
        ("A Caribbean Mystery", 1964, 256, None),
        ("At Bertram's Hotel", 1965, 272, None),
        ("Third Girl", 1966, 256, None),
        ("Endless Night", 1967, 224, None),
        ("By the Pricking of My Thumbs", 1968, 268, None),
        ("Hallowe'en Party", 1969, 248, None),
        ("Passenger to Frankfurt", 1970, 272, None),
        ("Nemesis", 1971, 256, None),
        ("Elephants Can Remember", 1972, 256, None),
        ("Postern of Fate", 1973, 256, None),
        ("Sleeping Murder", 1976, 224, None),
    ]),

    # ─── ISAAC ASIMOV ────────────────────────────────────────────────
    ("Isaac Asimov", "en", ["Science Fiction"], [
        ("Foundation", 1951, 244, None),
        ("Foundation and Empire", 1952, 247, None),
        ("Second Foundation", 1953, 210, None),
        ("Foundation's Edge", 1982, 367, None),
        ("Foundation and Earth", 1986, 356, None),
        ("Prelude to Foundation", 1988, 403, None),
        ("Forward the Foundation", 1993, 415, None),
        ("I, Robot", 1950, 253, ["Science Fiction", "Short Stories"]),
        ("The Caves of Steel", 1954, 224, None),
        ("The Naked Sun", 1957, 187, None),
        ("The Robots of Dawn", 1983, 435, None),
        ("Robots and Empire", 1985, 383, None),
        ("The End of Eternity", 1955, 191, None),
        ("Pebble in the Sky", 1950, 223, None),
        ("The Stars, Like Dust", 1951, 218, None),
        ("The Currents of Space", 1952, 217, None),
        ("The Gods Themselves", 1972, 288, None),
        ("Nightfall", 1990, 339, None),
        ("The Bicentennial Man", 1976, 211, ["Science Fiction", "Short Stories"]),
        ("Nemesis", 1989, 364, None),
    ]),

    # ─── PHILIP K. DICK ─────────────────────────────────────────────
    ("Philip K. Dick", "en", ["Science Fiction"], [
        ("Do Androids Dream of Electric Sheep?", 1968, 210, None),
        ("The Man in the High Castle", 1962, 239, None),
        ("A Scanner Darkly", 1977, 220, None),
        ("Ubik", 1969, 202, None),
        ("VALIS", 1981, 227, None),
        ("The Three Stigmata of Palmer Eldritch", 1965, 230, None),
        ("Flow My Tears, the Policeman Said", 1974, 204, None),
        ("Time Out of Joint", 1959, 224, None),
        ("Martian Time-Slip", 1964, 220, None),
        ("The Simulacra", 1964, 192, None),
        ("Dr. Bloodmoney", 1965, 256, None),
        ("Now Wait for Last Year", 1966, 214, None),
        ("Galactic Pot-Healer", 1969, 143, None),
        ("Our Friends from Frolix 8", 1970, 190, None),
        ("We Can Build You", 1972, 243, None),
        ("A Maze of Death", 1970, 192, None),
        ("Clans of the Alphane Moon", 1964, 253, None),
        ("The Penultimate Truth", 1964, 174, None),
        ("The World Jones Made", 1956, 199, None),
        ("Eye in the Sky", 1957, 254, None),
        ("Solar Lottery", 1955, 188, None),
        ("The Cosmic Puppets", 1957, 128, None),
        ("Counter-Clock World", 1967, 160, None),
        ("The Divine Invasion", 1981, 239, None),
        ("The Transmigration of Timothy Archer", 1982, 256, None),
        ("Radio Free Albemuth", 1985, 224, None),
    ]),

    # ─── URSULA K. LE GUIN ──────────────────────────────────────────
    ("Ursula K. Le Guin", "en", ["Science Fiction", "Fantasy"], [
        ("A Wizard of Earthsea", 1968, 183, ["Fantasy"]),
        ("The Tombs of Atuan", 1970, 163, ["Fantasy"]),
        ("The Farthest Shore", 1972, 197, ["Fantasy"]),
        ("Tehanu", 1990, 226, ["Fantasy"]),
        ("Tales from Earthsea", 2001, 280, ["Fantasy", "Short Stories"]),
        ("The Other Wind", 2001, 211, ["Fantasy"]),
        ("The Left Hand of Darkness", 1969, 286, ["Science Fiction"]),
        ("The Dispossessed", 1974, 387, ["Science Fiction"]),
        ("The Lathe of Heaven", 1971, 184, ["Science Fiction"]),
        ("The Word for World Is Forest", 1972, 189, ["Science Fiction"]),
        ("The Telling", 2000, 264, ["Science Fiction"]),
        ("Always Coming Home", 1985, 525, ["Science Fiction"]),
        ("The Beginning Place", 1980, 183, ["Fantasy"]),
        ("Malafrena", 1979, 369, ["Literary Fiction", "Historical Fiction"]),
        ("Changing Planes", 2003, 246, ["Science Fiction", "Short Stories"]),
        ("The Birthday of the World", 2002, 362, ["Science Fiction", "Short Stories"]),
        ("Four Ways to Forgiveness", 1995, 228, ["Science Fiction"]),
        ("The Wind's Twelve Quarters", 1975, 303, ["Science Fiction", "Short Stories"]),
        ("Orsinian Tales", 1976, 179, ["Literary Fiction", "Short Stories"]),
        ("Searoad", 1991, 193, ["Literary Fiction", "Short Stories"]),
        ("Lavinia", 2008, 280, ["Literary Fiction", "Historical Fiction"]),
    ]),

    # ─── TERRY PRATCHETT (Discworld) ─────────────────────────────────
    ("Terry Pratchett", "en", ["Fantasy", "Humor"], [
        ("The Colour of Magic", 1983, 288, None),
        ("The Light Fantastic", 1986, 241, None),
        ("Equal Rites", 1987, 282, None),
        ("Mort", 1987, 272, None),
        ("Sourcery", 1988, 260, None),
        ("Wyrd Sisters", 1988, 331, None),
        ("Pyramids", 1989, 358, None),
        ("Guards! Guards!", 1989, 354, None),
        ("Eric", 1990, 155, None),
        ("Moving Pictures", 1990, 393, None),
        ("Reaper Man", 1991, 285, None),
        ("Witches Abroad", 1991, 293, None),
        ("Small Gods", 1992, 347, None),
        ("Lords and Ladies", 1992, 282, None),
        ("Men at Arms", 1993, 357, None),
        ("Soul Music", 1994, 373, None),
        ("Interesting Times", 1994, 344, None),
        ("Maskerade", 1995, 360, None),
        ("Feet of Clay", 1996, 357, None),
        ("Hogfather", 1996, 354, None),
        ("Jingo", 1997, 380, None),
        ("The Last Continent", 1998, 354, None),
        ("Carpe Jugulum", 1998, 378, None),
        ("The Fifth Elephant", 1999, 383, None),
        ("The Truth", 2000, 324, None),
        ("Thief of Time", 2001, 324, None),
        ("The Last Hero", 2001, 176, None),
        ("The Amazing Maurice and His Educated Rodents", 2001, 272, ["Fantasy", "Children's"]),
        ("Night Watch", 2002, 338, None),
        ("The Wee Free Men", 2003, 271, ["Fantasy", "Children's"]),
        ("Monstrous Regiment", 2003, 353, None),
        ("A Hat Full of Sky", 2004, 279, ["Fantasy", "Children's"]),
        ("Going Postal", 2004, 361, None),
        ("Thud!", 2005, 358, None),
        ("Wintersmith", 2006, 323, ["Fantasy", "Children's"]),
        ("Making Money", 2007, 394, None),
        ("Unseen Academicals", 2009, 400, None),
        ("I Shall Wear Midnight", 2010, 355, ["Fantasy", "Children's"]),
        ("Snuff", 2011, 378, None),
        ("Raising Steam", 2013, 361, None),
        ("The Shepherd's Crown", 2015, 304, None),
        ("Good Omens", 1990, 288, ["Fantasy", "Humor"]),
    ]),

    # ─── JAMES PATTERSON ─────────────────────────────────────────────
    ("James Patterson", "en", ["Thriller"], [
        ("Along Came a Spider", 1993, 435, ["Thriller", "Mystery"]),
        ("Kiss the Girls", 1995, 451, ["Thriller", "Mystery"]),
        ("Jack & Jill", 1996, 432, ["Thriller", "Mystery"]),
        ("Cat & Mouse", 1997, 399, ["Thriller", "Mystery"]),
        ("Pop Goes the Weasel", 1999, 424, ["Thriller", "Mystery"]),
        ("Roses Are Red", 2000, 400, ["Thriller", "Mystery"]),
        ("Violets Are Blue", 2001, 392, ["Thriller", "Mystery"]),
        ("Four Blind Mice", 2002, 358, ["Thriller", "Mystery"]),
        ("The Big Bad Wolf", 2003, 399, ["Thriller", "Mystery"]),
        ("London Bridges", 2004, 391, ["Thriller", "Mystery"]),
        ("Mary, Mary", 2005, 388, ["Thriller", "Mystery"]),
        ("Cross", 2006, 393, ["Thriller", "Mystery"]),
        ("Double Cross", 2007, 373, ["Thriller", "Mystery"]),
        ("Cross Country", 2008, 416, ["Thriller", "Mystery"]),
        ("Alex Cross's Trial", 2009, 371, ["Thriller", "Mystery"]),
        ("I, Alex Cross", 2009, 374, ["Thriller", "Mystery"]),
        ("Cross Fire", 2010, 371, ["Thriller", "Mystery"]),
        ("Kill Alex Cross", 2011, 371, ["Thriller", "Mystery"]),
        ("Merry Christmas, Alex Cross", 2012, 292, ["Thriller", "Mystery"]),
        ("Cross My Heart", 2013, 384, ["Thriller", "Mystery"]),
        ("Hope to Die", 2014, 373, ["Thriller", "Mystery"]),
        ("Cross Justice", 2015, 384, ["Thriller", "Mystery"]),
        ("Cross the Line", 2016, 400, ["Thriller", "Mystery"]),
        ("The People vs. Alex Cross", 2017, 384, ["Thriller", "Mystery"]),
        ("Target: Alex Cross", 2018, 368, ["Thriller", "Mystery"]),
        ("1st to Die", 2001, 361, ["Thriller", "Mystery"]),
        ("2nd Chance", 2002, 400, ["Thriller", "Mystery"]),
        ("3rd Degree", 2004, 346, ["Thriller", "Mystery"]),
        ("4th of July", 2005, 357, ["Thriller", "Mystery"]),
        ("The 5th Horseman", 2006, 360, ["Thriller", "Mystery"]),
        ("The 6th Target", 2007, 388, ["Thriller", "Mystery"]),
        ("7th Heaven", 2008, 368, ["Thriller", "Mystery"]),
        ("The 8th Confession", 2009, 371, ["Thriller", "Mystery"]),
        ("The 9th Judgment", 2010, 304, ["Thriller", "Mystery"]),
        ("10th Anniversary", 2011, 368, ["Thriller", "Mystery"]),
        ("11th Hour", 2012, 372, ["Thriller", "Mystery"]),
        ("12th of Never", 2013, 368, ["Thriller", "Mystery"]),
        ("Maximum Ride: The Angel Experiment", 2005, 422, ["Thriller", "Young Adult", "Science Fiction"]),
    ]),

    # ─── DANIELLE STEEL ──────────────────────────────────────────────
    ("Danielle Steel", "en", ["Romance"], [
        ("Going Home", 1973, 208, None),
        ("The Promise", 1978, 328, None),
        ("Season of Passion", 1979, 416, None),
        ("Summer's End", 1979, 255, None),
        ("The Ring", 1980, 464, None),
        ("Palomino", 1981, 384, None),
        ("Remembrance", 1981, 404, None),
        ("Crossings", 1982, 405, None),
        ("Once in a Lifetime", 1982, 384, None),
        ("Changes", 1983, 404, None),
        ("Full Circle", 1984, 416, None),
        ("Family Album", 1985, 448, None),
        ("Secrets", 1985, 384, None),
        ("Wanderlust", 1986, 464, None),
        ("Fine Things", 1987, 384, None),
        ("Kaleidoscope", 1987, 480, None),
        ("Zoya", 1988, 448, ["Romance", "Historical Fiction"]),
        ("Daddy", 1989, 384, None),
        ("Message from Nam", 1990, 448, ["Romance", "War Fiction"]),
        ("Heartbeat", 1991, 384, None),
        ("No Greater Love", 1991, 384, ["Romance", "Historical Fiction"]),
        ("Jewels", 1992, 480, ["Romance", "Historical Fiction"]),
        ("Mixed Blessings", 1992, 384, None),
        ("Vanished", 1993, 384, None),
        ("Accident", 1994, 320, None),
        ("The Gift", 1994, 288, None),
        ("Wings", 1994, 416, ["Romance", "Historical Fiction"]),
        ("Lightning", 1995, 384, None),
        ("Five Days in Paris", 1995, 284, None),
        ("Malice", 1996, 310, None),
        ("Silent Honor", 1996, 384, ["Romance", "Historical Fiction"]),
        ("The Ranch", 1997, 320, None),
        ("Special Delivery", 1997, 288, None),
        ("The Ghost", 1997, 384, None),
        ("The Long Road Home", 1998, 384, None),
        ("Mirror Image", 1998, 316, None),
        ("Bittersweet", 1999, 384, None),
        ("Granny Dan", 1999, 224, None),
        ("Irresistible Forces", 1999, 304, None),
        ("The Wedding", 2000, 326, None),
        ("The House on Hope Street", 2000, 260, None),
        ("Leap of Faith", 2001, 288, None),
        ("The Kiss", 2001, 288, None),
        ("Lone Eagle", 2001, 400, ["Romance", "Historical Fiction"]),
        ("The Cottage", 2002, 384, None),
        ("Sunset in St. Tropez", 2002, 224, None),
        ("Answered Prayers", 2002, 288, None),
        ("Dating Game", 2003, 288, None),
        ("Johnny Angel", 2003, 194, None),
        ("Safe Harbour", 2003, 336, None),
    ]),

    # ─── P.G. WODEHOUSE ──────────────────────────────────────────────
    ("P.G. Wodehouse", "en", ["Humor", "Classics"], [
        ("The Inimitable Jeeves", 1923, 233, None),
        ("Carry On, Jeeves", 1925, 287, None),
        ("Very Good, Jeeves", 1930, 288, None),
        ("Thank You, Jeeves", 1934, 256, None),
        ("Right Ho, Jeeves", 1934, 304, None),
        ("The Code of the Woosters", 1938, 304, None),
        ("Joy in the Morning", 1946, 272, None),
        ("The Mating Season", 1949, 272, None),
        ("Ring for Jeeves", 1953, 216, None),
        ("Jeeves and the Feudal Spirit", 1954, 256, None),
        ("Jeeves in the Offing", 1960, 224, None),
        ("Stiff Upper Lip, Jeeves", 1963, 224, None),
        ("Much Obliged, Jeeves", 1971, 192, None),
        ("Aunts Aren't Gentlemen", 1974, 192, None),
        ("Leave It to Psmith", 1923, 256, None),
        ("Something Fresh", 1915, 320, None),
        ("Summer Lightning", 1929, 288, None),
        ("Heavy Weather", 1933, 288, None),
        ("Uncle Fred in the Springtime", 1939, 256, None),
        ("Full Moon", 1947, 252, None),
        ("Pigs Have Wings", 1952, 224, None),
        ("Galahad at Blandings", 1965, 224, None),
        ("A Pelican at Blandings", 1969, 223, None),
        ("Sunset at Blandings", 1977, 192, None),
        ("The Luck of the Bodkins", 1935, 306, None),
        ("Laughing Gas", 1936, 256, None),
        ("Piccadilly Jim", 1917, 320, None),
        ("A Damsel in Distress", 1919, 284, None),
        ("The Girl on the Boat", 1922, 256, None),
        ("Bill the Conqueror", 1924, 288, None),
    ]),

    # ─── GABRIEL GARCÍA MÁRQUEZ ──────────────────────────────────────
    ("Gabriel García Márquez", "es", ["Literary Fiction", "Magical Realism"], [
        ("In Evil Hour", 1962, 183, None),
        ("Big Mama's Funeral", 1962, 146, ["Literary Fiction", "Short Stories"]),
        ("Eyes of a Blue Dog", 1947, 170, ["Literary Fiction", "Short Stories"]),
        ("The Story of a Shipwrecked Sailor", 1970, 106, None),
        ("Innocent Eréndira", 1972, 183, ["Literary Fiction", "Short Stories"]),
        ("The Autumn of the Patriarch", 1975, 269, None),
        ("News of a Kidnapping", 1996, 291, ["Non-Fiction"]),
        ("Living to Tell the Tale", 2002, 483, ["Memoir"]),
        ("Memories of My Melancholy Whores", 2004, 115, None),
        ("Until August", 2024, 144, None),
    ]),

    # ─── HARUKI MURAKAMI ─────────────────────────────────────────────
    ("Haruki Murakami", "ja", ["Literary Fiction"], [
        ("Hear the Wind Sing", 1979, 130, None),
        ("Pinball, 1973", 1980, 166, None),
        ("A Wild Sheep Chase", 1982, 299, None),
        ("Hard-Boiled Wonderland and the End of the World", 1985, 400, ["Literary Fiction", "Science Fiction"]),
        ("Dance Dance Dance", 1988, 393, None),
        ("South of the Border, West of the Sun", 1992, 213, None),
        ("The Wind-Up Bird Chronicle", 1994, 607, None),
        ("Sputnik Sweetheart", 1999, 229, None),
        ("Kafka on the Shore", 2002, 467, ["Literary Fiction", "Fantasy"]),
        ("After Dark", 2004, 191, None),
        ("1Q84", 2009, 925, None),
        ("Colorless Tsukuru Tazaki and His Years of Pilgrimage", 2013, 386, None),
        ("Killing Commendatore", 2017, 681, None),
        ("The City and Its Uncertain Walls", 2023, 464, None),
        ("Norwegian Wood", 1987, 296, None),
        ("What I Talk About When I Talk About Running", 2007, 180, ["Memoir"]),
        ("Underground", 1997, 309, ["Non-Fiction"]),
        ("Men Without Women", 2014, 228, ["Literary Fiction", "Short Stories"]),
        ("First Person Singular", 2020, 241, ["Literary Fiction", "Short Stories"]),
        ("Blind Willow, Sleeping Woman", 2006, 333, ["Literary Fiction", "Short Stories"]),
        ("After the Quake", 2000, 181, ["Literary Fiction", "Short Stories"]),
        ("The Elephant Vanishes", 1993, 327, ["Literary Fiction", "Short Stories"]),
    ]),

    # ─── MICHAEL CRICHTON ────────────────────────────────────────────
    ("Michael Crichton", "en", ["Thriller", "Science Fiction"], [
        ("The Andromeda Strain", 1969, 295, None),
        ("The Terminal Man", 1972, 247, None),
        ("The Great Train Robbery", 1975, 266, ["Thriller", "Historical Fiction"]),
        ("Eaters of the Dead", 1976, 193, None),
        ("Congo", 1980, 348, None),
        ("Sphere", 1987, 385, None),
        ("Jurassic Park", 1990, 399, None),
        ("The Lost World", 1995, 393, None),
        ("Rising Sun", 1992, 355, ["Thriller"]),
        ("Disclosure", 1994, 597, ["Thriller"]),
        ("Airframe", 1996, 352, ["Thriller"]),
        ("Timeline", 1999, 449, ["Thriller", "Science Fiction", "Historical Fiction"]),
        ("Prey", 2002, 370, None),
        ("State of Fear", 2004, 603, None),
        ("Next", 2006, 431, None),
        ("Pirate Latitudes", 2009, 312, ["Adventure", "Historical Fiction"]),
        ("Micro", 2011, 424, None),
        ("Dragon Teeth", 2017, 295, ["Adventure", "Historical Fiction"]),
    ]),

    # ─── ARTHUR C. CLARKE ────────────────────────────────────────────
    ("Arthur C. Clarke", "en", ["Science Fiction"], [
        ("Childhood's End", 1953, 224, None),
        ("The City and the Stars", 1956, 256, None),
        ("2001: A Space Odyssey", 1968, 221, None),
        ("2010: Odyssey Two", 1982, 291, None),
        ("2061: Odyssey Three", 1987, 256, None),
        ("3001: The Final Odyssey", 1997, 263, None),
        ("Rendezvous with Rama", 1973, 243, None),
        ("Rama II", 1989, 466, None),
        ("The Garden of Rama", 1991, 440, None),
        ("Rama Revealed", 1993, 512, None),
        ("The Fountains of Paradise", 1979, 255, None),
        ("Imperial Earth", 1975, 305, None),
        ("The Songs of Distant Earth", 1986, 256, None),
        ("A Fall of Moondust", 1961, 224, None),
        ("Earthlight", 1955, 186, None),
        ("The Deep Range", 1957, 238, None),
        ("Prelude to Space", 1951, 161, None),
        ("The Sands of Mars", 1951, 215, None),
        ("Islands in the Sky", 1952, 198, None),
        ("Against the Fall of Night", 1953, 160, None),
        ("Glide Path", 1963, 256, None),
        ("The Ghost from the Grand Banks", 1990, 255, None),
        ("The Hammer of God", 1993, 226, None),
        ("The Light of Other Days", 2000, 318, None),
        ("The Last Theorem", 2008, 299, None),
    ]),

    # ─── DEAN KOONTZ ────────────────────────────────────────────────
    ("Dean Koontz", "en", ["Thriller", "Horror"], [
        ("Phantoms", 1983, 352, None),
        ("Strangers", 1986, 681, None),
        ("Watchers", 1987, 451, None),
        ("Lightning", 1988, 351, None),
        ("Midnight", 1989, 470, None),
        ("The Bad Place", 1990, 382, None),
        ("Cold Fire", 1991, 363, None),
        ("Hideaway", 1992, 359, None),
        ("Dragon Tears", 1993, 377, None),
        ("Mr. Murder", 1993, 431, None),
        ("Dark Rivers of the Heart", 1994, 487, None),
        ("Intensity", 1995, 307, None),
        ("Sole Survivor", 1997, 368, None),
        ("Seize the Night", 1998, 401, None),
        ("Fear Nothing", 1998, 391, None),
        ("From the Corner of His Eye", 2000, 738, None),
        ("One Door Away from Heaven", 2001, 681, None),
        ("By the Light of the Moon", 2002, 431, None),
        ("Odd Thomas", 2003, 390, None),
        ("The Taking", 2004, 338, None),
        ("Velocity", 2005, 400, None),
        ("The Husband", 2006, 400, None),
        ("The Good Guy", 2007, 390, None),
        ("The Darkest Evening of the Year", 2007, 353, None),
        ("Breathless", 2009, 326, None),
        ("Relentless", 2009, 356, None),
        ("What the Night Knows", 2010, 368, None),
        ("77 Shadow Street", 2011, 395, None),
        ("The City", 2014, 426, None),
        ("Ashley Bell", 2015, 528, None),
        ("The Silent Corner", 2017, 464, None),
        ("The Whispering Room", 2017, 416, None),
        ("The Crooked Staircase", 2018, 432, None),
        ("The Forbidden Door", 2018, 448, None),
        ("The Night Window", 2019, 496, None),
        ("Devoted", 2020, 384, None),
        ("Quicksilver", 2022, 384, None),
        ("The Big Dark Sky", 2022, 464, None),
        ("The House at the End of the World", 2023, 384, None),
        ("After Death", 2023, 352, None),
    ]),

    # ─── ROBIN COOK (Medical Thrillers) ──────────────────────────────
    ("Robin Cook", "en", ["Thriller", "Medical Thriller"], [
        ("Coma", 1977, 306, None),
        ("Brain", 1981, 278, None),
        ("Fever", 1982, 310, None),
        ("Godplayer", 1983, 340, None),
        ("Mindbend", 1985, 319, None),
        ("Outbreak", 1987, 372, None),
        ("Mortal Fear", 1988, 364, None),
        ("Mutation", 1989, 323, None),
        ("Harmful Intent", 1990, 369, None),
        ("Vital Signs", 1991, 396, None),
        ("Blindsight", 1992, 352, None),
        ("Terminal", 1993, 355, None),
        ("Acceptable Risk", 1994, 404, None),
        ("Contagion", 1996, 420, None),
        ("Chromosome 6", 1997, 468, None),
        ("Toxin", 1998, 384, None),
        ("Vector", 1999, 404, None),
        ("Abduction", 2000, 340, None),
        ("Shock", 2001, 372, None),
        ("Seizure", 2003, 418, None),
        ("Marker", 2005, 404, None),
        ("Crisis", 2006, 415, None),
        ("Critical", 2007, 404, None),
        ("Foreign Body", 2008, 404, None),
        ("Intervention", 2009, 384, None),
        ("Cure", 2010, 384, None),
        ("Death Benefit", 2011, 416, None),
        ("Nano", 2012, 420, None),
        ("Cell", 2014, 384, None),
        ("Host", 2015, 400, None),
        ("Charlatans", 2017, 384, None),
        ("Genesis", 2019, 384, None),
        ("Viral", 2021, 448, None),
        ("Night Shift", 2022, 384, None),
    ]),

    # ─── PATRICIA CORNWELL ───────────────────────────────────────────
    ("Patricia Cornwell", "en", ["Thriller", "Mystery", "Crime Fiction"], [
        ("Postmortem", 1990, 323, None),
        ("Body of Evidence", 1991, 387, None),
        ("All That Remains", 1992, 373, None),
        ("Cruel and Unusual", 1993, 372, None),
        ("The Body Farm", 1994, 371, None),
        ("From Potter's Field", 1995, 370, None),
        ("Cause of Death", 1996, 357, None),
        ("Unnatural Exposure", 1997, 339, None),
        ("Point of Origin", 1998, 370, None),
        ("Black Notice", 1999, 405, None),
        ("The Last Precinct", 2000, 427, None),
        ("Blow Fly", 2003, 478, None),
        ("Trace", 2004, 355, None),
        ("Predator", 2005, 370, None),
        ("Book of the Dead", 2007, 388, None),
        ("Scarpetta", 2008, 374, None),
        ("The Scarpetta Factor", 2009, 400, None),
        ("Port Mortuary", 2010, 336, None),
        ("Red Mist", 2011, 384, None),
        ("The Bone Bed", 2012, 394, None),
        ("Dust", 2013, 388, None),
        ("Flesh and Blood", 2014, 384, None),
        ("Depraved Heart", 2015, 435, None),
        ("Chaos", 2016, 422, None),
        ("Autopsy", 2021, 400, None),
        ("Livid", 2022, 384, None),
        ("Identity Unknown", 2023, 368, None),
        ("Unnatural Death", 2024, 384, None),
    ]),

    # ─── ALEXANDER McCALL SMITH ──────────────────────────────────────
    ("Alexander McCall Smith", "en", ["Mystery", "Literary Fiction"], [
        ("The No. 1 Ladies' Detective Agency", 1998, 235, None),
        ("Tears of the Giraffe", 2000, 227, None),
        ("Morality for Beautiful Girls", 2001, 227, None),
        ("The Kalahari Typing School for Men", 2002, 226, None),
        ("The Full Cupboard of Life", 2003, 211, None),
        ("In the Company of Cheerful Ladies", 2004, 233, None),
        ("Blue Shoes and Happiness", 2006, 227, None),
        ("The Good Husband of Zebra Drive", 2007, 213, None),
        ("The Miracle at Speedy Motors", 2008, 213, None),
        ("Tea Time for the Traditionally Built", 2009, 213, None),
        ("The Double Comfort Safari Club", 2010, 213, None),
        ("The Saturday Big Tent Wedding Party", 2011, 213, None),
        ("The Limpopo Academy of Private Detection", 2012, 211, None),
        ("The Minor Adjustment Beauty Salon", 2013, 256, None),
        ("The Handsome Man's De Luxe Café", 2014, 224, None),
        ("The Woman Who Walked in Sunshine", 2015, 240, None),
        ("Precious and Grace", 2016, 224, None),
        ("The House of Unexpected Sisters", 2017, 240, None),
        ("The Colors of All the Cattle", 2018, 244, None),
        ("To the Land of Long Lost Friends", 2019, 224, None),
        ("How to Raise an Elephant", 2020, 224, None),
        ("The Joy and Light Bus Company", 2021, 224, None),
        ("A Song of Comfortable Chairs", 2022, 240, None),
        ("From a Far and Lovely Country", 2023, 256, None),
        ("44 Scotland Street", 2005, 352, ["Literary Fiction"]),
        ("Espresso Tales", 2005, 369, ["Literary Fiction"]),
        ("Love Over Scotland", 2006, 357, ["Literary Fiction"]),
        ("The World According to Bertie", 2007, 290, ["Literary Fiction"]),
        ("The Unbearable Lightness of Scones", 2008, 288, ["Literary Fiction"]),
    ]),
]


def write_batch(batch_dir: Path, name: str, books: list):
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

    # Split into batches of ~100 for manageability
    batch_size = 100
    total = 0
    batch_num = 42
    for i in range(0, len(all_books), batch_size):
        chunk = all_books[i:i + batch_size]
        name = f"batch_{batch_num:02d}_authors_{batch_num - 41}"
        total += write_batch(batch_dir, name, chunk)
        batch_num += 1

    print(f"\nTotal new books: {total}")


if __name__ == "__main__":
    main()
