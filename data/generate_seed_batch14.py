#!/usr/bin/env python3
"""Batch 14: YA, children's, graphic novels, technology, business, philosophy."""
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


BOOKS = []

# YA Fiction
YA_BOOKS = [
    ("The Hunger Games", "Suzanne Collins", 2008, 374, ["Young Adult", "Science Fiction", "Dystopian"]),
    ("Catching Fire", "Suzanne Collins", 2009, 391, ["Young Adult", "Science Fiction", "Dystopian"]),
    ("Mockingjay", "Suzanne Collins", 2010, 390, ["Young Adult", "Science Fiction", "Dystopian"]),
    ("The Ballad of Songbirds and Snakes", "Suzanne Collins", 2020, 517, ["Young Adult", "Science Fiction"]),
    ("Sunrise on the Reaping", "Suzanne Collins", 2025, 400, ["Young Adult", "Science Fiction"]),
    ("Divergent", "Veronica Roth", 2011, 487, ["Young Adult", "Science Fiction", "Dystopian"]),
    ("Insurgent", "Veronica Roth", 2012, 525, ["Young Adult", "Science Fiction", "Dystopian"]),
    ("Allegiant", "Veronica Roth", 2013, 526, ["Young Adult", "Science Fiction"]),
    ("The Maze Runner", "James Dashner", 2009, 375, ["Young Adult", "Science Fiction"]),
    ("The Scorch Trials", "James Dashner", 2010, 360, ["Young Adult", "Science Fiction"]),
    ("The Death Cure", "James Dashner", 2011, 325, ["Young Adult", "Science Fiction"]),
    ("The Giver", "Lois Lowry", 1993, 180, ["Young Adult", "Science Fiction", "Classic"]),
    ("Gathering Blue", "Lois Lowry", 2000, 215, ["Young Adult", "Science Fiction"]),
    ("Messenger", "Lois Lowry", 2004, 169, ["Young Adult", "Science Fiction"]),
    ("Son", "Lois Lowry", 2012, 393, ["Young Adult", "Science Fiction"]),
    ("Number the Stars", "Lois Lowry", 1989, 137, ["Young Adult", "Historical Fiction"]),
    ("The Fault in Our Stars", "John Green", 2012, 313, ["Young Adult", "Romance"]),
    ("Looking for Alaska", "John Green", 2005, 221, ["Young Adult"]),
    ("An Abundance of Katherines", "John Green", 2006, 227, ["Young Adult", "Humor"]),
    ("Paper Towns", "John Green", 2008, 305, ["Young Adult"]),
    ("Turtles All the Way Down", "John Green", 2017, 286, ["Young Adult"]),
    ("The Anthropocene Reviewed", "John Green", 2021, 293, ["Non-Fiction"]),
    ("Twilight", "Stephenie Meyer", 2005, 498, ["Young Adult", "Romance", "Fantasy"]),
    ("New Moon", "Stephenie Meyer", 2006, 563, ["Young Adult", "Romance", "Fantasy"]),
    ("Eclipse", "Stephenie Meyer", 2007, 629, ["Young Adult", "Romance", "Fantasy"]),
    ("Breaking Dawn", "Stephenie Meyer", 2008, 756, ["Young Adult", "Romance", "Fantasy"]),
    ("The Host", "Stephenie Meyer", 2008, 619, ["Science Fiction"]),
    ("Midnight Sun", "Stephenie Meyer", 2020, 658, ["Young Adult", "Romance", "Fantasy"]),
    ("Percy Jackson and the Lightning Thief", "Rick Riordan", 2005, 375, ["Young Adult", "Fantasy"]),
    ("Percy Jackson and the Sea of Monsters", "Rick Riordan", 2006, 279, ["Young Adult", "Fantasy"]),
    ("Percy Jackson and the Titan's Curse", "Rick Riordan", 2007, 312, ["Young Adult", "Fantasy"]),
    ("Percy Jackson and the Battle of the Labyrinth", "Rick Riordan", 2008, 361, ["Young Adult", "Fantasy"]),
    ("Percy Jackson and the Last Olympian", "Rick Riordan", 2009, 381, ["Young Adult", "Fantasy"]),
    ("The Red Pyramid", "Rick Riordan", 2010, 516, ["Young Adult", "Fantasy"]),
    ("The Lost Hero", "Rick Riordan", 2010, 553, ["Young Adult", "Fantasy"]),
    ("Eragon", "Christopher Paolini", 2003, 503, ["Young Adult", "Fantasy"]),
    ("Eldest", "Christopher Paolini", 2005, 681, ["Young Adult", "Fantasy"]),
    ("Brisingr", "Christopher Paolini", 2008, 748, ["Young Adult", "Fantasy"]),
    ("Inheritance", "Christopher Paolini", 2011, 849, ["Young Adult", "Fantasy"]),
    ("The Book Thief", "Markus Zusak", 2005, 552, ["Young Adult", "Historical Fiction"]),
    ("I Am the Messenger", "Markus Zusak", 2002, 357, ["Young Adult"]),
    ("Bridge to Terabithia", "Katherine Paterson", 1977, 128, ["Young Adult", "Classic"]),
    ("Jacob Have I Loved", "Katherine Paterson", 1980, 216, ["Young Adult"]),
    ("Holes", "Louis Sachar", 1998, 233, ["Young Adult"]),
    ("Hatchet", "Gary Paulsen", 1987, 195, ["Young Adult", "Adventure"]),
    ("The Outsiders", "S.E. Hinton", 1967, 192, ["Young Adult", "Classic"]),
    ("That Was Then, This Is Now", "S.E. Hinton", 1971, 159, ["Young Adult"]),
    ("Rumble Fish", "S.E. Hinton", 1975, 122, ["Young Adult"]),
    ("Tex", "S.E. Hinton", 1979, 194, ["Young Adult"]),
    ("Speak", "Laurie Halse Anderson", 1999, 198, ["Young Adult"]),
    ("Wintergirls", "Laurie Halse Anderson", 2009, 278, ["Young Adult"]),
    ("Chains", "Laurie Halse Anderson", 2008, 316, ["Young Adult", "Historical Fiction"]),
    ("Fever 1793", "Laurie Halse Anderson", 2000, 251, ["Young Adult", "Historical Fiction"]),
    ("The Perks of Being a Wallflower", "Stephen Chbosky", 1999, 213, ["Young Adult"]),
    ("Stargirl", "Jerry Spinelli", 2000, 186, ["Young Adult"]),
    ("Maniac Magee", "Jerry Spinelli", 1990, 184, ["Young Adult"]),
    ("Monster", "Walter Dean Myers", 1999, 281, ["Young Adult"]),
    ("Scorpions", "Walter Dean Myers", 1988, 216, ["Young Adult"]),
    ("Fallen Angels", "Walter Dean Myers", 1988, 309, ["Young Adult", "War"]),
    ("The Hate U Give", "Angie Thomas", 2017, 444, ["Young Adult"]),
    ("On the Come Up", "Angie Thomas", 2019, 447, ["Young Adult"]),
    ("Concrete Rose", "Angie Thomas", 2021, 304, ["Young Adult"]),
    ("Children of Blood and Bone", "Tomi Adeyemi", 2018, 525, ["Young Adult", "Fantasy"]),
    ("Children of Virtue and Vengeance", "Tomi Adeyemi", 2019, 400, ["Young Adult", "Fantasy"]),
    ("Six of Crows", "Leigh Bardugo", 2015, 465, ["Young Adult", "Fantasy"]),
    ("Crooked Kingdom", "Leigh Bardugo", 2016, 536, ["Young Adult", "Fantasy"]),
    ("Shadow and Bone", "Leigh Bardugo", 2012, 358, ["Young Adult", "Fantasy"]),
    ("Siege and Storm", "Leigh Bardugo", 2013, 435, ["Young Adult", "Fantasy"]),
    ("Ruin and Rising", "Leigh Bardugo", 2014, 422, ["Young Adult", "Fantasy"]),
    ("Ninth House", "Leigh Bardugo", 2019, 458, ["Fantasy"]),
    ("The Cruel Prince", "Holly Black", 2018, 370, ["Young Adult", "Fantasy"]),
    ("The Wicked King", "Holly Black", 2019, 336, ["Young Adult", "Fantasy"]),
    ("The Queen of Nothing", "Holly Black", 2019, 308, ["Young Adult", "Fantasy"]),
]

