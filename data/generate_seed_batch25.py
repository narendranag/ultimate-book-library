#!/usr/bin/env python3
"""Batch 25: Massive expansion - underrepresented genres, fresh prolific authors."""
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

# === WESTERNS & ADVENTURE ===

# Zane Grey
for title, year, pages in [
    ("Riders of the Purple Sage", 1912, 334), ("The Last of the Plainsmen", 1908, 309),
    ("The Heritage of the Desert", 1910, 297), ("Desert Gold", 1913, 314),
    ("The Light of Western Stars", 1914, 348), ("The Lone Star Ranger", 1914, 352),
    ("The Rainbow Trail", 1915, 371), ("Wildfire", 1917, 308),
    ("The U.P. Trail", 1918, 408), ("The Man of the Forest", 1920, 347),
    ("The Mysterious Rider", 1921, 348), ("To the Last Man", 1921, 313),
    ("Wanderer of the Wasteland", 1923, 400), ("The Call of the Canyon", 1924, 289),
    ("The Thundering Herd", 1925, 320), ("Under the Tonto Rim", 1926, 319),
    ("Nevada", 1928, 338), ("Fighting Caravans", 1929, 368),
    ("Sunset Pass", 1931, 316), ("West of the Pecos", 1937, 314),
]:
    ALL_BOOKS.append(make_book(title, "Zane Grey", year, pages, ["Western", "Adventure"]))

# Max Brand (Frederick Faust)
for title, year, pages in [
    ("The Untamed", 1919, 323), ("Trailin'!", 1920, 302),
    ("The Night Horseman", 1920, 351), ("Alcatraz", 1923, 308),
    ("Destry Rides Again", 1930, 304), ("The Seventh Man", 1921, 300),
    ("Dan Barry's Daughter", 1924, 315), ("The Garden of Eden", 1922, 303),
    ("Fire Brain", 1926, 248), ("Hired Guns", 1948, 240),
    ("Riders of the Silences", 1920, 253), ("Bull Hunter", 1921, 279),
    ("The Long Chance", 1921, 313), ("Way of the Lawless", 1924, 256),
    ("Montana Rides Again", 1934, 253), ("Singing Guns", 1928, 303),
]:
    ALL_BOOKS.append(make_book(title, "Max Brand", year, pages, ["Western", "Adventure"]))

# Jack London
for title, year, pages in [
    ("The Call of the Wild", 1903, 232), ("The Sea-Wolf", 1904, 366),
    ("White Fang", 1906, 298), ("The Iron Heel", 1908, 354),
    ("Martin Eden", 1909, 411), ("Burning Daylight", 1910, 361),
    ("Adventure", 1911, 385), ("The Valley of the Moon", 1913, 530),
    ("The Star Rover", 1915, 329), ("The Mutiny of the Elsinore", 1914, 372),
    ("Jerry of the Islands", 1917, 341), ("Michael, Brother of Jerry", 1917, 346),
    ("South Sea Tales", 1911, 327), ("The People of the Abyss", 1903, 319),
]:
    ALL_BOOKS.append(make_book(title, "Jack London", year, pages, ["Adventure", "Literary Fiction"]))

# === CLASSIC DETECTIVE/MYSTERY ===

# Rex Stout - Nero Wolfe
for title, year, pages in [
    ("Fer-de-Lance", 1934, 318), ("The League of Frightened Men", 1935, 304),
    ("The Rubber Band", 1936, 297), ("The Red Box", 1937, 292),
    ("Too Many Cooks", 1938, 262), ("Some Buried Caesar", 1939, 270),
    ("Over My Dead Body", 1940, 275), ("Where There's a Will", 1940, 213),
    ("Black Orchids", 1942, 218), ("Not Quite Dead Enough", 1944, 160),
    ("The Silent Speaker", 1946, 309), ("Too Many Women", 1947, 246),
    ("And Be a Villain", 1948, 218), ("Trouble in Triplicate", 1949, 191),
    ("The Second Confession", 1949, 245), ("In the Best Families", 1950, 218),
    ("Murder by the Book", 1951, 188), ("Prisoner's Base", 1952, 189),
    ("The Golden Spiders", 1953, 186), ("The Black Mountain", 1954, 190),
    ("Before Midnight", 1955, 185), ("Might as Well Be Dead", 1956, 188),
    ("If Death Ever Slept", 1957, 186), ("Champagne for One", 1958, 186),
    ("Plot It Yourself", 1959, 186), ("Too Many Clients", 1960, 186),
    ("The Final Deduction", 1961, 186), ("Gambit", 1962, 186),
    ("The Mother Hunt", 1963, 185), ("A Right to Die", 1964, 182),
]:
    ALL_BOOKS.append(make_book(title, "Rex Stout", year, pages, ["Mystery", "Crime Fiction"]))

