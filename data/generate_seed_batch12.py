#!/usr/bin/env python3
"""Batch 12: Non-fiction powerhouses - science, history, politics, biography (batches 79-85)."""
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


BOOKS = []

# Science
SCIENCE_BOOKS = [
    ("The Selfish Gene", "Richard Dawkins", 1976, 360, ["Science", "Biology"]),
    ("The Extended Phenotype", "Richard Dawkins", 1982, 307, ["Science", "Biology"]),
    ("The Blind Watchmaker", "Richard Dawkins", 1986, 332, ["Science", "Biology"]),
    ("Climbing Mount Improbable", "Richard Dawkins", 1996, 340, ["Science", "Biology"]),
    ("Unweaving the Rainbow", "Richard Dawkins", 1998, 336, ["Science"]),
    ("The Ancestor's Tale", "Richard Dawkins", 2004, 614, ["Science", "Biology"]),
    ("The God Delusion", "Richard Dawkins", 2006, 374, ["Science", "Philosophy"]),
    ("The Greatest Show on Earth", "Richard Dawkins", 2009, 470, ["Science", "Biology"]),
    ("A Brief History of Time", "Stephen Hawking", 1988, 256, ["Science", "Physics"]),
    ("The Universe in a Nutshell", "Stephen Hawking", 2001, 216, ["Science", "Physics"]),
    ("The Grand Design", "Stephen Hawking", 2010, 199, ["Science", "Physics"]),
    ("Brief Answers to the Big Questions", "Stephen Hawking", 2018, 256, ["Science", "Physics"]),
    ("Cosmos", "Carl Sagan", 1980, 365, ["Science", "Astronomy"]),
    ("The Dragons of Eden", "Carl Sagan", 1977, 263, ["Science"]),
    ("Broca's Brain", "Carl Sagan", 1979, 347, ["Science"]),
    ("Contact", "Carl Sagan", 1985, 432, ["Science Fiction"]),
    ("Pale Blue Dot", "Carl Sagan", 1994, 429, ["Science", "Astronomy"]),
    ("The Demon-Haunted World", "Carl Sagan", 1995, 457, ["Science"]),
    ("Billions & Billions", "Carl Sagan", 1997, 296, ["Science"]),
    ("The Elegant Universe", "Brian Greene", 1999, 448, ["Science", "Physics"]),
    ("The Fabric of the Cosmos", "Brian Greene", 2004, 569, ["Science", "Physics"]),
    ("The Hidden Reality", "Brian Greene", 2011, 370, ["Science", "Physics"]),
    ("Until the End of Time", "Brian Greene", 2020, 428, ["Science", "Physics"]),
    ("Surely You're Joking, Mr. Feynman!", "Richard Feynman", 1985, 350, ["Science", "Memoir"]),
    ("What Do You Care What Other People Think?", "Richard Feynman", 1988, 255, ["Science", "Memoir"]),
    ("The Pleasure of Finding Things Out", "Richard Feynman", 1999, 270, ["Science"]),
    ("QED: The Strange Theory of Light and Matter", "Richard Feynman", 1985, 158, ["Science", "Physics"]),
    ("Six Easy Pieces", "Richard Feynman", 1994, 168, ["Science", "Physics"]),
    ("The Structure of Scientific Revolutions", "Thomas S. Kuhn", 1962, 210, ["Science", "Philosophy"]),
    ("Gödel, Escher, Bach", "Douglas Hofstadter", 1979, 777, ["Science", "Philosophy", "Classic"]),
    ("I Am a Strange Loop", "Douglas Hofstadter", 2007, 412, ["Science", "Philosophy"]),
    ("The Emperor's New Mind", "Roger Penrose", 1989, 602, ["Science", "Physics"]),
    ("The Road to Reality", "Roger Penrose", 2004, 1099, ["Science", "Physics"]),
    ("Chaos", "James Gleick", 1987, 352, ["Science"]),
    ("The Information", "James Gleick", 2011, 526, ["Science", "History"]),
    ("Genius: The Life and Science of Richard Feynman", "James Gleick", 1992, 532, ["Science", "Biography"]),
    ("Isaac Newton", "James Gleick", 2003, 191, ["Science", "Biography"]),
    ("The Gene: An Intimate History", "Siddhartha Mukherjee", 2016, 592, ["Science", "Biology"]),
    ("The Emperor of All Maladies", "Siddhartha Mukherjee", 2010, 571, ["Science", "History"]),
    ("The Song of the Cell", "Siddhartha Mukherjee", 2022, 496, ["Science", "Biology"]),
    ("Sapiens", "Yuval Noah Harari", 2011, 443, ["Science", "History"]),
    ("Homo Deus", "Yuval Noah Harari", 2015, 449, ["Science", "History"]),
    ("21 Lessons for the 21st Century", "Yuval Noah Harari", 2018, 372, ["Science"]),
    ("The Origin of Species", "Charles Darwin", 1859, 502, ["Science", "Biology", "Classic"]),
    ("The Descent of Man", "Charles Darwin", 1871, 425, ["Science", "Biology"]),
    ("On the Origin of Species by Means of Natural Selection", "Charles Darwin", 1859, 502, ["Science", "Classic"]),
    ("Silent Spring", "Rachel Carson", 1962, 378, ["Science", "Environment"]),
    ("The Sea Around Us", "Rachel Carson", 1951, 250, ["Science"]),
    ("Under the Sea Wind", "Rachel Carson", 1941, 314, ["Science"]),
    ("The Edge of the Sea", "Rachel Carson", 1955, 276, ["Science"]),
    ("Thinking, Fast and Slow", "Daniel Kahneman", 2011, 499, ["Science", "Psychology"]),
    ("Noise: A Flaw in Human Judgment", "Daniel Kahneman", 2021, 454, ["Science", "Psychology"]),
    ("The Black Swan", "Nassim Nicholas Taleb", 2007, 366, ["Science", "Philosophy"]),
    ("Antifragile", "Nassim Nicholas Taleb", 2012, 544, ["Science", "Philosophy"]),
    ("Fooled by Randomness", "Nassim Nicholas Taleb", 2001, 316, ["Science"]),
    ("Skin in the Game", "Nassim Nicholas Taleb", 2018, 304, ["Science", "Philosophy"]),
    ("The Man Who Mistook His Wife for a Hat", "Oliver Sacks", 1985, 233, ["Science", "Psychology"]),
    ("Awakenings", "Oliver Sacks", 1973, 408, ["Science"]),
    ("An Anthropologist on Mars", "Oliver Sacks", 1995, 327, ["Science"]),
    ("Musicophilia", "Oliver Sacks", 2007, 381, ["Science", "Music"]),
    ("Hallucinations", "Oliver Sacks", 2012, 326, ["Science"]),
    ("On the Move", "Oliver Sacks", 2015, 397, ["Science", "Memoir"]),
    ("The Double Helix", "James Watson", 1968, 226, ["Science", "Memoir"]),
    ("A Short History of Nearly Everything", "Bill Bryson", 2003, 544, ["Science", "History"]),
    ("The Body: A Guide for Occupants", "Bill Bryson", 2019, 464, ["Science"]),
    ("Guns, Germs, and Steel", "Jared Diamond", 1997, 480, ["Science", "History"]),
    ("Collapse", "Jared Diamond", 2005, 575, ["Science", "History"]),
    ("The Third Chimpanzee", "Jared Diamond", 1991, 407, ["Science"]),
    ("Upheaval", "Jared Diamond", 2019, 502, ["Science", "History"]),
    ("The Sixth Extinction", "Elizabeth Kolbert", 2014, 319, ["Science", "Environment"]),
    ("Under a White Sky", "Elizabeth Kolbert", 2021, 234, ["Science", "Environment"]),
    ("Field Notes from a Catastrophe", "Elizabeth Kolbert", 2006, 210, ["Science", "Environment"]),
]

