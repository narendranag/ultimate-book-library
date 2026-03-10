#!/usr/bin/env python3
"""Batch 8: More prolific author bibliographies (batches 57-62)."""
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


# Format: (author, lang, default_genres, [(title, year, pages, extra_genres), ...])
AUTHORS = [
    ("James Patterson", "en", ["Thriller", "Mystery"], [
        ("Along Came a Spider", 1993, 435, []),
        ("Kiss the Girls", 1995, 451, []),
        ("Jack & Jill", 1996, 432, []),
        ("Cat & Mouse", 1997, 399, []),
        ("Pop Goes the Weasel", 1999, 423, []),
        ("Roses Are Red", 2000, 400, []),
        ("Violets Are Blue", 2001, 393, []),
        ("Four Blind Mice", 2002, 387, []),
        ("The Big Bad Wolf", 2003, 396, []),
        ("London Bridges", 2004, 391, []),
        ("Mary, Mary", 2005, 387, []),
        ("Cross", 2006, 393, []),
        ("Double Cross", 2007, 385, []),
        ("Cross Country", 2008, 389, []),
        ("Alex Cross's Trial", 2009, 404, []),
        ("I, Alex Cross", 2009, 374, []),
        ("Cross Fire", 2010, 373, []),
        ("Kill Alex Cross", 2011, 383, []),
        ("Merry Christmas, Alex Cross", 2012, 302, []),
        ("Alex Cross, Run", 2013, 369, []),
        ("Cross My Heart", 2013, 373, []),
        ("Hope to Die", 2014, 383, []),
        ("Cross Justice", 2015, 385, []),
        ("Cross the Line", 2016, 394, []),
        ("The People vs. Alex Cross", 2017, 373, []),
        ("Target: Alex Cross", 2018, 373, []),
        ("Criss Cross", 2019, 373, []),
        ("Deadly Cross", 2020, 400, []),
        ("Fear No Evil", 2021, 385, []),
    ]),
    ("John Grisham", "en", ["Thriller", "Legal Thriller"], [
        ("A Time to Kill", 1989, 515, ["Literary Fiction"]),
        ("The Firm", 1991, 421, []),
        ("The Pelican Brief", 1992, 371, []),
        ("The Client", 1993, 422, []),
        ("The Chamber", 1994, 486, []),
        ("The Rainmaker", 1995, 434, []),
        ("The Runaway Jury", 1996, 414, []),
        ("The Partner", 1997, 366, []),
        ("The Street Lawyer", 1998, 348, []),
        ("The Testament", 1999, 435, []),
        ("The Brethren", 2000, 366, []),
        ("A Painted House", 2001, 388, ["Literary Fiction"]),
        ("The Summons", 2002, 341, []),
        ("The King of Torts", 2003, 373, []),
        ("Bleachers", 2003, 182, ["Literary Fiction"]),
        ("The Last Juror", 2004, 373, []),
        ("The Broker", 2005, 357, []),
        ("Playing for Pizza", 2007, 262, ["Humor"]),
        ("The Appeal", 2008, 358, []),
        ("The Associate", 2009, 373, []),
        ("The Confession", 2010, 418, []),
        ("The Litigators", 2011, 385, []),
        ("Calico Joe", 2012, 197, ["Literary Fiction"]),
        ("The Racketeer", 2012, 340, []),
        ("Sycamore Row", 2013, 448, []),
        ("Gray Mountain", 2014, 384, []),
        ("Rogue Lawyer", 2015, 340, []),
        ("The Whistler", 2016, 384, []),
        ("Camino Island", 2017, 290, ["Literary Fiction"]),
        ("The Rooster Bar", 2017, 353, []),
        ("The Reckoning", 2018, 404, ["Historical Fiction"]),
        ("The Guardians", 2019, 384, []),
        ("A Time for Mercy", 2020, 464, []),
        ("The Judge's List", 2021, 368, []),
    ]),
    ("Haruki Murakami", "ja", ["Literary Fiction", "Magical Realism"], [
        ("Hear the Wind Sing", 1979, 130, []),
        ("Pinball, 1973", 1980, 175, []),
        ("A Wild Sheep Chase", 1982, 299, []),
        ("Hard-Boiled Wonderland and the End of the World", 1985, 400, ["Science Fiction"]),
        ("Norwegian Wood", 1987, 296, ["Romance"]),
        ("Dance Dance Dance", 1988, 393, []),
        ("South of the Border, West of the Sun", 1992, 213, []),
        ("The Wind-Up Bird Chronicle", 1994, 607, []),
        ("Sputnik Sweetheart", 1999, 210, []),
        ("After Dark", 2004, 191, []),
        ("Colorless Tsukuru Tazaki", 2013, 386, []),
        ("Killing Commendatore", 2017, 681, []),
        ("The City and Its Uncertain Walls", 2023, 464, []),
        ("After the Quake", 2000, 181, ["Short Stories"]),
        ("Blind Willow, Sleeping Woman", 2006, 333, ["Short Stories"]),
        ("Men Without Women", 2014, 228, ["Short Stories"]),
        ("First Person Singular", 2020, 241, ["Short Stories"]),
        ("Underground", 1997, 309, ["Non-Fiction"]),
        ("What I Talk About When I Talk About Running", 2007, 180, ["Non-Fiction", "Memoir"]),
    ]),
    ("Toni Morrison", "en", ["Literary Fiction", "Classic"], [
        ("The Bluest Eye", 1970, 206, []),
        ("Sula", 1973, 174, []),
        ("Song of Solomon", 1977, 337, []),
        ("Tar Baby", 1981, 305, []),
        ("Beloved", 1987, 275, ["Historical Fiction"]),
        ("Jazz", 1992, 229, []),
        ("Paradise", 1997, 318, []),
        ("Love", 2003, 202, []),
        ("A Mercy", 2008, 167, ["Historical Fiction"]),
        ("Home", 2012, 145, []),
        ("God Help the Child", 2015, 178, []),
    ]),
    ("Philip Roth", "en", ["Literary Fiction"], [
        ("Goodbye, Columbus", 1959, 298, ["Short Stories"]),
        ("Letting Go", 1962, 630, []),
        ("When She Was Good", 1967, 306, []),
        ("Portnoy's Complaint", 1969, 274, ["Humor"]),
        ("Our Gang", 1971, 200, ["Satire"]),
        ("The Breast", 1972, 89, []),
        ("The Great American Novel", 1973, 382, ["Humor"]),
        ("My Life as a Man", 1974, 334, []),
        ("The Professor of Desire", 1977, 263, []),
        ("The Ghost Writer", 1979, 180, []),
        ("Zuckerman Unbound", 1981, 225, []),
        ("The Anatomy Lesson", 1983, 291, []),
        ("The Counterlife", 1986, 324, []),
        ("Deception", 1990, 208, []),
        ("Operation Shylock", 1993, 398, []),
        ("Sabbath's Theater", 1995, 451, []),
        ("American Pastoral", 1997, 423, []),
        ("I Married a Communist", 1998, 323, []),
        ("The Human Stain", 2000, 361, []),
        ("The Dying Animal", 2001, 156, []),
        ("The Plot Against America", 2004, 391, ["Alternate History"]),
        ("Everyman", 2006, 182, []),
        ("Exit Ghost", 2007, 292, []),
        ("Indignation", 2008, 233, []),
        ("The Humbling", 2009, 140, []),
        ("Nemesis", 2010, 280, []),
    ]),
    ("Don DeLillo", "en", ["Literary Fiction", "Postmodern"], [
        ("Americana", 1971, 377, []),
        ("End Zone", 1972, 242, []),
        ("Great Jones Street", 1973, 265, []),
        ("Ratner's Star", 1976, 438, ["Science Fiction"]),
        ("Players", 1977, 212, []),
        ("Running Dog", 1978, 243, []),
        ("The Names", 1982, 339, []),
        ("White Noise", 1985, 326, ["Classic"]),
        ("Libra", 1988, 456, ["Historical Fiction"]),
        ("Mao II", 1991, 241, []),
        ("Underworld", 1997, 827, []),
        ("The Body Artist", 2001, 124, []),
        ("Cosmopolis", 2003, 209, []),
        ("Falling Man", 2007, 246, []),
        ("Point Omega", 2010, 117, []),
        ("Zero K", 2016, 274, ["Science Fiction"]),
        ("The Silence", 2020, 116, []),
    ]),
    ("Thomas Pynchon", "en", ["Literary Fiction", "Postmodern"], [
        ("V.", 1963, 492, []),
        ("The Crying of Lot 49", 1966, 152, []),
        ("Gravity's Rainbow", 1973, 776, ["Classic"]),
        ("Vineland", 1990, 385, []),
        ("Mason & Dixon", 1997, 773, ["Historical Fiction"]),
        ("Against the Day", 2006, 1085, ["Historical Fiction"]),
        ("Inherent Vice", 2009, 369, ["Mystery"]),
        ("Bleeding Edge", 2013, 477, ["Mystery"]),
    ]),
    ("Ursula K. Le Guin", "en", ["Science Fiction", "Fantasy"], [
        ("Rocannon's World", 1966, 136, []),
        ("Planet of Exile", 1966, 126, []),
        ("City of Illusions", 1967, 160, []),
        ("The Left Hand of Darkness", 1969, 286, ["Classic"]),
        ("The Lathe of Heaven", 1971, 184, []),
        ("The Word for World Is Forest", 1972, 189, []),
        ("The Dispossessed", 1974, 341, ["Classic"]),
        ("Malafrena", 1979, 369, ["Historical Fiction"]),
        ("The Beginning Place", 1980, 183, []),
        ("Always Coming Home", 1985, 525, []),
        ("Tehanu", 1990, 226, ["Fantasy"]),
        ("The Telling", 2000, 264, []),
        ("Lavinia", 2008, 279, ["Historical Fiction"]),
        ("The Ones Who Walk Away from Omelas", 1973, 32, ["Short Stories"]),
        ("The Wind's Twelve Quarters", 1975, 303, ["Short Stories"]),
        ("Changing Planes", 2003, 246, ["Short Stories"]),
    ]),
    ("Ray Bradbury", "en", ["Science Fiction", "Fantasy"], [
        ("The Martian Chronicles", 1950, 222, ["Classic"]),
        ("The Illustrated Man", 1951, 270, ["Short Stories"]),
        ("Fahrenheit 451", 1953, 194, ["Classic", "Dystopian"]),
        ("Dandelion Wine", 1957, 239, ["Literary Fiction"]),
        ("Something Wicked This Way Comes", 1962, 293, ["Horror"]),
        ("The Halloween Tree", 1972, 145, ["Horror"]),
        ("I Sing the Body Electric!", 1969, 305, ["Short Stories"]),
        ("Long After Midnight", 1976, 279, ["Short Stories"]),
        ("The Toynbee Convector", 1988, 281, ["Short Stories"]),
        ("Quicker Than the Eye", 1996, 260, ["Short Stories"]),
        ("From the Dust Returned", 2001, 204, ["Horror"]),
        ("Let's All Kill Constance", 2002, 229, ["Mystery"]),
        ("Farewell Summer", 2006, 211, ["Literary Fiction"]),
        ("Now and Forever", 2007, 197, []),
        ("Death Is a Lonely Business", 1985, 279, ["Mystery"]),
        ("A Graveyard for Lunatics", 1990, 285, ["Mystery"]),
        ("Green Shadows, White Whale", 1992, 271, ["Literary Fiction"]),
    ]),
    ("Kurt Vonnegut", "en", ["Literary Fiction", "Science Fiction", "Satire"], [
        ("Player Piano", 1952, 341, ["Dystopian"]),
        ("The Sirens of Titan", 1959, 326, []),
        ("Mother Night", 1961, 268, []),
        ("Cat's Cradle", 1963, 287, ["Classic"]),
        ("God Bless You, Mr. Rosewater", 1965, 218, []),
        ("Slaughterhouse-Five", 1969, 275, ["Classic", "War"]),
        ("Breakfast of Champions", 1973, 303, []),
        ("Slapstick", 1976, 243, []),
        ("Jailbird", 1979, 310, []),
        ("Deadeye Dick", 1982, 240, []),
        ("Galápagos", 1985, 324, []),
        ("Bluebeard", 1987, 300, []),
        ("Hocus Pocus", 1990, 302, []),
        ("Timequake", 1997, 219, []),
        ("Welcome to the Monkey House", 1968, 298, ["Short Stories"]),
    ]),
    ("Michael Connelly", "en", ["Mystery", "Thriller", "Crime Fiction"], [
        ("The Black Echo", 1992, 393, []),
        ("The Black Ice", 1993, 322, []),
        ("The Concrete Blonde", 1994, 382, []),
        ("The Last Coyote", 1995, 363, []),
        ("The Poet", 1996, 433, []),
        ("Trunk Music", 1997, 349, []),
        ("Blood Work", 1998, 393, []),
        ("Angels Flight", 1999, 393, []),
        ("Void Moon", 1999, 357, []),
        ("A Darkness More Than Night", 2001, 418, []),
        ("City of Bones", 2002, 393, []),
        ("Chasing the Dime", 2002, 371, []),
        ("Lost Light", 2003, 355, []),
        ("The Narrows", 2004, 404, []),
        ("The Closers", 2005, 403, []),
        ("The Lincoln Lawyer", 2005, 404, []),
        ("Echo Park", 2006, 404, []),
        ("The Overlook", 2007, 225, []),
        ("The Brass Verdict", 2008, 422, []),
        ("The Scarecrow", 2009, 418, []),
        ("Nine Dragons", 2009, 377, []),
        ("The Reversal", 2010, 389, []),
        ("The Fifth Witness", 2011, 389, []),
        ("The Drop", 2011, 389, []),
        ("The Black Box", 2012, 416, []),
        ("The Gods of Guilt", 2013, 389, []),
        ("The Burning Room", 2014, 388, []),
        ("The Crossing", 2015, 388, []),
        ("The Wrong Side of Goodbye", 2016, 388, []),
        ("Two Kinds of Truth", 2017, 388, []),
        ("Dark Sacred Night", 2018, 388, []),
        ("The Night Fire", 2019, 388, []),
        ("The Law of Innocence", 2020, 404, []),
        ("The Dark Hours", 2021, 388, []),
    ]),
    ("Lee Child", "en", ["Thriller", "Action"], [
        ("Killing Floor", 1997, 355, []),
        ("Die Trying", 1998, 372, []),
        ("Tripwire", 1999, 342, []),
        ("Running Blind", 2000, 372, []),
        ("Echo Burning", 2001, 372, []),
        ("Without Fail", 2002, 372, []),
        ("Persuader", 2003, 342, []),
        ("The Enemy", 2004, 372, []),
        ("One Shot", 2005, 372, []),
        ("The Hard Way", 2006, 372, []),
        ("Bad Luck and Trouble", 2007, 372, []),
        ("Nothing to Lose", 2008, 401, []),
        ("Gone Tomorrow", 2009, 401, []),
        ("61 Hours", 2010, 383, []),
        ("Worth Dying For", 2010, 383, []),
        ("The Affair", 2011, 405, []),
        ("A Wanted Man", 2012, 405, []),
        ("Never Go Back", 2013, 405, []),
        ("Personal", 2014, 353, []),
        ("Make Me", 2015, 405, []),
        ("Night School", 2016, 353, []),
        ("The Midnight Line", 2017, 353, []),
        ("Past Tense", 2018, 390, []),
        ("Blue Moon", 2019, 353, []),
    ]),
]


def generate():
    batch_num = 57
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