# Erle Stanley Gardner - Perry Mason
for title, year, pages in [
    ("The Case of the Velvet Claws", 1933, 279), ("The Case of the Sulky Girl", 1933, 256),
    ("The Case of the Lucky Legs", 1934, 283), ("The Case of the Howling Dog", 1934, 258),
    ("The Case of the Curious Bride", 1934, 267), ("The Case of the Counterfeit Eye", 1935, 256),
    ("The Case of the Caretaker's Cat", 1935, 290), ("The Case of the Sleepwalker's Niece", 1936, 268),
    ("The Case of the Stuttering Bishop", 1936, 262), ("The Case of the Dangerous Dowager", 1937, 279),
    ("The Case of the Lame Canary", 1937, 261), ("The Case of the Substitute Face", 1938, 270),
    ("The Case of the Shoplifter's Shoe", 1938, 259), ("The Case of the Perjured Parrot", 1939, 249),
    ("The Case of the Rolling Bones", 1939, 248), ("The Case of the Baited Hook", 1940, 256),
    ("The Case of the Silent Partner", 1940, 241), ("The Case of the Haunted Husband", 1941, 254),
    ("The Case of the Turning Tide", 1941, 225), ("The Case of the Buried Clock", 1943, 231),
    ("The Case of the Drowning Duck", 1942, 242), ("The Case of the Careless Kitten", 1942, 224),
    ("The Case of the Crooked Candle", 1944, 245), ("The Case of the Golddigger's Purse", 1945, 242),
    ("The Case of the Half-Wakened Wife", 1945, 224), ("The Case of the Borrowed Brunette", 1946, 233),
]:
    ALL_BOOKS.append(make_book(title, "Erle Stanley Gardner", year, pages, ["Mystery", "Crime Fiction"]))

# Ngaio Marsh
for title, year, pages in [
    ("A Man Lay Dead", 1934, 254), ("Enter a Murderer", 1935, 254),
    ("The Nursing Home Murder", 1935, 253), ("Death in Ecstasy", 1936, 284),
    ("Vintage Murder", 1937, 246), ("Artists in Crime", 1938, 316),
    ("Death in a White Tie", 1938, 287), ("Overture to Death", 1939, 289),
    ("Death at the Bar", 1940, 292), ("Death of a Peer", 1940, 264),
    ("Death and the Dancing Footman", 1942, 291), ("Colour Scheme", 1943, 310),
    ("Died in the Wool", 1945, 253), ("Final Curtain", 1947, 291),
    ("Swing, Brother, Swing", 1949, 286), ("Opening Night", 1951, 223),
    ("Spinsters in Jeopardy", 1953, 241), ("Scales of Justice", 1955, 248),
    ("Off with His Head", 1957, 254), ("Singing in the Shrouds", 1958, 265),
    ("False Scent", 1960, 261), ("Hand in Glove", 1962, 258),
    ("Dead Water", 1963, 254), ("Killer Dolphin", 1966, 286),
    ("Clutch of Constables", 1968, 255), ("When in Rome", 1970, 249),
    ("Tied Up in Tinsel", 1972, 303), ("Black as He's Painted", 1974, 266),
    ("Last Ditch", 1977, 281), ("Grave Mistake", 1978, 252),
    ("Photo Finish", 1980, 252), ("Light Thickens", 1982, 232),
]:
    ALL_BOOKS.append(make_book(title, "Ngaio Marsh", year, pages, ["Mystery", "Crime Fiction"]))