# History
HISTORY_BOOKS = [
    ("A People's History of the United States", "Howard Zinn", 1980, 729, ["History"]),
    ("The Rise and Fall of the Third Reich", "William L. Shirer", 1960, 1143, ["History"]),
    ("Guns of August", "Barbara W. Tuchman", 1962, 511, ["History", "War"]),
    ("A Distant Mirror", "Barbara W. Tuchman", 1978, 677, ["History"]),
    ("The Proud Tower", "Barbara W. Tuchman", 1966, 528, ["History"]),
    ("The March of Folly", "Barbara W. Tuchman", 1984, 447, ["History"]),
    ("The Gulag Archipelago", "Aleksandr Solzhenitsyn", 1973, 472, ["History", "Memoir"]),
    ("SPQR: A History of Ancient Rome", "Mary Beard", 2015, 606, ["History"]),
    ("The Civilization of the Renaissance in Italy", "Jacob Burckhardt", 1860, 432, ["History"]),
    ("The Age of Revolution", "Eric Hobsbawm", 1962, 366, ["History"]),
    ("The Age of Capital", "Eric Hobsbawm", 1975, 354, ["History"]),
    ("The Age of Empire", "Eric Hobsbawm", 1987, 404, ["History"]),
    ("The Age of Extremes", "Eric Hobsbawm", 1994, 627, ["History"]),
    ("The Histories", "Herodotus", -440, 716, ["History", "Classic"]),
    ("The Peloponnesian War", "Thucydides", -411, 648, ["History", "Classic"]),
    ("The Decline and Fall of the Roman Empire", "Edward Gibbon", 1776, 3886, ["History", "Classic"]),
    ("Postwar: A History of Europe Since 1945", "Tony Judt", 2005, 878, ["History"]),
    ("Ill Fares the Land", "Tony Judt", 2010, 237, ["History", "Politics"]),
    ("Thinking the Twentieth Century", "Tony Judt", 2012, 414, ["History"]),
    ("The Origins of Totalitarianism", "Hannah Arendt", 1951, 704, ["History", "Philosophy"]),
    ("Eichmann in Jerusalem", "Hannah Arendt", 1963, 312, ["History"]),
    ("The Human Condition", "Hannah Arendt", 1958, 332, ["Philosophy"]),
    ("On Revolution", "Hannah Arendt", 1963, 344, ["History", "Philosophy"]),
    ("Between Past and Future", "Hannah Arendt", 1961, 246, ["Philosophy"]),
    ("Orientalism", "Edward Said", 1978, 368, ["History", "Non-Fiction"]),
    ("Culture and Imperialism", "Edward Said", 1993, 380, ["History", "Non-Fiction"]),
    ("The Silk Roads", "Peter Frankopan", 2015, 636, ["History"]),
    ("The New Silk Roads", "Peter Frankopan", 2018, 304, ["History"]),
    ("The Earth Transformed", "Peter Frankopan", 2023, 720, ["History", "Science"]),
    ("Stamped from the Beginning", "Ibram X. Kendi", 2016, 592, ["History"]),
    ("How to Be an Antiracist", "Ibram X. Kendi", 2019, 305, ["History", "Non-Fiction"]),
    ("The New Jim Crow", "Michelle Alexander", 2010, 290, ["History", "Politics"]),
    ("An Indigenous Peoples' History of the United States", "Roxanne Dunbar-Ortiz", 2014, 296, ["History"]),
    ("1491: New Revelations of the Americas Before Columbus", "Charles C. Mann", 2005, 541, ["History", "Science"]),
    ("1493: Uncovering the New World Columbus Created", "Charles C. Mann", 2011, 535, ["History"]),
    ("Empire of the Summer Moon", "S.C. Gwynne", 2010, 371, ["History"]),
    ("Rebel Yell", "S.C. Gwynne", 2014, 540, ["History", "Biography"]),
    ("The Warmth of Other Suns", "Isabel Wilkerson", 2010, 622, ["History"]),
    ("Caste", "Isabel Wilkerson", 2020, 476, ["History", "Non-Fiction"]),
    ("Bury My Heart at Wounded Knee", "Dee Brown", 1970, 487, ["History"]),
    ("Team of Rivals", "Doris Kearns Goodwin", 2005, 916, ["History", "Biography"]),
    ("No Ordinary Time", "Doris Kearns Goodwin", 1994, 759, ["History", "Biography"]),
    ("The Bully Pulpit", "Doris Kearns Goodwin", 2013, 910, ["History", "Biography"]),
    ("Leadership", "Doris Kearns Goodwin", 2018, 473, ["History", "Biography"]),
]

