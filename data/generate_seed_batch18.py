#!/usr/bin/env python3
"""Batch 18: Massive batch - war fiction, westerns, sports, music, art, travel, food, humor."""
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

# War Fiction & Non-Fiction
WAR_BOOKS = [
    ("All Quiet on the Western Front", "Erich Maria Remarque", 1929, 296, ["War", "Classic"]),
    ("The Naked and the Dead", "Norman Mailer", 1948, 721, ["War", "Classic"]),
    ("The Thin Red Line", "James Jones", 1962, 495, ["War"]),
    ("From Here to Eternity", "James Jones", 1951, 861, ["War", "Classic"]),
    ("Catch-22", "Joseph Heller", 1961, 453, ["War", "Classic", "Humor"]),
    ("Something Happened", "Joseph Heller", 1974, 569, ["Literary Fiction"]),
    ("Good as Gold", "Joseph Heller", 1979, 447, ["Humor"]),
    ("God Knows", "Joseph Heller", 1984, 353, ["Humor", "Historical Fiction"]),
    ("Closing Time", "Joseph Heller", 1994, 464, ["War", "Literary Fiction"]),
    ("The Things They Carried", "Tim O'Brien", 1990, 233, ["War", "Classic", "Short Stories"]),
    ("Going After Cacciato", "Tim O'Brien", 1978, 338, ["War"]),
    ("If I Die in a Combat Zone", "Tim O'Brien", 1973, 209, ["War", "Memoir"]),
    ("In the Lake of the Woods", "Tim O'Brien", 1994, 306, ["Mystery"]),
    ("Matterhorn", "Karl Marlantes", 2010, 592, ["War"]),
    ("What It Is Like to Go to War", "Karl Marlantes", 2011, 256, ["War", "Non-Fiction"]),
    ("The Yellow Birds", "Kevin Powers", 2012, 226, ["War"]),
    ("Redeployment", "Phil Klay", 2014, 291, ["War", "Short Stories"]),
    ("Missionaries", "Phil Klay", 2020, 400, ["War"]),
    ("Billy Lynn's Long Halftime Walk", "Ben Fountain", 2012, 307, ["War", "Satire"]),
    ("The Kite Runner", "Khaled Hosseini", 2003, 371, ["Literary Fiction"]),
    ("A Thousand Splendid Suns", "Khaled Hosseini", 2007, 372, ["Literary Fiction"]),
    ("And the Mountains Echoed", "Khaled Hosseini", 2013, 404, ["Literary Fiction"]),
    ("The Bookseller of Kabul", "Åsne Seierstad", 2002, 288, ["Non-Fiction"]),
    ("The English Patient", "Michael Ondaatje", 1992, 307, ["War", "Literary Fiction", "Classic"]),
    ("Anil's Ghost", "Michael Ondaatje", 2000, 311, ["Literary Fiction"]),
    ("The Cat's Table", "Michael Ondaatje", 2011, 269, ["Literary Fiction"]),
    ("Warlight", "Michael Ondaatje", 2018, 290, ["Literary Fiction"]),
    ("Birdsong", "Sebastian Faulks", 1993, 503, ["War", "Historical Fiction"]),
    ("Charlotte Gray", "Sebastian Faulks", 1998, 399, ["War", "Historical Fiction"]),
    ("Engleby", "Sebastian Faulks", 2007, 316, ["Literary Fiction"]),
    ("A Week in December", "Sebastian Faulks", 2009, 392, ["Literary Fiction"]),
    ("Where My Heart Used to Beat", "Sebastian Faulks", 2015, 288, ["War"]),
    ("Paris Echo", "Sebastian Faulks", 2018, 272, ["Literary Fiction"]),
    ("Band of Brothers", "Stephen E. Ambrose", 1992, 333, ["War", "History"]),
    ("D-Day", "Stephen E. Ambrose", 1994, 655, ["War", "History"]),
    ("Citizen Soldiers", "Stephen E. Ambrose", 1997, 512, ["War", "History"]),
    ("The Longest Day", "Cornelius Ryan", 1959, 350, ["War", "History"]),
    ("A Bridge Too Far", "Cornelius Ryan", 1974, 670, ["War", "History"]),
    ("Black Hawk Down", "Mark Bowden", 1999, 386, ["War", "Non-Fiction"]),
    ("Killing Pablo", "Mark Bowden", 2001, 296, ["Non-Fiction", "History"]),
    ("The Finish", "Mark Bowden", 2012, 263, ["Non-Fiction"]),
]