# Children's Literature
CHILDREN_BOOKS = [
    ("Charlotte's Web", "E.B. White", 1952, 184, ["Children's", "Classic"]),
    ("Stuart Little", "E.B. White", 1945, 131, ["Children's", "Classic"]),
    ("The Trumpet of the Swan", "E.B. White", 1970, 210, ["Children's"]),
    ("Charlie and the Chocolate Factory", "Roald Dahl", 1964, 176, ["Children's", "Classic"]),
    ("James and the Giant Peach", "Roald Dahl", 1961, 160, ["Children's", "Classic"]),
    ("Matilda", "Roald Dahl", 1988, 240, ["Children's", "Classic"]),
    ("The BFG", "Roald Dahl", 1982, 208, ["Children's", "Fantasy"]),
    ("The Witches", "Roald Dahl", 1983, 208, ["Children's", "Fantasy"]),
    ("Danny the Champion of the World", "Roald Dahl", 1975, 196, ["Children's"]),
    ("Fantastic Mr Fox", "Roald Dahl", 1970, 96, ["Children's"]),
    ("The Twits", "Roald Dahl", 1980, 112, ["Children's", "Humor"]),
    ("George's Marvellous Medicine", "Roald Dahl", 1981, 89, ["Children's"]),
    ("Boy: Tales of Childhood", "Roald Dahl", 1984, 176, ["Memoir"]),
    ("Going Solo", "Roald Dahl", 1986, 209, ["Memoir"]),
    ("A Wrinkle in Time", "Madeleine L'Engle", 1962, 211, ["Children's", "Science Fiction", "Classic"]),
    ("A Wind in the Door", "Madeleine L'Engle", 1973, 211, ["Children's", "Science Fiction"]),
    ("A Swiftly Tilting Planet", "Madeleine L'Engle", 1978, 278, ["Children's", "Science Fiction"]),
    ("The Lion, the Witch and the Wardrobe", "C.S. Lewis", 1950, 206, ["Children's", "Fantasy", "Classic"]),
    ("Prince Caspian", "C.S. Lewis", 1951, 195, ["Children's", "Fantasy"]),
    ("The Voyage of the Dawn Treader", "C.S. Lewis", 1952, 223, ["Children's", "Fantasy"]),
    ("The Silver Chair", "C.S. Lewis", 1953, 217, ["Children's", "Fantasy"]),
    ("The Horse and His Boy", "C.S. Lewis", 1954, 199, ["Children's", "Fantasy"]),
    ("The Magician's Nephew", "C.S. Lewis", 1955, 183, ["Children's", "Fantasy"]),
    ("The Last Battle", "C.S. Lewis", 1956, 184, ["Children's", "Fantasy"]),
    ("The Phantom Tollbooth", "Norton Juster", 1961, 255, ["Children's", "Fantasy", "Classic"]),
    ("Where the Wild Things Are", "Maurice Sendak", 1963, 48, ["Children's", "Classic"]),
    ("The Very Hungry Caterpillar", "Eric Carle", 1969, 22, ["Children's", "Classic"]),
    ("Goodnight Moon", "Margaret Wise Brown", 1947, 30, ["Children's", "Classic"]),
    ("The Giving Tree", "Shel Silverstein", 1964, 64, ["Children's", "Classic"]),
    ("Where the Sidewalk Ends", "Shel Silverstein", 1974, 176, ["Children's", "Poetry"]),
    ("A Light in the Attic", "Shel Silverstein", 1981, 176, ["Children's", "Poetry"]),
    ("Anne of Green Gables", "L.M. Montgomery", 1908, 320, ["Children's", "Classic"]),
    ("Anne of Avonlea", "L.M. Montgomery", 1909, 278, ["Children's"]),
    ("Anne of the Island", "L.M. Montgomery", 1915, 326, ["Children's"]),
    ("The Secret Garden", "Frances Hodgson Burnett", 1911, 256, ["Children's", "Classic"]),
    ("A Little Princess", "Frances Hodgson Burnett", 1905, 246, ["Children's", "Classic"]),
    ("The Wind in the Willows", "Kenneth Grahame", 1908, 200, ["Children's", "Classic"]),
    ("Treasure Island", "Robert Louis Stevenson", 1883, 292, ["Children's", "Adventure", "Classic"]),
    ("Kidnapped", "Robert Louis Stevenson", 1886, 252, ["Adventure", "Classic"]),
    ("The Strange Case of Dr Jekyll and Mr Hyde", "Robert Louis Stevenson", 1886, 141, ["Horror", "Classic"]),
    ("The Adventures of Tom Sawyer", "Mark Twain", 1876, 274, ["Children's", "Classic"]),
    ("Adventures of Huckleberry Finn", "Mark Twain", 1884, 366, ["Classic"]),
    ("A Connecticut Yankee in King Arthur's Court", "Mark Twain", 1889, 469, ["Classic", "Fantasy"]),
    ("The Prince and the Pauper", "Mark Twain", 1881, 226, ["Classic", "Historical Fiction"]),
    ("The Wonderful Wizard of Oz", "L. Frank Baum", 1900, 148, ["Children's", "Fantasy", "Classic"]),
    ("Peter Pan", "J.M. Barrie", 1911, 200, ["Children's", "Fantasy", "Classic"]),
    ("Alice's Adventures in Wonderland", "Lewis Carroll", 1865, 96, ["Children's", "Fantasy", "Classic"]),
    ("Through the Looking-Glass", "Lewis Carroll", 1871, 100, ["Children's", "Fantasy", "Classic"]),
    ("The Jungle Book", "Rudyard Kipling", 1894, 212, ["Children's", "Classic"]),
    ("Kim", "Rudyard Kipling", 1901, 368, ["Classic", "Adventure"]),
    ("The Just So Stories", "Rudyard Kipling", 1902, 120, ["Children's", "Classic", "Short Stories"]),
    ("Pinocchio", "Carlo Collodi", 1883, 240, ["Children's", "Classic"]),
    ("Little Women", "Louisa May Alcott", 1868, 449, ["Classic", "Literary Fiction"]),
    ("Little Men", "Louisa May Alcott", 1871, 376, ["Children's", "Classic"]),
    ("The Call of the Wild", "Jack London", 1903, 128, ["Classic", "Adventure"]),
    ("White Fang", "Jack London", 1906, 298, ["Classic", "Adventure"]),
    ("The Sea-Wolf", "Jack London", 1904, 366, ["Classic", "Adventure"]),
    ("Heidi", "Johanna Spyri", 1881, 288, ["Children's", "Classic"]),
    ("The Little Prince", "Antoine de Saint-Exupéry", 1943, 96, ["Children's", "Classic", "Philosophy"]),
    ("Night Flight", "Antoine de Saint-Exupéry", 1931, 128, ["Classic"]),
    ("Wind, Sand and Stars", "Antoine de Saint-Exupéry", 1939, 224, ["Memoir", "Classic"]),
]

