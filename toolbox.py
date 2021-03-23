from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup
import json


def full_stamp():
    """Return now's date(Y/m/d) and time(H:M:S)"""
    return datetime.now().strftime("%Y/%m/%d/ %H:%M:%S")


def click_and_soup(lien):
    """Take a URL, open the connection, read the page, close the connection,
    return the BeautifulSoup version"""
    
    try:
        client = urlopen(lien)
        page_html = client.read()
        client.close()
        page_soup = BeautifulSoup(page_html, "lxml")
    except:
        return "404"
    return page_soup


def save_as_html(file, filename):
    """Take a soup file and save it as an html."""
    f = open("html/" + filename + '.html', 'w')
    f.write(str(file))
    f.close()
    return


def save_as_txt(string_object, filename):
    """Take a string and save it in a txt file. """
    with open("txt/" + filename + ".txt", "w") as text_file:
        text_file.write(string_object)
        return


def load_db(filename):
    """Load the database and return its size (in keys, ie partitions)."""
    with open('datasets/' + filename, 'r') as read_file:  # 2-line opener
        database = json.load(read_file)
    dbsize = len(database)
    return database, dbsize


def main():
    pass


if __name__ == "__main__":
    # stuff only to run when not called via 'import' here
    main()