# Humor / Satire
HUMOR_BOOKS = [
    ("The Hitchhiker's Guide to the Galaxy", "Douglas Adams", 1979, 193, ["Science Fiction", "Humor", "Classic"]),
    ("The Restaurant at the End of the Universe", "Douglas Adams", 1980, 200, ["Science Fiction", "Humor"]),
    ("Life, the Universe and Everything", "Douglas Adams", 1982, 224, ["Science Fiction", "Humor"]),
    ("So Long, and Thanks for All the Fish", "Douglas Adams", 1984, 204, ["Science Fiction", "Humor"]),
    ("Mostly Harmless", "Douglas Adams", 1992, 240, ["Science Fiction", "Humor"]),
    ("Dirk Gently's Holistic Detective Agency", "Douglas Adams", 1987, 306, ["Science Fiction", "Humor"]),
    ("The Long Dark Tea-Time of the Soul", "Douglas Adams", 1988, 307, ["Fantasy", "Humor"]),
    ("Lucky Jim", "Kingsley Amis", 1954, 256, ["Literary Fiction", "Humor", "Classic"]),
    ("Money", "Martin Amis", 1984, 394, ["Literary Fiction", "Humor"]),
    ("London Fields", "Martin Amis", 1989, 470, ["Literary Fiction"]),
    ("Time's Arrow", "Martin Amis", 1991, 168, ["Literary Fiction"]),
    ("The Information", "Martin Amis", 1995, 373, ["Literary Fiction", "Humor"]),
    ("The Rachel Papers", "Martin Amis", 1973, 219, ["Literary Fiction"]),
    ("A Confederacy of Dunces", "John Kennedy Toole", 1980, 394, ["Literary Fiction", "Humor", "Classic"]),
    ("The Neon Bible", "John Kennedy Toole", 1989, 167, ["Literary Fiction"]),
    ("Bridget Jones's Diary", "Helen Fielding", 1996, 310, ["Humor", "Romance"]),
    ("Bridget Jones: The Edge of Reason", "Helen Fielding", 1999, 338, ["Humor", "Romance"]),
    ("Bridget Jones: Mad About the Boy", "Helen Fielding", 2013, 390, ["Humor", "Romance"]),
    ("High Fidelity", "Nick Hornby", 1995, 245, ["Literary Fiction", "Humor"]),
    ("About a Boy", "Nick Hornby", 1998, 307, ["Literary Fiction", "Humor"]),
    ("How to Be Good", "Nick Hornby", 2001, 305, ["Literary Fiction", "Humor"]),
    ("A Long Way Down", "Nick Hornby", 2005, 333, ["Literary Fiction", "Humor"]),
    ("Juliet, Naked", "Nick Hornby", 2009, 406, ["Literary Fiction", "Humor"]),
    ("Funny Girl", "Nick Hornby", 2014, 452, ["Literary Fiction", "Humor"]),
    ("Just Like You", "Nick Hornby", 2020, 374, ["Literary Fiction", "Romance"]),
    ("Heartburn", "Nora Ephron", 1983, 179, ["Humor", "Romance"]),
    ("I Feel Bad About My Neck", "Nora Ephron", 2006, 137, ["Humor", "Memoir"]),
    ("I Remember Nothing", "Nora Ephron", 2010, 137, ["Humor", "Memoir"]),
    ("Is Everyone Hanging Out Without Me?", "Mindy Kaling", 2011, 222, ["Humor", "Memoir"]),
    ("Why Not Me?", "Mindy Kaling", 2015, 228, ["Humor", "Memoir"]),
    ("Bossypants", "Tina Fey", 2011, 277, ["Humor", "Memoir"]),
    ("Yes Please", "Amy Poehler", 2014, 329, ["Humor", "Memoir"]),
    ("Talking as Fast as I Can", "Lauren Graham", 2016, 223, ["Humor", "Memoir"]),
    ("Scrappy Little Nobody", "Anna Kendrick", 2016, 252, ["Humor", "Memoir"]),
    ("Me Talk Pretty One Day", "David Sedaris", 2000, 272, ["Humor", "Memoir"]),
    ("Dress Your Family in Corduroy and Denim", "David Sedaris", 2004, 272, ["Humor", "Memoir"]),
    ("When You Are Engulfed in Flames", "David Sedaris", 2008, 323, ["Humor", "Memoir"]),
    ("Let's Explore Diabetes with Owls", "David Sedaris", 2013, 275, ["Humor", "Memoir"]),
    ("Calypso", "David Sedaris", 2018, 272, ["Humor", "Memoir"]),
    ("Happy-Go-Lucky", "David Sedaris", 2022, 258, ["Humor", "Memoir"]),
    ("A Walk in the Woods", "Bill Bryson", 1998, 276, ["Humor", "Travel"]),
    ("In a Sunburned Country", "Bill Bryson", 2000, 307, ["Humor", "Travel"]),
    ("I'm a Stranger Here Myself", "Bill Bryson", 1999, 288, ["Humor"]),
    ("The Life and Times of the Thunderbolt Kid", "Bill Bryson", 2006, 270, ["Humor", "Memoir"]),
    ("At Home", "Bill Bryson", 2010, 497, ["History", "Humor"]),
    ("Notes from a Small Island", "Bill Bryson", 1995, 252, ["Humor", "Travel"]),
    ("Neither Here Nor There", "Bill Bryson", 1991, 254, ["Humor", "Travel"]),
    ("The Mother Tongue", "Bill Bryson", 1990, 270, ["Humor"]),
    ("Made in America", "Bill Bryson", 1994, 417, ["History"]),
    ("One Summer: America, 1927", "Bill Bryson", 2013, 505, ["History"]),
    ("The Road to Little Dribbling", "Bill Bryson", 2015, 381, ["Humor", "Travel"]),
    ("Three Men in a Boat", "Jerome K. Jerome", 1889, 228, ["Humor", "Classic"]),
    ("The Importance of Being Earnest", "Oscar Wilde", 1895, 76, ["Drama", "Humor", "Classic"]),
    ("The Picture of Dorian Gray", "Oscar Wilde", 1890, 254, ["Literary Fiction", "Classic"]),
    ("De Profundis", "Oscar Wilde", 1905, 100, ["Memoir"]),
    ("An Ideal Husband", "Oscar Wilde", 1895, 96, ["Drama", "Classic"]),
    ("Lady Windermere's Fan", "Oscar Wilde", 1892, 80, ["Drama", "Classic"]),
]