# Graphic novels and comics
GRAPHIC_NOVELS = [
    ("Watchmen", "Alan Moore", 1987, 416, ["Graphic Novel", "Science Fiction", "Classic"]),
    ("V for Vendetta", "Alan Moore", 1989, 296, ["Graphic Novel", "Dystopian"]),
    ("From Hell", "Alan Moore", 1999, 572, ["Graphic Novel", "Historical Fiction"]),
    ("The League of Extraordinary Gentlemen", "Alan Moore", 1999, 176, ["Graphic Novel", "Adventure"]),
    ("Saga of the Swamp Thing", "Alan Moore", 1987, 208, ["Graphic Novel", "Horror"]),
    ("Promethea", "Alan Moore", 2000, 160, ["Graphic Novel", "Fantasy"]),
    ("Batman: The Dark Knight Returns", "Frank Miller", 1986, 224, ["Graphic Novel"]),
    ("Sin City", "Frank Miller", 1991, 208, ["Graphic Novel", "Crime Fiction"]),
    ("300", "Frank Miller", 1998, 88, ["Graphic Novel", "Historical Fiction"]),
    ("Batman: Year One", "Frank Miller", 1987, 144, ["Graphic Novel"]),
    ("Sandman: Preludes & Nocturnes", "Neil Gaiman", 1989, 240, ["Graphic Novel", "Fantasy"]),
    ("Sandman: The Doll's House", "Neil Gaiman", 1990, 232, ["Graphic Novel", "Fantasy"]),
    ("Sandman: Dream Country", "Neil Gaiman", 1991, 160, ["Graphic Novel", "Fantasy"]),
    ("Sandman: Season of Mists", "Neil Gaiman", 1992, 192, ["Graphic Novel", "Fantasy"]),
    ("Sandman: A Game of You", "Neil Gaiman", 1993, 192, ["Graphic Novel", "Fantasy"]),
    ("Sandman: Fables & Reflections", "Neil Gaiman", 1993, 264, ["Graphic Novel", "Fantasy"]),
    ("Sandman: Brief Lives", "Neil Gaiman", 1994, 256, ["Graphic Novel", "Fantasy"]),
    ("Sandman: World's End", "Neil Gaiman", 1994, 168, ["Graphic Novel", "Fantasy"]),
    ("Sandman: The Kindly Ones", "Neil Gaiman", 1996, 352, ["Graphic Novel", "Fantasy"]),
    ("Sandman: The Wake", "Neil Gaiman", 1997, 192, ["Graphic Novel", "Fantasy"]),
    ("Saga Volume 1", "Brian K. Vaughan", 2012, 160, ["Graphic Novel", "Science Fiction"]),
    ("Y: The Last Man Volume 1", "Brian K. Vaughan", 2002, 128, ["Graphic Novel", "Science Fiction"]),
    ("Paper Girls Volume 1", "Brian K. Vaughan", 2016, 128, ["Graphic Novel", "Science Fiction"]),
    ("Bone: Out from Boneville", "Jeff Smith", 1991, 138, ["Graphic Novel", "Fantasy"]),
    ("Jimmy Corrigan: The Smartest Kid on Earth", "Chris Ware", 2000, 380, ["Graphic Novel"]),
    ("Ghost World", "Daniel Clowes", 1997, 80, ["Graphic Novel"]),
    ("Blankets", "Craig Thompson", 2003, 582, ["Graphic Novel", "Memoir"]),
    ("Black Hole", "Charles Burns", 2005, 368, ["Graphic Novel", "Horror"]),
    ("Building Stories", "Chris Ware", 2012, 260, ["Graphic Novel"]),
    ("My Favorite Thing Is Monsters", "Emil Ferris", 2017, 388, ["Graphic Novel", "Mystery"]),
    ("March: Book One", "John Lewis", 2013, 121, ["Graphic Novel", "History", "Memoir"]),
    ("March: Book Two", "John Lewis", 2015, 192, ["Graphic Novel", "History", "Memoir"]),
    ("March: Book Three", "John Lewis", 2016, 246, ["Graphic Novel", "History", "Memoir"]),
    ("Nimona", "Noelle Stevenson", 2015, 266, ["Graphic Novel", "Fantasy"]),
    ("Daytripper", "Fábio Moon", 2011, 256, ["Graphic Novel", "Literary Fiction"]),
]