# Ellery Queen
for title, year, pages in [
    ("The Roman Hat Mystery", 1929, 325), ("The French Powder Mystery", 1930, 320),
    ("The Dutch Shoe Mystery", 1931, 282), ("The Greek Coffin Mystery", 1932, 335),
    ("The Egyptian Cross Mystery", 1932, 332), ("The American Gun Mystery", 1933, 303),
    ("The Siamese Twin Mystery", 1933, 303), ("The Chinese Orange Mystery", 1934, 309),
    ("The Spanish Cape Mystery", 1935, 295), ("Halfway House", 1936, 286),
    ("The Door Between", 1937, 247), ("The Devil to Pay", 1938, 275),
    ("The Four of Hearts", 1938, 295), ("The Dragon's Teeth", 1939, 283),
    ("Calamity Town", 1942, 275), ("There Was an Old Woman", 1943, 277),
    ("The Murderer Is a Fox", 1945, 225), ("Ten Days' Wonder", 1948, 276),
    ("Cat of Many Tails", 1949, 278), ("Double, Double", 1950, 224),
    ("The Origin of Evil", 1951, 255), ("The King Is Dead", 1952, 238),
    ("The Scarlet Letters", 1953, 213), ("The Glass Village", 1954, 255),
    ("Inspector Queen's Own Case", 1956, 224),
]:
    ALL_BOOKS.append(make_book(title, "Ellery Queen", year, pages, ["Mystery", "Crime Fiction"]))

# === SCIENCE FICTION EXPANSION ===

# Frederick Pohl
for title, year, pages in [
    ("The Space Merchants", 1953, 179), ("Slave Ship", 1957, 191),
    ("Drunkard's Walk", 1960, 156), ("A Plague of Pythons", 1965, 191),
    ("The Age of the Pussyfoot", 1969, 186), ("Gateway", 1977, 313),
    ("Man Plus", 1976, 215), ("JEM", 1979, 337),
    ("Beyond the Blue Event Horizon", 1980, 327), ("The Years of the City", 1984, 330),
    ("The Coming of the Quantum Cats", 1986, 294),
    ("Heechee Rendezvous", 1984, 311), ("The Annals of the Heechee", 1987, 389),
    ("Chernobyl", 1987, 355), ("The Gateway Trip", 1990, 252),
    ("Mining the Oort", 1992, 263), ("The Other End of Time", 1996, 345),
    ("The Siege of Eternity", 1997, 316), ("The Far Shore of Time", 1999, 345),
    ("The Boy Who Would Live Forever", 2004, 375), ("All the Lives He Led", 2011, 352),
]:
    ALL_BOOKS.append(make_book(title, "Frederik Pohl", year, pages, ["Science Fiction"]))

# Clifford D. Simak
for title, year, pages in [
    ("Cosmic Engineers", 1939, 224), ("City", 1952, 256),
    ("Ring Around the Sun", 1953, 243), ("Time and Again", 1951, 253),
    ("Way Station", 1963, 210), ("All Flesh Is Grass", 1965, 191),
    ("Why Call Them Back from Heaven?", 1967, 190),
    ("The Goblin Reservation", 1968, 192), ("The Werewolf Principle", 1967, 188),
    ("A Choice of Gods", 1972, 183), ("Cemetery World", 1973, 207),
    ("Shakespeare's Planet", 1976, 218), ("A Heritage of Stars", 1977, 217),
    ("Mastodonia", 1978, 280), ("Project Pope", 1981, 280),
    ("Special Deliverance", 1982, 300), ("Highway of Eternity", 1986, 279),
]:
    ALL_BOOKS.append(make_book(title, "Clifford D. Simak", year, pages, ["Science Fiction"]))

# Poul Anderson
for title, year, pages in [
    ("Brain Wave", 1954, 176), ("The Broken Sword", 1954, 240),
    ("The High Crusade", 1960, 192), ("Tau Zero", 1970, 190),
    ("The Boat of a Million Years", 1989, 470), ("The Fleet of Stars", 1997, 384),
    ("Harvest of Stars", 1993, 448), ("The Stars Are Also Fire", 1994, 416),
    ("Orion Shall Rise", 1983, 483), ("The Day of Their Return", 1973, 250),
    ("A Midsummer Tempest", 1974, 207), ("There Will Be Time", 1972, 191),
    ("Fire Time", 1974, 270), ("The Avatar", 1978, 300),
    ("The People of the Wind", 1973, 185), ("A Knight of Ghosts and Shadows", 1974, 256),
    ("The Game of Empire", 1985, 288), ("War of the Gods", 1997, 304),
    ("Genesis", 2000, 304), ("For Love and Glory", 2003, 336),
]:
    ALL_BOOKS.append(make_book(title, "Poul Anderson", year, pages, ["Science Fiction", "Fantasy"]))

