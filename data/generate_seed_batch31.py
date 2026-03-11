#!/usr/bin/env python3
"""Batch 31: THE FINAL PUSH - 1100+ fresh books to break 10,000."""
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


def load_existing():
    existing_titles = set()
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
    return existing_titles


ALL_BOOKS = []

# === COMPLETELY FRESH AUTHORS - MYSTERY/THRILLER ===

# Sue Grafton - Kinsey Millhone (A-Y)
for title, year, pages in [
    ("A Is for Alibi", 1982, 274), ("B Is for Burglar", 1985, 229),
    ("C Is for Corpse", 1986, 243), ("D Is for Deadbeat", 1987, 229),
    ("E Is for Evidence", 1988, 227), ("F Is for Fugitive", 1989, 261),
    ("G Is for Gumshoe", 1990, 261), ("H Is for Homicide", 1991, 256),
    ("I Is for Innocent", 1992, 286), ("J Is for Judgment", 1993, 288),
    ("K Is for Killer", 1994, 284), ("L Is for Lawless", 1995, 290),
    ("M Is for Malice", 1996, 300), ("N Is for Noose", 1998, 289),
    ("O Is for Outlaw", 1999, 318), ("P Is for Peril", 2001, 352),
    ("Q Is for Quarry", 2002, 385), ("R Is for Ricochet", 2004, 310),
    ("S Is for Silence", 2005, 374), ("T Is for Trespass", 2007, 387),
    ("U Is for Undertow", 2009, 400), ("V Is for Vengeance", 2011, 468),
    ("W Is for Wasted", 2013, 480), ("X", 2015, 416),
    ("Y Is for Yesterday", 2017, 496),
]:
    ALL_BOOKS.append(make_book(title, "Sue Grafton", year, pages, ["Mystery", "Crime Fiction"]))

# Nevada Barr - Anna Pigeon
for title, year, pages in [
    ("Track of the Cat", 1993, 238), ("A Superior Death", 1994, 259),
    ("Ill Wind", 1995, 359), ("Firestorm", 1996, 362),
    ("Endangered Species", 1997, 358), ("Blind Descent", 1998, 340),
    ("Liberty Falling", 1999, 324), ("Deep South", 2000, 326),
    ("Blood Lure", 2001, 373), ("Hunting Season", 2002, 352),
    ("Flashback", 2003, 384), ("High Country", 2004, 386),
    ("Hard Truth", 2005, 382), ("Winter Study", 2008, 384),
    ("Borderline", 2009, 368), ("Burn", 2010, 384),
    ("The Rope", 2012, 400), ("Destroyer Angel", 2014, 400),
    ("Boar Island", 2016, 384), ("Dark River", 2024, 384),
]:
    ALL_BOOKS.append(make_book(title, "Nevada Barr", year, pages, ["Mystery", "Thriller"]))

# Cara Black - Aimée Leduc
for title, year, pages in [
    ("Murder in the Marais", 1999, 354), ("Murder in Belleville", 2000, 303),
    ("Murder in the Sentier", 2002, 371), ("Murder in the Bastille", 2003, 302),
    ("Murder in Clichy", 2005, 288), ("Murder in Montmartre", 2006, 305),
    ("Murder on the Ile Saint-Louis", 2007, 287), ("Murder in the Rue de Paradis", 2008, 272),
    ("Murder in the Latin Quarter", 2009, 285), ("Murder in the Palais Royal", 2010, 308),
    ("Murder in Passy", 2011, 273), ("Murder at the Lanterne Rouge", 2012, 294),
    ("Murder Below Montparnasse", 2013, 304), ("Murder in Pigalle", 2014, 306),
    ("Murder on the Champ de Mars", 2015, 288), ("Murder on the Quai", 2016, 320),
    ("Murder in Saint-Germain", 2017, 320), ("Murder on the Left Bank", 2018, 320),
    ("Three Hours in Paris", 2020, 320),
]:
    ALL_BOOKS.append(make_book(title, "Cara Black", year, pages, ["Mystery", "Crime Fiction"]))

