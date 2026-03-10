#!/usr/bin/env python3
"""Batch 19: Massive fresh authors batch - Western, sports, music biographies,
true crime, cozy mystery, domestic fiction, women's fiction, literary debuts."""
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
    # Western fiction
    ("Louis L'Amour", "en", ["Western", "Adventure"], [
        ("Hondo", 1953, 256, []),
        ("Shalako", 1962, 155, []),
        ("The Daybreakers", 1960, 195, []),
        ("Sackett", 1961, 184, []),
        ("Lando", 1962, 178, []),
        ("Mojave Crossing", 1964, 166, []),
        ("The Sackett Brand", 1965, 185, []),
        ("Mustang Man", 1966, 180, []),
        ("The Lonely Men", 1969, 174, []),
        ("Galloway", 1970, 167, []),
        ("Ride the Dark Trail", 1972, 185, []),
        ("The Man from the Broken Hills", 1975, 240, []),
        ("Lonely on the Mountain", 1980, 181, []),
        ("Jubal Sackett", 1985, 375, []),
        ("Last of the Breed", 1986, 292, []),
        ("The Walking Drum", 1984, 425, ["Historical Fiction"]),
        ("Fair Blows the Wind", 1978, 267, []),
        ("The Lonesome Gods", 1983, 450, []),
        ("Comstock Lode", 1981, 401, []),
        ("Bendigo Shafter", 1979, 324, []),
        ("Flint", 1960, 177, []),
        ("Kilkenny", 1954, 166, []),
        ("Conagher", 1969, 175, []),
        ("Catlow", 1963, 167, []),
        ("The Haunted Mesa", 1987, 350, []),
    ]),
    ("Larry McMurtry", "en", ["Western", "Literary Fiction"], [
        ("Horseman, Pass By", 1961, 176, []),
        ("Leaving Cheyenne", 1963, 254, []),
        ("The Last Picture Show", 1966, 280, ["Classic"]),
        ("Moving On", 1970, 794, []),
        ("All My Friends Are Going to Be Strangers", 1972, 286, []),
        ("Terms of Endearment", 1975, 410, []),
        ("Cadillac Jack", 1982, 334, []),
        ("The Desert Rose", 1983, 254, []),
        ("Lonesome Dove", 1985, 843, ["Classic"]),
        ("Texasville", 1987, 542, []),
        ("Anything for Billy", 1988, 382, []),
        ("Some Can Whistle", 1989, 340, []),
        ("Buffalo Girls", 1990, 351, []),
        ("The Evening Star", 1992, 640, []),
        ("Streets of Laredo", 1993, 589, []),
        ("Comanche Moon", 1997, 752, []),
        ("Dead Man's Walk", 1995, 477, []),
        ("Duane's Depressed", 1999, 431, []),
        ("Sin Killer", 2002, 300, []),
        ("By Sorrow's River", 2003, 347, []),
        ("The Wandering Hill", 2003, 330, []),
        ("Folly and Glory", 2004, 270, []),
    ]),
    ("Elmore Leonard", "en", ["Western", "Crime Fiction", "Thriller"], [
        ("The Bounty Hunters", 1953, 192, []),
        ("The Law at Randado", 1954, 160, []),
        ("Escape from Five Shadows", 1956, 160, []),
        ("Last Stand at Saber River", 1959, 195, []),
        ("Hombre", 1961, 179, ["Classic"]),
        ("Valdez Is Coming", 1970, 165, []),
        ("Forty Lashes Less One", 1972, 181, []),
        ("52 Pickup", 1974, 231, []),
        ("Swag", 1976, 204, []),
        ("Unknown Man #89", 1977, 221, []),
        ("The Switch", 1978, 214, []),
        ("City Primeval", 1980, 230, []),
        ("Split Images", 1981, 277, []),
        ("Cat Chaser", 1982, 260, []),
        ("Stick", 1983, 299, []),
        ("LaBrava", 1983, 279, []),
        ("Glitz", 1985, 258, []),
        ("Bandits", 1987, 345, []),
        ("Freaky Deaky", 1988, 341, []),
        ("Killshot", 1989, 287, []),
        ("Get Shorty", 1990, 292, ["Humor"]),
        ("Maximum Bob", 1991, 295, []),
        ("Rum Punch", 1992, 297, []),
        ("Out of Sight", 1996, 296, []),
        ("Be Cool", 1999, 292, ["Humor"]),
        ("Tishomingo Blues", 2002, 308, []),
        ("Mr. Paradise", 2004, 291, []),
        ("The Hot Kid", 2005, 308, []),
        ("Up in Honey's Room", 2007, 291, []),
        ("Road Dogs", 2009, 262, []),
        ("Djibouti", 2010, 279, []),
        ("Raylan", 2012, 263, []),
    ]),
    # Cozy mystery
    ("Agatha Raisin series - M.C. Beaton", "en", ["Mystery", "Humor"], [
        ("Agatha Raisin and the Quiche of Death", 1992, 188, []),
        ("Agatha Raisin and the Vicious Vet", 1993, 198, []),
        ("Agatha Raisin and the Potted Gardener", 1994, 229, []),
        ("Agatha Raisin and the Walkers of Dembley", 1995, 230, []),
        ("Agatha Raisin and the Murderous Marriage", 1996, 224, []),
        ("Agatha Raisin and the Terrible Tourist", 1997, 218, []),
        ("Agatha Raisin and the Wellspring of Death", 1998, 220, []),
        ("Agatha Raisin and the Witch of Wyckhadden", 1999, 216, []),
        ("Agatha Raisin and the Wizard of Evesham", 1999, 210, []),
        ("Agatha Raisin and the Fairies of Fryfam", 2000, 204, []),
        ("Agatha Raisin and the Love from Hell", 2001, 218, []),
        ("Agatha Raisin and the Day the Floods Came", 2002, 218, []),
        ("Agatha Raisin and the Case of the Curious Curate", 2003, 220, []),
        ("Agatha Raisin and the Haunted House", 2003, 218, []),
        ("Agatha Raisin and the Deadly Dance", 2004, 225, []),
        ("Agatha Raisin and the Perfect Paragon", 2005, 220, []),
        ("Agatha Raisin and Love, Lies and Liquor", 2006, 210, []),
        ("Agatha Raisin: Kissing Christmas Goodbye", 2007, 230, []),
        ("Agatha Raisin: A Spoonful of Poison", 2008, 230, []),
        ("Agatha Raisin: There Goes the Bride", 2009, 234, []),
    ]),
    ("M.C. Beaton", "en", ["Mystery", "Humor"], [
        ("Death of a Gossip", 1985, 164, []),
        ("Death of a Cad", 1987, 180, []),
        ("Death of an Outsider", 1988, 182, []),
        ("Death of a Perfect Wife", 1989, 155, []),
        ("Death of a Hussy", 1990, 163, []),
        ("Death of a Snob", 1991, 148, []),
        ("Death of a Prankster", 1992, 177, []),
        ("Death of a Glutton", 1993, 176, []),
        ("Death of a Travelling Man", 1993, 182, []),
        ("Death of a Charming Man", 1994, 170, []),
        ("Death of a Nag", 1995, 180, []),
        ("Death of a Macho Man", 1996, 195, []),
        ("Death of a Dentist", 1997, 210, []),
        ("Death of a Scriptwriter", 1998, 195, []),
        ("Death of an Addict", 1999, 225, []),
        ("Death of a Dustman", 2001, 230, []),
        ("Death of a Celebrity", 2001, 212, []),
        ("Death of a Village", 2003, 233, []),
        ("Death of a Poison Pen", 2004, 212, []),
        ("Death of a Bore", 2005, 244, []),
    ]),
    # True Crime
    ("Truman Capote", "en", ["Literary Fiction", "True Crime"], [
        ("Other Voices, Other Rooms", 1948, 231, []),
        ("The Grass Harp", 1951, 181, []),
        ("Breakfast at Tiffany's", 1958, 179, ["Classic"]),
        ("In Cold Blood", 1966, 343, ["Classic", "Non-Fiction"]),
        ("Music for Chameleons", 1980, 262, ["Short Stories"]),
        ("A Christmas Memory", 1956, 48, ["Short Stories"]),
        ("Answered Prayers", 1987, 180, []),
    ]),
    ("Erik Larson", "en", ["Non-Fiction", "History"], [
        ("The Devil in the White City", 2003, 447, ["True Crime"]),
        ("Isaac's Storm", 1999, 323, ["Science"]),
        ("Thunderstruck", 2006, 390, []),
        ("In the Garden of Beasts", 2011, 448, []),
        ("Dead Wake", 2015, 430, []),
        ("The Splendid and the Vile", 2020, 546, []),
        ("The Demon of Unrest", 2024, 544, []),
    ]),
    ("Ann Rule", "en", ["True Crime", "Non-Fiction"], [
        ("The Stranger Beside Me", 1980, 536, []),
        ("Small Sacrifices", 1987, 531, []),
        ("If You Really Loved Me", 1991, 555, []),
        ("Everything She Ever Wanted", 1992, 560, []),
        ("Dead by Sunset", 1995, 520, []),
        ("Bitter Harvest", 1997, 560, []),
        ("And Never Let Her Go", 1999, 560, []),
        ("Every Breath You Take", 2001, 544, []),
        ("Heart Full of Lies", 2003, 368, []),
        ("Green River, Running Red", 2004, 656, []),
        ("Too Late to Say Goodbye", 2007, 480, []),
        ("But I Trusted You", 2009, 448, []),
        ("In the Still of the Night", 2010, 464, []),
    ]),
    # Women's / Domestic fiction
    ("Maeve Binchy", "en", ["Literary Fiction", "Romance"], [
        ("Light a Penny Candle", 1982, 544, []),
        ("Echoes", 1985, 496, []),
        ("Firefly Summer", 1987, 608, []),
        ("Circle of Friends", 1990, 565, []),
        ("The Glass Lake", 1994, 558, []),
        ("Evening Class", 1996, 398, []),
        ("Tara Road", 1998, 518, []),
        ("Scarlet Feather", 2000, 502, []),
        ("Quentins", 2002, 390, []),
        ("Nights of Rain and Stars", 2004, 302, []),
        ("Whitethorn Woods", 2006, 338, []),
        ("Heart and Soul", 2008, 436, []),
        ("Minding Frankie", 2010, 480, []),
        ("A Week in Winter", 2012, 341, []),
    ]),
    ("Rosamunde Pilcher", "en", ["Literary Fiction", "Romance"], [
        ("The Shell Seekers", 1987, 530, []),
        ("September", 1990, 536, []),
        ("Coming Home", 1995, 728, []),
        ("Winter Solstice", 2000, 454, []),
        ("Sleeping Tiger", 1967, 186, []),
        ("Another View", 1968, 186, []),
        ("The End of Summer", 1971, 205, []),
        ("Snow in April", 1972, 218, []),
        ("The Empty House", 1973, 200, []),
        ("The Day of the Storm", 1975, 220, []),
        ("Under Gemini", 1976, 260, []),
        ("Wild Mountain Thyme", 1978, 220, []),
        ("The Carousel", 1982, 186, []),
        ("Voices in Summer", 1984, 222, []),
        ("The Blue Bedroom", 1985, 260, ["Short Stories"]),
    ]),
    # Sports books
    ("John Grisham", "en", ["Literary Fiction"], [
        ("The Innocent Man", 2006, 360, ["True Crime", "Non-Fiction"]),
    ]),
    ("Michael Lewis", "en", ["Non-Fiction"], [
        ("Liar's Poker", 1989, 249, ["Business", "Memoir"]),
        ("The New New Thing", 1999, 268, ["Business"]),
        ("Moneyball", 2003, 317, ["Sports"]),
        ("The Blind Side", 2006, 299, ["Sports"]),
        ("The Big Short", 2010, 266, ["Business"]),
        ("Boomerang", 2011, 213, ["Business"]),
        ("Flash Boys", 2014, 274, ["Business"]),
        ("The Undoing Project", 2016, 362, ["Psychology"]),
        ("The Fifth Risk", 2018, 219, ["Politics"]),
        ("The Premonition", 2021, 304, ["Science"]),
        ("Going Infinite", 2023, 267, ["Business"]),
    ]),
    ("Andre Agassi", "en", ["Memoir", "Sports"], [
        ("Open", 2009, 385, []),
    ]),
    ("Phil Jackson", "en", ["Memoir", "Sports"], [
        ("Sacred Hoops", 1995, 238, []),
        ("Eleven Rings", 2013, 370, []),
    ]),
    # More literary debuts and contemporary fiction
    ("Donna Tartt", "en", ["Literary Fiction"], [
        ("The Secret History", 1992, 559, ["Thriller", "Classic"]),
    ]),
    ("Amor Towles", "en", ["Literary Fiction", "Historical Fiction"], [
        ("Rules of Civility", 2011, 335, []),
        ("A Gentleman in Moscow", 2016, 462, []),
        ("The Lincoln Highway", 2021, 592, []),
        ("Table for Two", 2024, 379, ["Short Stories"]),
    ]),
    ("Anthony Doerr", "en", ["Literary Fiction"], [
        ("The Shell Collector", 2002, 233, ["Short Stories"]),
        ("About Grace", 2004, 402, []),
        ("All the Light We Cannot See", 2014, 531, ["Historical Fiction", "War"]),
        ("Cloud Cuckoo Land", 2021, 622, []),
        ("Memory Wall", 2010, 243, ["Short Stories"]),
    ]),
    ("Celeste Ng", "en", ["Literary Fiction"], [
        ("Everything I Never Told You", 2014, 292, []),
        ("Little Fires Everywhere", 2017, 338, []),
        ("Our Missing Hearts", 2022, 336, []),
    ]),
    ("Matt Haig", "en", ["Literary Fiction"], [
        ("The Dead Fathers Club", 2006, 327, []),
        ("The Possession of Mr Cave", 2008, 244, []),
        ("The Radleys", 2010, 326, ["Horror"]),
        ("The Humans", 2013, 305, ["Science Fiction"]),
        ("How to Stop Time", 2017, 326, ["Science Fiction"]),
        ("The Midnight Library", 2020, 288, []),
        ("The Life Impossible", 2024, 384, []),
        ("Reasons to Stay Alive", 2015, 264, ["Memoir"]),
        ("Notes on a Nervous Planet", 2018, 310, ["Non-Fiction"]),
        ("The Comfort Book", 2021, 272, ["Non-Fiction"]),
    ]),
    ("Fredrik Backman", "en", ["Literary Fiction", "Humor"], [
        ("A Man Called Ove", 2012, 337, []),
        ("My Grandmother Asked Me to Tell You She's Sorry", 2013, 372, []),
        ("Britt-Marie Was Here", 2014, 324, []),
        ("Beartown", 2016, 418, ["Sports"]),
        ("Us Against You", 2017, 432, ["Sports"]),
        ("Anxious People", 2019, 341, []),
        ("The Winners", 2022, 672, ["Sports"]),
        ("The Deal of a Lifetime", 2017, 64, []),
        ("And Every Morning the Way Home Gets Longer and Longer", 2015, 96, []),
    ]),
    ("Delia Owens", "en", ["Literary Fiction", "Mystery"], [
        ("Where the Crawdads Sing", 2018, 368, []),
    ]),
    ("V.E. Schwab", "en", ["Fantasy", "Science Fiction"], [
        ("Vicious", 2013, 364, []),
        ("Vengeful", 2018, 400, []),
        ("A Darker Shade of Magic", 2015, 400, []),
        ("A Gathering of Shadows", 2016, 512, []),
        ("A Conjuring of Light", 2017, 624, []),
        ("The Invisible Life of Addie LaRue", 2020, 444, ["Literary Fiction"]),
        ("Gallant", 2022, 352, ["Young Adult"]),
        ("The Fragile Threads of Power", 2023, 576, []),
    ]),
    ("Madeline Miller", "en", ["Literary Fiction", "Fantasy", "Historical Fiction"], [
        ("The Song of Achilles", 2011, 352, ["Mythology"]),
        ("Circe", 2018, 393, ["Mythology"]),
    ]),
    ("Erin Morgenstern", "en", ["Fantasy", "Literary Fiction"], [
        ("The Night Circus", 2011, 387, []),
        ("The Starless Sea", 2019, 498, []),
    ]),
    ("Naomi Novik", "en", ["Fantasy"], [
        ("His Majesty's Dragon", 2006, 353, ["Historical Fiction"]),
        ("Throne of Jade", 2006, 398, ["Historical Fiction"]),
        ("Black Powder War", 2006, 365, ["Historical Fiction"]),
        ("Empire of Ivory", 2007, 404, []),
        ("Victory of Eagles", 2008, 352, []),
        ("Tongues of Serpents", 2010, 361, []),
        ("Crucible of Gold", 2012, 300, []),
        ("Blood of Tyrants", 2013, 364, []),
        ("League of Dragons", 2016, 384, []),
        ("Uprooted", 2015, 435, []),
        ("Spinning Silver", 2018, 466, []),
        ("A Deadly Education", 2020, 336, []),
        ("The Last Graduate", 2021, 388, []),
        ("The Golden Enclaves", 2022, 404, []),
    ]),
    ("T.J. Klune", "en", ["Fantasy", "Romance"], [
        ("The House in the Cerulean Sea", 2020, 398, []),
        ("Under the Whispering Door", 2021, 352, []),
        ("In the Lives of Puppets", 2023, 432, []),
        ("Somewhere Beyond the Sea", 2024, 400, []),
    ]),
    ("R.F. Kuang", "en", ["Fantasy", "Historical Fiction"], [
        ("The Poppy War", 2018, 527, []),
        ("The Dragon Republic", 2019, 658, []),
        ("The Burning God", 2020, 622, []),
        ("Babel", 2022, 560, []),
        ("Yellowface", 2023, 323, ["Literary Fiction", "Satire"]),
    ]),
    ("Travis Baldree", "en", ["Fantasy"], [
        ("Legends & Lattes", 2022, 296, []),
        ("Bookshops & Bonedust", 2023, 352, []),
    ]),
    ("Sarah J. Maas", "en", ["Fantasy", "Romance"], [
        ("Throne of Glass", 2012, 404, []),
        ("Crown of Midnight", 2013, 418, []),
        ("Heir of Fire", 2014, 565, []),
        ("Queen of Shadows", 2015, 645, []),
        ("Empire of Storms", 2016, 693, []),
        ("Tower of Dawn", 2017, 660, []),
        ("Kingdom of Ash", 2018, 980, []),
        ("A Court of Thorns and Roses", 2015, 419, []),
        ("A Court of Mist and Fury", 2016, 624, []),
        ("A Court of Wings and Ruin", 2017, 699, []),
        ("A Court of Frost and Starlight", 2018, 229, []),
        ("A Court of Silver Flames", 2021, 757, []),
        ("House of Earth and Blood", 2020, 803, []),
        ("House of Sky and Breath", 2022, 768, []),
        ("House of Flame and Shadow", 2024, 821, []),
    ]),
    ("Rebecca Yarros", "en", ["Fantasy", "Romance"], [
        ("Fourth Wing", 2023, 498, []),
        ("Iron Flame", 2023, 623, []),
        ("Onyx Storm", 2025, 550, []),
    ]),
]


def generate():
    batch_num = 115
    books_in_batch = []

    for author, lang, default_genres, works in AUTHORS:
        for title, year, pages, extra_genres in works:
            genres = list(default_genres) + extra_genres
            book = make_book(title, author, year, pages, genres, lang)
            books_in_batch.append(book)

            if len(books_in_batch) >= 100:
                fname = f"batch_{batch_num:03d}_batch19_{batch_num - 114}.json"
                path = os.path.join(BATCH_DIR, fname)
                with open(path, "w") as f:
                    json.dump(books_in_batch, f, indent=2)
                print(f"  {fname}: {len(books_in_batch)} books")
                batch_num += 1
                books_in_batch = []

    if books_in_batch:
        fname = f"batch_{batch_num:03d}_batch19_{batch_num - 114}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(books_in_batch, f, indent=2)
        print(f"  {fname}: {len(books_in_batch)} books")
        batch_num += 1

    total = sum(len(works) for _, _, _, works in AUTHORS)
    print(f"\nTotal new books: {total}")


if __name__ == "__main__":
    generate()
