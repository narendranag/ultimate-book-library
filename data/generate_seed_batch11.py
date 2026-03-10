#!/usr/bin/env python3
"""Batch 11: Classic literature, Nobel laureates, world fiction (batches 72-78)."""
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


def make_book(title, author, year, pages, genres, lang="en", description=""):
    isbn13 = make_isbn13(title, author)
    isbn10 = make_isbn10(isbn13)
    return {
        "title": title,
        "author": author,
        "year": year,
        "isbn_13": isbn13,
        "isbn_10": isbn10,
        "pages": pages,
        "genres": genres,
        "language": lang,
        "description": description,
    }


AUTHORS = [
    # Nobel Prize winners
    ("William Faulkner", "en", ["Literary Fiction", "Classic"], [
        ("The Sound and the Fury", 1929, 326, []),
        ("As I Lay Dying", 1930, 267, []),
        ("Sanctuary", 1931, 309, []),
        ("Light in August", 1932, 507, []),
        ("Absalom, Absalom!", 1936, 378, []),
        ("The Wild Palms", 1939, 339, []),
        ("The Hamlet", 1940, 366, []),
        ("Go Down, Moses", 1942, 383, ["Short Stories"]),
        ("Intruder in the Dust", 1948, 247, []),
        ("Requiem for a Nun", 1951, 286, []),
        ("A Fable", 1954, 437, []),
        ("The Town", 1957, 371, []),
        ("The Mansion", 1959, 436, []),
        ("The Reivers", 1962, 305, []),
    ]),
    ("Ernest Hemingway", "en", ["Literary Fiction", "Classic"], [
        ("The Sun Also Rises", 1926, 251, []),
        ("A Farewell to Arms", 1929, 332, ["War"]),
        ("To Have and Have Not", 1937, 262, []),
        ("For Whom the Bell Tolls", 1940, 471, ["War"]),
        ("Across the River and into the Trees", 1950, 272, []),
        ("The Old Man and the Sea", 1952, 127, []),
        ("Islands in the Stream", 1970, 466, []),
        ("The Garden of Eden", 1986, 247, []),
        ("True at First Light", 1999, 322, []),
        ("A Moveable Feast", 1964, 241, ["Memoir"]),
        ("In Our Time", 1925, 156, ["Short Stories"]),
        ("Men Without Women", 1927, 232, ["Short Stories"]),
        ("Winner Take Nothing", 1933, 244, ["Short Stories"]),
        ("The Nick Adams Stories", 1972, 268, ["Short Stories"]),
    ]),
    ("John Steinbeck", "en", ["Literary Fiction", "Classic"], [
        ("Cup of Gold", 1929, 266, []),
        ("The Pastures of Heaven", 1932, 302, []),
        ("To a God Unknown", 1933, 261, []),
        ("Tortilla Flat", 1935, 207, ["Humor"]),
        ("In Dubious Battle", 1936, 349, []),
        ("Of Mice and Men", 1937, 107, []),
        ("The Grapes of Wrath", 1939, 464, []),
        ("Cannery Row", 1945, 196, []),
        ("The Pearl", 1947, 96, []),
        ("East of Eden", 1952, 601, []),
        ("Sweet Thursday", 1954, 273, []),
        ("The Winter of Our Discontent", 1961, 311, []),
        ("Travels with Charley", 1962, 277, ["Travel", "Non-Fiction"]),
        ("The Log from the Sea of Cortez", 1951, 288, ["Science", "Non-Fiction"]),
    ]),
    ("Gabriel García Márquez", "es", ["Literary Fiction", "Magical Realism"], [
        ("Leaf Storm", 1955, 114, []),
        ("No One Writes to the Colonel", 1961, 115, []),
        ("In Evil Hour", 1962, 183, []),
        ("One Hundred Years of Solitude", 1967, 417, ["Classic"]),
        ("The Autumn of the Patriarch", 1975, 269, []),
        ("Chronicle of a Death Foretold", 1981, 120, []),
        ("Love in the Time of Cholera", 1985, 348, ["Romance"]),
        ("The General in His Labyrinth", 1989, 285, ["Historical Fiction"]),
        ("Of Love and Other Demons", 1994, 147, []),
        ("Memories of My Melancholy Whores", 2004, 115, []),
        ("Strange Pilgrims", 1992, 188, ["Short Stories"]),
        ("Living to Tell the Tale", 2002, 483, ["Memoir"]),
    ]),
    ("Saul Bellow", "en", ["Literary Fiction", "Classic"], [
        ("Dangling Man", 1944, 191, []),
        ("The Victim", 1947, 294, []),
        ("The Adventures of Augie March", 1953, 586, []),
        ("Seize the Day", 1956, 118, []),
        ("Henderson the Rain King", 1959, 341, []),
        ("Herzog", 1964, 341, []),
        ("Mr. Sammler's Planet", 1970, 313, []),
        ("Humboldt's Gift", 1975, 487, []),
        ("The Dean's December", 1982, 312, []),
        ("More Die of Heartbreak", 1987, 335, []),
        ("A Theft", 1989, 109, []),
        ("The Bellarosa Connection", 1989, 102, []),
        ("The Actual", 1997, 104, []),
        ("Ravelstein", 2000, 233, []),
    ]),
    ("V.S. Naipaul", "en", ["Literary Fiction"], [
        ("The Mystic Masseur", 1957, 215, []),
        ("The Suffrage of Elvira", 1958, 240, []),
        ("Miguel Street", 1959, 222, ["Short Stories"]),
        ("A House for Mr Biswas", 1961, 564, ["Classic"]),
        ("Mr Stone and the Knights Companion", 1963, 160, []),
        ("The Mimic Men", 1967, 301, []),
        ("In a Free State", 1971, 246, []),
        ("Guerrillas", 1975, 309, []),
        ("A Bend in the River", 1979, 278, []),
        ("The Enigma of Arrival", 1987, 354, []),
        ("A Way in the World", 1994, 380, []),
        ("Half a Life", 2001, 211, []),
        ("Magic Seeds", 2004, 280, []),
        ("An Area of Darkness", 1964, 281, ["Travel", "Non-Fiction"]),
        ("India: A Wounded Civilization", 1977, 175, ["Non-Fiction"]),
        ("Among the Believers", 1981, 430, ["Travel", "Non-Fiction"]),
    ]),
    ("Naguib Mahfouz", "ar", ["Literary Fiction"], [
        ("Palace Walk", 1956, 498, ["Historical Fiction"]),
        ("Palace of Desire", 1957, 422, []),
        ("Sugar Street", 1957, 308, []),
        ("Children of the Alley", 1959, 448, []),
        ("The Thief and the Dogs", 1961, 158, []),
        ("The Search", 1964, 186, []),
        ("Adrift on the Nile", 1966, 167, []),
        ("Miramar", 1967, 208, []),
        ("Mirrors", 1972, 227, []),
        ("The Harafish", 1977, 438, []),
        ("The Day the Leader Was Killed", 1985, 118, []),
    ]),
    ("Kenzaburō Ōe", "ja", ["Literary Fiction"], [
        ("A Personal Matter", 1964, 165, []),
        ("The Silent Cry", 1967, 274, []),
        ("Teach Us to Outgrow Our Madness", 1969, 261, ["Short Stories"]),
        ("The Pinch Runner Memorandum", 1976, 380, []),
        ("A Quiet Life", 1990, 240, []),
        ("Somersault", 1999, 570, []),
        ("Rouse Up O Young Men of the New Age!", 1983, 261, []),
        ("The Changeling", 2000, 468, []),
        ("Death by Water", 2009, 421, []),
    ]),
    ("José Saramago", "pt", ["Literary Fiction", "Magical Realism"], [
        ("Baltasar and Blimunda", 1982, 348, ["Historical Fiction"]),
        ("The Year of the Death of Ricardo Reis", 1984, 341, []),
        ("The Stone Raft", 1986, 263, []),
        ("The History of the Siege of Lisbon", 1989, 314, []),
        ("The Gospel According to Jesus Christ", 1991, 392, []),
        ("Blindness", 1995, 326, ["Classic"]),
        ("All the Names", 1997, 238, []),
        ("The Cave", 2000, 307, []),
        ("The Double", 2002, 324, []),
        ("Seeing", 2004, 307, []),
        ("Death with Interruptions", 2005, 238, []),
        ("The Elephant's Journey", 2008, 205, []),
        ("Cain", 2009, 160, []),
    ]),
    ("Svetlana Alexievich", "ru", ["Literary Fiction", "Non-Fiction"], [
        ("War's Unwomanly Face", 1985, 331, ["War", "History"]),
        ("Last Witnesses", 1985, 252, ["War", "History"]),
        ("Zinky Boys", 1990, 199, ["War"]),
        ("Voices from Chernobyl", 1997, 236, ["History"]),
        ("Secondhand Time", 2013, 496, ["History"]),
    ]),
    # More world literature
    ("Fyodor Dostoevsky", "ru", ["Literary Fiction", "Classic", "Philosophy"], [
        ("Poor Folk", 1846, 150, []),
        ("The Double", 1846, 138, []),
        ("Netochka Nezvanova", 1849, 186, []),
        ("The House of the Dead", 1862, 338, []),
        ("Notes from Underground", 1864, 136, []),
        ("Crime and Punishment", 1866, 671, []),
        ("The Gambler", 1867, 180, []),
        ("The Idiot", 1869, 656, []),
        ("Demons", 1872, 768, []),
        ("The Adolescent", 1875, 542, []),
        ("The Brothers Karamazov", 1880, 796, []),
    ]),
    ("Leo Tolstoy", "ru", ["Literary Fiction", "Classic"], [
        ("Childhood", 1852, 161, []),
        ("Boyhood", 1854, 106, []),
        ("Youth", 1857, 180, []),
        ("The Cossacks", 1863, 194, []),
        ("War and Peace", 1869, 1225, ["Historical Fiction"]),
        ("Anna Karenina", 1877, 864, ["Romance"]),
        ("The Death of Ivan Ilyich", 1886, 86, []),
        ("The Kreutzer Sonata", 1889, 122, []),
        ("Resurrection", 1899, 576, []),
        ("Hadji Murad", 1912, 160, []),
    ]),
    ("Anton Chekhov", "ru", ["Literary Fiction", "Classic"], [
        ("The Steppe", 1888, 80, ["Short Stories"]),
        ("The Duel", 1891, 96, []),
        ("Ward No. 6", 1892, 64, ["Short Stories"]),
        ("The Lady with the Dog", 1899, 40, ["Short Stories"]),
        ("The Seagull", 1896, 96, ["Drama"]),
        ("Uncle Vanya", 1897, 84, ["Drama"]),
        ("Three Sisters", 1901, 96, ["Drama"]),
        ("The Cherry Orchard", 1904, 96, ["Drama"]),
    ]),
    ("Franz Kafka", "de", ["Literary Fiction", "Classic"], [
        ("The Trial", 1925, 255, []),
        ("The Castle", 1926, 352, []),
        ("Amerika", 1927, 299, []),
        ("The Metamorphosis", 1915, 55, []),
        ("In the Penal Colony", 1919, 50, ["Short Stories"]),
        ("A Hunger Artist", 1922, 52, ["Short Stories"]),
        ("The Complete Stories", 1971, 486, ["Short Stories"]),
    ]),
    ("Thomas Mann", "de", ["Literary Fiction", "Classic"], [
        ("Buddenbrooks", 1901, 731, []),
        ("Tonio Kröger", 1903, 96, []),
        ("Royal Highness", 1909, 367, []),
        ("Death in Venice", 1912, 88, []),
        ("The Magic Mountain", 1924, 706, []),
        ("Joseph and His Brothers", 1943, 1492, []),
        ("Doctor Faustus", 1947, 510, []),
        ("The Holy Sinner", 1951, 337, []),
        ("Confessions of Felix Krull", 1954, 384, ["Humor"]),
    ]),
    ("Marcel Proust", "fr", ["Literary Fiction", "Classic"], [
        ("Swann's Way", 1913, 468, []),
        ("In the Shadow of Young Girls in Flower", 1919, 629, []),
        ("The Guermantes Way", 1920, 610, []),
        ("Sodom and Gomorrah", 1921, 502, []),
        ("The Prisoner", 1923, 446, []),
        ("The Fugitive", 1925, 390, []),
        ("Time Regained", 1927, 448, []),
        ("Jean Santeuil", 1952, 740, []),
    ]),
    ("James Joyce", "en", ["Literary Fiction", "Classic"], [
        ("Dubliners", 1914, 152, ["Short Stories"]),
        ("A Portrait of the Artist as a Young Man", 1916, 299, []),
        ("Ulysses", 1922, 730, []),
        ("Finnegans Wake", 1939, 628, []),
        ("Stephen Hero", 1944, 234, []),
    ]),
    ("Virginia Woolf", "en", ["Literary Fiction", "Classic"], [
        ("The Voyage Out", 1915, 398, []),
        ("Night and Day", 1919, 538, []),
        ("Jacob's Room", 1922, 281, []),
        ("Mrs Dalloway", 1925, 194, []),
        ("To the Lighthouse", 1927, 209, []),
        ("Orlando", 1928, 336, []),
        ("The Waves", 1931, 297, []),
        ("The Years", 1937, 435, []),
        ("Between the Acts", 1941, 256, []),
        ("A Room of One's Own", 1929, 112, ["Non-Fiction"]),
    ]),
    ("Albert Camus", "fr", ["Literary Fiction", "Classic", "Philosophy"], [
        ("The Stranger", 1942, 123, []),
        ("The Plague", 1947, 308, []),
        ("The Fall", 1956, 147, []),
        ("A Happy Death", 1971, 151, []),
        ("The First Man", 1994, 325, []),
        ("Exile and the Kingdom", 1957, 159, ["Short Stories"]),
        ("The Myth of Sisyphus", 1942, 212, ["Non-Fiction", "Philosophy"]),
        ("The Rebel", 1951, 306, ["Non-Fiction", "Philosophy"]),
    ]),
    ("Jean-Paul Sartre", "fr", ["Literary Fiction", "Classic", "Philosophy"], [
        ("Nausea", 1938, 253, []),
        ("The Age of Reason", 1945, 397, []),
        ("The Reprieve", 1945, 324, []),
        ("Troubled Sleep", 1949, 421, []),
        ("The Wall", 1939, 226, ["Short Stories"]),
        ("Being and Nothingness", 1943, 638, ["Non-Fiction", "Philosophy"]),
        ("No Exit", 1944, 46, ["Drama"]),
        ("The Words", 1964, 255, ["Memoir"]),
    ]),
    ("Günter Grass", "de", ["Literary Fiction", "Classic"], [
        ("The Tin Drum", 1959, 592, []),
        ("Cat and Mouse", 1961, 189, []),
        ("Dog Years", 1963, 570, []),
        ("Local Anaesthetic", 1969, 284, []),
        ("From the Diary of a Snail", 1972, 310, []),
        ("The Flounder", 1977, 547, []),
        ("The Meeting at Telgte", 1979, 147, []),
        ("Headbirths", 1980, 134, []),
        ("The Rat", 1986, 371, []),
        ("The Call of the Toad", 1992, 248, []),
        ("Too Far Afield", 1995, 658, []),
        ("Crabwalk", 2002, 234, ["Historical Fiction"]),
        ("Peeling the Onion", 2006, 425, ["Memoir"]),
    ]),
    ("Italo Calvino", "it", ["Literary Fiction", "Postmodern"], [
        ("The Path to the Nest of Spiders", 1947, 146, []),
        ("The Baron in the Trees", 1957, 217, ["Fantasy"]),
        ("The Cloven Viscount", 1952, 118, ["Fantasy"]),
        ("The Nonexistent Knight", 1959, 119, ["Fantasy"]),
        ("Cosmicomics", 1965, 153, ["Science Fiction", "Short Stories"]),
        ("t zero", 1967, 152, ["Science Fiction", "Short Stories"]),
        ("Invisible Cities", 1972, 165, []),
        ("The Castle of Crossed Destinies", 1973, 129, []),
        ("If on a winter's night a traveler", 1979, 260, []),
        ("Mr. Palomar", 1983, 126, []),
        ("Under the Jaguar Sun", 1986, 86, ["Short Stories"]),
        ("Six Memos for the Next Millennium", 1988, 124, ["Non-Fiction"]),
    ]),
    ("Umberto Eco", "it", ["Literary Fiction", "Historical Fiction"], [
        ("The Name of the Rose", 1980, 502, ["Mystery", "Classic"]),
        ("Foucault's Pendulum", 1988, 641, ["Thriller"]),
        ("The Island of the Day Before", 1994, 515, []),
        ("Baudolino", 2000, 528, []),
        ("The Mysterious Flame of Queen Loana", 2004, 469, []),
        ("The Prague Cemetery", 2010, 444, ["Thriller"]),
        ("Numero Zero", 2015, 191, ["Thriller"]),
    ]),
    ("Milan Kundera", "cs", ["Literary Fiction", "Postmodern"], [
        ("The Joke", 1967, 323, []),
        ("Life Is Elsewhere", 1973, 303, []),
        ("The Farewell Waltz", 1976, 237, []),
        ("The Book of Laughter and Forgetting", 1979, 228, []),
        ("The Unbearable Lightness of Being", 1984, 314, ["Classic"]),
        ("Immortality", 1990, 345, []),
        ("Slowness", 1995, 132, []),
        ("Identity", 1998, 153, []),
        ("Ignorance", 2000, 195, []),
        ("The Festival of Insignificance", 2013, 115, []),
    ]),
    ("Hermann Hesse", "de", ["Literary Fiction", "Classic"], [
        ("Peter Camenzind", 1904, 172, []),
        ("Beneath the Wheel", 1906, 178, []),
        ("Gertrude", 1910, 160, []),
        ("Rosshalde", 1914, 201, []),
        ("Demian", 1919, 171, []),
        ("Siddhartha", 1922, 152, ["Philosophy"]),
        ("Steppenwolf", 1927, 237, []),
        ("Narcissus and Goldmund", 1930, 312, []),
        ("The Journey to the East", 1932, 118, []),
        ("The Glass Bead Game", 1943, 558, []),
    ]),
    ("Mikhail Bulgakov", "ru", ["Literary Fiction", "Classic", "Magical Realism"], [
        ("The White Guard", 1925, 307, ["Historical Fiction"]),
        ("The Heart of a Dog", 1925, 128, ["Satire"]),
        ("The Master and Margarita", 1967, 372, []),
        ("A Country Doctor's Notebook", 1926, 128, ["Short Stories"]),
        ("Black Snow", 1965, 221, []),
        ("The Fatal Eggs", 1925, 120, ["Science Fiction"]),
    ]),
    ("Yasunari Kawabata", "ja", ["Literary Fiction", "Classic"], [
        ("Snow Country", 1948, 175, []),
        ("Thousand Cranes", 1952, 147, []),
        ("The Sound of the Mountain", 1954, 276, []),
        ("The House of the Sleeping Beauties", 1961, 99, []),
        ("The Old Capital", 1962, 182, []),
        ("Beauty and Sadness", 1965, 206, []),
        ("The Master of Go", 1972, 189, []),
        ("Palm-of-the-Hand Stories", 1988, 238, ["Short Stories"]),
    ]),
    ("Haruki Murakami", "ja", ["Literary Fiction", "Magical Realism"], [
        ("1Q84", 2009, 925, []),
        ("Kafka on the Shore", 2002, 467, []),
        ("The Elephant Vanishes", 1993, 327, ["Short Stories"]),
    ]),
    ("Banana Yoshimoto", "ja", ["Literary Fiction"], [
        ("Kitchen", 1988, 152, []),
        ("N.P.", 1990, 179, []),
        ("Lizard", 1993, 160, ["Short Stories"]),
        ("Amrita", 1994, 366, []),
        ("Goodbye Tsugumi", 1989, 188, []),
        ("Asleep", 2000, 177, []),
        ("Hardboiled & Hard Luck", 1999, 186, []),
        ("The Lake", 2005, 188, []),
        ("Moshi Moshi", 2010, 208, []),
    ]),
    ("Yōko Ogawa", "ja", ["Literary Fiction"], [
        ("The Memory Police", 1994, 274, ["Science Fiction"]),
        ("The Housekeeper and the Professor", 2003, 180, []),
        ("The Diving Pool", 1990, 180, ["Short Stories"]),
        ("Hotel Iris", 1996, 179, []),
        ("Revenge", 2009, 166, ["Short Stories"]),
    ]),
    # Latin American boom
    ("Jorge Luis Borges", "es", ["Literary Fiction", "Short Stories"], [
        ("Ficciones", 1944, 174, ["Classic"]),
        ("The Aleph", 1949, 190, []),
        ("A Universal History of Iniquity", 1935, 146, []),
        ("The Book of Sand", 1975, 155, []),
        ("Labyrinths", 1962, 240, ["Classic"]),
        ("Dreamtigers", 1960, 95, []),
        ("The Book of Imaginary Beings", 1957, 235, ["Non-Fiction"]),
        ("Doctor Brodie's Report", 1970, 145, []),
    ]),
    ("Julio Cortázar", "es", ["Literary Fiction"], [
        ("The Winners", 1960, 371, []),
        ("Hopscotch", 1963, 564, ["Classic"]),
        ("62: A Model Kit", 1968, 280, []),
        ("A Manual for Manuel", 1973, 394, []),
        ("Blow-Up and Other Stories", 1967, 277, ["Short Stories"]),
        ("All Fires the Fire", 1966, 171, ["Short Stories"]),
        ("Cronopios and Famas", 1962, 161, ["Short Stories", "Humor"]),
        ("We Love Glenda So Much", 1980, 165, ["Short Stories"]),
    ]),
    ("Mario Vargas Llosa", "es", ["Literary Fiction"], [
        ("The Time of the Hero", 1963, 409, []),
        ("The Green House", 1966, 405, []),
        ("Conversation in the Cathedral", 1969, 601, []),
        ("Captain Pantoja and the Special Service", 1973, 303, ["Humor"]),
        ("Aunt Julia and the Scriptwriter", 1977, 374, ["Humor"]),
        ("The War of the End of the World", 1981, 568, ["Historical Fiction"]),
        ("The Real Life of Alejandro Mayta", 1984, 310, []),
        ("The Storyteller", 1987, 246, []),
        ("The Feast of the Goat", 2000, 404, ["Historical Fiction"]),
        ("The Bad Girl", 2006, 376, []),
        ("The Dream of the Celt", 2010, 358, ["Historical Fiction"]),
        ("The Discreet Hero", 2013, 336, []),
        ("The Neighborhood", 2018, 304, []),
        ("Harsh Times", 2019, 354, ["Historical Fiction"]),
    ]),
    ("Carlos Fuentes", "es", ["Literary Fiction"], [
        ("Where the Air Is Clear", 1958, 369, []),
        ("The Death of Artemio Cruz", 1962, 307, ["Classic"]),
        ("Aura", 1962, 62, []),
        ("A Change of Skin", 1967, 462, []),
        ("Terra Nostra", 1975, 778, ["Historical Fiction"]),
        ("Distant Relations", 1980, 216, []),
        ("The Old Gringo", 1985, 199, ["Historical Fiction"]),
        ("Christopher Unborn", 1987, 531, []),
        ("The Campaign", 1990, 246, ["Historical Fiction"]),
        ("The Years with Laura Díaz", 1999, 518, []),
        ("The Eagle's Throne", 2002, 341, []),
        ("Destiny and Desire", 2008, 436, []),
    ]),
    ("Isabel Allende", "es", ["Literary Fiction", "Magical Realism"], [
        ("The House of the Spirits", 1982, 433, ["Classic"]),
        ("Of Love and Shadows", 1984, 274, []),
        ("Eva Luna", 1987, 271, []),
        ("The Stories of Eva Luna", 1989, 330, ["Short Stories"]),
        ("The Infinite Plan", 1991, 382, []),
        ("Daughter of Fortune", 1999, 399, ["Historical Fiction"]),
        ("Portrait in Sepia", 2000, 304, []),
        ("Zorro", 2005, 390, ["Adventure", "Historical Fiction"]),
        ("Inés of My Soul", 2006, 321, ["Historical Fiction"]),
        ("The Island Beneath the Sea", 2009, 457, ["Historical Fiction"]),
        ("Maya's Notebook", 2011, 383, []),
        ("The Japanese Lover", 2015, 322, []),
        ("A Long Petal of the Sea", 2019, 338, ["Historical Fiction"]),
        ("Violeta", 2022, 301, []),
        ("Paula", 1994, 330, ["Memoir"]),
        ("My Invented Country", 2003, 199, ["Memoir"]),
    ]),
    ("Roberto Bolaño", "es", ["Literary Fiction"], [
        ("The Skating Rink", 1993, 181, []),
        ("Nazi Literature in the Americas", 1996, 259, []),
        ("Distant Star", 1996, 164, []),
        ("The Savage Detectives", 1998, 577, ["Classic"]),
        ("Amulet", 1999, 184, []),
        ("By Night in Chile", 2000, 130, []),
        ("2666", 2004, 898, ["Classic"]),
        ("The Third Reich", 2010, 277, []),
        ("Woes of the True Policeman", 2011, 186, []),
        ("The Spirit of Science Fiction", 2016, 194, []),
        ("Last Evenings on Earth", 2001, 204, ["Short Stories"]),
    ]),
]


def generate():
    batch_num = 72
    books_in_batch = []

    for author, lang, default_genres, works in AUTHORS:
        for title, year, pages, extra_genres in works:
            genres = list(default_genres) + extra_genres
            book = make_book(title, author, year, pages, genres, lang)
            books_in_batch.append(book)

            if len(books_in_batch) >= 100:
                fname = f"batch_{batch_num:02d}_classics_{batch_num - 71}.json"
                path = os.path.join(BATCH_DIR, fname)
                with open(path, "w") as f:
                    json.dump(books_in_batch, f, indent=2)
                print(f"  {fname}: {len(books_in_batch)} books")
                batch_num += 1
                books_in_batch = []

    if books_in_batch:
        fname = f"batch_{batch_num:02d}_classics_{batch_num - 71}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(books_in_batch, f, indent=2)
        print(f"  {fname}: {len(books_in_batch)} books")
        batch_num += 1

    total = sum(len(works) for _, _, _, works in AUTHORS)
    print(f"\nTotal new books: {total}")


if __name__ == "__main__":
    generate()