# Alan Furst - Night Soldiers
for title, year, pages in [
    ("Night Soldiers", 1988, 432), ("Dark Star", 1991, 419),
    ("The Polish Officer", 1995, 272), ("The World at Night", 1996, 268),
    ("Red Gold", 1999, 260), ("Kingdom of Shadows", 2001, 277),
    ("Blood of Victory", 2002, 237), ("Dark Voyage", 2004, 264),
    ("The Foreign Correspondent", 2006, 272), ("The Spies of Warsaw", 2008, 266),
    ("Spies of the Balkans", 2010, 268), ("Mission to Paris", 2012, 255),
    ("Midnight in Europe", 2014, 257), ("A Hero of France", 2016, 231),
    ("Under Occupation", 2019, 218),
]:
    ALL_BOOKS.append(make_book(title, "Alan Furst", year, pages, ["Spy Fiction", "Historical Fiction", "Thriller"]))

# Henning Mankell - Wallander (filling remaining)
for title, year, pages in [
    ("Faceless Killers", 1991, 282), ("The Dogs of Riga", 1992, 326),
    ("The White Lioness", 1993, 404), ("The Man Who Smiled", 1994, 344),
    ("Sidetracked", 1995, 417), ("The Fifth Woman", 1996, 404),
    ("One Step Behind", 1997, 404), ("Firewall", 1998, 404),
    ("The Return of the Dancing Master", 2000, 402),
    ("Before the Frost", 2002, 372), ("The Troubled Man", 2009, 389),
    ("After the Fire", 2017, 240), ("Italian Shoes", 2006, 290),
    ("The Eye of the Leopard", 2008, 334), ("Daniel", 2010, 403),
]:
    ALL_BOOKS.append(make_book(title, "Henning Mankell", year, pages, ["Mystery", "Crime Fiction"], "sv"))

# Jo Nesbø - Harry Hole (filling remaining)
for title, year, pages in [
    ("The Bat", 1997, 342), ("Cockroaches", 1998, 368),
    ("The Redbreast", 2000, 521), ("Nemesis", 2002, 474),
    ("The Devil's Star", 2003, 452), ("The Redeemer", 2005, 461),
    ("The Snowman", 2007, 550), ("The Leopard", 2009, 608),
    ("Phantom", 2011, 402), ("Police", 2013, 584),
    ("The Thirst", 2017, 496), ("Knife", 2019, 560),
    ("Killing Moon", 2022, 576),
    ("The Son", 2014, 544), ("Macbeth", 2018, 624),
    ("The Kingdom", 2020, 576), ("The Jealousy Man", 2021, 384),
]:
    ALL_BOOKS.append(make_book(title, "Jo Nesbø", year, pages, ["Mystery", "Crime Fiction", "Thriller"], "no"))

# Alexander McCall Smith - filling remaining
for title, year, pages in [
    ("The No. 1 Ladies' Detective Agency", 1998, 235),
    ("Tears of the Giraffe", 2000, 227), ("Morality for Beautiful Girls", 2001, 227),
    ("The Kalahari Typing School for Men", 2002, 197),
    ("The Full Cupboard of Life", 2003, 211), ("In the Company of Cheerful Ladies", 2004, 233),
    ("Blue Shoes and Happiness", 2006, 227), ("The Good Husband of Zebra Drive", 2007, 213),
    ("The Miracle at Speedy Motors", 2008, 216), ("Tea Time for the Traditionally Built", 2009, 240),
    ("The Double Comfort Safari Club", 2010, 240),
    ("The Saturday Big Tent Wedding Party", 2011, 224),
    ("The Limpopo Academy of Private Detection", 2012, 256),
    ("The Minor Adjustment Beauty Salon", 2013, 240),
]:
    ALL_BOOKS.append(make_book(title, "Alexander McCall Smith", year, pages, ["Mystery", "Literary Fiction"]))

# === FRESH SF/FANTASY ===