# Jack Vance
for title, year, pages in [
    ("The Dying Earth", 1950, 176), ("Big Planet", 1957, 160),
    ("The Languages of Pao", 1958, 185), ("The Dragon Masters", 1962, 78),
    ("The Star King", 1964, 192), ("The Killing Machine", 1964, 192),
    ("The Palace of Love", 1967, 188), ("The Last Castle", 1967, 60),
    ("Emphyrio", 1969, 190), ("The Eyes of the Overworld", 1966, 222),
    ("The Anome", 1973, 208), ("The Brave Free Men", 1973, 184),
    ("The Asutra", 1973, 206), ("Showboat World", 1975, 218),
    ("Maske: Thaery", 1976, 206), ("The Face", 1979, 187),
    ("The Book of Dreams", 1981, 192), ("Lyonesse", 1983, 470),
    ("The Green Pearl", 1985, 440), ("Madouc", 1989, 412),
    ("Araminta Station", 1988, 450), ("Ecce and Old Earth", 1991, 358),
    ("Throy", 1992, 284), ("Night Lamp", 1996, 380),
    ("Ports of Call", 1998, 350), ("Lurulu", 2004, 318),
]:
    ALL_BOOKS.append(make_book(title, "Jack Vance", year, pages, ["Science Fiction", "Fantasy"]))

# Roger Zelazny
for title, year, pages in [
    ("This Immortal", 1966, 174), ("The Dream Master", 1966, 172),
    ("Lord of Light", 1967, 257), ("Isle of the Dead", 1969, 182),
    ("Creatures of Light and Darkness", 1969, 192), ("Damnation Alley", 1969, 157),
    ("Jack of Shadows", 1971, 207), ("Today We Choose Faces", 1973, 178),
    ("To Die in Italbar", 1973, 192), ("Doorways in the Sand", 1976, 181),
    ("Nine Princes in Amber", 1970, 175), ("The Guns of Avalon", 1972, 180),
    ("Sign of the Unicorn", 1975, 186), ("The Hand of Oberon", 1976, 181),
    ("The Courts of Chaos", 1978, 183), ("Trumps of Doom", 1985, 183),
    ("Blood of Amber", 1986, 215), ("Sign of Chaos", 1987, 214),
    ("Knight of Shadows", 1989, 251), ("Prince of Chaos", 1991, 225),
    ("Eye of Cat", 1982, 184), ("A Night in the Lonesome October", 1993, 280),
    ("Lord Demon", 1999, 320), ("Donnerjack", 1997, 503),
]:
    ALL_BOOKS.append(make_book(title, "Roger Zelazny", year, pages, ["Science Fiction", "Fantasy"]))

# Gene Wolfe
for title, year, pages in [
    ("Operation Ares", 1970, 222), ("The Fifth Head of Cerberus", 1972, 232),
    ("Peace", 1975, 260), ("The Devil in a Forest", 1976, 221),
    ("The Shadow of the Torturer", 1980, 303), ("The Claw of the Conciliator", 1981, 303),
    ("The Sword of the Lictor", 1982, 302), ("The Citadel of the Autarch", 1983, 317),
    ("Free Live Free", 1984, 399), ("Soldier of the Mist", 1986, 335),
    ("Soldier of Arete", 1989, 354), ("There Are Doors", 1988, 313),
    ("Castleview", 1990, 278), ("Nightside the Long Sun", 1993, 379),
    ("Lake of the Long Sun", 1994, 381), ("Caldé of the Long Sun", 1994, 381),
    ("Exodus from the Long Sun", 1996, 408), ("On Blue's Waters", 1999, 381),
    ("In Green's Jungles", 2000, 374), ("Return to the Whorl", 2001, 412),
    ("The Wizard Knight", 2004, 912), ("The Urth of the New Sun", 1987, 372),
    ("Pirate Freedom", 2007, 320), ("An Evil Guest", 2008, 302),
    ("The Sorcerer's House", 2010, 302), ("Home Fires", 2011, 304),
    ("The Land Across", 2013, 288), ("A Borrowed Man", 2015, 284),
]:
    ALL_BOOKS.append(make_book(title, "Gene Wolfe", year, pages, ["Science Fiction", "Fantasy"]))

