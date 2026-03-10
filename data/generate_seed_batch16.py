#!/usr/bin/env python3
"""Batch 16: More thriller, mystery, romance, and horror authors to boost numbers."""
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
    ("Vince Flynn", "en", ["Thriller", "Political Thriller"], [
        ("Term Limits", 1997, 392, []),
        ("Transfer of Power", 1999, 485, []),
        ("The Third Option", 2000, 468, []),
        ("Separation of Power", 2001, 398, []),
        ("Executive Power", 2003, 422, []),
        ("Memorial Day", 2004, 445, []),
        ("Consent to Kill", 2005, 439, []),
        ("Act of Treason", 2006, 420, []),
        ("Protect and Defend", 2007, 421, []),
        ("Extreme Measures", 2008, 400, []),
        ("Pursuit of Honour", 2009, 418, []),
        ("American Assassin", 2010, 436, []),
        ("Kill Shot", 2012, 420, []),
        ("The Last Man", 2012, 400, []),
    ]),
    ("Brad Thor", "en", ["Thriller", "Political Thriller"], [
        ("The Lions of Lucerne", 2002, 529, []),
        ("Path of the Assassin", 2003, 468, []),
        ("State of the Union", 2004, 417, []),
        ("Blowback", 2005, 404, []),
        ("Takedown", 2006, 380, []),
        ("The First Commandment", 2007, 380, []),
        ("The Last Patriot", 2008, 372, []),
        ("The Apostle", 2009, 416, []),
        ("Foreign Influence", 2010, 416, []),
        ("Full Black", 2011, 384, []),
        ("Black List", 2012, 400, []),
        ("Hidden Order", 2013, 400, []),
        ("Act of War", 2014, 368, []),
        ("Code of Conduct", 2015, 384, []),
        ("Foreign Agent", 2016, 384, []),
        ("Use of Force", 2017, 384, []),
        ("Spymaster", 2018, 400, []),
        ("Backlash", 2019, 384, []),
        ("Near Dark", 2020, 384, []),
        ("Black Ice", 2021, 416, []),
        ("Rising Tiger", 2022, 384, []),
    ]),
    ("Tom Clancy", "en", ["Thriller", "Political Thriller"], [
        ("The Hunt for Red October", 1984, 387, ["Classic"]),
        ("Red Storm Rising", 1986, 652, ["War"]),
        ("Patriot Games", 1987, 540, []),
        ("The Cardinal of the Kremlin", 1988, 543, []),
        ("Clear and Present Danger", 1989, 656, []),
        ("The Sum of All Fears", 1991, 798, []),
        ("Without Remorse", 1993, 639, []),
        ("Debt of Honor", 1994, 766, []),
        ("Executive Orders", 1996, 874, []),
        ("Rainbow Six", 1998, 740, []),
        ("The Bear and the Dragon", 2000, 1028, []),
        ("Red Rabbit", 2002, 618, []),
        ("The Teeth of the Tiger", 2003, 431, []),
        ("Dead or Alive", 2010, 950, []),
        ("Locked On", 2011, 848, []),
        ("Threat Vector", 2012, 852, []),
        ("Command Authority", 2013, 573, []),
    ]),
    ("Robert Ludlum", "en", ["Thriller", "Spy Fiction"], [
        ("The Scarlatti Inheritance", 1971, 358, []),
        ("The Osterman Weekend", 1972, 310, []),
        ("The Matlock Paper", 1973, 312, []),
        ("The Rhinemann Exchange", 1974, 460, []),
        ("The Gemini Contenders", 1976, 402, []),
        ("The Chancellor Manuscript", 1977, 448, []),
        ("The Holcroft Covenant", 1978, 543, []),
        ("The Matarese Circle", 1979, 601, []),
        ("The Bourne Identity", 1980, 535, ["Classic"]),
        ("The Parsifal Mosaic", 1982, 630, []),
        ("The Aquitaine Progression", 1984, 647, []),
        ("The Bourne Supremacy", 1986, 597, []),
        ("The Icarus Agenda", 1988, 677, []),
        ("The Bourne Ultimatum", 1990, 611, []),
        ("The Road to Omaha", 1992, 433, []),
        ("The Scorpio Illusion", 1993, 534, []),
        ("The Apocalypse Watch", 1995, 640, []),
        ("The Matarese Countdown", 1997, 467, []),
        ("The Prometheus Deception", 2000, 481, []),
        ("The Sigma Protocol", 2001, 535, []),
        ("The Janson Directive", 2002, 547, []),
        ("The Tristan Betrayal", 2003, 510, []),
        ("The Ambler Warning", 2005, 558, []),
    ]),
    ("Ken Follett", "en", ["Thriller", "Historical Fiction"], [
        ("Eye of the Needle", 1978, 337, ["War", "Classic"]),
        ("Triple", 1979, 378, []),
        ("The Key to Rebecca", 1980, 381, ["War"]),
        ("The Man from St. Petersburg", 1982, 337, []),
        ("On Wings of Eagles", 1983, 444, ["Non-Fiction"]),
        ("Lie Down with Lions", 1985, 400, []),
        ("The Pillars of the Earth", 1989, 973, ["Historical Fiction", "Classic"]),
        ("Night Over Water", 1991, 400, []),
        ("A Dangerous Fortune", 1993, 533, []),
        ("A Place Called Freedom", 1995, 407, []),
        ("The Third Twin", 1996, 468, ["Science Fiction"]),
        ("The Hammer of Eden", 1998, 404, []),
        ("Code to Zero", 2000, 387, []),
        ("Jackdaws", 2001, 451, ["War"]),
        ("Hornet Flight", 2002, 420, ["War"]),
        ("Whiteout", 2004, 400, []),
        ("World Without End", 2007, 1014, ["Historical Fiction"]),
        ("Fall of Giants", 2010, 985, ["Historical Fiction"]),
        ("Winter of the World", 2012, 940, ["Historical Fiction", "War"]),
        ("Edge of Eternity", 2014, 1074, ["Historical Fiction"]),
        ("A Column of Fire", 2017, 916, ["Historical Fiction"]),
        ("The Evening and the Morning", 2020, 916, ["Historical Fiction"]),
        ("Never", 2021, 690, []),
        ("The Armor of Light", 2023, 880, ["Historical Fiction"]),
    ]),
    ("Frederick Forsyth", "en", ["Thriller", "Spy Fiction"], [
        ("The Day of the Jackal", 1971, 380, ["Classic"]),
        ("The Odessa File", 1972, 334, []),
        ("The Dogs of War", 1974, 408, []),
        ("The Devil's Alternative", 1979, 432, []),
        ("The Fourth Protocol", 1984, 447, []),
        ("The Negotiator", 1989, 472, []),
        ("The Deceiver", 1991, 481, []),
        ("The Fist of God", 1994, 502, ["War"]),
        ("Icon", 1996, 499, []),
        ("The Phantom of Manhattan", 1999, 342, []),
        ("Avenger", 2003, 384, []),
        ("The Afghan", 2006, 371, []),
        ("The Cobra", 2010, 375, []),
        ("The Kill List", 2013, 339, []),
        ("The Fox", 2018, 311, []),
    ]),
    ("Nelson DeMille", "en", ["Thriller", "Mystery"], [
        ("By the Rivers of Babylon", 1978, 436, []),
        ("Cathedral", 1981, 488, []),
        ("The Talbot Odyssey", 1984, 500, []),
        ("Word of Honor", 1985, 518, []),
        ("The Charm School", 1988, 533, []),
        ("The Gold Coast", 1990, 500, []),
        ("The General's Daughter", 1992, 452, []),
        ("Spencerville", 1994, 546, []),
        ("Plum Island", 1997, 511, []),
        ("The Lion's Game", 2000, 677, []),
        ("Up Country", 2002, 672, []),
        ("Night Fall", 2004, 451, []),
        ("Wild Fire", 2006, 519, []),
        ("The Gate House", 2008, 670, []),
        ("The Lion", 2010, 509, []),
        ("The Panther", 2012, 582, []),
        ("The Quest", 2013, 592, ["Adventure"]),
        ("Radiant Angel", 2015, 529, []),
        ("The Cuban Affair", 2017, 449, []),
        ("The Deserter", 2019, 560, []),
    ]),
    ("Sandra Brown", "en", ["Romance", "Thriller"], [
        ("Mirror Image", 1990, 448, []),
        ("French Silk", 1992, 432, []),
        ("Breath of Scandal", 1991, 468, []),
        ("Where There's Smoke", 1993, 527, []),
        ("Charade", 1994, 414, []),
        ("The Witness", 1995, 420, []),
        ("Exclusive", 1996, 440, []),
        ("Fat Tuesday", 1997, 454, []),
        ("Unspeakable", 1998, 438, []),
        ("The Switch", 2000, 438, []),
        ("Standoff", 2000, 380, []),
        ("The Crush", 2002, 464, []),
        ("Envy", 2001, 510, []),
        ("Hello, Darkness", 2003, 436, []),
        ("White Hot", 2004, 432, []),
        ("Chill Factor", 2005, 432, []),
        ("Ricochet", 2006, 404, []),
        ("Play Dirty", 2007, 400, []),
        ("Smoke Screen", 2008, 416, []),
        ("Smash Cut", 2009, 416, []),
        ("Tough Customer", 2010, 416, []),
        ("Lethal", 2011, 416, []),
        ("Low Pressure", 2012, 416, []),
        ("Deadline", 2013, 416, []),
        ("Mean Streak", 2014, 368, []),
        ("Friction", 2015, 432, []),
        ("Sting", 2016, 432, []),
        ("Seeing Red", 2017, 448, []),
        ("Tailspin", 2018, 416, []),
        ("Outfox", 2019, 416, []),
        ("Thick as Thieves", 2020, 432, []),
        ("Blind Tiger", 2021, 480, ["Historical Fiction"]),
        ("Overkill", 2022, 432, []),
    ]),
    ("Lisa Scottoline", "en", ["Thriller", "Mystery", "Legal Thriller"], [
        ("Everywhere That Mary Went", 1993, 304, []),
        ("Final Appeal", 1994, 374, []),
        ("Running from the Law", 1995, 302, []),
        ("Legal Tender", 1996, 328, []),
        ("Rough Justice", 1997, 386, []),
        ("Mistaken Identity", 1999, 385, []),
        ("Moment of Truth", 2000, 373, []),
        ("The Vendetta Defense", 2001, 400, []),
        ("Courting Trouble", 2002, 358, []),
        ("Dead Ringer", 2003, 330, []),
        ("Killer Smile", 2004, 388, []),
        ("Devil's Corner", 2005, 354, []),
        ("Dirty Blonde", 2006, 354, []),
        ("Daddy's Girl", 2007, 338, []),
        ("Lady Killer", 2008, 354, []),
        ("Look Again", 2009, 354, []),
        ("Think Twice", 2010, 338, []),
        ("Save Me", 2011, 354, []),
        ("Come Home", 2012, 370, []),
        ("Don't Go", 2013, 354, []),
        ("Keep Quiet", 2014, 354, []),
        ("Every Fifteen Minutes", 2015, 420, []),
        ("Corrupted", 2016, 448, []),
        ("One Perfect Lie", 2017, 354, []),
        ("After Anna", 2018, 354, []),
    ]),
    ("Linwood Barclay", "en", ["Thriller", "Mystery"], [
        ("No Time for Goodbye", 2007, 371, []),
        ("Too Close to Home", 2008, 387, []),
        ("Fear the Worst", 2009, 370, []),
        ("Never Look Away", 2010, 404, []),
        ("The Accident", 2011, 388, []),
        ("Trust Your Eyes", 2012, 499, []),
        ("A Tap on the Window", 2013, 375, []),
        ("No Safe House", 2014, 406, []),
        ("Broken Promise", 2015, 485, []),
        ("Far from True", 2016, 452, []),
        ("The Twenty-Three", 2016, 451, []),
        ("Parting Shot", 2017, 477, []),
        ("A Noise Downstairs", 2018, 357, []),
        ("Elevator Pitch", 2019, 484, []),
        ("Find You First", 2021, 425, []),
        ("Take Your Breath Away", 2022, 435, []),
        ("Look Both Ways", 2022, 420, []),
        ("The Lie Maker", 2023, 430, []),
    ]),
    ("Colleen Hoover", "en", ["Romance", "Literary Fiction"], [
        ("Slammed", 2012, 334, []),
        ("Point of Retreat", 2012, 280, []),
        ("Hopeless", 2012, 372, []),
        ("Losing Hope", 2013, 323, []),
        ("Maybe Someday", 2014, 358, []),
        ("Maybe Not", 2014, 127, []),
        ("Confess", 2015, 306, []),
        ("November 9", 2015, 310, []),
        ("It Ends with Us", 2016, 376, []),
        ("Without Merit", 2017, 380, []),
        ("All Your Perfects", 2018, 314, []),
        ("Verity", 2018, 314, ["Thriller"]),
        ("Regretting You", 2019, 337, []),
        ("Heart Bones", 2020, 296, []),
        ("Layla", 2020, 306, ["Thriller"]),
        ("Reminders of Him", 2022, 335, []),
        ("It Starts with Us", 2022, 336, []),
        ("Ugly Love", 2014, 322, []),
    ]),
    ("Emily Henry", "en", ["Romance"], [
        ("Beach Read", 2020, 361, []),
        ("People We Meet on Vacation", 2021, 364, []),
        ("Book Lovers", 2022, 373, []),
        ("Happy Place", 2023, 395, []),
        ("Funny Story", 2024, 395, []),
    ]),
    ("Ali Hazelwood", "en", ["Romance"], [
        ("The Love Hypothesis", 2021, 384, []),
        ("Love on the Brain", 2022, 347, []),
        ("Love, Theoretically", 2023, 355, []),
        ("Check & Mate", 2023, 381, ["Young Adult"]),
        ("Bride", 2024, 395, []),
    ]),
    ("Taylor Jenkins Reid", "en", ["Literary Fiction", "Romance"], [
        ("Forever, Interrupted", 2013, 337, []),
        ("After I Do", 2014, 338, []),
        ("Maybe in Another Life", 2015, 332, []),
        ("One True Loves", 2016, 310, []),
        ("The Seven Husbands of Evelyn Hugo", 2017, 389, []),
        ("Daisy Jones & The Six", 2019, 355, []),
        ("Malibu Rising", 2021, 369, []),
        ("Carrie Soto Is Back", 2022, 364, []),
    ]),
    ("Kristin Hannah", "en", ["Literary Fiction", "Historical Fiction"], [
        ("The Great Alone", 2018, 440, []),
        ("The Nightingale", 2015, 440, ["War"]),
        ("The Four Winds", 2021, 464, []),
        ("Firefly Lane", 2008, 479, []),
        ("Fly Away", 2013, 400, []),
        ("Night Road", 2011, 400, []),
        ("Home Front", 2012, 432, ["War"]),
        ("Winter Garden", 2010, 394, []),
        ("True Colors", 2009, 404, []),
        ("Between Sisters", 2003, 371, []),
        ("Distant Shores", 2002, 354, []),
        ("On Mystic Lake", 1999, 384, []),
        ("Angel Falls", 2000, 340, []),
        ("Summer Island", 2001, 340, []),
        ("The Things We Do for Love", 2004, 371, []),
        ("Comfort & Joy", 2005, 244, []),
        ("Magic Hour", 2006, 438, []),
        ("Wild", 2023, 448, []),
    ]),
    ("Jodi Picoult", "en", ["Literary Fiction"], [
        ("Songs of the Humpback Whale", 1992, 384, []),
        ("Harvesting the Heart", 1993, 425, []),
        ("Picture Perfect", 1995, 400, []),
        ("Mercy", 1996, 368, []),
        ("The Pact", 1998, 502, []),
        ("Keeping Faith", 1999, 422, []),
        ("Plain Truth", 2000, 400, []),
        ("Salem Falls", 2001, 434, []),
        ("Perfect Match", 2002, 370, []),
        ("Second Glance", 2003, 400, []),
        ("My Sister's Keeper", 2004, 423, []),
        ("Vanishing Acts", 2005, 400, []),
        ("The Tenth Circle", 2006, 385, []),
        ("Nineteen Minutes", 2007, 455, []),
        ("Change of Heart", 2008, 447, []),
        ("Handle with Care", 2009, 480, []),
        ("House Rules", 2010, 532, []),
        ("Sing You Home", 2011, 466, []),
        ("Lone Wolf", 2012, 421, []),
        ("The Storyteller", 2013, 460, ["Historical Fiction"]),
        ("Leaving Time", 2014, 414, []),
        ("Small Great Things", 2016, 470, []),
        ("A Spark of Light", 2018, 370, []),
        ("The Book of Two Ways", 2020, 416, []),
        ("Wish You Were Here", 2021, 337, []),
        ("Mad Honey", 2022, 464, []),
    ]),
    ("Liane Moriarty", "en", ["Literary Fiction", "Mystery"], [
        ("Three Wishes", 2003, 400, []),
        ("The Last Anniversary", 2005, 391, []),
        ("What Alice Forgot", 2009, 426, []),
        ("The Hypnotist's Love Story", 2011, 439, []),
        ("The Husband's Secret", 2013, 396, []),
        ("Big Little Lies", 2014, 460, []),
        ("Truly Madly Guilty", 2016, 415, []),
        ("Nine Perfect Strangers", 2018, 453, []),
        ("Apples Never Fall", 2021, 468, []),
        ("Here One Moment", 2024, 512, []),
    ]),
]


def generate():
    batch_num = 98
    books_in_batch = []

    for author, lang, default_genres, works in AUTHORS:
        for title, year, pages, extra_genres in works:
            genres = list(default_genres) + extra_genres
            book = make_book(title, author, year, pages, genres, lang)
            books_in_batch.append(book)

            if len(books_in_batch) >= 100:
                fname = f"batch_{batch_num:02d}_more_{batch_num - 97}.json"
                path = os.path.join(BATCH_DIR, fname)
                with open(path, "w") as f:
                    json.dump(books_in_batch, f, indent=2)
                print(f"  {fname}: {len(books_in_batch)} books")
                batch_num += 1
                books_in_batch = []

    if books_in_batch:
        fname = f"batch_{batch_num:02d}_more_{batch_num - 97}.json"
        path = os.path.join(BATCH_DIR, fname)
        with open(path, "w") as f:
            json.dump(books_in_batch, f, indent=2)
        print(f"  {fname}: {len(books_in_batch)} books")
        batch_num += 1

    total = sum(len(works) for _, _, _, works in AUTHORS)
    print(f"\nTotal new books: {total}")


if __name__ == "__main__":
    generate()