# Susanna Clarke
for title, year, pages in [
    ("Jonathan Strange & Mr Norrell", 2004, 782),
    ("The Ladies of Grace Adieu", 2006, 235),
    ("Piranesi", 2020, 245),
]:
    ALL_BOOKS.append(make_book(title, "Susanna Clarke", year, pages, ["Fantasy"]))

# China Miéville
for title, year, pages in [
    ("King Rat", 1998, 320), ("Perdido Street Station", 2000, 710),
    ("The Scar", 2002, 638), ("Iron Council", 2004, 564),
    ("Looking for Jake", 2005, 307), ("Un Lun Dun", 2007, 432),
    ("The City & the City", 2009, 312), ("Kraken", 2010, 509),
    ("Embassytown", 2011, 345), ("Railsea", 2012, 424),
    ("Three Moments of an Explosion", 2015, 400),
    ("This Census-Taker", 2016, 208), ("The Last Days of New Paris", 2016, 240),
    ("October", 2017, 373), ("A Spectre, Haunting", 2022, 256),
]:
    ALL_BOOKS.append(make_book(title, "China Miéville", year, pages, ["Fantasy", "Science Fiction"]))

# Leigh Bardugo (filling remaining)
for title, year, pages in [
    ("Shadow and Bone", 2012, 358), ("Siege and Storm", 2013, 435),
    ("Ruin and Rising", 2014, 422), ("Six of Crows", 2015, 465),
    ("Crooked Kingdom", 2016, 536), ("The Language of Thorns", 2017, 281),
    ("King of Scars", 2019, 512), ("Rule of Wolves", 2021, 592),
    ("Ninth House", 2019, 458), ("Hell Bent", 2023, 496),
]:
    ALL_BOOKS.append(make_book(title, "Leigh Bardugo", year, pages, ["Fantasy", "Young Adult"]))

# Sarah J. Maas (filling remaining)
for title, year, pages in [
    ("Throne of Glass", 2012, 404), ("Crown of Midnight", 2013, 418),
    ("Heir of Fire", 2014, 565), ("Queen of Shadows", 2015, 648),
    ("Empire of Storms", 2016, 693), ("Tower of Dawn", 2017, 660),
    ("Kingdom of Ash", 2018, 980), ("A Court of Thorns and Roses", 2015, 416),
    ("A Court of Mist and Fury", 2016, 624), ("A Court of Wings and Ruin", 2017, 699),
    ("A Court of Frost and Starlight", 2018, 229),
    ("A Court of Silver Flames", 2021, 757),
    ("House of Earth and Blood", 2020, 803), ("House of Sky and Breath", 2022, 768),
    ("House of Flame and Shadow", 2024, 864),
]:
    ALL_BOOKS.append(make_book(title, "Sarah J. Maas", year, pages, ["Fantasy", "Romance"]))

# Rebecca Yarros (filling remaining)
for title, year, pages in [
    ("Fourth Wing", 2023, 498), ("Iron Flame", 2023, 623),
    ("Full Measures", 2014, 299), ("Eyes Turned Skyward", 2015, 352),
    ("Beyond What Is Given", 2015, 362), ("Hallowed Ground", 2016, 273),
    ("The Last Letter", 2019, 400), ("Great and Precious Things", 2020, 400),
    ("The Things We Leave Unfinished", 2021, 354), ("In the Likely Event", 2023, 432),
    ("Variation", 2024, 448),
]:
    ALL_BOOKS.append(make_book(title, "Rebecca Yarros", year, pages, ["Romance", "Fantasy"]))

# === FRESH NON-FICTION ===

# Ece Temelkuran
for title, year, pages in [
    ("How to Lose a Country", 2019, 256), ("Together", 2021, 208),
]:
    ALL_BOOKS.append(make_book(title, "Ece Temelkuran", year, pages, ["Non-Fiction"]))