# === LITERARY FICTION - MORE FRESH AUTHORS ===

# Toni Morrison (filling remaining)
for title, year, pages in [
    ("The Bluest Eye", 1970, 206), ("Sula", 1973, 174),
    ("Song of Solomon", 1977, 337), ("Tar Baby", 1981, 305),
    ("Beloved", 1987, 324), ("Jazz", 1992, 229),
    ("Paradise", 1997, 318), ("Love", 2003, 202),
    ("A Mercy", 2008, 167), ("Home", 2012, 147),
    ("God Help the Child", 2015, 178),
]:
    ALL_BOOKS.append(make_book(title, "Toni Morrison", year, pages, ["Literary Fiction"]))

# Don DeLillo (filling remaining)
for title, year, pages in [
    ("Americana", 1971, 377), ("End Zone", 1972, 242),
    ("Great Jones Street", 1973, 265), ("Ratner's Star", 1976, 438),
    ("Players", 1977, 212), ("Running Dog", 1978, 243),
    ("The Names", 1982, 339), ("White Noise", 1985, 326),
    ("Libra", 1988, 456), ("Mao II", 1991, 241),
    ("Underworld", 1997, 827), ("The Body Artist", 2001, 124),
    ("Cosmopolis", 2003, 209), ("Falling Man", 2007, 246),
    ("Point Omega", 2010, 117), ("Zero K", 2016, 274),
    ("The Silence", 2020, 116),
]:
    ALL_BOOKS.append(make_book(title, "Don DeLillo", year, pages, ["Literary Fiction"]))

# Anne Tyler
for title, year, pages in [
    ("If Morning Ever Comes", 1964, 265), ("The Tin Can Tree", 1965, 273),
    ("A Slipping-Down Life", 1970, 214), ("The Clock Winder", 1972, 312),
    ("Celestial Navigation", 1974, 273), ("Searching for Caleb", 1976, 309),
    ("Earthly Possessions", 1977, 197), ("Morgan's Passing", 1980, 311),
    ("Dinner at the Homesick Restaurant", 1982, 303),
    ("The Accidental Tourist", 1985, 355), ("Breathing Lessons", 1988, 327),
    ("Saint Maybe", 1991, 337), ("Ladder of Years", 1995, 325),
    ("A Patchwork Planet", 1998, 287), ("Back When We Were Grownups", 2001, 273),
    ("The Amateur Marriage", 2004, 306), ("Digging to America", 2006, 277),
    ("Noah's Compass", 2009, 277), ("The Beginner's Goodbye", 2012, 197),
    ("A Spool of Blue Thread", 2015, 358), ("Clock Dance", 2018, 295),
    ("Redhead by the Side of the Road", 2020, 178),
    ("French Braid", 2022, 258),
]:
    ALL_BOOKS.append(make_book(title, "Anne Tyler", year, pages, ["Literary Fiction"]))

# John Banville
for title, year, pages in [
    ("Long Lankin", 1970, 208), ("Nightspawn", 1971, 238),
    ("Birchwood", 1973, 174), ("Doctor Copernicus", 1976, 246),
    ("Kepler", 1981, 192), ("The Newton Letter", 1982, 82),
    ("Mefisto", 1986, 234), ("The Book of Evidence", 1989, 220),
    ("Ghosts", 1993, 246), ("Athena", 1995, 233),
    ("The Untouchable", 1997, 405), ("Eclipse", 2000, 213),
    ("Shroud", 2002, 368), ("The Sea", 2005, 195),
    ("The Infinities", 2009, 273), ("Ancient Light", 2012, 304),
    ("The Blue Guitar", 2015, 256), ("Mrs. Osmond", 2017, 288),
    ("Snow", 2020, 256), ("The Singularities", 2022, 304),
]:
    ALL_BOOKS.append(make_book(title, "John Banville", year, pages, ["Literary Fiction"]))

