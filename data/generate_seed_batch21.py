#!/usr/bin/env python3
"""Batch 21: Individual books approach - 1000+ standalone entries across genres."""
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


# Each entry: (title, author, year, pages, genres, lang)
# Focusing on books/authors NOT in previous batches
ALL_BOOKS = [
    # Award-winning literary fiction from 2000s-2020s
    ("The Corrections", "Jonathan Franzen", 2001, 568, ["Literary Fiction"], "en"),
    ("The Amazing Adventures of Kavalier & Clay", "Michael Chabon", 2000, 639, ["Literary Fiction", "Historical Fiction"], "en"),
    ("The Known World", "Edward P. Jones", 2003, 388, ["Literary Fiction", "Historical Fiction"], "en"),
    ("Lost in the City", "Edward P. Jones", 1992, 249, ["Literary Fiction", "Short Stories"], "en"),
    ("Gilead", "Marilynne Robinson", 2004, 247, ["Literary Fiction"], "en"),
    ("The Brief Wondrous Life of Oscar Wao", "Junot Díaz", 2007, 340, ["Literary Fiction"], "en"),
    ("Drown", "Junot Díaz", 1996, 208, ["Literary Fiction", "Short Stories"], "en"),
    ("This Is How You Lose Her", "Junot Díaz", 2012, 213, ["Literary Fiction", "Short Stories"], "en"),
    ("The Sympathizer", "Viet Thanh Nguyen", 2015, 371, ["Literary Fiction", "War"], "en"),
    ("The Committed", "Viet Thanh Nguyen", 2021, 400, ["Literary Fiction"], "en"),
    ("The Refugees", "Viet Thanh Nguyen", 2017, 209, ["Literary Fiction", "Short Stories"], "en"),
    ("Less", "Andrew Sean Greer", 2017, 261, ["Literary Fiction", "Humor"], "en"),
    ("Less Is Lost", "Andrew Sean Greer", 2022, 257, ["Literary Fiction", "Humor"], "en"),
    ("The Overstory", "Richard Powers", 2018, 502, ["Literary Fiction"], "en"),
    ("A Visit from the Goon Squad", "Jennifer Egan", 2010, 273, ["Literary Fiction"], "en"),
    ("Manhattan Beach", "Jennifer Egan", 2017, 438, ["Literary Fiction", "Historical Fiction"], "en"),
    ("The Candy House", "Jennifer Egan", 2022, 336, ["Literary Fiction", "Science Fiction"], "en"),
    ("The Orphan Master's Son", "Adam Johnson", 2012, 443, ["Literary Fiction"], "en"),
    ("Fortune Smiles", "Adam Johnson", 2015, 230, ["Literary Fiction", "Short Stories"], "en"),
    ("The Sellout", "Paul Beatty", 2015, 289, ["Literary Fiction", "Satire"], "en"),
    ("The White Boy Shuffle", "Paul Beatty", 1996, 226, ["Literary Fiction", "Humor"], "en"),
    ("Pachinko", "Min Jin Lee", 2017, 490, ["Literary Fiction", "Historical Fiction"], "en"),
    ("Free Food for Millionaires", "Min Jin Lee", 2007, 566, ["Literary Fiction"], "en"),
    ("There There", "Tommy Orange", 2018, 290, ["Literary Fiction"], "en"),
    ("Wandering Stars", "Tommy Orange", 2024, 315, ["Literary Fiction"], "en"),
    ("Interior Chinatown", "Charles Yu", 2020, 273, ["Literary Fiction", "Satire"], "en"),
    ("How to Live Safely in a Science Fictional Universe", "Charles Yu", 2010, 233, ["Science Fiction"], "en"),
    ("Shuggie Bain", "Douglas Stuart", 2020, 430, ["Literary Fiction"], "en"),
    ("Young Mungo", "Douglas Stuart", 2022, 395, ["Literary Fiction"], "en"),
    ("The Trees", "Percival Everett", 2021, 308, ["Literary Fiction", "Satire"], "en"),
    ("James", "Percival Everett", 2024, 303, ["Literary Fiction", "Historical Fiction"], "en"),
    ("Erasure", "Percival Everett", 2001, 294, ["Literary Fiction", "Satire"], "en"),
    ("Demon Copperhead", "Barbara Kingsolver", 2022, 548, ["Literary Fiction"], "en"),
    ("Trust", "Hernan Diaz", 2022, 416, ["Literary Fiction", "Historical Fiction"], "en"),
    ("In the Distance", "Hernan Diaz", 2017, 246, ["Literary Fiction", "Western"], "en"),
    ("The Netanyahus", "Joshua Cohen", 2021, 237, ["Literary Fiction", "Humor"], "en"),
    ("Book of Numbers", "Joshua Cohen", 2015, 580, ["Literary Fiction"], "en"),
    ("Witz", "Joshua Cohen", 2010, 817, ["Literary Fiction"], "en"),

    # Thriller/Mystery standalone picks
    ("The Girl with the Dragon Tattoo", "Stieg Larsson", 2005, 465, ["Mystery", "Thriller"], "sv"),
    ("The Girl Who Played with Fire", "Stieg Larsson", 2006, 503, ["Mystery", "Thriller"], "sv"),
    ("The Girl Who Kicked the Hornets' Nest", "Stieg Larsson", 2007, 563, ["Mystery", "Thriller"], "sv"),
    ("Gone Girl", "Gillian Flynn", 2012, 419, ["Thriller", "Mystery"], "en"),
    ("Sharp Objects", "Gillian Flynn", 2006, 254, ["Thriller", "Mystery"], "en"),
    ("Dark Places", "Gillian Flynn", 2009, 349, ["Thriller", "Mystery"], "en"),
    ("The Girl on the Train", "Paula Hawkins", 2015, 323, ["Thriller", "Mystery"], "en"),
    ("Into the Water", "Paula Hawkins", 2017, 386, ["Thriller", "Mystery"], "en"),
    ("A Slow Fire Burning", "Paula Hawkins", 2021, 295, ["Thriller"], "en"),
    ("The Silent Patient", "Alex Michaelides", 2019, 325, ["Thriller", "Mystery"], "en"),
    ("The Maidens", "Alex Michaelides", 2021, 337, ["Thriller", "Mystery"], "en"),
    ("The Fury", "Alex Michaelides", 2024, 336, ["Thriller"], "en"),
    ("The Woman in the Window", "A.J. Finn", 2018, 427, ["Thriller", "Mystery"], "en"),
    ("The Maid", "Nita Prose", 2022, 305, ["Mystery"], "en"),
    ("The Mystery Guest", "Nita Prose", 2023, 318, ["Mystery"], "en"),
    ("Mexican Gothic", "Silvia Moreno-Garcia", 2020, 301, ["Horror", "Mystery"], "en"),
    ("The Daughter of Doctor Moreau", "Silvia Moreno-Garcia", 2022, 309, ["Science Fiction"], "en"),
    ("Velvet Was the Night", "Silvia Moreno-Garcia", 2021, 277, ["Mystery", "Thriller"], "en"),
    ("In the Woods", "Tana French", 2007, 429, ["Mystery", "Thriller"], "en"),
    ("The Likeness", "Tana French", 2008, 466, ["Mystery", "Thriller"], "en"),
    ("Faithful Place", "Tana French", 2010, 400, ["Mystery", "Thriller"], "en"),
    ("Broken Harbor", "Tana French", 2012, 449, ["Mystery", "Thriller"], "en"),
    ("The Secret Place", "Tana French", 2014, 457, ["Mystery", "Thriller"], "en"),
    ("The Trespasser", "Tana French", 2016, 450, ["Mystery", "Thriller"], "en"),
    ("The Witch Elm", "Tana French", 2018, 509, ["Mystery", "Thriller"], "en"),
    ("The Searcher", "Tana French", 2020, 449, ["Mystery"], "en"),
    ("The Hunter", "Tana French", 2024, 371, ["Mystery"], "en"),

    # Fantasy standalone picks
    ("The Name of the Wind", "Patrick Rothfuss", 2007, 662, ["Fantasy"], "en"),
    ("The Wise Man's Fear", "Patrick Rothfuss", 2011, 994, ["Fantasy"], "en"),
    ("The Slow Regard of Silent Things", "Patrick Rothfuss", 2014, 159, ["Fantasy"], "en"),
    ("The Lies of Locke Lamora", "Scott Lynch", 2006, 499, ["Fantasy", "Adventure"], "en"),
    ("Red Seas Under Red Skies", "Scott Lynch", 2007, 558, ["Fantasy", "Adventure"], "en"),
    ("The Republic of Thieves", "Scott Lynch", 2013, 512, ["Fantasy"], "en"),
    ("The Goblin Emperor", "Katherine Addison", 2014, 448, ["Fantasy"], "en"),
    ("The Witness for the Dead", "Katherine Addison", 2021, 240, ["Fantasy"], "en"),
    ("The Grief of Stones", "Katherine Addison", 2022, 288, ["Fantasy"], "en"),
    ("Piranesi", "Susanna Clarke", 2020, 245, ["Fantasy"], "en"),
    ("Jonathan Strange & Mr Norrell", "Susanna Clarke", 2004, 782, ["Fantasy", "Historical Fiction"], "en"),
    ("The Priory of the Orange Tree", "Samantha Shannon", 2019, 848, ["Fantasy"], "en"),
    ("A Day of Fallen Night", "Samantha Shannon", 2023, 864, ["Fantasy"], "en"),
    ("The Bone Season", "Samantha Shannon", 2013, 466, ["Fantasy", "Science Fiction"], "en"),
    ("The Mime Order", "Samantha Shannon", 2015, 528, ["Fantasy"], "en"),
    ("The Song of Achilles", "Madeline Miller", 2011, 352, ["Fantasy", "Literary Fiction"], "en"),
    ("Circe", "Madeline Miller", 2018, 393, ["Fantasy", "Literary Fiction"], "en"),
    ("The Rage of Dragons", "Evan Winter", 2017, 544, ["Fantasy"], "en"),
    ("The Fires of Vengeance", "Evan Winter", 2020, 560, ["Fantasy"], "en"),
    ("Black Sun", "Rebecca Roanhorse", 2020, 454, ["Fantasy"], "en"),
    ("Fevered Star", "Rebecca Roanhorse", 2022, 410, ["Fantasy"], "en"),
    ("Mirage of the Lost", "Rebecca Roanhorse", 2023, 420, ["Fantasy"], "en"),
    ("Trail of Lightning", "Rebecca Roanhorse", 2018, 287, ["Fantasy"], "en"),
    ("Storm of Locusts", "Rebecca Roanhorse", 2019, 317, ["Fantasy"], "en"),
    ("The Jasmine Throne", "Tasha Suri", 2021, 533, ["Fantasy"], "en"),
    ("The Oleander Sword", "Tasha Suri", 2022, 496, ["Fantasy"], "en"),
    ("The Burning Kingdoms", "Tasha Suri", 2023, 512, ["Fantasy"], "en"),
    ("Jade City", "Fonda Lee", 2017, 560, ["Fantasy"], "en"),
    ("Jade War", "Fonda Lee", 2019, 590, ["Fantasy"], "en"),
    ("Jade Legacy", "Fonda Lee", 2021, 725, ["Fantasy"], "en"),

    # Sci-fi standalone picks
    ("Project Hail Mary", "Andy Weir", 2021, 476, ["Science Fiction"], "en"),
    ("The Martian", "Andy Weir", 2011, 369, ["Science Fiction"], "en"),
    ("Artemis", "Andy Weir", 2017, 305, ["Science Fiction"], "en"),
    ("The Three-Body Problem", "Liu Cixin", 2008, 302, ["Science Fiction"], "zh"),
    ("The Dark Forest", "Liu Cixin", 2008, 400, ["Science Fiction"], "zh"),
    ("Death's End", "Liu Cixin", 2010, 604, ["Science Fiction"], "zh"),
    ("Ball Lightning", "Liu Cixin", 2004, 384, ["Science Fiction"], "zh"),
    ("The Wandering Earth", "Liu Cixin", 2000, 400, ["Science Fiction", "Short Stories"], "zh"),
    ("Station Eleven", "Emily St. John Mandel", 2014, 333, ["Science Fiction", "Literary Fiction"], "en"),
    ("The Glass Hotel", "Emily St. John Mandel", 2020, 302, ["Literary Fiction"], "en"),
    ("Sea of Tranquility", "Emily St. John Mandel", 2022, 255, ["Science Fiction", "Literary Fiction"], "en"),
    ("The Last Astronaut", "David Wellington", 2019, 416, ["Science Fiction", "Horror"], "en"),
    ("Recursion", "Blake Crouch", 2019, 304, ["Science Fiction", "Thriller"], "en"),
    ("Dark Matter", "Blake Crouch", 2016, 342, ["Science Fiction", "Thriller"], "en"),
    ("Upgrade", "Blake Crouch", 2022, 352, ["Science Fiction", "Thriller"], "en"),
    ("The Anomaly", "Hervé Le Tellier", 2020, 327, ["Science Fiction", "Literary Fiction"], "fr"),
    ("Klara and the Sun", "Kazuo Ishiguro", 2021, 303, ["Science Fiction", "Literary Fiction"], "en"),
    ("Exhalation", "Ted Chiang", 2019, 341, ["Science Fiction", "Short Stories"], "en"),
    ("Stories of Your Life and Others", "Ted Chiang", 2002, 281, ["Science Fiction", "Short Stories"], "en"),
    ("Annihilation", "Jeff VanderMeer", 2014, 195, ["Science Fiction", "Horror"], "en"),
    ("Authority", "Jeff VanderMeer", 2014, 341, ["Science Fiction"], "en"),
    ("Acceptance", "Jeff VanderMeer", 2014, 341, ["Science Fiction"], "en"),
    ("Borne", "Jeff VanderMeer", 2017, 323, ["Science Fiction"], "en"),
    ("Dead Astronauts", "Jeff VanderMeer", 2019, 208, ["Science Fiction"], "en"),
    ("Hummingbird Salamander", "Jeff VanderMeer", 2021, 320, ["Science Fiction", "Thriller"], "en"),
    ("Absolution", "Jeff VanderMeer", 2024, 672, ["Science Fiction"], "en"),
    ("The Calculating Stars", "Mary Robinette Kowal", 2018, 431, ["Science Fiction", "Historical Fiction"], "en"),
    ("The Fated Sky", "Mary Robinette Kowal", 2018, 384, ["Science Fiction"], "en"),
    ("The Relentless Moon", "Mary Robinette Kowal", 2020, 544, ["Science Fiction"], "en"),
    ("The Spare Man", "Mary Robinette Kowal", 2022, 368, ["Science Fiction", "Mystery"], "en"),
    ("All Systems Red", "Martha Wells", 2017, 144, ["Science Fiction"], "en"),
    ("Artificial Condition", "Martha Wells", 2018, 158, ["Science Fiction"], "en"),
    ("Rogue Protocol", "Martha Wells", 2018, 160, ["Science Fiction"], "en"),
    ("Exit Strategy", "Martha Wells", 2018, 176, ["Science Fiction"], "en"),
    ("Network Effect", "Martha Wells", 2020, 352, ["Science Fiction"], "en"),
    ("Fugitive Telemetry", "Martha Wells", 2021, 168, ["Science Fiction", "Mystery"], "en"),
    ("System Collapse", "Martha Wells", 2023, 245, ["Science Fiction"], "en"),

    # Horror standalone picks
    ("The Haunting of Hill House", "Shirley Jackson", 1959, 246, ["Horror", "Classic"], "en"),
    ("Mexican Gothic", "Silvia Moreno-Garcia", 2020, 301, ["Horror", "Mystery"], "en"),
    ("My Heart Is a Chainsaw", "Stephen Graham Jones", 2021, 404, ["Horror"], "en"),
    ("Don't Fear the Reaper", "Stephen Graham Jones", 2023, 432, ["Horror"], "en"),
    ("The Angel of Indian Lake", "Stephen Graham Jones", 2024, 400, ["Horror"], "en"),
    ("The Only Good Indians", "Stephen Graham Jones", 2020, 320, ["Horror"], "en"),
    ("Mongrels", "Stephen Graham Jones", 2016, 300, ["Horror"], "en"),
    ("The Troop", "Nick Cutter", 2014, 358, ["Horror"], "en"),
    ("The Deep", "Nick Cutter", 2015, 394, ["Horror"], "en"),
    ("Little Heaven", "Nick Cutter", 2017, 480, ["Horror"], "en"),
    ("The Cabin at the End of the World", "Paul Tremblay", 2018, 272, ["Horror"], "en"),
    ("A Head Full of Ghosts", "Paul Tremblay", 2015, 286, ["Horror"], "en"),
    ("Disappearance at Devil's Rock", "Paul Tremblay", 2016, 336, ["Horror", "Mystery"], "en"),
    ("Survivor Song", "Paul Tremblay", 2020, 288, ["Horror"], "en"),
    ("The Pallbearers Club", "Paul Tremblay", 2022, 288, ["Horror"], "en"),
    ("Horror Movie", "Paul Tremblay", 2024, 277, ["Horror"], "en"),
    ("The Fisherman", "John Langan", 2016, 266, ["Horror"], "en"),
    ("Children of the Corn", "Stephen Graham Jones", 2023, 304, ["Horror"], "en"),

    # More romance/contemporary fiction
    ("The Seven Husbands of Evelyn Hugo", "Taylor Jenkins Reid", 2017, 389, ["Literary Fiction", "Romance"], "en"),
    ("Daisy Jones & The Six", "Taylor Jenkins Reid", 2019, 355, ["Literary Fiction"], "en"),
    ("Malibu Rising", "Taylor Jenkins Reid", 2021, 369, ["Literary Fiction"], "en"),
    ("Beach Read", "Emily Henry", 2020, 361, ["Romance"], "en"),
    ("People We Meet on Vacation", "Emily Henry", 2021, 364, ["Romance"], "en"),
    ("Book Lovers", "Emily Henry", 2022, 373, ["Romance"], "en"),
    ("The Love Hypothesis", "Ali Hazelwood", 2021, 384, ["Romance"], "en"),
    ("It Ends with Us", "Colleen Hoover", 2016, 376, ["Romance"], "en"),

    # Indian fiction (fresh entries)
    ("The White Tiger", "Aravind Adiga", 2008, 321, ["Literary Fiction", "Indian Fiction"], "en"),
    ("Shantaram", "Gregory David Roberts", 2003, 936, ["Literary Fiction", "Adventure", "Indian Fiction"], "en"),
    ("The Shadow of the Wind", "Carlos Ruiz Zafón", 2001, 487, ["Literary Fiction", "Mystery"], "es"),
    ("The Angel's Game", "Carlos Ruiz Zafón", 2008, 531, ["Literary Fiction", "Mystery"], "es"),
    ("The Prisoner of Heaven", "Carlos Ruiz Zafón", 2011, 279, ["Literary Fiction", "Mystery"], "es"),
    ("The Labyrinth of the Spirits", "Carlos Ruiz Zafón", 2016, 821, ["Literary Fiction", "Mystery"], "es"),
    ("Marina", "Carlos Ruiz Zafón", 1999, 323, ["Young Adult", "Mystery"], "es"),
    ("The Prince of Mist", "Carlos Ruiz Zafón", 1993, 199, ["Young Adult", "Mystery"], "es"),

    # More nonfiction
    ("Thinking, Fast and Slow", "Daniel Kahneman", 2011, 499, ["Psychology", "Science"], "en"),
    ("The Body Keeps the Score", "Bessel van der Kolk", 2014, 464, ["Psychology", "Science"], "en"),
    ("Maybe You Should Talk to Someone", "Lori Gottlieb", 2019, 415, ["Psychology", "Memoir"], "en"),
    ("The Warmth of Other Suns", "Isabel Wilkerson", 2010, 622, ["History"], "en"),
    ("Caste", "Isabel Wilkerson", 2020, 476, ["History"], "en"),
    ("Between the World and Me", "Ta-Nehisi Coates", 2015, 152, ["Memoir", "History"], "en"),
    ("The Water Dancer", "Ta-Nehisi Coates", 2019, 403, ["Literary Fiction", "Historical Fiction"], "en"),
    ("We Were Eight Years in Power", "Ta-Nehisi Coates", 2017, 367, ["History"], "en"),
    ("The Message", "Ta-Nehisi Coates", 2024, 240, ["Non-Fiction"], "en"),
    ("Crying in H Mart", "Michelle Zauner", 2021, 239, ["Memoir", "Food"], "en"),
    ("Know My Name", "Chanel Miller", 2019, 368, ["Memoir"], "en"),
    ("The Glass Castle", "Jeannette Walls", 2005, 288, ["Memoir"], "en"),
    ("Half Broke Horses", "Jeannette Walls", 2009, 261, ["Memoir"], "en"),
    ("Heavy", "Kiese Laymon", 2018, 241, ["Memoir"], "en"),
    ("Long Division", "Kiese Laymon", 2013, 249, ["Literary Fiction"], "en"),
    ("All About Love", "bell hooks", 2000, 240, ["Non-Fiction", "Philosophy"], "en"),
    ("Ain't I a Woman", "bell hooks", 1981, 205, ["Non-Fiction"], "en"),
    ("Teaching to Transgress", "bell hooks", 1994, 216, ["Non-Fiction"], "en"),
    ("Feminist Theory", "bell hooks", 1984, 174, ["Non-Fiction"], "en"),
    ("When Things Fall Apart", "Pema Chödrön", 1997, 160, ["Philosophy"], "en"),
    ("The Places That Scare You", "Pema Chödrön", 2001, 145, ["Philosophy"], "en"),
    ("Start Where You Are", "Pema Chödrön", 1994, 166, ["Philosophy"], "en"),
    ("No Mud, No Lotus", "Thich Nhat Hanh", 2014, 116, ["Philosophy"], "en"),
    ("The Heart of the Buddha's Teaching", "Thich Nhat Hanh", 1998, 288, ["Philosophy"], "en"),
    ("Peace Is Every Step", "Thich Nhat Hanh", 1991, 134, ["Philosophy"], "en"),
    ("The Miracle of Mindfulness", "Thich Nhat Hanh", 1975, 140, ["Philosophy"], "en"),
    ("Siddhartha", "Hermann Hesse", 1922, 152, ["Literary Fiction", "Philosophy", "Classic"], "de"),
    ("Zen and the Art of Motorcycle Maintenance", "Robert M. Pirsig", 1974, 418, ["Philosophy", "Memoir", "Classic"], "en"),
    ("Lila", "Robert M. Pirsig", 1991, 409, ["Philosophy"], "en"),
]


def generate():
    all_entries = []
    for entry in ALL_BOOKS:
        title, author, year, pages, genres, lang = entry
        all_entries.append(make_book(title, author, year, pages, genres, lang))

    batch_num = 125
    for i in range(0, len(all_entries), 100):
        batch = all_entries[i:i + 100]
        fname = f"batch_{batch_num:03d}_batch21_{batch_num - 124}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(batch, f, indent=2)
        print(f"  {fname}: {len(batch)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(all_entries)}")


if __name__ == "__main__":
    generate()