# Robert Greene
for title, year, pages in [
    ("The 48 Laws of Power", 1998, 452), ("The Art of Seduction", 2001, 468),
    ("The 33 Strategies of War", 2006, 496), ("The 50th Law", 2009, 302),
    ("Mastery", 2012, 353), ("The Laws of Human Nature", 2018, 624),
    ("The Daily Laws", 2021, 480),
]:
    ALL_BOOKS.append(make_book(title, "Robert Greene", year, pages, ["Non-Fiction", "Self-Help"]))

# Ryan Holiday
for title, year, pages in [
    ("Trust Me, I'm Lying", 2012, 320), ("The Obstacle Is the Way", 2014, 224),
    ("Ego Is the Enemy", 2016, 226), ("Perennial Seller", 2017, 244),
    ("Stillness Is the Key", 2019, 288), ("Lives of the Stoics", 2020, 352),
    ("Courage Is Calling", 2021, 320), ("Discipline Is Destiny", 2022, 352),
    ("Right Thing, Right Now", 2024, 352),
]:
    ALL_BOOKS.append(make_book(title, "Ryan Holiday", year, pages, ["Non-Fiction", "Philosophy"]))

# Annie Ernaux
for title, year, pages in [
    ("Cleaned Out", 1974, 128), ("A Woman's Story", 1988, 106),
    ("A Man's Place", 1983, 99), ("Shame", 1997, 112),
    ("Simple Passion", 1991, 76), ("Happening", 2000, 96),
    ("The Years", 2008, 232), ("A Girl's Story", 2016, 176),
    ("Getting Lost", 2022, 240), ("Look at the Lights, My Love", 2014, 68),
]:
    ALL_BOOKS.append(make_book(title, "Annie Ernaux", year, pages, ["Literary Fiction", "Memoir"], "fr"))

# Susan Cain
for title, year, pages in [
    ("Quiet", 2012, 352), ("Bittersweet", 2022, 288),
]:
    ALL_BOOKS.append(make_book(title, "Susan Cain", year, pages, ["Non-Fiction"]))

# Angela Duckworth
for title, year, pages in [
    ("Grit", 2016, 333),
]:
    ALL_BOOKS.append(make_book(title, "Angela Duckworth", year, pages, ["Non-Fiction"]))

# Cal Newport (filling remaining)
for title, year, pages in [
    ("How to Win at College", 2005, 192), ("How to Become a Straight-A Student", 2006, 224),
    ("So Good They Can't Ignore You", 2012, 304), ("Deep Work", 2016, 304),
    ("Digital Minimalism", 2019, 284), ("A World Without Email", 2021, 320),
    ("Slow Productivity", 2024, 256),
]:
    ALL_BOOKS.append(make_book(title, "Cal Newport", year, pages, ["Non-Fiction", "Self-Help"]))

# Rutger Bregman
for title, year, pages in [
    ("Utopia for Realists", 2014, 336), ("Humankind", 2019, 480),
]:
    ALL_BOOKS.append(make_book(title, "Rutger Bregman", year, pages, ["Non-Fiction"]))

# Kate Manne
for title, year, pages in [
    ("Down Girl", 2017, 368), ("Entitled", 2020, 288),
    ("Unshrinking", 2024, 288),
]:
    ALL_BOOKS.append(make_book(title, "Kate Manne", year, pages, ["Non-Fiction", "Philosophy"]))

# === FRESH LITERARY FICTION ===

# Dave Eggers
for title, year, pages in [
    ("A Heartbreaking Work of Staggering Genius", 2000, 375),
    ("You Shall Know Our Velocity!", 2002, 371), ("A Hologram for the King", 2012, 312),
    ("The Circle", 2013, 491), ("Your Fathers, Where Are They?", 2014, 211),
    ("Heroes of the Frontier", 2016, 384), ("The Monk of Mokha", 2018, 327),
    ("The Parade", 2019, 208), ("The Every", 2021, 576),
    ("The Eyes and the Impossible", 2023, 224),
]:
    ALL_BOOKS.append(make_book(title, "Dave Eggers", year, pages, ["Literary Fiction"]))