# William Trevor
for title, year, pages in [
    ("A Standard of Behaviour", 1958, 224), ("The Old Boys", 1964, 255),
    ("The Boarding-House", 1965, 256), ("Mrs Eckdorf in O'Neill's Hotel", 1969, 274),
    ("Miss Gomez and the Brethren", 1971, 310), ("Elizabeth Alone", 1973, 288),
    ("The Children of Dynmouth", 1976, 209), ("Other People's Worlds", 1980, 254),
    ("Fools of Fortune", 1983, 238), ("Nights at the Alexandra", 1987, 128),
    ("The Silence in the Garden", 1988, 204), ("Two Lives", 1991, 379),
    ("Felicia's Journey", 1994, 213), ("Death in Summer", 1998, 214),
    ("The Story of Lucy Gault", 2002, 227), ("Love and Summer", 2009, 211),
    ("The Collected Stories", 1992, 1261),
]:
    ALL_BOOKS.append(make_book(title, "William Trevor", year, pages, ["Literary Fiction"]))

# Anita Brookner
for title, year, pages in [
    ("A Start in Life", 1981, 176), ("Providence", 1982, 184),
    ("Look at Me", 1983, 192), ("Hotel du Lac", 1984, 184),
    ("Family and Friends", 1985, 187), ("A Misalliance", 1986, 188),
    ("A Friend from England", 1987, 175), ("Latecomers", 1988, 248),
    ("Lewis Percy", 1989, 261), ("Brief Lives", 1990, 260),
    ("A Closed Eye", 1991, 228), ("Fraud", 1992, 262),
    ("A Family Romance", 1993, 218), ("A Private View", 1994, 218),
    ("Incidents in the Rue Laugier", 1995, 224), ("Altered States", 1996, 233),
    ("Visitors", 1997, 219), ("Falling Slowly", 1998, 234),
    ("Undue Influence", 1999, 226), ("The Bay of Angels", 2001, 208),
    ("The Next Big Thing", 2002, 230), ("The Rules of Engagement", 2003, 247),
    ("Leaving Home", 2005, 212), ("Strangers", 2009, 229),
]:
    ALL_BOOKS.append(make_book(title, "Anita Brookner", year, pages, ["Literary Fiction"]))

# === PHILOSOPHY & ESSAYS ===

# Montaigne
for title, year, pages in [
    ("The Complete Essays", 1580, 1283),
]:
    ALL_BOOKS.append(make_book(title, "Michel de Montaigne", year, pages, ["Philosophy", "Classic"], "fr"))

# Bertrand Russell
for title, year, pages in [
    ("The Problems of Philosophy", 1912, 167),
    ("Mysticism and Logic", 1918, 234), ("The Analysis of Mind", 1921, 310),
    ("What I Believe", 1925, 68), ("Marriage and Morals", 1929, 320),
    ("The Conquest of Happiness", 1930, 190), ("Education and the Social Order", 1932, 246),
    ("In Praise of Idleness", 1935, 192), ("Power", 1938, 328),
    ("A History of Western Philosophy", 1945, 895), ("Human Knowledge", 1948, 524),
    ("Authority and the Individual", 1949, 135), ("Unpopular Essays", 1950, 206),
    ("The Impact of Science on Society", 1952, 114), ("Why I Am Not a Christian", 1957, 225),
    ("My Philosophical Development", 1959, 279), ("Has Man a Future?", 1961, 128),
    ("Autobiography", 1967, 742),
]:
    ALL_BOOKS.append(make_book(title, "Bertrand Russell", year, pages, ["Philosophy", "Non-Fiction"]))

# Hannah Arendt
for title, year, pages in [
    ("The Origins of Totalitarianism", 1951, 576), ("The Human Condition", 1958, 349),
    ("Between Past and Future", 1961, 246), ("On Revolution", 1963, 344),
    ("Eichmann in Jerusalem", 1963, 312), ("Men in Dark Times", 1968, 267),
    ("On Violence", 1970, 106), ("Crises of the Republic", 1972, 240),
    ("The Life of the Mind", 1978, 521),
]:
    ALL_BOOKS.append(make_book(title, "Hannah Arendt", year, pages, ["Philosophy", "Non-Fiction"]))

# === GRAPHIC NOVELS / COMICS ===

# Art Spiegelman
for title, year, pages in [
    ("Maus I: A Survivor's Tale", 1986, 159),
    ("Maus II: And Here My Troubles Began", 1991, 136),
    ("In the Shadow of No Towers", 2004, 42),
]:
    ALL_BOOKS.append(make_book(title, "Art Spiegelman", year, pages, ["Graphic Novel", "Memoir"]))