# Politics & Economics
POLITICS_BOOKS = [
    ("The Wealth of Nations", "Adam Smith", 1776, 1152, ["Economics", "Classic"]),
    ("Capital", "Karl Marx", 1867, 1152, ["Economics", "Classic", "Philosophy"]),
    ("The Communist Manifesto", "Karl Marx", 1848, 80, ["Politics", "Classic"]),
    ("The Republic", "Plato", -375, 416, ["Philosophy", "Classic"]),
    ("The Prince", "Niccolò Machiavelli", 1532, 140, ["Politics", "Classic"]),
    ("On Liberty", "John Stuart Mill", 1859, 128, ["Philosophy", "Classic"]),
    ("A Theory of Justice", "John Rawls", 1971, 607, ["Philosophy", "Politics"]),
    ("The Road to Serfdom", "Friedrich Hayek", 1944, 274, ["Economics", "Politics"]),
    ("Capitalism and Freedom", "Milton Friedman", 1962, 202, ["Economics", "Politics"]),
    ("Free to Choose", "Milton Friedman", 1980, 338, ["Economics", "Politics"]),
    ("Manufacturing Consent", "Noam Chomsky", 1988, 412, ["Politics"]),
    ("Understanding Power", "Noam Chomsky", 2002, 407, ["Politics"]),
    ("Hegemony or Survival", "Noam Chomsky", 2003, 278, ["Politics"]),
    ("Who Rules the World?", "Noam Chomsky", 2016, 307, ["Politics"]),
    ("The Shock Doctrine", "Naomi Klein", 2007, 558, ["Politics", "Economics"]),
    ("This Changes Everything", "Naomi Klein", 2014, 566, ["Politics", "Environment"]),
    ("No Logo", "Naomi Klein", 1999, 490, ["Politics"]),
    ("On Fire", "Naomi Klein", 2019, 310, ["Politics", "Environment"]),
    ("Capital in the Twenty-First Century", "Thomas Piketty", 2013, 696, ["Economics"]),
    ("Capital and Ideology", "Thomas Piketty", 2019, 1104, ["Economics", "History"]),
    ("A Brief History of Equality", "Thomas Piketty", 2021, 274, ["Economics"]),
    ("Why Nations Fail", "Daron Acemoglu", 2012, 529, ["Economics", "Politics", "History"]),
    ("The Narrow Corridor", "Daron Acemoglu", 2019, 560, ["Economics", "Politics"]),
    ("Freakonomics", "Steven D. Levitt", 2005, 242, ["Economics"]),
    ("SuperFreakonomics", "Steven D. Levitt", 2009, 270, ["Economics"]),
    ("Think Like a Freak", "Steven D. Levitt", 2014, 286, ["Economics"]),
    ("Nudge", "Richard H. Thaler", 2008, 312, ["Economics", "Psychology"]),
    ("Misbehaving", "Richard H. Thaler", 2015, 415, ["Economics", "Memoir"]),
    ("The Poverty of Historicism", "Karl Popper", 1957, 166, ["Philosophy"]),
    ("The Open Society and Its Enemies", "Karl Popper", 1945, 732, ["Philosophy", "Politics"]),
    ("The Logic of Scientific Discovery", "Karl Popper", 1959, 513, ["Philosophy", "Science"]),
    ("The Art of War", "Sun Tzu", -500, 68, ["Politics", "Classic"]),
    ("Meditations", "Marcus Aurelius", 180, 254, ["Philosophy", "Classic"]),
    ("The Social Contract", "Jean-Jacques Rousseau", 1762, 168, ["Philosophy", "Classic"]),
    ("Leviathan", "Thomas Hobbes", 1651, 736, ["Philosophy", "Classic"]),
    ("Second Treatise of Government", "John Locke", 1689, 124, ["Philosophy", "Classic"]),
    ("Democracy in America", "Alexis de Tocqueville", 1835, 900, ["Politics", "Classic"]),
]