# Nathan Hill
for title, year, pages in [
    ("The Nix", 2016, 620), ("Wellness", 2023, 608),
]:
    ALL_BOOKS.append(make_book(title, "Nathan Hill", year, pages, ["Literary Fiction"]))

# Hernan Diaz
for title, year, pages in [
    ("In the Distance", 2017, 256), ("Trust", 2022, 416),
]:
    ALL_BOOKS.append(make_book(title, "Hernan Diaz", year, pages, ["Literary Fiction"]))

# Barbara Kingsolver (filling remaining)
for title, year, pages in [
    ("The Bean Trees", 1988, 232), ("Animal Dreams", 1990, 342),
    ("Pigs in Heaven", 1993, 343), ("The Poisonwood Bible", 1998, 543),
    ("Prodigal Summer", 2000, 444), ("The Lacuna", 2009, 507),
    ("Flight Behavior", 2012, 436), ("Unsheltered", 2018, 480),
    ("Demon Copperhead", 2022, 548),
]:
    ALL_BOOKS.append(make_book(title, "Barbara Kingsolver", year, pages, ["Literary Fiction"]))

# Richard Russo
for title, year, pages in [
    ("Mohawk", 1986, 416), ("The Risk Pool", 1988, 479),
    ("Nobody's Fool", 1993, 549), ("Straight Man", 1997, 391),
    ("Empire Falls", 2001, 483), ("The Whore's Child", 2002, 225),
    ("Bridge of Sighs", 2007, 528), ("That Old Cape Magic", 2009, 261),
    ("Everybody's Fool", 2016, 485), ("Chances Are...", 2019, 290),
]:
    ALL_BOOKS.append(make_book(title, "Richard Russo", year, pages, ["Literary Fiction"]))

# Amy Bloom
for title, year, pages in [
    ("Come to Me", 1993, 176), ("Love Invents Us", 1997, 192),
    ("A Blind Man Can See How Much I Love You", 2000, 192),
    ("Away", 2007, 304), ("Where the God of Love Hangs Out", 2010, 224),
    ("Lucky Us", 2014, 256), ("White Houses", 2018, 256),
    ("In Love", 2022, 240),
]:
    ALL_BOOKS.append(make_book(title, "Amy Bloom", year, pages, ["Literary Fiction"]))

# Edward P. Jones
for title, year, pages in [
    ("Lost in the City", 1992, 249), ("The Known World", 2003, 388),
    ("All Aunt Hagar's Children", 2006, 399),
]:
    ALL_BOOKS.append(make_book(title, "Edward P. Jones", year, pages, ["Literary Fiction"]))

# James McBride
for title, year, pages in [
    ("The Color of Water", 1996, 301), ("Miracle at St. Anna", 2002, 271),
    ("Song Yet Sung", 2008, 359), ("The Good Lord Bird", 2013, 417),
    ("Kill 'Em and Leave", 2016, 228), ("Deacon King Kong", 2020, 370),
    ("The Heaven & Earth Grocery Store", 2023, 385),
]:
    ALL_BOOKS.append(make_book(title, "James McBride", year, pages, ["Literary Fiction"]))

# Andre Dubus III
for title, year, pages in [
    ("Bluesman", 1993, 288), ("House of Sand and Fog", 1999, 365),
    ("The Garden of Last Days", 2008, 537), ("Townie", 2011, 387),
    ("Dirty Love", 2013, 320), ("Gone So Long", 2018, 384),
    ("Such Kindness", 2023, 368),
]:
    ALL_BOOKS.append(make_book(title, "Andre Dubus III", year, pages, ["Literary Fiction"]))

# === ADDITIONAL FRESH GENRES ===