# Marjane Satrapi
for title, year, pages in [
    ("Persepolis: The Story of a Childhood", 2000, 153),
    ("Persepolis 2: The Story of a Return", 2004, 187),
    ("Embroideries", 2005, 134), ("Chicken with Plums", 2006, 84),
]:
    ALL_BOOKS.append(make_book(title, "Marjane Satrapi", year, pages, ["Graphic Novel", "Memoir"]))

# Chris Ware
for title, year, pages in [
    ("Jimmy Corrigan, the Smartest Kid on Earth", 2000, 380),
    ("Building Stories", 2012, 260), ("Rusty Brown", 2019, 356),
]:
    ALL_BOOKS.append(make_book(title, "Chris Ware", year, pages, ["Graphic Novel"]))

# === SPORTS & ADVENTURE NON-FICTION ===

# David Epstein
for title, year, pages in [
    ("The Sports Gene", 2013, 338), ("Range", 2019, 339),
]:
    ALL_BOOKS.append(make_book(title, "David Epstein", year, pages, ["Non-Fiction", "Science"]))

# Sebastian Junger
for title, year, pages in [
    ("The Perfect Storm", 1997, 227), ("Fire", 2001, 224),
    ("A Death in Belmont", 2006, 247), ("War", 2010, 287),
    ("Tribe", 2016, 192), ("Freedom", 2021, 152),
    ("In My Time of Dying", 2024, 224),
]:
    ALL_BOOKS.append(make_book(title, "Sebastian Junger", year, pages, ["Non-Fiction", "Adventure"]))

# === ROMANCE/WOMEN'S FICTION EXPANSION ===

# LaVyrle Spencer
for title, year, pages in [
    ("The Fulfillment", 1979, 379), ("The Endearment", 1982, 372),
    ("Hummingbird", 1983, 393), ("A Heart Speaks", 1984, 528),
    ("Separate Beds", 1985, 384), ("Forsaking All Others", 1982, 336),
    ("Sweet Memories", 1984, 252), ("Spring Fancy", 1984, 299),
    ("Years", 1986, 356), ("Morning Glory", 1989, 388),
    ("Bitter Sweet", 1990, 368), ("Forgiving", 1991, 368),
    ("Bygones", 1992, 350), ("November of the Heart", 1993, 352),
    ("Family Blessings", 1994, 339), ("Home Song", 1995, 339),
    ("That Camden Summer", 1996, 368), ("Small Town Girl", 1997, 384),
    ("Then Came Heaven", 1997, 352),
]:
    ALL_BOOKS.append(make_book(title, "LaVyrle Spencer", year, pages, ["Romance"]))

# Susan Elizabeth Phillips
for title, year, pages in [
    ("Glitter Baby", 1987, 352), ("Fancy Pants", 1989, 384),
    ("Hot Shot", 1991, 448), ("Honey Moon", 1993, 416),
    ("It Had to Be You", 1994, 384), ("Heaven, Texas", 1995, 384),
    ("Kiss an Angel", 1996, 384), ("Nobody's Baby But Mine", 1997, 384),
    ("Dream a Little Dream", 1998, 352), ("Lady Be Good", 1999, 352),
    ("First Lady", 2000, 384), ("Just Imagine", 2001, 400),
    ("This Heart of Mine", 2001, 384), ("Ain't She Sweet", 2004, 384),
    ("Match Me If You Can", 2005, 384), ("Natural Born Charmer", 2007, 384),
    ("What I Did for Love", 2009, 384), ("Call Me Irresistible", 2010, 384),
    ("The Great Escape", 2012, 400), ("Heroes Are My Weakness", 2014, 384),
    ("First Star I See Tonight", 2016, 384), ("When Stars Collide", 2021, 384),
]:
    ALL_BOOKS.append(make_book(title, "Susan Elizabeth Phillips", year, pages, ["Romance"]))