# Music, Art, Cinema books
ARTS_BOOKS = [
    ("Just Kids", "Patti Smith", 2010, 279, ["Memoir", "Art"]),
    ("M Train", "Patti Smith", 2015, 253, ["Memoir"]),
    ("Year of the Monkey", "Patti Smith", 2019, 197, ["Memoir"]),
    ("Chronicles: Volume One", "Bob Dylan", 2004, 293, ["Memoir", "Music"]),
    ("The Philosophy of Andy Warhol", "Andy Warhol", 1975, 241, ["Art", "Memoir"]),
    ("Life", "Keith Richards", 2010, 564, ["Memoir", "Music"]),
    ("Scar Tissue", "Anthony Kiedis", 2004, 465, ["Memoir", "Music"]),
    ("Born to Run", "Bruce Springsteen", 2016, 508, ["Memoir", "Music"]),
    ("The Rest Is Noise", "Alex Ross", 2007, 624, ["Music", "History"]),
    ("How Music Works", "David Byrne", 2012, 350, ["Music"]),
    ("Rip It Up and Start Again", "Simon Reynolds", 2005, 402, ["Music", "History"]),
    ("Please Kill Me", "Legs McNeil", 1996, 432, ["Music", "History"]),
    ("Our Band Could Be Your Life", "Michael Azerrad", 2001, 520, ["Music", "History"]),
    ("Love Is a Mix Tape", "Rob Sheffield", 2007, 224, ["Memoir", "Music"]),
    ("Talking to Girls About Duran Duran", "Rob Sheffield", 2010, 240, ["Memoir", "Music"]),
    ("The Story of Art", "E.H. Gombrich", 1950, 688, ["Art", "History"]),
    ("Ways of Seeing", "John Berger", 1972, 176, ["Art", "Non-Fiction"]),
    ("The Shock of the New", "Robert Hughes", 1980, 444, ["Art", "History"]),
    ("Interaction of Color", "Josef Albers", 1963, 196, ["Art"]),
    ("On Photography", "Susan Sontag", 1977, 207, ["Art", "Non-Fiction"]),
    ("Regarding the Pain of Others", "Susan Sontag", 2003, 131, ["Non-Fiction"]),
    ("Illness as Metaphor", "Susan Sontag", 1978, 87, ["Non-Fiction"]),
    ("Against Interpretation", "Susan Sontag", 1966, 312, ["Non-Fiction"]),
    ("Easy Riders, Raging Bulls", "Peter Biskind", 1998, 512, ["Cinema", "History"]),
    ("Hitchcock/Truffaut", "François Truffaut", 1966, 367, ["Cinema"]),
    ("Adventures in the Screen Trade", "William Goldman", 1983, 418, ["Cinema", "Memoir"]),
    ("Which Lie Did I Tell?", "William Goldman", 2000, 484, ["Cinema", "Memoir"]),
    ("Rebel Without a Crew", "Robert Rodriguez", 1995, 285, ["Cinema", "Memoir"]),
    ("In the Blink of an Eye", "Walter Murch", 2001, 148, ["Cinema"]),
    ("When the Shooting Stops", "Ralph Rosenblum", 1979, 305, ["Cinema"]),
    ("Sculpting in Time", "Andrei Tarkovsky", 1967, 252, ["Cinema"]),
    ("Notes on the Cinematographer", "Robert Bresson", 1975, 135, ["Cinema"]),
]