# Technology & Business
TECH_BOOKS = [
    ("The Innovator's Dilemma", "Clayton M. Christensen", 1997, 286, ["Business"]),
    ("The Lean Startup", "Eric Ries", 2011, 336, ["Business"]),
    ("Zero to One", "Peter Thiel", 2014, 195, ["Business"]),
    ("Good to Great", "Jim Collins", 2001, 300, ["Business"]),
    ("Built to Last", "Jim Collins", 1994, 342, ["Business"]),
    ("The Hard Thing About Hard Things", "Ben Horowitz", 2014, 304, ["Business", "Memoir"]),
    ("Shoe Dog", "Phil Knight", 2016, 386, ["Business", "Memoir"]),
    ("The Everything Store", "Brad Stone", 2013, 372, ["Business", "Biography"]),
    ("Creativity, Inc.", "Ed Catmull", 2014, 368, ["Business"]),
    ("Bad Blood", "John Carreyrou", 2018, 352, ["Business", "Non-Fiction"]),
    ("The Social Dilemma", "Jeff Orlowski", 2020, 250, ["Technology"]),
    ("The Age of Surveillance Capitalism", "Shoshana Zuboff", 2019, 691, ["Technology", "Non-Fiction"]),
    ("Weapons of Math Destruction", "Cathy O'Neil", 2016, 259, ["Technology", "Non-Fiction"]),
    ("Automating Inequality", "Virginia Eubanks", 2018, 260, ["Technology", "Non-Fiction"]),
    ("Race After Technology", "Ruha Benjamin", 2019, 172, ["Technology", "Non-Fiction"]),
    ("Life 3.0", "Max Tegmark", 2017, 364, ["Technology", "Science"]),
    ("Superintelligence", "Nick Bostrom", 2014, 352, ["Technology", "Science"]),
    ("The Singularity Is Near", "Ray Kurzweil", 2005, 652, ["Technology", "Science"]),
    ("How to Create a Mind", "Ray Kurzweil", 2012, 282, ["Technology", "Science"]),
    ("Hackers", "Steven Levy", 1984, 511, ["Technology", "History"]),
    ("The Soul of a New Machine", "Tracy Kidder", 1981, 293, ["Technology", "Non-Fiction"]),
    ("Dealers of Lightning", "Michael A. Hiltzik", 1999, 470, ["Technology", "History"]),
    ("Where Wizards Stay Up Late", "Katie Hafner", 1996, 304, ["Technology", "History"]),
    ("The Cluetrain Manifesto", "Rick Levine", 2000, 190, ["Technology", "Business"]),
    ("In the Plex", "Steven Levy", 2011, 424, ["Technology", "Business"]),
    ("The Filter Bubble", "Eli Pariser", 2011, 294, ["Technology"]),
    ("Algorithms to Live By", "Brian Christian", 2016, 368, ["Technology", "Science"]),
    ("The Master Algorithm", "Pedro Domingos", 2015, 352, ["Technology", "Science"]),
    ("Permanent Record", "Edward Snowden", 2019, 339, ["Memoir", "Technology"]),
    ("The Code Book", "Simon Singh", 1999, 402, ["Technology", "History"]),
    ("Cryptonomicon", "Neal Stephenson", 1999, 918, ["Science Fiction", "Thriller"]),
    ("Snow Crash", "Neal Stephenson", 1992, 440, ["Science Fiction", "Classic"]),
    ("The Diamond Age", "Neal Stephenson", 1995, 455, ["Science Fiction"]),
    ("Anathem", "Neal Stephenson", 2008, 937, ["Science Fiction"]),
    ("Seveneves", "Neal Stephenson", 2015, 880, ["Science Fiction"]),
    ("Reamde", "Neal Stephenson", 2011, 1044, ["Thriller"]),
    ("Termination Shock", "Neal Stephenson", 2021, 720, ["Science Fiction"]),
    ("Neuromancer", "William Gibson", 1984, 271, ["Science Fiction", "Classic"]),
    ("Count Zero", "William Gibson", 1986, 256, ["Science Fiction"]),
    ("Mona Lisa Overdrive", "William Gibson", 1988, 260, ["Science Fiction"]),
    ("Virtual Light", "William Gibson", 1993, 304, ["Science Fiction"]),
    ("Idoru", "William Gibson", 1996, 292, ["Science Fiction"]),
    ("All Tomorrow's Parties", "William Gibson", 1999, 277, ["Science Fiction"]),
    ("Pattern Recognition", "William Gibson", 2003, 356, ["Science Fiction"]),
    ("Spook Country", "William Gibson", 2007, 371, ["Science Fiction"]),
    ("Zero History", "William Gibson", 2010, 404, ["Science Fiction"]),
    ("The Peripheral", "William Gibson", 2014, 485, ["Science Fiction"]),
    ("Agency", "William Gibson", 2020, 416, ["Science Fiction"]),
]

