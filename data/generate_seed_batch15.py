#!/usr/bin/env python3
"""Batch 15: Indian, Asian, African, Middle Eastern, and more world literature."""
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
    # Indian Fiction - contemporary
    ("Vikram Seth", "en", ["Literary Fiction", "Indian Fiction"], [
        ("The Golden Gate", 1986, 307, ["Poetry"]),
        ("A Suitable Boy", 1993, 1349, []),
        ("An Equal Music", 1999, 381, []),
        ("Two Lives", 2005, 503, ["Memoir"]),
        ("A Suitable Girl", 2016, 900, []),
    ]),
    ("Kiran Desai", "en", ["Literary Fiction", "Indian Fiction"], [
        ("Hullabaloo in the Guava Orchard", 1998, 209, ["Humor"]),
        ("The Inheritance of Loss", 2006, 324, []),
    ]),
    ("Anita Desai", "en", ["Literary Fiction", "Indian Fiction"], [
        ("Cry, the Peacock", 1963, 218, []),
        ("Voices in the City", 1965, 256, []),
        ("Fire on the Mountain", 1977, 145, []),
        ("Clear Light of Day", 1980, 182, []),
        ("In Custody", 1984, 204, []),
        ("Baumgartner's Bombay", 1988, 241, []),
        ("Journey to Ithaca", 1995, 332, []),
        ("Fasting, Feasting", 1999, 227, []),
        ("The Zigzag Way", 2004, 165, []),
        ("The Artist of Disappearance", 2011, 167, ["Short Stories"]),
    ]),
    ("Rohinton Mistry", "en", ["Literary Fiction", "Indian Fiction"], [
        ("Tales from Firozsha Baag", 1987, 260, ["Short Stories"]),
        ("Such a Long Journey", 1991, 339, []),
        ("A Fine Balance", 1995, 603, ["Classic"]),
        ("Family Matters", 2002, 434, []),
    ]),
    ("Vikram Chandra", "en", ["Literary Fiction", "Indian Fiction"], [
        ("Red Earth and Pouring Rain", 1995, 530, []),
        ("Love and Longing in Bombay", 1997, 261, ["Short Stories"]),
        ("Sacred Games", 2006, 916, ["Thriller"]),
        ("Mirrored Mind", 2013, 432, ["Non-Fiction"]),
    ]),
    ("Amitav Ghosh", "en", ["Literary Fiction", "Indian Fiction"], [
        ("The Circle of Reason", 1986, 423, []),
        ("In an Antique Land", 1992, 393, ["Non-Fiction"]),
        ("The Calcutta Chromosome", 1996, 310, ["Science Fiction"]),
        ("The Hungry Tide", 2004, 333, []),
        ("The Great Derangement", 2016, 176, ["Non-Fiction"]),
    ]),
    ("Arvind Adiga", "en", ["Literary Fiction", "Indian Fiction"], [
        ("The White Tiger", 2008, 321, []),
        ("Between the Assassinations", 2008, 330, ["Short Stories"]),
        ("Last Man in Tower", 2011, 421, []),
        ("Selection Day", 2016, 339, []),
        ("Amnesty", 2020, 256, []),
    ]),
    ("Chitra Banerjee Divakaruni", "en", ["Literary Fiction", "Indian Fiction"], [
        ("Arranged Marriage", 1995, 306, ["Short Stories"]),
        ("The Mistress of Spices", 1997, 317, ["Magical Realism"]),
        ("Sister of My Heart", 1999, 322, []),
        ("The Vine of Desire", 2002, 340, []),
        ("Queen of Dreams", 2004, 320, []),
        ("The Palace of Illusions", 2008, 360, ["Historical Fiction", "Mythology"]),
        ("One Amazing Thing", 2009, 220, []),
        ("Oleander Girl", 2013, 289, []),
        ("The Forest of Enchantments", 2019, 384, ["Mythology"]),
        ("Independence", 2022, 336, ["Historical Fiction"]),
    ]),
    ("Aravind Adiga", "en", ["Literary Fiction", "Indian Fiction"], [
        ("The White Tiger", 2008, 321, []),
    ]),
    ("Shashi Tharoor", "en", ["Literary Fiction", "Indian Fiction"], [
        ("The Great Indian Novel", 1989, 423, ["Satire"]),
        ("Show Business", 1992, 341, []),
        ("Riot", 2001, 275, []),
        ("An Era of Darkness", 2016, 339, ["History", "Non-Fiction"]),
        ("Why I Am a Hindu", 2018, 302, ["Non-Fiction"]),
        ("The Battle of Belonging", 2020, 408, ["Non-Fiction"]),
        ("Pride, Prejudice and Punditry", 2021, 200, ["Non-Fiction"]),
    ]),
    ("Perumal Murugan", "en", ["Literary Fiction", "Indian Fiction"], [
        ("Seasons of the Palm", 2004, 196, []),
        ("One Part Woman", 2010, 240, []),
        ("Pyre", 2016, 196, []),
        ("Trial by Silence", 2019, 320, []),
        ("The Story of a Goat", 2020, 184, []),
    ]),
    # More African literature
    ("Ngugi wa Thiong'o", "en", ["Literary Fiction", "African Literature"], [
        ("Weep Not, Child", 1964, 136, []),
        ("The River Between", 1965, 152, []),
        ("A Grain of Wheat", 1967, 247, []),
        ("Petals of Blood", 1977, 345, []),
        ("Devil on the Cross", 1980, 254, []),
        ("Matigari", 1986, 175, []),
        ("Wizard of the Crow", 2006, 768, ["Magical Realism"]),
        ("Decolonising the Mind", 1986, 114, ["Non-Fiction"]),
        ("Dreams in a Time of War", 2010, 256, ["Memoir"]),
        ("The Perfect Nine", 2020, 256, []),
    ]),
    ("Chinua Achebe", "en", ["Literary Fiction", "African Literature", "Classic"], [
        ("Things Fall Apart", 1958, 209, []),
        ("No Longer at Ease", 1960, 170, []),
        ("Arrow of God", 1964, 287, []),
        ("A Man of the People", 1966, 166, []),
        ("Anthills of the Savannah", 1987, 233, []),
        ("Girls at War and Other Stories", 1972, 118, ["Short Stories"]),
    ]),
    ("Wole Soyinka", "en", ["Literary Fiction", "African Literature"], [
        ("The Interpreters", 1965, 253, []),
        ("Season of Anomy", 1973, 320, []),
        ("Aké: The Years of Childhood", 1981, 230, ["Memoir"]),
        ("Isara: A Voyage Around Essay", 1989, 262, ["Memoir"]),
        ("Death and the King's Horseman", 1975, 80, ["Drama"]),
        ("The Lion and the Jewel", 1963, 64, ["Drama"]),
        ("A Dance of the Forests", 1960, 89, ["Drama"]),
        ("The Road", 1965, 100, ["Drama"]),
        ("You Must Set Forth at Dawn", 2006, 499, ["Memoir"]),
    ]),
    ("Ben Okri", "en", ["Literary Fiction", "African Literature", "Magical Realism"], [
        ("Flowers and Shadows", 1980, 189, []),
        ("The Landscapes Within", 1981, 275, []),
        ("Incidents at the Shrine", 1986, 153, ["Short Stories"]),
        ("Stars of the New Curfew", 1988, 189, ["Short Stories"]),
        ("The Famished Road", 1991, 500, ["Classic"]),
        ("Songs of Enchantment", 1993, 295, []),
        ("Infinite Riches", 1998, 377, []),
        ("In Arcadia", 2002, 260, []),
        ("Starbook", 2007, 321, []),
        ("The Age of Magic", 2014, 245, []),
        ("The Freedom Artist", 2019, 179, []),
        ("The Last Gift of the Master Artists", 2021, 320, []),
    ]),
    ("Tsitsi Dangarembga", "en", ["Literary Fiction", "African Literature"], [
        ("Nervous Conditions", 1988, 204, ["Classic"]),
        ("The Book of Not", 2006, 272, []),
        ("This Mournable Body", 2018, 283, []),
    ]),
    ("NoViolet Bulawayo", "en", ["Literary Fiction", "African Literature"], [
        ("We Need New Names", 2013, 296, []),
        ("Glory", 2022, 401, []),
    ]),
    ("Yaa Gyasi", "en", ["Literary Fiction", "African Literature"], [
        ("Homegoing", 2016, 300, ["Historical Fiction"]),
        ("Transcendent Kingdom", 2020, 264, []),
    ]),
    ("Aminatta Forna", "en", ["Literary Fiction", "African Literature"], [
        ("The Devil That Danced on the Water", 2002, 367, ["Memoir"]),
        ("Ancestor Stones", 2006, 319, []),
        ("The Memory of Love", 2010, 393, []),
        ("The Hired Man", 2013, 283, []),
        ("Happiness", 2018, 320, []),
    ]),
    # East Asian Literature
    ("Mo Yan", "zh", ["Literary Fiction"], [
        ("Red Sorghum", 1987, 359, []),
        ("The Garlic Ballads", 1988, 291, []),
        ("The Republic of Wine", 1992, 400, []),
        ("Big Breasts and Wide Hips", 1995, 532, []),
        ("Life and Death Are Wearing Me Out", 2006, 540, ["Magical Realism"]),
        ("Frog", 2009, 350, []),
        ("Sandalwood Death", 2001, 392, ["Historical Fiction"]),
        ("Change", 2010, 160, []),
    ]),
    ("Yu Hua", "zh", ["Literary Fiction"], [
        ("To Live", 1992, 235, ["Classic"]),
        ("Chronicle of a Blood Merchant", 1995, 252, []),
        ("Brothers", 2005, 641, []),
        ("The Seventh Day", 2013, 225, []),
        ("Cries in the Drizzle", 1991, 292, []),
    ]),
    ("Yoko Tawada", "ja", ["Literary Fiction"], [
        ("The Bridegroom Was a Dog", 1993, 112, []),
        ("Where Europe Begins", 2002, 208, ["Short Stories"]),
        ("The Naked Eye", 2004, 200, []),
        ("Memoirs of a Polar Bear", 2011, 312, []),
        ("The Emissary", 2014, 138, ["Science Fiction"]),
        ("Scattered All Over the Earth", 2022, 304, []),
    ]),
    ("Han Kang", "ko", ["Literary Fiction"], [
        ("The Vegetarian", 2007, 188, []),
        ("Human Acts", 2014, 216, ["Historical Fiction"]),
        ("The White Book", 2016, 160, []),
        ("Greek Lessons", 2023, 187, []),
        ("We Do Not Part", 2021, 280, []),
    ]),
    ("Hideo Levy", "ja", ["Literary Fiction"], [
        ("A Room Where the Star-Spangled Banner Cannot Be Heard", 1992, 180, []),
        ("The Gate of the Country of Stars", 2003, 256, []),
    ]),
    ("Sayaka Murata", "ja", ["Literary Fiction"], [
        ("Convenience Store Woman", 2016, 163, []),
        ("Earthlings", 2018, 238, []),
        ("Life Ceremony", 2019, 198, ["Short Stories"]),
    ]),
    ("Mieko Kawakami", "ja", ["Literary Fiction"], [
        ("Breasts and Eggs", 2020, 430, []),
        ("Heaven", 2009, 194, []),
        ("All the Lovers in the Night", 2011, 224, []),
    ]),
    # Middle Eastern literature
    ("Amin Maalouf", "fr", ["Literary Fiction", "Historical Fiction"], [
        ("Leo Africanus", 1986, 346, []),
        ("Samarkand", 1988, 311, []),
        ("The Rock of Tanios", 1993, 279, []),
        ("Ports of Call", 1996, 341, []),
        ("Balthasar's Odyssey", 2000, 391, []),
        ("The Crusades Through Arab Eyes", 1983, 293, ["History"]),
        ("In the Name of Identity", 1996, 164, ["Non-Fiction"]),
        ("The Gardens of Light", 1991, 261, []),
        ("Adrift", 2020, 256, ["Non-Fiction"]),
    ]),
    ("Hanan al-Shaykh", "ar", ["Literary Fiction"], [
        ("The Story of Zahra", 1980, 247, []),
        ("Women of Sand and Myrrh", 1989, 323, []),
        ("Beirut Blues", 1992, 359, []),
        ("Only in London", 2001, 305, []),
        ("One Thousand and One Nights", 2011, 317, []),
    ]),
    ("Orhan Pamuk", "tr", ["Literary Fiction"], [
        ("Cevdet Bey and His Sons", 1982, 550, []),
        ("The Silent House", 1983, 334, []),
    ]),
    # Caribbean
    ("Derek Walcott", "en", ["Poetry", "Caribbean Literature"], [
        ("In a Green Night", 1962, 88, []),
        ("The Castaway", 1965, 64, []),
        ("Another Life", 1973, 153, []),
        ("The Star-Apple Kingdom", 1979, 58, []),
        ("Midsummer", 1984, 53, []),
        ("The Arkansas Testament", 1987, 117, []),
        ("Omeros", 1990, 325, ["Epic", "Classic"]),
        ("The Bounty", 1997, 79, []),
        ("Tiepolo's Hound", 2000, 164, []),
        ("White Egrets", 2010, 86, []),
    ]),
    ("Edwidge Danticat", "en", ["Literary Fiction", "Caribbean Literature"], [
        ("Breath, Eyes, Memory", 1994, 234, []),
        ("Krik? Krak!", 1995, 224, ["Short Stories"]),
        ("The Farming of Bones", 1998, 312, ["Historical Fiction"]),
        ("The Dew Breaker", 2004, 244, []),
        ("Brother, I'm Dying", 2007, 272, ["Memoir"]),
        ("Create Dangerously", 2010, 189, ["Non-Fiction"]),
        ("Claire of the Sea Light", 2013, 256, []),
        ("Everything Inside", 2019, 224, ["Short Stories"]),
    ]),
    # Australian
    ("Peter Carey", "en", ["Literary Fiction"], [
        ("Bliss", 1981, 304, []),
        ("Illywhacker", 1985, 600, []),
        ("Oscar and Lucinda", 1988, 518, []),
        ("The Tax Inspector", 1991, 310, []),
        ("The Unusual Life of Tristan Smith", 1994, 398, []),
        ("Jack Maggs", 1997, 326, ["Historical Fiction"]),
        ("True History of the Kelly Gang", 2000, 355, ["Historical Fiction"]),
        ("My Life as a Fake", 2003, 274, []),
        ("Theft: A Love Story", 2006, 271, []),
        ("His Illegal Self", 2008, 262, []),
        ("Parrot and Olivier in America", 2009, 379, ["Historical Fiction"]),
        ("The Chemistry of Tears", 2012, 251, []),
        ("Amnesia", 2014, 384, []),
        ("A Long Way from Home", 2017, 291, []),
    ]),
    ("Tim Winton", "en", ["Literary Fiction"], [
        ("An Open Swimmer", 1982, 175, []),
        ("Shallows", 1984, 248, []),
        ("That Eye, the Sky", 1986, 173, []),
        ("In the Winter Dark", 1988, 150, []),
        ("Cloudstreet", 1991, 426, ["Classic"]),
        ("The Riders", 1994, 377, []),
        ("Dirt Music", 2001, 411, []),
        ("Breath", 2008, 218, []),
        ("Eyrie", 2013, 424, []),
        ("The Shepherd's Hut", 2018, 265, []),
        ("Juice", 2024, 496, []),
        ("The Turning", 2004, 318, ["Short Stories"]),
    ]),
    # Scandinavian crime/noir
    ("Arnaldur Indriðason", "is", ["Mystery", "Crime Fiction"], [
        ("Sons of Dust", 1997, 320, []),
        ("Silent Kill", 1998, 330, []),
        ("Jar City", 2000, 314, []),
        ("Silence of the Grave", 2001, 312, []),
        ("Voices", 2002, 308, []),
        ("The Draining Lake", 2004, 312, []),
        ("Arctic Chill", 2005, 295, []),
        ("Hypothermia", 2007, 312, []),
        ("Outrage", 2008, 304, []),
        ("Black Skies", 2009, 320, []),
        ("Strange Shores", 2010, 288, []),
        ("Reykjavik Nights", 2012, 288, []),
        ("Into Oblivion", 2014, 288, []),
        ("The Shadow District", 2013, 288, []),
        ("The Shadow Killer", 2015, 304, []),
    ]),
    ("Camilla Läckberg", "sv", ["Mystery", "Thriller"], [
        ("The Ice Princess", 2003, 392, []),
        ("The Preacher", 2004, 404, []),
        ("The Stonecutter", 2005, 416, []),
        ("The Stranger", 2008, 452, []),
        ("The Hidden Child", 2007, 456, []),
        ("The Drowning", 2008, 420, []),
        ("The Lost Boy", 2009, 432, []),
        ("Buried Angels", 2011, 464, []),
        ("The Ice Child", 2013, 432, []),
        ("The Girl in the Woods", 2017, 432, []),
        ("The Gilded Cage", 2019, 496, []),
        ("Silver Tears", 2020, 448, []),
        ("Wings of Silver", 2021, 432, []),
    ]),
    ("Jussi Adler-Olsen", "da", ["Mystery", "Thriller"], [
        ("The Keeper of Lost Causes", 2007, 396, []),
        ("The Absent One", 2008, 466, []),
        ("A Conspiracy of Faith", 2009, 480, []),
        ("The Purity of Vengeance", 2010, 496, []),
        ("The Marco Effect", 2012, 544, []),
        ("The Hanging Girl", 2014, 530, []),
        ("The Scarred Woman", 2017, 560, []),
        ("Victim 2117", 2019, 559, []),
        ("The Shadow Murders", 2021, 512, []),
    ]),
    # Eastern European
    ("Olga Tokarczuk", "pl", ["Literary Fiction"], [
        ("Primeval and Other Times", 1996, 248, ["Magical Realism"]),
        ("House of Day, House of Night", 1998, 384, []),
        ("Flights", 2007, 403, []),
        ("Drive Your Plow Over the Bones of the Dead", 2009, 242, ["Mystery"]),
        ("The Books of Jacob", 2014, 912, ["Historical Fiction"]),
    ]),
    ("Dubravka Ugrešić", "hr", ["Literary Fiction"], [
        ("The Museum of Unconditional Surrender", 1996, 290, []),
        ("The Ministry of Pain", 2004, 270, []),
        ("Baba Yaga Laid an Egg", 2008, 340, []),
        ("Fox", 2017, 242, []),
        ("The Culture of Lies", 1998, 256, ["Non-Fiction"]),
    ]),
    ("László Krasznahorkai", "hu", ["Literary Fiction"], [
        ("Satantango", 1985, 274, []),
        ("The Melancholy of Resistance", 1989, 316, []),
        ("War & War", 1999, 287, []),
        ("Seiobo There Below", 2008, 444, []),
        ("Baron Wenckheim's Homecoming", 2016, 567, []),
    ]),
    # More contemporary global fiction
    ("Mohsin Hamid", "en", ["Literary Fiction"], [
        ("Moth Smoke", 2000, 247, []),
        ("The Reluctant Fundamentalist", 2007, 184, []),
        ("How to Get Filthy Rich in Rising Asia", 2013, 228, []),
        ("Exit West", 2017, 231, ["Magical Realism"]),
        ("The Last White Man", 2022, 192, []),
    ]),
    ("Kamila Shamsie", "en", ["Literary Fiction"], [
        ("In the City by the Sea", 1998, 199, []),
        ("Salt and Saffron", 2000, 245, []),
        ("Kartography", 2002, 305, []),
        ("Broken Verses", 2005, 346, []),
        ("Burnt Shadows", 2009, 366, ["Historical Fiction"]),
        ("A God in Every Stone", 2014, 289, ["Historical Fiction"]),
        ("Home Fire", 2017, 276, []),
        ("Best of Friends", 2022, 277, []),
    ]),
    ("Elif Shafak", "en", ["Literary Fiction"], [
        ("The Flea Palace", 2002, 384, []),
        ("The Saint of Incipient Insanities", 2004, 356, []),
        ("The Bastard of Istanbul", 2006, 360, []),
        ("The Forty Rules of Love", 2009, 354, ["Historical Fiction"]),
        ("Honour", 2012, 352, []),
        ("The Architect's Apprentice", 2013, 387, ["Historical Fiction"]),
        ("Three Daughters of Eve", 2016, 383, []),
        ("10 Minutes 38 Seconds in This Strange World", 2019, 303, []),
        ("The Island of Missing Trees", 2021, 352, []),
    ]),
    ("Ngũgĩ wa Thiong'o", "en", ["Literary Fiction", "African Literature"], [
        ("The River Between", 1965, 152, []),
    ]),
    ("Tayeb Salih", "ar", ["Literary Fiction"], [
        ("Season of Migration to the North", 1966, 169, ["Classic"]),
        ("The Wedding of Zein", 1969, 142, ["Short Stories"]),
        ("Bandarshah", 1971, 185, []),
    ]),
    ("Naguib Mahfouz", "ar", ["Literary Fiction"], [
        ("Autumn Quail", 1962, 166, []),
        ("Respected Sir", 1975, 148, []),
        ("Arabian Nights and Days", 1982, 227, []),
    ]),
    ("R.K. Narayan", "en", ["Literary Fiction", "Indian Fiction", "Classic"], [
        ("Swami and Friends", 1935, 181, []),
        ("The Bachelor of Arts", 1937, 223, []),
        ("The Dark Room", 1938, 159, []),
        ("The English Teacher", 1945, 184, []),
        ("Mr. Sampath", 1949, 205, []),
        ("The Financial Expert", 1952, 219, []),
        ("Waiting for the Mahatma", 1955, 256, []),
        ("The Guide", 1958, 220, []),
        ("The Man-Eater of Malgudi", 1961, 183, []),
        ("The Vendor of Sweets", 1967, 184, []),
        ("The Painter of Signs", 1976, 176, []),
        ("A Tiger for Malgudi", 1983, 178, []),
        ("Talkative Man", 1986, 128, []),
        ("The World of Nagaraj", 1990, 170, []),
        ("Malgudi Days", 1943, 256, ["Short Stories"]),
        ("My Days", 1974, 176, ["Memoir"]),
    ]),
    ("Mulk Raj Anand", "en", ["Literary Fiction", "Indian Fiction", "Classic"], [
        ("Untouchable", 1935, 156, []),
        ("Coolie", 1936, 283, []),
        ("Two Leaves and a Bud", 1937, 274, []),
        ("The Village", 1939, 296, []),
        ("Across the Black Waters", 1940, 254, []),
        ("The Sword and the Sickle", 1942, 350, []),
        ("The Big Heart", 1945, 206, []),
        ("The Private Life of an Indian Prince", 1953, 272, []),
    ]),
    ("Raja Rao", "en", ["Literary Fiction", "Indian Fiction", "Classic"], [
        ("Kanthapura", 1938, 200, []),
        ("The Serpent and the Rope", 1960, 399, []),
        ("The Cat and Shakespeare", 1965, 129, []),
        ("Comrade Kirillov", 1976, 179, []),
        ("The Chessmaster and His Moves", 1988, 640, []),
    ]),
    ("Ismat Chughtai", "en", ["Literary Fiction", "Indian Fiction"], [
        ("The Quilt and Other Stories", 1994, 207, ["Short Stories"]),
        ("The Crooked Line", 1944, 307, []),
        ("The Wild One", 1955, 257, []),
        ("A Life in Words", 2012, 312, ["Memoir"]),
    ]),
    ("Saadat Hasan Manto", "en", ["Literary Fiction", "Indian Fiction", "Short Stories"], [
        ("Mottled Dawn", 1997, 214, []),
        ("Stars from Another Sky", 1998, 237, []),
        ("Kingdom's End and Other Stories", 1955, 182, []),
        ("Bitter Fruit", 2008, 250, []),
        ("Bombay Stories", 2012, 230, []),
    ]),
]


def generate():
    batch_num = 93
    books_in_batch = []

    for author, lang, default_genres, works in AUTHORS:
        for title, year, pages, extra_genres in works:
            genres = list(default_genres) + extra_genres
            book = make_book(title, author, year, pages, genres, lang)
            books_in_batch.append(book)

            if len(books_in_batch) >= 100:
                fname = f"batch_{batch_num:02d}_world_{batch_num - 92}.json"
                path = os.path.join(BATCH_DIR, fname)
                with open(path, "w") as f:
                    json.dump(books_in_batch, f, indent=2)
                print(f"  {fname}: {len(books_in_batch)} books")
                batch_num += 1
                books_in_batch = []

    if books_in_batch:
        fname = f"batch_{batch_num:02d}_world_{batch_num - 92}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(books_in_batch, f, indent=2)
        print(f"  {fname}: {len(books_in_batch)} books")
        batch_num += 1

    total = sum(len(works) for _, _, _, works in AUTHORS)
    print(f"\nTotal new books: {total}")


if __name__ == "__main__":
    generate()