# Travel & Nature
TRAVEL_BOOKS = [
    ("In Patagonia", "Bruce Chatwin", 1977, 204, ["Travel", "Classic"]),
    ("The Songlines", "Bruce Chatwin", 1987, 293, ["Travel"]),
    ("On the Road with Charley", "John Steinbeck", 1962, 246, ["Travel"]),
    ("The Great Railway Bazaar", "Paul Theroux", 1975, 342, ["Travel"]),
    ("The Old Patagonian Express", "Paul Theroux", 1979, 404, ["Travel"]),
    ("The Pillars of Hercules", "Paul Theroux", 1995, 509, ["Travel"]),
    ("Ghost Train to the Eastern Star", "Paul Theroux", 2008, 496, ["Travel"]),
    ("Dark Star Safari", "Paul Theroux", 2002, 472, ["Travel"]),
    ("The Mosquito Coast", "Paul Theroux", 1981, 374, ["Literary Fiction", "Adventure"]),
    ("Under the Tuscan Sun", "Frances Mayes", 1996, 280, ["Travel", "Memoir"]),
    ("Bella Tuscany", "Frances Mayes", 1999, 302, ["Travel", "Memoir"]),
    ("A Year in Provence", "Peter Mayle", 1989, 207, ["Travel", "Humor"]),
    ("Toujours Provence", "Peter Mayle", 1991, 241, ["Travel", "Humor"]),
    ("The Alchemist", "Paulo Coelho", 1988, 197, ["Literary Fiction", "Philosophy", "Classic"]),
    ("The Pilgrimage", "Paulo Coelho", 1987, 254, ["Travel"]),
    ("Brida", "Paulo Coelho", 1990, 249, ["Literary Fiction"]),
    ("Veronika Decides to Die", "Paulo Coelho", 1998, 210, ["Literary Fiction"]),
    ("Eleven Minutes", "Paulo Coelho", 2003, 302, ["Literary Fiction"]),
    ("The Zahir", "Paulo Coelho", 2005, 351, ["Literary Fiction"]),
    ("The Witch of Portobello", "Paulo Coelho", 2006, 305, ["Literary Fiction"]),
    ("Aleph", "Paulo Coelho", 2011, 269, ["Literary Fiction"]),
    ("The Snow Leopard", "Peter Matthiessen", 1978, 338, ["Travel", "Memoir", "Classic"]),
    ("The Cloud Forest", "Peter Matthiessen", 1961, 280, ["Travel"]),
    ("Shadow Country", "Peter Matthiessen", 2008, 892, ["Literary Fiction"]),
    ("Arabian Sands", "Wilfred Thesiger", 1959, 347, ["Travel", "Classic"]),
    ("The Marsh Arabs", "Wilfred Thesiger", 1964, 233, ["Travel"]),
    ("Seven Pillars of Wisdom", "T.E. Lawrence", 1926, 672, ["Memoir", "Classic", "History"]),
    ("Kon-Tiki", "Thor Heyerdahl", 1948, 238, ["Travel", "Adventure"]),
    ("The Sheltering Sky", "Paul Bowles", 1949, 335, ["Literary Fiction", "Classic"]),
    ("Let It Come Down", "Paul Bowles", 1952, 311, ["Literary Fiction"]),
    ("The Spider's House", "Paul Bowles", 1955, 406, ["Literary Fiction"]),
    ("Collected Stories of Paul Bowles", "Paul Bowles", 1979, 481, ["Short Stories"]),
    ("Wild", "Cheryl Strayed", 2012, 311, ["Memoir", "Travel"]),
    ("Tiny Beautiful Things", "Cheryl Strayed", 2012, 353, ["Non-Fiction"]),
    ("H Is for Hawk", "Helen Macdonald", 2014, 300, ["Memoir", "Nature"]),
    ("Vesper Flights", "Helen Macdonald", 2020, 272, ["Nature"]),
    ("Pilgrim at Tinker Creek", "Annie Dillard", 1974, 271, ["Nature", "Classic"]),
    ("Teaching a Stone to Talk", "Annie Dillard", 1982, 177, ["Nature"]),
    ("An American Childhood", "Annie Dillard", 1987, 255, ["Memoir"]),
    ("The Writing Life", "Annie Dillard", 1989, 111, ["Non-Fiction"]),
    ("Braiding Sweetgrass", "Robin Wall Kimmerer", 2013, 390, ["Nature", "Science"]),
    ("The Hidden Life of Trees", "Peter Wohlleben", 2015, 288, ["Nature", "Science"]),
    ("Entangled Life", "Merlin Sheldrake", 2020, 358, ["Nature", "Science"]),
    ("The Overstory", "Richard Powers", 2018, 502, ["Literary Fiction"]),
    ("Lab Girl", "Hope Jahren", 2016, 290, ["Memoir", "Science"]),
    ("The Invention of Nature", "Andrea Wulf", 2015, 473, ["Nature", "Biography"]),
    ("Underland", "Robert Macfarlane", 2019, 488, ["Nature", "Travel"]),
    ("The Old Ways", "Robert Macfarlane", 2012, 432, ["Nature", "Travel"]),
    ("Landmarks", "Robert Macfarlane", 2015, 380, ["Nature"]),
    ("The Wild Places", "Robert Macfarlane", 2007, 340, ["Nature", "Travel"]),
    ("Mountains of the Mind", "Robert Macfarlane", 2003, 306, ["Nature"]),
]