# Philosophy (core texts)
PHILOSOPHY_BOOKS = [
    ("Nicomachean Ethics", "Aristotle", -350, 266, ["Philosophy", "Classic"]),
    ("Poetics", "Aristotle", -335, 100, ["Philosophy", "Classic"]),
    ("Politics", "Aristotle", -350, 368, ["Philosophy", "Classic", "Politics"]),
    ("Critique of Pure Reason", "Immanuel Kant", 1781, 856, ["Philosophy", "Classic"]),
    ("Groundwork of the Metaphysics of Morals", "Immanuel Kant", 1785, 112, ["Philosophy", "Classic"]),
    ("Critique of Practical Reason", "Immanuel Kant", 1788, 204, ["Philosophy", "Classic"]),
    ("Beyond Good and Evil", "Friedrich Nietzsche", 1886, 240, ["Philosophy", "Classic"]),
    ("Thus Spoke Zarathustra", "Friedrich Nietzsche", 1883, 352, ["Philosophy", "Classic"]),
    ("On the Genealogy of Morals", "Friedrich Nietzsche", 1887, 208, ["Philosophy", "Classic"]),
    ("The Birth of Tragedy", "Friedrich Nietzsche", 1872, 160, ["Philosophy", "Classic"]),
    ("Ecce Homo", "Friedrich Nietzsche", 1908, 144, ["Philosophy", "Memoir"]),
    ("The Will to Power", "Friedrich Nietzsche", 1901, 546, ["Philosophy"]),
    ("Twilight of the Idols", "Friedrich Nietzsche", 1889, 112, ["Philosophy"]),
    ("Phenomenology of Spirit", "G.W.F. Hegel", 1807, 591, ["Philosophy", "Classic"]),
    ("The World as Will and Representation", "Arthur Schopenhauer", 1818, 534, ["Philosophy", "Classic"]),
    ("Fear and Trembling", "Søren Kierkegaard", 1843, 158, ["Philosophy", "Classic"]),
    ("Either/Or", "Søren Kierkegaard", 1843, 460, ["Philosophy", "Classic"]),
    ("The Sickness unto Death", "Søren Kierkegaard", 1849, 150, ["Philosophy", "Classic"]),
    ("Philosophical Investigations", "Ludwig Wittgenstein", 1953, 250, ["Philosophy", "Classic"]),
    ("Tractatus Logico-Philosophicus", "Ludwig Wittgenstein", 1921, 75, ["Philosophy", "Classic"]),
    ("Being and Time", "Martin Heidegger", 1927, 589, ["Philosophy", "Classic"]),
    ("The Ethics", "Baruch Spinoza", 1677, 308, ["Philosophy", "Classic"]),
    ("An Essay Concerning Human Understanding", "John Locke", 1689, 700, ["Philosophy", "Classic"]),
    ("A Treatise of Human Nature", "David Hume", 1739, 621, ["Philosophy", "Classic"]),
    ("An Enquiry Concerning Human Understanding", "David Hume", 1748, 186, ["Philosophy", "Classic"]),
    ("Discourse on the Method", "René Descartes", 1637, 86, ["Philosophy", "Classic"]),
    ("Meditations on First Philosophy", "René Descartes", 1641, 59, ["Philosophy", "Classic"]),
    ("The Confessions", "Saint Augustine", 397, 341, ["Philosophy", "Classic", "Memoir"]),
    ("Summa Theologica", "Thomas Aquinas", 1274, 1800, ["Philosophy", "Classic"]),
    ("The Tao Te Ching", "Lao Tzu", -600, 81, ["Philosophy", "Classic"]),
    ("The Analects", "Confucius", -479, 128, ["Philosophy", "Classic"]),
    ("The Art of Living", "Epictetus", 135, 124, ["Philosophy", "Classic"]),
    ("Letters from a Stoic", "Seneca", 65, 256, ["Philosophy", "Classic"]),
    ("The Consolation of Philosophy", "Boethius", 524, 154, ["Philosophy", "Classic"]),
    ("Utilitarianism", "John Stuart Mill", 1863, 70, ["Philosophy", "Classic"]),
    ("The Pragmatist", "William James", 1907, 286, ["Philosophy"]),
    ("Process and Reality", "Alfred North Whitehead", 1929, 413, ["Philosophy"]),
    ("Justice", "Michael Sandel", 2009, 308, ["Philosophy", "Politics"]),
    ("The Moral Landscape", "Sam Harris", 2010, 291, ["Philosophy", "Science"]),
    ("Free Will", "Sam Harris", 2012, 96, ["Philosophy"]),
    ("Waking Up", "Sam Harris", 2014, 256, ["Philosophy"]),
]


def generate():
    all_entries = []
    for title, author, year, pages, genres in YA_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in CHILDREN_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in GRAPHIC_NOVELS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in TECH_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in PHILOSOPHY_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))

    batch_num = 90
    for i in range(0, len(all_entries), 100):
        batch = all_entries[i:i + 100]
        fname = f"batch_{batch_num:02d}_mixed_{batch_num - 89}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(batch, f, indent=2)
        print(f"  {fname}: {len(batch)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(all_entries)}")


if __name__ == "__main__":
    generate()