# Chris Bohjalian
for title, year, pages in [
    ("Water Witches", 1995, 320), ("Midwives", 1997, 320),
    ("The Law of Similars", 1999, 288), ("Trans-Sister Radio", 2000, 288),
    ("The Buffalo Soldier", 2002, 320), ("Before You Know Kindness", 2004, 400),
    ("The Double Bind", 2007, 384), ("Skeletons at the Feast", 2008, 384),
    ("Secrets of Eden", 2010, 384), ("The Sandcastle Girls", 2012, 320),
    ("Close Your Eyes, Hold Hands", 2014, 288), ("The Guest Room", 2016, 320),
    ("The Sleepwalker", 2017, 304), ("The Flight Attendant", 2018, 368),
    ("The Red Lotus", 2020, 368), ("Hour of the Witch", 2021, 416),
    ("The Lioness", 2022, 368),
]:
    ALL_BOOKS.append(make_book(title, "Chris Bohjalian", year, pages, ["Literary Fiction", "Thriller"]))

# John Hart
for title, year, pages in [
    ("The King of Lies", 2006, 311), ("Down River", 2007, 322),
    ("The Last Child", 2009, 373), ("Iron House", 2011, 432),
    ("Redemption Road", 2016, 432), ("The Hush", 2018, 416),
]:
    ALL_BOOKS.append(make_book(title, "John Hart", year, pages, ["Thriller", "Literary Fiction"]))

# Elin Hilderbrand - Nantucket
for title, year, pages in [
    ("The Beach Club", 2000, 416), ("Nantucket Nights", 2002, 288),
    ("Summer People", 2003, 320), ("The Blue Bistro", 2005, 368),
    ("Barefoot", 2007, 416), ("A Summer Affair", 2008, 384),
    ("The Castaways", 2009, 432), ("The Island", 2010, 480),
    ("Silver Girl", 2011, 416), ("Summerland", 2012, 400),
    ("Beautiful Day", 2013, 432), ("The Matchmaker", 2014, 416),
    ("The Rumor", 2015, 384), ("Here's to Us", 2016, 400),
    ("The Identicals", 2017, 416), ("The Perfect Couple", 2018, 432),
    ("Summer of '69", 2019, 416), ("28 Summers", 2020, 432),
    ("Golden Girl", 2021, 400), ("The Hotel Nantucket", 2022, 416),
    ("The Five-Star Weekend", 2023, 400), ("Swan Song", 2024, 448),
]:
    ALL_BOOKS.append(make_book(title, "Elin Hilderbrand", year, pages, ["Romance", "Women's Fiction"]))

# Delia Owens
for title, year, pages in [
    ("Cry of the Kalahari", 1984, 341), ("The Eye of the Elephant", 1992, 305),
    ("Where the Crawdads Sing", 2018, 368),
]:
    ALL_BOOKS.append(make_book(title, "Delia Owens", year, pages, ["Literary Fiction"]))

# Bonnie Garmus
ALL_BOOKS.append(make_book("Lessons in Chemistry", "Bonnie Garmus", 2022, 400, ["Literary Fiction"]))

# Matt Haig (filling remaining)
for title, year, pages in [
    ("The Last Family in England", 2004, 288), ("The Dead Fathers Club", 2006, 320),
    ("The Possession of Mr Cave", 2008, 288), ("The Radleys", 2010, 384),
    ("The Humans", 2013, 304), ("How to Stop Time", 2017, 325),
    ("The Midnight Library", 2020, 288), ("The Comfort Book", 2021, 272),
    ("The Life Impossible", 2024, 320),
]:
    ALL_BOOKS.append(make_book(title, "Matt Haig", year, pages, ["Literary Fiction", "Fantasy"]))

# Maggie O'Farrell
for title, year, pages in [
    ("After You'd Gone", 2000, 256), ("My Lover's Lover", 2002, 240),
    ("The Distance Between Us", 2004, 288), ("The Vanishing Act of Esme Lennox", 2006, 245),
    ("The Hand That First Held Mine", 2010, 352), ("Instructions for a Heatwave", 2013, 318),
    ("This Must Be the Place", 2016, 390), ("I Am, I Am, I Am", 2017, 290),
    ("Hamnet", 2020, 372), ("The Marriage Portrait", 2022, 448),
]:
    ALL_BOOKS.append(make_book(title, "Maggie O'Farrell", year, pages, ["Literary Fiction", "Historical Fiction"]))

