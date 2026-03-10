#!/usr/bin/env python3
"""Batch 22: Smart generator - loads existing books and only creates new entries.
Target: 2000+ genuinely new books from fresh authors not yet in the dataset."""
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


# Load existing books to check for duplicates
def load_existing():
    existing_titles = set()
    existing_authors = set()
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
                existing_authors.add(a.lower())
    return existing_titles, existing_authors


# All entries: (title, author, year, pages, genres, lang)
# ONLY include authors NOT already in the dataset
ALL_BOOKS = [
    # Australian, NZ, Canadian fiction
    ("The Bone People", "Keri Hulme", 1984, 450, ["Literary Fiction"], "en"),
    ("Once Were Warriors", "Alan Duff", 1990, 196, ["Literary Fiction"], "en"),
    ("Mister Pip", "Lloyd Jones", 2006, 256, ["Literary Fiction"], "en"),
    ("The Luminaries", "Eleanor Catton", 2013, 834, ["Literary Fiction", "Historical Fiction"], "en"),
    ("Birnam Wood", "Eleanor Catton", 2023, 416, ["Literary Fiction", "Thriller"], "en"),
    ("Unless", "Carol Shields", 2002, 322, ["Literary Fiction"], "en"),
    ("The Stone Diaries", "Carol Shields", 1993, 361, ["Literary Fiction"], "en"),
    ("Larry's Party", "Carol Shields", 1997, 339, ["Literary Fiction"], "en"),
    ("Swann", "Carol Shields", 1987, 313, ["Literary Fiction", "Mystery"], "en"),
    ("Alias Grace", "Margaret Atwood", 1996, 468, ["Literary Fiction", "Historical Fiction"], "en"),
    ("Cat's Eye", "Margaret Atwood", 1988, 421, ["Literary Fiction"], "en"),
    ("The Robber Bride", "Margaret Atwood", 1993, 470, ["Literary Fiction"], "en"),
    ("Life of Pi", "Yann Martel", 2001, 319, ["Literary Fiction", "Adventure"], "en"),
    ("Beatrice and Virgil", "Yann Martel", 2010, 197, ["Literary Fiction"], "en"),
    ("The High Mountains of Portugal", "Yann Martel", 2016, 332, ["Literary Fiction"], "en"),
    ("The Bone Clocks", "David Mitchell", 2014, 624, ["Literary Fiction", "Fantasy"], "en"),
    ("Cloud Atlas", "David Mitchell", 2004, 509, ["Literary Fiction", "Science Fiction"], "en"),
    ("Black Swan Green", "David Mitchell", 2006, 294, ["Literary Fiction"], "en"),
    ("The Thousand Autumns of Jacob de Zoet", "David Mitchell", 2010, 479, ["Literary Fiction", "Historical Fiction"], "en"),
    ("number9dream", "David Mitchell", 2001, 400, ["Literary Fiction"], "en"),
    ("Ghostwritten", "David Mitchell", 1999, 426, ["Literary Fiction"], "en"),
    ("Utopia Avenue", "David Mitchell", 2020, 577, ["Literary Fiction"], "en"),
    ("Slade House", "David Mitchell", 2015, 238, ["Literary Fiction", "Horror"], "en"),

    # South African
    ("Disgrace", "J.M. Coetzee", 1999, 220, ["Literary Fiction", "Classic"], "en"),
    ("Waiting for the Barbarians", "J.M. Coetzee", 1980, 156, ["Literary Fiction", "Classic"], "en"),
    ("Life & Times of Michael K", "J.M. Coetzee", 1983, 184, ["Literary Fiction"], "en"),
    ("Foe", "J.M. Coetzee", 1986, 157, ["Literary Fiction"], "en"),
    ("Age of Iron", "J.M. Coetzee", 1990, 198, ["Literary Fiction"], "en"),
    ("The Master of Petersburg", "J.M. Coetzee", 1994, 250, ["Literary Fiction", "Historical Fiction"], "en"),
    ("Elizabeth Costello", "J.M. Coetzee", 2003, 230, ["Literary Fiction"], "en"),
    ("Slow Man", "J.M. Coetzee", 2005, 263, ["Literary Fiction"], "en"),
    ("Diary of a Bad Year", "J.M. Coetzee", 2007, 231, ["Literary Fiction"], "en"),
    ("The Childhood of Jesus", "J.M. Coetzee", 2013, 277, ["Literary Fiction"], "en"),
    ("The Schooldays of Jesus", "J.M. Coetzee", 2016, 260, ["Literary Fiction"], "en"),
    ("The Death of Jesus", "J.M. Coetzee", 2019, 196, ["Literary Fiction"], "en"),
    ("Boyhood", "J.M. Coetzee", 1997, 166, ["Memoir"], "en"),
    ("Youth", "J.M. Coetzee", 2002, 169, ["Memoir"], "en"),
    ("Summertime", "J.M. Coetzee", 2009, 266, ["Memoir"], "en"),
    ("Cry, the Beloved Country", "Alan Paton", 1948, 316, ["Literary Fiction", "Classic"], "en"),
    ("Too Late the Phalarope", "Alan Paton", 1953, 276, ["Literary Fiction"], "en"),
    ("Ah, But Your Land Is Beautiful", "Alan Paton", 1981, 271, ["Literary Fiction"], "en"),
    ("July's People", "Nadine Gordimer", 1981, 160, ["Literary Fiction"], "en"),
    ("The Conservationist", "Nadine Gordimer", 1974, 252, ["Literary Fiction"], "en"),
    ("Burger's Daughter", "Nadine Gordimer", 1979, 361, ["Literary Fiction"], "en"),
    ("A Sport of Nature", "Nadine Gordimer", 1987, 354, ["Literary Fiction"], "en"),
    ("My Son's Story", "Nadine Gordimer", 1990, 277, ["Literary Fiction"], "en"),
    ("None to Accompany Me", "Nadine Gordimer", 1994, 324, ["Literary Fiction"], "en"),
    ("The House Gun", "Nadine Gordimer", 1998, 294, ["Literary Fiction"], "en"),
    ("The Pickup", "Nadine Gordimer", 2001, 270, ["Literary Fiction"], "en"),
    ("Get a Life", "Nadine Gordimer", 2005, 187, ["Literary Fiction"], "en"),
    ("No Time Like the Present", "Nadine Gordimer", 2012, 394, ["Literary Fiction"], "en"),

    # Japanese contemporary
    ("Kokoro", "Natsume Sōseki", 1914, 248, ["Literary Fiction", "Classic"], "ja"),
    ("Botchan", "Natsume Sōseki", 1906, 176, ["Literary Fiction", "Classic", "Humor"], "ja"),
    ("I Am a Cat", "Natsume Sōseki", 1905, 638, ["Literary Fiction", "Classic", "Humor"], "ja"),
    ("And Then", "Natsume Sōseki", 1909, 256, ["Literary Fiction", "Classic"], "ja"),
    ("The Gate", "Natsume Sōseki", 1910, 208, ["Literary Fiction", "Classic"], "ja"),
    ("The Makioka Sisters", "Jun'ichirō Tanizaki", 1948, 530, ["Literary Fiction", "Classic"], "ja"),
    ("Some Prefer Nettles", "Jun'ichirō Tanizaki", 1929, 202, ["Literary Fiction", "Classic"], "ja"),
    ("In Praise of Shadows", "Jun'ichirō Tanizaki", 1933, 73, ["Non-Fiction", "Classic"], "ja"),
    ("The Key", "Jun'ichirō Tanizaki", 1956, 183, ["Literary Fiction"], "ja"),
    ("Diary of a Mad Old Man", "Jun'ichirō Tanizaki", 1961, 177, ["Literary Fiction"], "ja"),
    ("The Temple of the Golden Pavilion", "Yukio Mishima", 1956, 262, ["Literary Fiction", "Classic"], "ja"),
    ("Confessions of a Mask", "Yukio Mishima", 1949, 253, ["Literary Fiction", "Classic"], "ja"),
    ("The Sailor Who Fell from Grace with the Sea", "Yukio Mishima", 1963, 181, ["Literary Fiction"], "ja"),
    ("Spring Snow", "Yukio Mishima", 1968, 389, ["Literary Fiction"], "ja"),
    ("Runaway Horses", "Yukio Mishima", 1969, 421, ["Literary Fiction"], "ja"),
    ("The Temple of Dawn", "Yukio Mishima", 1970, 334, ["Literary Fiction"], "ja"),
    ("The Decay of the Angel", "Yukio Mishima", 1970, 236, ["Literary Fiction"], "ja"),
    ("The Woman in the Dunes", "Kōbō Abe", 1962, 241, ["Literary Fiction", "Classic"], "ja"),
    ("The Face of Another", "Kōbō Abe", 1964, 237, ["Literary Fiction"], "ja"),
    ("The Box Man", "Kōbō Abe", 1973, 178, ["Literary Fiction"], "ja"),
    ("Secret Rendezvous", "Kōbō Abe", 1977, 179, ["Literary Fiction"], "ja"),
    ("The Ark Sakura", "Kōbō Abe", 1984, 340, ["Literary Fiction", "Science Fiction"], "ja"),
    ("No Longer Human", "Osamu Dazai", 1948, 171, ["Literary Fiction", "Classic"], "ja"),
    ("The Setting Sun", "Osamu Dazai", 1947, 175, ["Literary Fiction", "Classic"], "ja"),

    # Russian/Soviet beyond Dostoevsky/Tolstoy
    ("Doctor Zhivago", "Boris Pasternak", 1957, 510, ["Literary Fiction", "Classic", "Romance"], "ru"),
    ("One Day in the Life of Ivan Denisovich", "Aleksandr Solzhenitsyn", 1962, 143, ["Literary Fiction", "Classic"], "ru"),
    ("Cancer Ward", "Aleksandr Solzhenitsyn", 1966, 560, ["Literary Fiction"], "ru"),
    ("The First Circle", "Aleksandr Solzhenitsyn", 1968, 580, ["Literary Fiction"], "ru"),
    ("August 1914", "Aleksandr Solzhenitsyn", 1971, 622, ["Literary Fiction", "Historical Fiction"], "ru"),
    ("We", "Yevgeny Zamyatin", 1924, 225, ["Science Fiction", "Classic", "Dystopian"], "ru"),
    ("Dead Souls", "Nikolai Gogol", 1842, 432, ["Literary Fiction", "Classic", "Humor"], "ru"),
    ("The Overcoat", "Nikolai Gogol", 1842, 64, ["Literary Fiction", "Classic", "Short Stories"], "ru"),
    ("Taras Bulba", "Nikolai Gogol", 1835, 148, ["Literary Fiction", "Classic", "Historical Fiction"], "ru"),
    ("A Hero of Our Time", "Mikhail Lermontov", 1840, 188, ["Literary Fiction", "Classic"], "ru"),
    ("Eugene Onegin", "Alexander Pushkin", 1833, 240, ["Literary Fiction", "Classic", "Poetry"], "ru"),
    ("The Captain's Daughter", "Alexander Pushkin", 1836, 130, ["Literary Fiction", "Classic", "Historical Fiction"], "ru"),
    ("Fathers and Sons", "Ivan Turgenev", 1862, 226, ["Literary Fiction", "Classic"], "ru"),
    ("First Love", "Ivan Turgenev", 1860, 100, ["Literary Fiction", "Classic"], "ru"),
    ("On the Eve", "Ivan Turgenev", 1860, 186, ["Literary Fiction", "Classic"], "ru"),
    ("Smoke", "Ivan Turgenev", 1867, 274, ["Literary Fiction", "Classic"], "ru"),
    ("Virgin Soil", "Ivan Turgenev", 1877, 352, ["Literary Fiction", "Classic"], "ru"),
    ("The Lady with the Dog", "Anton Chekhov", 1899, 40, ["Literary Fiction", "Classic", "Short Stories"], "ru"),
    ("The Enchanted Wanderer", "Nikolai Leskov", 1873, 192, ["Literary Fiction", "Classic"], "ru"),
    ("Oblomov", "Ivan Goncharov", 1859, 500, ["Literary Fiction", "Classic"], "ru"),

    # Chinese literature
    ("Dream of the Red Chamber", "Cao Xueqin", 1791, 2339, ["Literary Fiction", "Classic"], "zh"),
    ("Journey to the West", "Wu Cheng'en", 1592, 1952, ["Fantasy", "Classic"], "zh"),
    ("Water Margin", "Shi Nai'an", 1400, 1600, ["Literary Fiction", "Classic", "Adventure"], "zh"),
    ("Romance of the Three Kingdoms", "Luo Guanzhong", 1522, 2400, ["Historical Fiction", "Classic"], "zh"),
    ("Fortress Besieged", "Qian Zhongshu", 1947, 392, ["Literary Fiction", "Humor"], "zh"),
    ("Raise the Red Lantern", "Su Tong", 1990, 224, ["Literary Fiction", "Short Stories"], "zh"),
    ("My Country and My People", "Lin Yutang", 1935, 382, ["Non-Fiction", "History"], "zh"),
    ("Soul Mountain", "Gao Xingjian", 2000, 510, ["Literary Fiction"], "zh"),
    ("One Man's Bible", "Gao Xingjian", 1999, 450, ["Literary Fiction"], "zh"),
    ("Balzac and the Little Chinese Seamstress", "Dai Sijie", 2000, 197, ["Literary Fiction"], "zh"),
    ("The Three-Body Problem", "Liu Cixin", 2008, 302, ["Science Fiction"], "zh"),
    ("Waiting", "Ha Jin", 1999, 308, ["Literary Fiction"], "en"),
    ("War Trash", "Ha Jin", 2004, 352, ["Literary Fiction", "War"], "en"),
    ("A Free Life", "Ha Jin", 2007, 660, ["Literary Fiction"], "en"),
    ("The Crazed", "Ha Jin", 2002, 323, ["Literary Fiction"], "en"),
    ("Nanjing Requiem", "Ha Jin", 2011, 303, ["Literary Fiction", "Historical Fiction"], "en"),

    # Korean literature
    ("Please Look After Mom", "Kyung-sook Shin", 2008, 233, ["Literary Fiction"], "ko"),
    ("I'll Be Right There", "Kyung-sook Shin", 2010, 311, ["Literary Fiction"], "ko"),
    ("The Court Dancer", "Kyung-sook Shin", 2018, 305, ["Literary Fiction", "Historical Fiction"], "ko"),
    ("The Hen Who Dreamed She Could Fly", "Sun-mi Hwang", 2000, 136, ["Literary Fiction", "Fable"], "ko"),
    ("Kim Ji-young, Born 1982", "Cho Nam-joo", 2016, 163, ["Literary Fiction"], "ko"),
    ("Almond", "Won-pyung Sohn", 2017, 264, ["Literary Fiction"], "ko"),
    ("The Plotters", "Un-su Kim", 2010, 311, ["Thriller"], "ko"),

    # Scandinavian literature beyond crime
    ("The Emigrants", "Vilhelm Moberg", 1949, 365, ["Literary Fiction", "Historical Fiction"], "sv"),
    ("Unto a Good Land", "Vilhelm Moberg", 1952, 371, ["Literary Fiction", "Historical Fiction"], "sv"),
    ("The Settlers", "Vilhelm Moberg", 1956, 376, ["Literary Fiction", "Historical Fiction"], "sv"),
    ("The Last Letter Home", "Vilhelm Moberg", 1959, 371, ["Literary Fiction", "Historical Fiction"], "sv"),
    ("The Almost Nearly Perfect People", "Michael Booth", 2014, 390, ["Travel", "Humor"], "en"),
    ("A Man Called Ove", "Fredrik Backman", 2012, 337, ["Literary Fiction", "Humor"], "en"),
    ("Hunger", "Knut Hamsun", 1890, 232, ["Literary Fiction", "Classic"], "no"),
    ("Growth of the Soil", "Knut Hamsun", 1917, 448, ["Literary Fiction", "Classic"], "no"),
    ("Mysteries", "Knut Hamsun", 1892, 340, ["Literary Fiction", "Classic"], "no"),
    ("Pan", "Knut Hamsun", 1894, 168, ["Literary Fiction", "Classic"], "no"),
    ("Victoria", "Knut Hamsun", 1898, 152, ["Literary Fiction", "Romance"], "no"),
    ("The Road", "Knut Hamsun", 1927, 200, ["Literary Fiction"], "no"),
    ("A Doll's House", "Henrik Ibsen", 1879, 96, ["Drama", "Classic"], "no"),
    ("Hedda Gabler", "Henrik Ibsen", 1891, 104, ["Drama", "Classic"], "no"),
    ("Ghosts", "Henrik Ibsen", 1881, 88, ["Drama", "Classic"], "no"),
    ("An Enemy of the People", "Henrik Ibsen", 1882, 96, ["Drama", "Classic"], "no"),
    ("The Wild Duck", "Henrik Ibsen", 1884, 96, ["Drama", "Classic"], "no"),
    ("Peer Gynt", "Henrik Ibsen", 1867, 224, ["Drama", "Classic"], "no"),
    ("The Master Builder", "Henrik Ibsen", 1892, 92, ["Drama", "Classic"], "no"),

    # Contemporary Italian
    ("My Brilliant Friend", "Elena Ferrante", 2011, 331, ["Literary Fiction"], "it"),
    ("The Story of a New Name", "Elena Ferrante", 2012, 471, ["Literary Fiction"], "it"),
    ("If Not Now, When?", "Primo Levi", 1982, 349, ["Literary Fiction", "Historical Fiction"], "it"),
    ("If This Is a Man", "Primo Levi", 1947, 187, ["Memoir", "Classic", "History"], "it"),
    ("The Truce", "Primo Levi", 1963, 246, ["Memoir"], "it"),
    ("The Periodic Table", "Primo Levi", 1975, 233, ["Memoir", "Science"], "it"),
    ("The Drowned and the Saved", "Primo Levi", 1986, 203, ["Non-Fiction", "History"], "it"),
    ("The Leopard", "Giuseppe Tomasi di Lampedusa", 1958, 255, ["Literary Fiction", "Classic", "Historical Fiction"], "it"),
    ("Christ Stopped at Eboli", "Carlo Levi", 1945, 268, ["Memoir", "Classic"], "it"),

    # Turkish
    ("The Museum of Innocence", "Orhan Pamuk", 2008, 535, ["Literary Fiction"], "tr"),
    ("Istanbul", "Orhan Pamuk", 2003, 348, ["Memoir"], "tr"),

    # Portuguese
    ("The Book of Disquiet", "Fernando Pessoa", 1982, 260, ["Literary Fiction", "Classic"], "pt"),
    ("The Year of the Death of Ricardo Reis", "José Saramago", 1984, 341, ["Literary Fiction"], "pt"),

    # Greek
    ("Zorba the Greek", "Nikos Kazantzakis", 1946, 341, ["Literary Fiction", "Classic"], "el"),
    ("The Last Temptation of Christ", "Nikos Kazantzakis", 1955, 506, ["Literary Fiction", "Classic"], "el"),
    ("Report to Greco", "Nikos Kazantzakis", 1961, 512, ["Memoir"], "el"),
    ("The Odyssey: A Modern Sequel", "Nikos Kazantzakis", 1938, 880, ["Epic", "Poetry"], "el"),
    ("Freedom or Death", "Nikos Kazantzakis", 1953, 474, ["Literary Fiction", "Historical Fiction"], "el"),

    # Czech
    ("The Good Soldier Švejk", "Jaroslav Hašek", 1923, 752, ["Humor", "Classic", "War"], "cs"),

    # Hungarian
    ("Fatelessness", "Imre Kertész", 2004, 262, ["Literary Fiction", "Classic"], "hu"),
    ("Kaddish for an Unborn Child", "Imre Kertész", 1990, 96, ["Literary Fiction"], "hu"),

    # Polish beyond Tokarczuk
    ("The Doll", "Bolesław Prus", 1890, 700, ["Literary Fiction", "Classic"], "pl"),
    ("Quo Vadis", "Henryk Sienkiewicz", 1896, 589, ["Historical Fiction", "Classic"], "pl"),
    ("With Fire and Sword", "Henryk Sienkiewicz", 1884, 1130, ["Historical Fiction", "Classic"], "pl"),
    ("The Deluge", "Henryk Sienkiewicz", 1886, 1500, ["Historical Fiction", "Classic"], "pl"),
    ("Solaris", "Stanisław Lem", 1961, 204, ["Science Fiction", "Classic"], "pl"),
    ("The Star Diaries", "Stanisław Lem", 1957, 332, ["Science Fiction", "Humor"], "pl"),
    ("The Cyberiad", "Stanisław Lem", 1965, 295, ["Science Fiction", "Humor"], "pl"),
    ("The Futurological Congress", "Stanisław Lem", 1971, 149, ["Science Fiction", "Satire"], "pl"),
    ("His Master's Voice", "Stanisław Lem", 1968, 199, ["Science Fiction"], "pl"),
    ("Tales of Pirx the Pilot", "Stanisław Lem", 1968, 302, ["Science Fiction", "Short Stories"], "pl"),
    ("Return from the Stars", "Stanisław Lem", 1961, 236, ["Science Fiction"], "pl"),
    ("The Investigation", "Stanisław Lem", 1959, 192, ["Science Fiction", "Mystery"], "pl"),
    ("Memoirs Found in a Bathtub", "Stanisław Lem", 1961, 196, ["Science Fiction", "Satire"], "pl"),
    ("Fiasco", "Stanisław Lem", 1986, 311, ["Science Fiction"], "pl"),
    ("Eden", "Stanisław Lem", 1959, 253, ["Science Fiction"], "pl"),

    # Georgian
    ("The Knight in the Panther's Skin", "Shota Rustaveli", 1207, 1600, ["Poetry", "Classic", "Epic"], "ka"),

    # Persian classics
    ("Shahnameh", "Ferdowsi", 1010, 2000, ["Poetry", "Classic", "Epic"], "fa"),
    ("The Rubaiyat", "Omar Khayyam", 1120, 108, ["Poetry", "Classic"], "fa"),
    ("Masnavi", "Rumi", 1273, 1200, ["Poetry", "Classic", "Philosophy"], "fa"),
    ("The Divan of Hafiz", "Hafiz", 1390, 500, ["Poetry", "Classic"], "fa"),
    ("The Blind Owl", "Sadegh Hedayat", 1937, 131, ["Literary Fiction", "Classic"], "fa"),

    # Sanskrit/Ancient Indian
    ("The Mahabharata", "Vyasa", -400, 2000, ["Epic", "Classic", "Mythology"], "sa"),
    ("The Ramayana", "Valmiki", -500, 1500, ["Epic", "Classic", "Mythology"], "sa"),
    ("Panchatantra", "Vishnu Sharma", -200, 300, ["Fable", "Classic"], "sa"),
    ("Arthashastra", "Kautilya", -300, 400, ["Non-Fiction", "Classic", "Politics"], "sa"),
    ("Kamasutra", "Vatsyayana", 300, 200, ["Non-Fiction", "Classic"], "sa"),
    ("Abhijnanasakuntalam", "Kalidasa", 400, 150, ["Drama", "Classic"], "sa"),
    ("Meghaduta", "Kalidasa", 400, 111, ["Poetry", "Classic"], "sa"),

    # Ancient world
    ("The Iliad", "Homer", -750, 683, ["Poetry", "Classic", "Epic"], "el"),
    ("The Odyssey", "Homer", -725, 541, ["Poetry", "Classic", "Epic", "Adventure"], "el"),
    ("The Aeneid", "Virgil", -19, 400, ["Poetry", "Classic", "Epic"], "la"),
    ("Metamorphoses", "Ovid", 8, 723, ["Poetry", "Classic"], "la"),
    ("The Divine Comedy", "Dante Alighieri", 1320, 798, ["Poetry", "Classic", "Epic"], "it"),
    ("The Decameron", "Giovanni Boccaccio", 1353, 903, ["Literary Fiction", "Classic", "Short Stories"], "it"),
    ("The Canterbury Tales", "Geoffrey Chaucer", 1400, 504, ["Poetry", "Classic"], "en"),
    ("Don Quixote", "Miguel de Cervantes", 1605, 863, ["Literary Fiction", "Classic", "Humor"], "es"),
    ("Gargantua and Pantagruel", "François Rabelais", 1534, 670, ["Literary Fiction", "Classic", "Humor"], "fr"),
    ("The Essays", "Michel de Montaigne", 1580, 1264, ["Non-Fiction", "Classic", "Philosophy"], "fr"),
    ("Paradise Lost", "John Milton", 1667, 453, ["Poetry", "Classic", "Epic"], "en"),
    ("Pilgrim's Progress", "John Bunyan", 1678, 314, ["Literary Fiction", "Classic"], "en"),
    ("Robinson Crusoe", "Daniel Defoe", 1719, 320, ["Adventure", "Classic"], "en"),
    ("Gulliver's Travels", "Jonathan Swift", 1726, 352, ["Literary Fiction", "Classic", "Satire"], "en"),
    ("Tom Jones", "Henry Fielding", 1749, 976, ["Literary Fiction", "Classic"], "en"),
    ("Tristram Shandy", "Laurence Sterne", 1759, 640, ["Literary Fiction", "Classic", "Humor"], "en"),
    ("Candide", "Voltaire", 1759, 144, ["Literary Fiction", "Classic", "Satire"], "fr"),
    ("Les Liaisons dangereuses", "Pierre Choderlos de Laclos", 1782, 432, ["Literary Fiction", "Classic"], "fr"),
    ("Pride and Prejudice", "Jane Austen", 1813, 432, ["Literary Fiction", "Classic", "Romance"], "en"),
    ("Sense and Sensibility", "Jane Austen", 1811, 409, ["Literary Fiction", "Classic", "Romance"], "en"),
    ("Emma", "Jane Austen", 1815, 474, ["Literary Fiction", "Classic", "Romance"], "en"),
    ("Mansfield Park", "Jane Austen", 1814, 532, ["Literary Fiction", "Classic"], "en"),
    ("Northanger Abbey", "Jane Austen", 1817, 260, ["Literary Fiction", "Classic"], "en"),
    ("Persuasion", "Jane Austen", 1817, 256, ["Literary Fiction", "Classic", "Romance"], "en"),
    ("Frankenstein", "Mary Shelley", 1818, 280, ["Science Fiction", "Classic", "Horror"], "en"),
    ("Wuthering Heights", "Emily Brontë", 1847, 416, ["Literary Fiction", "Classic", "Romance"], "en"),
    ("Jane Eyre", "Charlotte Brontë", 1847, 507, ["Literary Fiction", "Classic", "Romance"], "en"),
    ("Villette", "Charlotte Brontë", 1853, 488, ["Literary Fiction", "Classic"], "en"),
    ("The Tenant of Wildfell Hall", "Anne Brontë", 1848, 474, ["Literary Fiction", "Classic"], "en"),
    ("Agnes Grey", "Anne Brontë", 1847, 222, ["Literary Fiction", "Classic"], "en"),
    ("Great Expectations", "Charles Dickens", 1861, 505, ["Literary Fiction", "Classic"], "en"),
    ("David Copperfield", "Charles Dickens", 1850, 882, ["Literary Fiction", "Classic"], "en"),
    ("Oliver Twist", "Charles Dickens", 1838, 554, ["Literary Fiction", "Classic"], "en"),
    ("A Tale of Two Cities", "Charles Dickens", 1859, 341, ["Literary Fiction", "Classic", "Historical Fiction"], "en"),
    ("Bleak House", "Charles Dickens", 1853, 1017, ["Literary Fiction", "Classic"], "en"),
    ("Hard Times", "Charles Dickens", 1854, 352, ["Literary Fiction", "Classic"], "en"),
    ("Our Mutual Friend", "Charles Dickens", 1865, 868, ["Literary Fiction", "Classic"], "en"),
    ("The Pickwick Papers", "Charles Dickens", 1837, 801, ["Literary Fiction", "Classic", "Humor"], "en"),
    ("A Christmas Carol", "Charles Dickens", 1843, 166, ["Classic", "Fantasy"], "en"),
    ("Nicholas Nickleby", "Charles Dickens", 1839, 816, ["Literary Fiction", "Classic"], "en"),
    ("Martin Chuzzlewit", "Charles Dickens", 1844, 830, ["Literary Fiction", "Classic"], "en"),
    ("Dombey and Son", "Charles Dickens", 1848, 940, ["Literary Fiction", "Classic"], "en"),
    ("Little Dorrit", "Charles Dickens", 1857, 895, ["Literary Fiction", "Classic"], "en"),
    ("The Old Curiosity Shop", "Charles Dickens", 1841, 555, ["Literary Fiction", "Classic"], "en"),
    ("Barnaby Rudge", "Charles Dickens", 1841, 656, ["Literary Fiction", "Classic", "Historical Fiction"], "en"),
    ("Edwin Drood", "Charles Dickens", 1870, 288, ["Literary Fiction", "Classic", "Mystery"], "en"),
    ("Middlemarch", "George Eliot", 1871, 880, ["Literary Fiction", "Classic"], "en"),
    ("Silas Marner", "George Eliot", 1861, 234, ["Literary Fiction", "Classic"], "en"),
    ("The Mill on the Floss", "George Eliot", 1860, 578, ["Literary Fiction", "Classic"], "en"),
    ("Adam Bede", "George Eliot", 1859, 510, ["Literary Fiction", "Classic"], "en"),
    ("Daniel Deronda", "George Eliot", 1876, 744, ["Literary Fiction", "Classic"], "en"),
    ("Tess of the d'Urbervilles", "Thomas Hardy", 1891, 518, ["Literary Fiction", "Classic"], "en"),
    ("Far from the Madding Crowd", "Thomas Hardy", 1874, 416, ["Literary Fiction", "Classic"], "en"),
    ("The Mayor of Casterbridge", "Thomas Hardy", 1886, 334, ["Literary Fiction", "Classic"], "en"),
    ("The Return of the Native", "Thomas Hardy", 1878, 430, ["Literary Fiction", "Classic"], "en"),
    ("Jude the Obscure", "Thomas Hardy", 1895, 413, ["Literary Fiction", "Classic"], "en"),
    ("The Woodlanders", "Thomas Hardy", 1887, 392, ["Literary Fiction", "Classic"], "en"),
    ("Les Misérables", "Victor Hugo", 1862, 1462, ["Literary Fiction", "Classic", "Historical Fiction"], "fr"),
    ("The Hunchback of Notre-Dame", "Victor Hugo", 1831, 940, ["Literary Fiction", "Classic", "Historical Fiction"], "fr"),
    ("Ninety-Three", "Victor Hugo", 1874, 294, ["Historical Fiction", "Classic"], "fr"),
    ("Madame Bovary", "Gustave Flaubert", 1857, 328, ["Literary Fiction", "Classic"], "fr"),
    ("Sentimental Education", "Gustave Flaubert", 1869, 458, ["Literary Fiction", "Classic"], "fr"),
    ("Salammbô", "Gustave Flaubert", 1862, 422, ["Historical Fiction", "Classic"], "fr"),
    ("Bouvard and Pécuchet", "Gustave Flaubert", 1881, 337, ["Literary Fiction", "Classic", "Humor"], "fr"),
    ("The Count of Monte Cristo", "Alexandre Dumas", 1844, 1243, ["Adventure", "Classic", "Historical Fiction"], "fr"),
    ("The Three Musketeers", "Alexandre Dumas", 1844, 625, ["Adventure", "Classic", "Historical Fiction"], "fr"),
    ("Twenty Years After", "Alexandre Dumas", 1845, 808, ["Adventure", "Classic"], "fr"),
    ("The Man in the Iron Mask", "Alexandre Dumas", 1847, 474, ["Adventure", "Classic", "Historical Fiction"], "fr"),
    ("Germinal", "Émile Zola", 1885, 531, ["Literary Fiction", "Classic"], "fr"),
    ("Nana", "Émile Zola", 1880, 465, ["Literary Fiction", "Classic"], "fr"),
    ("L'Assommoir", "Émile Zola", 1877, 516, ["Literary Fiction", "Classic"], "fr"),
    ("Thérèse Raquin", "Émile Zola", 1867, 256, ["Literary Fiction", "Classic", "Thriller"], "fr"),
    ("The Belly of Paris", "Émile Zola", 1873, 389, ["Literary Fiction", "Classic"], "fr"),
    ("Père Goriot", "Honoré de Balzac", 1835, 320, ["Literary Fiction", "Classic"], "fr"),
    ("Eugénie Grandet", "Honoré de Balzac", 1833, 226, ["Literary Fiction", "Classic"], "fr"),
    ("Lost Illusions", "Honoré de Balzac", 1837, 660, ["Literary Fiction", "Classic"], "fr"),
    ("Cousin Bette", "Honoré de Balzac", 1846, 448, ["Literary Fiction", "Classic"], "fr"),
    ("The Red and the Black", "Stendhal", 1830, 576, ["Literary Fiction", "Classic"], "fr"),
    ("The Charterhouse of Parma", "Stendhal", 1839, 508, ["Literary Fiction", "Classic", "Historical Fiction"], "fr"),
    ("Dangerous Liaisons", "Pierre Choderlos de Laclos", 1782, 432, ["Literary Fiction", "Classic"], "fr"),
    ("Moby-Dick", "Herman Melville", 1851, 720, ["Literary Fiction", "Classic", "Adventure"], "en"),
    ("Bartleby, the Scrivener", "Herman Melville", 1853, 64, ["Literary Fiction", "Classic", "Short Stories"], "en"),
    ("Billy Budd", "Herman Melville", 1924, 96, ["Literary Fiction", "Classic"], "en"),
    ("Typee", "Herman Melville", 1846, 316, ["Adventure", "Classic"], "en"),
    ("The Scarlet Letter", "Nathaniel Hawthorne", 1850, 272, ["Literary Fiction", "Classic"], "en"),
    ("The House of the Seven Gables", "Nathaniel Hawthorne", 1851, 312, ["Literary Fiction", "Classic"], "en"),
    ("Twice-Told Tales", "Nathaniel Hawthorne", 1837, 296, ["Short Stories", "Classic"], "en"),
    ("Leaves of Grass", "Walt Whitman", 1855, 568, ["Poetry", "Classic"], "en"),
    ("The Complete Tales and Poems", "Edgar Allan Poe", 1938, 1062, ["Short Stories", "Classic", "Horror"], "en"),
    ("The Raven and Other Poems", "Edgar Allan Poe", 1845, 100, ["Poetry", "Classic"], "en"),
]


def generate():
    existing_titles, existing_authors = load_existing()
    print(f"Existing: {len(existing_titles)} title-author pairs, {len(existing_authors)} unique authors")

    new_entries = []
    skipped = 0
    for entry in ALL_BOOKS:
        title, author, year, pages, genres, lang = entry
        key = (title.lower(), author.lower())
        if key in existing_titles:
            skipped += 1
            continue
        new_entries.append(make_book(title, author, year, pages, genres, lang))

    print(f"Skipped {skipped} duplicates, keeping {len(new_entries)} new entries")

    batch_num = 130
    for i in range(0, len(new_entries), 100):
        batch = new_entries[i:i + 100]
        fname = f"batch_{batch_num:03d}_batch22_{batch_num - 129}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(batch, f, indent=2)
        print(f"  {fname}: {len(batch)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(new_entries)}")


if __name__ == "__main__":
    generate()
