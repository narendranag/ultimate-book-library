#!/usr/bin/env python3
"""Batch 9: Classic and contemporary literary authors (batches 63-68)."""
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
    ("Kazuo Ishiguro", "en", ["Literary Fiction"], [
        ("A Pale View of Hills", 1982, 183, []),
        ("An Artist of the Floating World", 1986, 206, []),
        ("The Remains of the Day", 1989, 245, ["Classic"]),
        ("The Unconsoled", 1995, 535, []),
        ("When We Were Orphans", 2000, 313, ["Mystery"]),
        ("Never Let Me Go", 2005, 288, ["Science Fiction"]),
        ("The Buried Giant", 2015, 317, ["Fantasy"]),
        ("Klara and the Sun", 2021, 303, ["Science Fiction"]),
        ("Nocturnes", 2009, 221, ["Short Stories"]),
    ]),
    ("Salman Rushdie", "en", ["Literary Fiction", "Magical Realism"], [
        ("Grimus", 1975, 319, ["Fantasy"]),
        ("Midnight's Children", 1981, 446, ["Indian Fiction", "Classic"]),
        ("Shame", 1983, 286, []),
        ("The Satanic Verses", 1988, 546, []),
        ("Haroun and the Sea of Stories", 1990, 219, ["Fantasy", "Children's"]),
        ("The Moor's Last Sigh", 1995, 435, ["Indian Fiction"]),
        ("The Ground Beneath Her Feet", 1999, 575, []),
        ("Fury", 2001, 259, []),
        ("Shalimar the Clown", 2005, 398, []),
        ("The Enchantress of Florence", 2008, 355, ["Historical Fiction"]),
        ("Luka and the Fire of Life", 2010, 218, ["Fantasy"]),
        ("Two Years Eight Months and Twenty-Eight Nights", 2015, 290, ["Fantasy"]),
        ("The Golden House", 2017, 380, []),
        ("Quichotte", 2019, 397, []),
        ("Victory City", 2023, 343, ["Historical Fiction", "Indian Fiction"]),
    ]),
    ("Cormac McCarthy", "en", ["Literary Fiction", "Western"], [
        ("The Orchard Keeper", 1965, 246, []),
        ("Outer Dark", 1968, 242, []),
        ("Child of God", 1973, 197, []),
        ("Suttree", 1979, 471, []),
        ("Blood Meridian", 1985, 337, ["Classic"]),
        ("All the Pretty Horses", 1992, 302, []),
        ("The Crossing", 1994, 426, []),
        ("Cities of the Plain", 1998, 291, []),
        ("No Country for Old Men", 2005, 309, ["Thriller"]),
        ("The Road", 2006, 287, ["Post-Apocalyptic", "Classic"]),
        ("The Passenger", 2022, 383, []),
        ("Stella Maris", 2022, 190, []),
    ]),
    ("Ian McEwan", "en", ["Literary Fiction"], [
        ("First Love, Last Rites", 1975, 166, ["Short Stories"]),
        ("The Cement Garden", 1978, 138, []),
        ("The Comfort of Strangers", 1981, 100, []),
        ("The Child in Time", 1987, 220, []),
        ("The Innocent", 1990, 280, ["Thriller"]),
        ("Black Dogs", 1992, 174, []),
        ("Enduring Love", 1997, 247, ["Thriller"]),
        ("Amsterdam", 1998, 193, []),
        ("Atonement", 2001, 372, ["Historical Fiction", "Classic"]),
        ("Saturday", 2005, 279, []),
        ("On Chesil Beach", 2007, 166, []),
        ("Solar", 2010, 287, ["Humor"]),
        ("Sweet Tooth", 2012, 310, ["Thriller"]),
        ("The Children Act", 2014, 213, []),
        ("Nutshell", 2016, 199, []),
        ("Machines Like Me", 2019, 306, ["Science Fiction"]),
        ("Lessons", 2022, 485, []),
    ]),
    ("Zadie Smith", "en", ["Literary Fiction"], [
        ("White Teeth", 2000, 448, ["Humor"]),
        ("The Autograph Man", 2002, 347, []),
        ("On Beauty", 2005, 445, []),
        ("NW", 2012, 294, []),
        ("Swing Time", 2016, 453, []),
        ("The Fraud", 2023, 450, ["Historical Fiction"]),
        ("Grand Union", 2019, 242, ["Short Stories"]),
    ]),
    ("Chimamanda Ngozi Adichie", "en", ["Literary Fiction", "African Literature"], [
        ("Purple Hibiscus", 2003, 307, []),
        ("Half of a Yellow Sun", 2006, 433, ["Historical Fiction"]),
        ("Americanah", 2013, 477, []),
        ("The Thing Around Your Neck", 2009, 218, ["Short Stories"]),
        ("Notes on Grief", 2021, 80, ["Memoir"]),
    ]),
    ("Colson Whitehead", "en", ["Literary Fiction"], [
        ("The Intuitionist", 1999, 255, []),
        ("John Henry Days", 2001, 389, []),
        ("Apex Hides the Hurt", 2006, 212, []),
        ("Sag Harbor", 2009, 273, []),
        ("Zone One", 2011, 259, ["Horror"]),
        ("The Underground Railroad", 2016, 306, ["Historical Fiction"]),
        ("The Nickel Boys", 2019, 213, ["Historical Fiction"]),
        ("Harlem Shuffle", 2021, 318, ["Crime Fiction"]),
        ("Crook Manifesto", 2023, 400, ["Crime Fiction"]),
    ]),
    ("Jonathan Franzen", "en", ["Literary Fiction"], [
        ("The Twenty-Seventh City", 1988, 517, []),
        ("Strong Motion", 1992, 508, []),
        ("The Corrections", 2001, 568, ["Classic"]),
        ("Freedom", 2010, 562, []),
        ("Purity", 2015, 563, []),
        ("Crossroads", 2021, 580, []),
    ]),
    ("Paul Auster", "en", ["Literary Fiction", "Postmodern"], [
        ("The Invention of Solitude", 1982, 186, ["Memoir"]),
        ("City of Glass", 1985, 203, ["Mystery"]),
        ("Ghosts", 1986, 96, []),
        ("The Locked Room", 1986, 179, []),
        ("In the Country of Last Things", 1987, 188, ["Dystopian"]),
        ("Moon Palace", 1989, 307, []),
        ("The Music of Chance", 1990, 217, []),
        ("Leviathan", 1992, 275, []),
        ("Mr. Vertigo", 1994, 293, []),
        ("Timbuktu", 1999, 181, []),
        ("The Book of Illusions", 2002, 321, []),
        ("Oracle Night", 2003, 243, []),
        ("The Brooklyn Follies", 2005, 306, []),
        ("Travels in the Scriptorium", 2006, 145, []),
        ("Man in the Dark", 2008, 180, []),
        ("Invisible", 2009, 308, []),
        ("Sunset Park", 2010, 309, []),
        ("4 3 2 1", 2017, 866, []),
        ("Baumgartner", 2023, 208, []),
    ]),
    ("Donna Tartt", "en", ["Literary Fiction"], [
        ("The Secret History", 1992, 559, ["Thriller", "Classic"]),
        ("The Little Friend", 2002, 555, ["Mystery"]),
        ("The Goldfinch", 2013, 771, []),
    ]),
    ("Jeffrey Eugenides", "en", ["Literary Fiction"], [
        ("The Virgin Suicides", 1993, 249, []),
        ("Middlesex", 2002, 529, ["Classic"]),
        ("The Marriage Plot", 2011, 406, []),
        ("Fresh Complaint", 2017, 288, ["Short Stories"]),
    ]),
    ("Michael Chabon", "en", ["Literary Fiction"], [
        ("The Mysteries of Pittsburgh", 1988, 297, []),
        ("Wonder Boys", 1995, 368, ["Humor"]),
        ("The Amazing Adventures of Kavalier & Clay", 2000, 639, ["Historical Fiction", "Classic"]),
        ("The Final Solution", 2004, 131, ["Mystery"]),
        ("The Yiddish Policemen's Union", 2007, 414, ["Mystery", "Alternate History"]),
        ("Gentlemen of the Road", 2007, 204, ["Historical Fiction", "Adventure"]),
        ("Telegraph Avenue", 2012, 468, []),
        ("Moonglow", 2016, 430, []),
    ]),
    ("Louise Erdrich", "en", ["Literary Fiction"], [
        ("Love Medicine", 1984, 367, []),
        ("The Beet Queen", 1986, 338, []),
        ("Tracks", 1988, 226, []),
        ("The Bingo Palace", 1994, 274, []),
        ("Tales of Burning Love", 1996, 452, []),
        ("The Antelope Wife", 1998, 240, []),
        ("The Last Report on the Miracles at Little No Horse", 2001, 361, []),
        ("The Master Butchers Singing Club", 2003, 389, []),
        ("The Painted Drum", 2005, 277, []),
        ("The Plague of Doves", 2008, 313, []),
        ("Shadow Tag", 2010, 255, []),
        ("The Round House", 2012, 321, []),
        ("LaRose", 2016, 372, []),
        ("Future Home of the Living God", 2017, 263, ["Science Fiction"]),
        ("The Night Watchman", 2020, 451, ["Historical Fiction"]),
        ("The Sentence", 2021, 386, []),
    ]),
    ("Marilynne Robinson", "en", ["Literary Fiction"], [
        ("Housekeeping", 1980, 219, ["Classic"]),
        ("Gilead", 2004, 247, ["Classic"]),
        ("Home", 2008, 325, []),
        ("Lila", 2014, 261, []),
        ("Jack", 2020, 308, []),
    ]),
    ("Hilary Mantel", "en", ["Literary Fiction", "Historical Fiction"], [
        ("Every Day Is Mother's Day", 1985, 256, []),
        ("Vacant Possession", 1986, 230, []),
        ("Eight Months on Ghazzah Street", 1988, 272, []),
        ("Fludd", 1989, 181, []),
        ("A Place of Greater Safety", 1992, 749, []),
        ("A Change of Climate", 1994, 342, []),
        ("An Experiment in Love", 1995, 250, []),
        ("The Giant, O'Brien", 1998, 213, []),
        ("Beyond Black", 2005, 365, []),
        ("Wolf Hall", 2009, 604, ["Classic"]),
        ("Bring Up the Bodies", 2012, 432, []),
        ("The Mirror & the Light", 2020, 754, []),
        ("Giving Up the Ghost", 2003, 250, ["Memoir"]),
    ]),
    ("Elena Ferrante", "it", ["Literary Fiction"], [
        ("Troubling Love", 1992, 140, []),
        ("The Days of Abandonment", 2002, 188, []),
        ("The Lost Daughter", 2006, 125, []),
        ("My Brilliant Friend", 2011, 331, []),
        ("The Story of a New Name", 2012, 471, []),
        ("Those Who Leave and Those Who Stay", 2013, 400, []),
        ("The Story of the Lost Child", 2014, 473, []),
        ("The Lying Life of Adults", 2019, 324, []),
    ]),
    ("Orhan Pamuk", "tr", ["Literary Fiction"], [
        ("The White Castle", 1985, 161, ["Historical Fiction"]),
        ("The Black Book", 1990, 462, ["Mystery"]),
        ("The New Life", 1994, 296, []),
        ("My Name Is Red", 1998, 417, ["Historical Fiction", "Mystery"]),
        ("Snow", 2002, 426, []),
        ("The Museum of Innocence", 2008, 535, []),
        ("A Strangeness in My Mind", 2014, 591, []),
        ("The Red-Haired Woman", 2016, 253, []),
        ("Nights of Plague", 2021, 694, ["Historical Fiction"]),
        ("Istanbul: Memories and the City", 2003, 348, ["Memoir"]),
    ]),
    ("Jhumpa Lahiri", "en", ["Literary Fiction", "Indian Fiction"], [
        ("Interpreter of Maladies", 1999, 198, ["Short Stories"]),
        ("The Namesake", 2003, 291, []),
        ("Unaccustomed Earth", 2008, 333, ["Short Stories"]),
        ("The Lowland", 2013, 340, []),
        ("Whereabouts", 2021, 176, []),
    ]),
    ("Arundhati Roy", "en", ["Literary Fiction", "Indian Fiction"], [
        ("The God of Small Things", 1997, 321, ["Classic"]),
        ("The Ministry of Utmost Happiness", 2017, 449, []),
    ]),
    ("Amitav Ghosh", "en", ["Literary Fiction", "Historical Fiction", "Indian Fiction"], [
        ("The Circle of Reason", 1986, 423, []),
        ("The Shadow Lines", 1988, 246, []),
        ("In an Antique Land", 1992, 393, ["Non-Fiction"]),
        ("The Calcutta Chromosome", 1996, 310, ["Science Fiction", "Mystery"]),
        ("The Glass Palace", 2000, 474, []),
        ("The Hungry Tide", 2004, 333, []),
        ("Sea of Poppies", 2008, 515, []),
        ("River of Smoke", 2011, 528, []),
        ("Flood of Fire", 2015, 616, []),
        ("Gun Island", 2019, 292, []),
        ("The Nutmeg's Curse", 2021, 336, ["Non-Fiction"]),
        ("Jungle Nama", 2021, 62, ["Poetry"]),
    ]),
    ("Harlan Coben", "en", ["Thriller", "Mystery"], [
        ("Play Dead", 1990, 324, []),
        ("Miracle Cure", 1991, 352, []),
        ("Deal Breaker", 1995, 312, []),
        ("Drop Shot", 1996, 322, []),
        ("Fade Away", 1996, 309, []),
        ("Back Spin", 1997, 336, []),
        ("One False Move", 1998, 322, []),
        ("The Final Detail", 1999, 340, []),
        ("Darkest Fear", 2000, 308, []),
        ("Tell No One", 2001, 370, []),
        ("Gone for Good", 2002, 340, []),
        ("No Second Chance", 2003, 355, []),
        ("Just One Look", 2004, 370, []),
        ("The Innocent", 2005, 389, []),
        ("Promise Me", 2006, 387, []),
        ("The Woods", 2007, 404, []),
        ("Hold Tight", 2008, 413, []),
        ("Long Lost", 2009, 387, []),
        ("Caught", 2010, 390, []),
        ("Live Wire", 2011, 372, []),
        ("Stay Close", 2012, 400, []),
        ("Six Years", 2013, 356, []),
        ("Missing You", 2014, 385, []),
        ("The Stranger", 2015, 378, []),
        ("Fool Me Once", 2016, 389, []),
        ("Home", 2016, 381, []),
        ("Don't Let Go", 2017, 372, []),
        ("Run Away", 2019, 372, []),
        ("The Boy from the Woods", 2020, 372, []),
        ("Win", 2021, 340, []),
    ]),
    ("Dennis Lehane", "en", ["Mystery", "Thriller", "Crime Fiction"], [
        ("A Drink Before the War", 1994, 273, []),
        ("Darkness, Take My Hand", 1996, 357, []),
        ("Sacred", 1997, 288, []),
        ("Gone, Baby, Gone", 1998, 323, []),
        ("Prayers for Rain", 1999, 337, []),
        ("Mystic River", 2001, 401, ["Literary Fiction"]),
        ("Shutter Island", 2003, 325, ["Horror"]),
        ("The Given Day", 2008, 704, ["Historical Fiction"]),
        ("Moonlight Mile", 2010, 322, []),
        ("Live by Night", 2012, 401, ["Historical Fiction"]),
        ("World Gone By", 2015, 334, ["Historical Fiction"]),
        ("Since We Fell", 2017, 401, []),
        ("Small Mercies", 2023, 320, ["Historical Fiction"]),
    ]),
    ("Jo Nesbø", "no", ["Mystery", "Thriller", "Crime Fiction"], [
        ("The Bat", 1997, 367, []),
        ("Cockroaches", 1998, 398, []),
        ("The Redbreast", 2000, 521, []),
        ("Nemesis", 2002, 474, []),
        ("The Devil's Star", 2003, 452, []),
        ("The Redeemer", 2005, 468, []),
        ("The Snowman", 2007, 550, []),
        ("The Leopard", 2009, 612, []),
        ("Phantom", 2012, 498, []),
        ("Police", 2013, 492, []),
        ("The Thirst", 2017, 496, []),
        ("Knife", 2019, 480, []),
        ("The Kingdom", 2020, 524, []),
        ("The Jealousy Man", 2021, 320, ["Short Stories"]),
        ("Killing Moon", 2023, 496, []),
        ("Headhunters", 2008, 265, []),
        ("Blood on Snow", 2015, 198, []),
        ("Midnight Sun", 2015, 259, []),
        ("Macbeth", 2018, 480, []),
        ("The Son", 2014, 506, []),
    ]),
    ("Henning Mankell", "sv", ["Mystery", "Thriller", "Crime Fiction"], [
        ("Faceless Killers", 1991, 310, []),
        ("The Dogs of Riga", 1992, 326, []),
        ("The White Lioness", 1993, 406, []),
        ("The Man Who Smiled", 1994, 339, []),
        ("Sidetracked", 1995, 410, []),
        ("The Fifth Woman", 1996, 404, []),
        ("One Step Behind", 1997, 407, []),
        ("Firewall", 1998, 402, []),
        ("Before the Frost", 2002, 371, []),
        ("The Troubled Man", 2009, 518, []),
        ("An Event in Autumn", 2013, 130, []),
        ("The Return of the Dancing Master", 2000, 391, []),
        ("Kennedy's Brain", 2005, 384, []),
        ("The Eye of the Leopard", 2008, 325, []),
        ("Italian Shoes", 2006, 310, ["Literary Fiction"]),
        ("Daniel", 2000, 442, ["Historical Fiction"]),
    ]),
]


def generate():
    batch_num = 63
    books_in_batch = []

    for author, lang, default_genres, works in AUTHORS:
        for title, year, pages, extra_genres in works:
            genres = list(default_genres) + extra_genres
            book = make_book(title, author, year, pages, genres, lang)
            books_in_batch.append(book)

            if len(books_in_batch) >= 100:
                fname = f"batch_{batch_num:02d}_authors_{batch_num - 41}.json"
                path = os.path.join(BATCH_DIR, fname)
                with open(path, "w") as f:
                    json.dump(books_in_batch, f, indent=2)
                print(f"  {fname}: {len(books_in_batch)} books")
                batch_num += 1
                books_in_batch = []

    if books_in_batch:
        fname = f"batch_{batch_num:02d}_authors_{batch_num - 41}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(books_in_batch, f, indent=2)
        print(f"  {fname}: {len(books_in_batch)} books")
        batch_num += 1

    total = sum(len(works) for _, _, _, works in AUTHORS)
    print(f"\nTotal new books: {total}")


if __name__ == "__main__":
    generate()