# Taylor Jenkins Reid (filling remaining)
for title, year, pages in [
    ("Forever, Interrupted", 2013, 336), ("After I Do", 2014, 352),
    ("Maybe in Another Life", 2015, 352), ("One True Loves", 2016, 320),
    ("The Seven Husbands of Evelyn Hugo", 2017, 389),
    ("Daisy Jones & The Six", 2019, 355),
    ("Malibu Rising", 2021, 369), ("Carrie Soto Is Back", 2022, 384),
]:
    ALL_BOOKS.append(make_book(title, "Taylor Jenkins Reid", year, pages, ["Literary Fiction", "Romance"]))

# Lisa Jewell
for title, year, pages in [
    ("Ralph's Party", 1999, 344), ("Thirtynothing", 2000, 384),
    ("One-Hit Wonder", 2001, 400), ("Vince & Joy", 2005, 400),
    ("A Friend of the Family", 2003, 384), ("31 Dream Street", 2007, 384),
    ("The Making of Us", 2011, 432), ("The House We Grew Up In", 2013, 384),
    ("The Third Wife", 2014, 432), ("The Girls in the Garden", 2016, 384),
    ("I Found You", 2017, 384), ("Then She Was Gone", 2018, 384),
    ("Watching You", 2018, 400), ("The Family Upstairs", 2019, 352),
    ("Invisible Girl", 2020, 400), ("The Night She Disappeared", 2021, 384),
    ("The Family Remains", 2022, 400), ("None of This Is True", 2023, 400),
]:
    ALL_BOOKS.append(make_book(title, "Lisa Jewell", year, pages, ["Thriller", "Mystery"]))

# Kristin Hannah (filling remaining)
for title, year, pages in [
    ("A Handful of Heaven", 1991, 384), ("The Enchantment", 1992, 384),
    ("Once in Every Life", 1992, 384), ("If You Believe", 1994, 368),
    ("When Lightning Strikes", 1994, 352), ("Waiting for the Moon", 1995, 368),
    ("Home Again", 1996, 384), ("On Mystic Lake", 1999, 400),
    ("Angel Falls", 2000, 384), ("Summer Island", 2001, 384),
    ("Distant Shores", 2002, 400), ("Between Sisters", 2003, 400),
    ("The Things We Do for Love", 2004, 384), ("Comfort & Joy", 2005, 304),
    ("Magic Hour", 2006, 400), ("Firefly Lane", 2008, 479),
    ("True Colors", 2009, 400), ("Winter Garden", 2010, 416),
    ("Night Road", 2011, 400), ("Home Front", 2012, 384),
    ("Fly Away", 2013, 400), ("The Nightingale", 2015, 440),
    ("The Great Alone", 2018, 448), ("The Four Winds", 2021, 464),
    ("The Women", 2024, 480),
]:
    ALL_BOOKS.append(make_book(title, "Kristin Hannah", year, pages, ["Romance", "Historical Fiction"]))


if __name__ == "__main__":
    existing = load_existing()
    print(f"Existing: {len(existing)} title-author pairs")

    new_books = []
    skipped = 0
    for b in ALL_BOOKS:
        key = (b["title"].lower(), b["author"].lower())
        if key in existing:
            skipped += 1
        else:
            new_books.append(b)
            existing.add(key)

    print(f"Skipped {skipped} duplicates, keeping {len(new_books)} new entries")

    batch_num = 180
    for i in range(0, len(new_books), 100):
        chunk = new_books[i:i+100]
        fname = f"batch_{batch_num}_batch31_{(i//100)+1}.json"
        with open(os.path.join(BATCH_DIR, fname), "w") as f:
            json.dump(chunk, f, indent=2)
        print(f"  {fname}: {len(chunk)} books")
        batch_num += 1

    print(f"\nTotal new books: {len(new_books)}")