# Biographies & Memoirs
BIO_BOOKS = [
    ("The Diary of a Young Girl", "Anne Frank", 1947, 283, ["Memoir", "Classic", "History"]),
    ("Long Walk to Freedom", "Nelson Mandela", 1994, 630, ["Memoir", "History"]),
    ("I Know Why the Caged Bird Sings", "Maya Angelou", 1969, 289, ["Memoir", "Classic"]),
    ("Gather Together in My Name", "Maya Angelou", 1974, 214, ["Memoir"]),
    ("The Heart of a Woman", "Maya Angelou", 1981, 272, ["Memoir"]),
    ("All God's Children Need Traveling Shoes", "Maya Angelou", 1986, 209, ["Memoir"]),
    ("Autobiography of Malcolm X", "Malcolm X", 1965, 500, ["Memoir", "History", "Classic"]),
    ("Dreams from My Father", "Barack Obama", 1995, 442, ["Memoir"]),
    ("A Promised Land", "Barack Obama", 2020, 768, ["Memoir", "History"]),
    ("Becoming", "Michelle Obama", 2018, 448, ["Memoir"]),
    ("The Light We Carry", "Michelle Obama", 2022, 336, ["Memoir"]),
    ("Born a Crime", "Trevor Noah", 2016, 304, ["Memoir", "Humor"]),
    ("When Breath Becomes Air", "Paul Kalanithi", 2016, 228, ["Memoir"]),
    ("Educated", "Tara Westover", 2018, 334, ["Memoir"]),
    ("The Glass Castle", "Jeannette Walls", 2005, 288, ["Memoir"]),
    ("Angela's Ashes", "Frank McCourt", 1996, 363, ["Memoir"]),
    ("'Tis", "Frank McCourt", 1999, 367, ["Memoir"]),
    ("Teacher Man", "Frank McCourt", 2005, 258, ["Memoir"]),
    ("Running with Scissors", "Augusten Burroughs", 2002, 304, ["Memoir", "Humor"]),
    ("Dry", "Augusten Burroughs", 2003, 293, ["Memoir"]),
    ("The Year of Magical Thinking", "Joan Didion", 2005, 227, ["Memoir"]),
    ("Blue Nights", "Joan Didion", 2011, 188, ["Memoir"]),
    ("Slouching Towards Bethlehem", "Joan Didion", 1968, 238, ["Non-Fiction"]),
    ("The White Album", "Joan Didion", 1979, 222, ["Non-Fiction"]),
    ("Steve Jobs", "Walter Isaacson", 2011, 656, ["Biography"]),
    ("Einstein: His Life and Universe", "Walter Isaacson", 2007, 675, ["Biography", "Science"]),
    ("Benjamin Franklin", "Walter Isaacson", 2003, 590, ["Biography", "History"]),
    ("Leonardo da Vinci", "Walter Isaacson", 2017, 599, ["Biography", "Art"]),
    ("The Code Breaker", "Walter Isaacson", 2021, 536, ["Biography", "Science"]),
    ("Elon Musk", "Walter Isaacson", 2023, 688, ["Biography"]),
    ("Alexander Hamilton", "Ron Chernow", 2004, 818, ["Biography", "History"]),
    ("Washington: A Life", "Ron Chernow", 2010, 904, ["Biography", "History"]),
    ("Grant", "Ron Chernow", 2017, 1074, ["Biography", "History"]),
    ("Titan: The Life of John D. Rockefeller", "Ron Chernow", 1998, 774, ["Biography", "History"]),
    ("The House of Morgan", "Ron Chernow", 1990, 812, ["History"]),
    ("Narrative of the Life of Frederick Douglass", "Frederick Douglass", 1845, 125, ["Memoir", "Classic", "History"]),
    ("My Bondage and My Freedom", "Frederick Douglass", 1855, 464, ["Memoir", "History"]),
    ("Walden", "Henry David Thoreau", 1854, 352, ["Memoir", "Classic", "Philosophy"]),
    ("On the Road", "Jack Kerouac", 1957, 307, ["Literary Fiction", "Classic"]),
    ("The Dharma Bums", "Jack Kerouac", 1958, 244, ["Literary Fiction"]),
    ("Big Sur", "Jack Kerouac", 1962, 241, ["Literary Fiction"]),
    ("Naked Lunch", "William S. Burroughs", 1959, 289, ["Literary Fiction"]),
    ("Junky", "William S. Burroughs", 1953, 166, ["Memoir"]),
    ("Howl and Other Poems", "Allen Ginsberg", 1956, 44, ["Poetry", "Classic"]),
    ("Persepolis", "Marjane Satrapi", 2000, 153, ["Memoir", "Graphic Novel"]),
    ("Persepolis 2", "Marjane Satrapi", 2004, 187, ["Memoir", "Graphic Novel"]),
    ("Fun Home", "Alison Bechdel", 2006, 232, ["Memoir", "Graphic Novel"]),
    ("Are You My Mother?", "Alison Bechdel", 2012, 286, ["Memoir", "Graphic Novel"]),
    ("Maus I: A Survivor's Tale", "Art Spiegelman", 1986, 159, ["Memoir", "Graphic Novel", "History"]),
    ("Maus II: And Here My Troubles Began", "Art Spiegelman", 1991, 136, ["Memoir", "Graphic Novel", "History"]),
    ("Shackleton's Boat Journey", "Frank Worsley", 1933, 220, ["Memoir", "Adventure"]),
    ("Endurance", "Alfred Lansing", 1959, 357, ["History", "Adventure"]),
    ("Into Thin Air", "Jon Krakauer", 1997, 332, ["Memoir", "Adventure"]),
    ("Into the Wild", "Jon Krakauer", 1996, 207, ["Non-Fiction", "Adventure"]),
    ("Under the Banner of Heaven", "Jon Krakauer", 2003, 372, ["Non-Fiction", "History"]),
    ("Where Men Win Glory", "Jon Krakauer", 2009, 380, ["Non-Fiction", "Biography"]),
]


def generate():
    all_entries = []
    for title, author, year, pages, genres in SCIENCE_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in HISTORY_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in POLITICS_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in BIO_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))

    batch_num = 79
    for i in range(0, len(all_entries), 100):
        batch = all_entries[i:i + 100]
        fname = f"batch_{batch_num:02d}_nonfiction_{batch_num - 78}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(batch, f, indent=2)
        print(f"  {fname}: {len(batch)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(all_entries)}")


if __name__ == "__main__":
    generate()