# Johanna Lindsey
for title, year, pages in [
    ("Captive Bride", 1977, 335), ("A Pirate's Love", 1978, 383),
    ("Fires of Winter", 1980, 381), ("A Gentle Feuding", 1984, 360),
    ("Brave the Wild Wind", 1984, 384), ("Heart of Thunder", 1983, 384),
    ("So Speaks the Heart", 1983, 344), ("Defy Not the Heart", 1989, 345),
    ("Silver Angel", 1988, 371), ("Tender Rebel", 1988, 377),
    ("Gentle Rogue", 1990, 391), ("Prisoner of My Desire", 1991, 390),
    ("Man of My Dreams", 1992, 371), ("Angel", 1992, 371),
    ("Say You Love Me", 1996, 387), ("The Present", 1998, 320),
    ("Joining", 1999, 352), ("Home for the Holidays", 2000, 256),
    ("Heart of a Warrior", 2001, 352), ("A Loving Scoundrel", 2004, 368),
    ("Captive of My Desires", 2006, 368), ("No Choice But Seduction", 2008, 384),
    ("That Perfect Someone", 2010, 384), ("When Passion Rules", 2011, 368),
    ("Let Love Find You", 2012, 384), ("One Heart to Win", 2013, 384),
    ("Wildfire in His Arms", 2015, 368), ("Beautiful Tempest", 2017, 384),
]:
    ALL_BOOKS.append(make_book(title, "Johanna Lindsey", year, pages, ["Romance", "Historical Fiction"]))

# === CHILDREN'S/YA EXPANSION ===

# Enid Blyton
for title, year, pages in [
    ("The Adventures of the Wishing-Chair", 1937, 224),
    ("The Enchanted Wood", 1939, 224), ("The Magic Faraway Tree", 1943, 240),
    ("The Folk of the Faraway Tree", 1946, 224),
    ("Five on a Treasure Island", 1942, 224), ("Five Go Adventuring Again", 1943, 192),
    ("Five Run Away Together", 1944, 208), ("Five Go to Smuggler's Top", 1945, 192),
    ("Five Go Off in a Caravan", 1946, 192), ("Five on Kirrin Island Again", 1947, 192),
    ("Five Go Off to Camp", 1948, 192), ("Five Get into Trouble", 1949, 192),
    ("Five Fall into Adventure", 1950, 192), ("Five on a Hike Together", 1951, 192),
    ("Five Have a Wonderful Time", 1952, 192), ("Five Go Down to the Sea", 1953, 192),
    ("The Secret Seven", 1949, 128), ("Secret Seven Adventure", 1950, 128),
    ("Well Done, Secret Seven", 1951, 128), ("Secret Seven on the Trail", 1952, 128),
    ("Go Ahead, Secret Seven", 1953, 128), ("Good Work, Secret Seven", 1954, 128),
    ("The Island of Adventure", 1944, 224), ("The Castle of Adventure", 1946, 224),
    ("The Valley of Adventure", 1947, 224), ("The Sea of Adventure", 1948, 224),
    ("The Mountain of Adventure", 1949, 224), ("The Ship of Adventure", 1950, 224),
    ("The Circus of Adventure", 1952, 224), ("The River of Adventure", 1955, 224),
]:
    ALL_BOOKS.append(make_book(title, "Enid Blyton", year, pages, ["Children's", "Adventure"]))

# Beverly Cleary
for title, year, pages in [
    ("Henry Huggins", 1950, 155), ("Henry and Beezus", 1952, 155),
    ("Henry and Ribsy", 1954, 192), ("Beezus and Ramona", 1955, 159),
    ("Fifteen", 1956, 254), ("Henry and the Paper Route", 1957, 192),
    ("The Luckiest Girl", 1958, 272), ("Jean and Johnny", 1959, 224),
    ("Ramona the Pest", 1968, 192), ("Runaway Ralph", 1970, 175),
    ("Ramona the Brave", 1975, 190), ("Ramona and Her Father", 1977, 186),
    ("Ramona and Her Mother", 1979, 208), ("Ramona Quimby, Age 8", 1981, 190),
    ("Dear Mr. Henshaw", 1983, 134), ("Ramona Forever", 1984, 192),
    ("Strider", 1991, 179), ("Ramona's World", 1999, 192),
]:
    ALL_BOOKS.append(make_book(title, "Beverly Cleary", year, pages, ["Children's"]))


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

    batch_num = 145
    for i in range(0, len(new_books), 100):
        chunk = new_books[i:i+100]
        fname = f"batch_{batch_num}_batch25_{(i//100)+1}.json"
        with open(os.path.join(BATCH_DIR, fname), "w") as f:
            json.dump(chunk, f, indent=2)
        print(f"  {fname}: {len(chunk)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(new_books)}")