# Self-help / Psychology / Productivity
SELFHELP_BOOKS = [
    ("Man's Search for Meaning", "Viktor E. Frankl", 1946, 184, ["Psychology", "Memoir", "Classic"]),
    ("The Power of Now", "Eckhart Tolle", 1997, 236, ["Self-Help", "Philosophy"]),
    ("A New Earth", "Eckhart Tolle", 2005, 316, ["Self-Help"]),
    ("Atomic Habits", "James Clear", 2018, 320, ["Self-Help"]),
    ("The 7 Habits of Highly Effective People", "Stephen R. Covey", 1989, 381, ["Self-Help", "Business"]),
    ("How to Win Friends and Influence People", "Dale Carnegie", 1936, 288, ["Self-Help", "Classic"]),
    ("The Subtle Art of Not Giving a F*ck", "Mark Manson", 2016, 224, ["Self-Help"]),
    ("Everything Is F*cked", "Mark Manson", 2019, 272, ["Self-Help"]),
    ("Deep Work", "Cal Newport", 2016, 296, ["Self-Help", "Business"]),
    ("Digital Minimalism", "Cal Newport", 2019, 302, ["Self-Help"]),
    ("So Good They Can't Ignore You", "Cal Newport", 2012, 268, ["Self-Help"]),
    ("A World Without Email", "Cal Newport", 2021, 288, ["Business"]),
    ("Essentialism", "Greg McKeown", 2014, 260, ["Self-Help"]),
    ("Effortless", "Greg McKeown", 2021, 256, ["Self-Help"]),
    ("Grit", "Angela Duckworth", 2016, 352, ["Psychology"]),
    ("Mindset", "Carol S. Dweck", 2006, 276, ["Psychology"]),
    ("Flow", "Mihaly Csikszentmihalyi", 1990, 303, ["Psychology", "Classic"]),
    ("Quiet", "Susan Cain", 2012, 333, ["Psychology"]),
    ("Bittersweet", "Susan Cain", 2022, 352, ["Psychology"]),
    ("Range", "David Epstein", 2019, 339, ["Psychology"]),
    ("The Sports Gene", "David Epstein", 2013, 338, ["Science", "Sports"]),
    ("Outliers", "Malcolm Gladwell", 2008, 309, ["Psychology", "Non-Fiction"]),
    ("Blink", "Malcolm Gladwell", 2005, 277, ["Psychology"]),
    ("The Tipping Point", "Malcolm Gladwell", 2000, 301, ["Psychology"]),
    ("David and Goliath", "Malcolm Gladwell", 2013, 305, ["Psychology"]),
    ("Talking to Strangers", "Malcolm Gladwell", 2019, 388, ["Psychology"]),
    ("The Bomber Mafia", "Malcolm Gladwell", 2021, 256, ["History"]),
    ("Influence", "Robert B. Cialdini", 1984, 320, ["Psychology", "Business"]),
    ("Pre-Suasion", "Robert B. Cialdini", 2016, 413, ["Psychology"]),
    ("Drive", "Daniel H. Pink", 2009, 242, ["Business", "Psychology"]),
    ("When", "Daniel H. Pink", 2018, 272, ["Psychology"]),
    ("To Sell Is Human", "Daniel H. Pink", 2012, 260, ["Business"]),
    ("The Power of Habit", "Charles Duhigg", 2012, 371, ["Psychology"]),
    ("Smarter Faster Better", "Charles Duhigg", 2016, 380, ["Psychology"]),
    ("Supercommunicators", "Charles Duhigg", 2024, 320, ["Psychology"]),
    ("Stumbling on Happiness", "Daniel Gilbert", 2006, 310, ["Psychology"]),
    ("Predictably Irrational", "Dan Ariely", 2008, 280, ["Psychology", "Economics"]),
    ("The Upside of Irrationality", "Dan Ariely", 2010, 334, ["Psychology"]),
    ("The Honest Truth About Dishonesty", "Dan Ariely", 2012, 298, ["Psychology"]),
    ("Sapiens", "Yuval Noah Harari", 2011, 443, ["History", "Science"]),
    ("Homo Deus", "Yuval Noah Harari", 2015, 449, ["Science"]),
]

# Food & Cooking
FOOD_BOOKS = [
    ("Kitchen Confidential", "Anthony Bourdain", 2000, 312, ["Memoir", "Food"]),
    ("A Cook's Tour", "Anthony Bourdain", 2001, 274, ["Travel", "Food"]),
    ("Medium Raw", "Anthony Bourdain", 2010, 281, ["Memoir", "Food"]),
    ("World Travel", "Anthony Bourdain", 2021, 480, ["Travel", "Food"]),
    ("The Omnivore's Dilemma", "Michael Pollan", 2006, 450, ["Food", "Science"]),
    ("In Defense of Food", "Michael Pollan", 2008, 244, ["Food"]),
    ("Cooked", "Michael Pollan", 2013, 468, ["Food"]),
    ("How to Change Your Mind", "Michael Pollan", 2018, 480, ["Science", "Psychology"]),
    ("My Life in France", "Julia Child", 2006, 304, ["Memoir", "Food"]),
    ("Heat", "Bill Buford", 2006, 318, ["Memoir", "Food"]),
    ("Dirt", "Bill Buford", 2020, 432, ["Memoir", "Food"]),
    ("Salt", "Mark Kurlansky", 2002, 484, ["Food", "History"]),
    ("Cod", "Mark Kurlansky", 1997, 294, ["Food", "History"]),
    ("Milk!", "Mark Kurlansky", 2018, 383, ["Food", "History"]),
    ("The Food of a Younger Land", "Mark Kurlansky", 2009, 397, ["Food", "History"]),
    ("Garlic and Sapphires", "Ruth Reichl", 2005, 333, ["Memoir", "Food"]),
    ("Tender at the Bone", "Ruth Reichl", 1998, 282, ["Memoir", "Food"]),
    ("Comfort Me with Apples", "Ruth Reichl", 2001, 302, ["Memoir", "Food"]),
    ("Delicious!", "Ruth Reichl", 2014, 356, ["Literary Fiction", "Food"]),
    ("Animal, Vegetable, Miracle", "Barbara Kingsolver", 2007, 370, ["Food", "Memoir"]),
    ("The Poisonwood Bible", "Barbara Kingsolver", 1998, 546, ["Literary Fiction", "Historical Fiction"]),
    ("The Bean Trees", "Barbara Kingsolver", 1988, 232, ["Literary Fiction"]),
    ("Pigs in Heaven", "Barbara Kingsolver", 1993, 343, ["Literary Fiction"]),
    ("The Lacuna", "Barbara Kingsolver", 2009, 507, ["Literary Fiction", "Historical Fiction"]),
    ("Flight Behavior", "Barbara Kingsolver", 2012, 436, ["Literary Fiction"]),
    ("Unsheltered", "Barbara Kingsolver", 2018, 462, ["Literary Fiction"]),
    ("Demon Copperhead", "Barbara Kingsolver", 2022, 548, ["Literary Fiction"]),
    ("Prodigal Summer", "Barbara Kingsolver", 2000, 444, ["Literary Fiction"]),
]


def generate():
    all_entries = []
    for title, author, year, pages, genres in WAR_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in HUMOR_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in ARTS_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in TRAVEL_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in SELFHELP_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))
    for title, author, year, pages, genres in FOOD_BOOKS:
        all_entries.append(make_book(title, author, year, pages, genres))

    batch_num = 110
    for i in range(0, len(all_entries), 100):
        batch = all_entries[i:i + 100]
        fname = f"batch_{batch_num:03d}_batch18_{batch_num - 109}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(batch, f, indent=2)
        print(f"  {fname}: {len(batch)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(all_entries)}")


if __name__ == "__main__":
    generate()
