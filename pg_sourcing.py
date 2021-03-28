import pandas as pd
# import numpy as np
import re
import toolbox as tb
import time
import random
# import html2text

# h2t = html2text.HTML2Text()
# h2t.ignore_images = True
# h2t.ignore_tables = True


def extract_essay_df():
    """
    Scrape PG's essay index at pg./articles.html and return a data frame with
    2 columns: post_title, post_link
    """
    url = "http://paulgraham.com/articles.html"
    soup = tb.click_and_soup(url)
    # all posts are contained within a "tr>td>table>tr>td>font>a" structure
    # <table> HTML table; <tr> table row; <th> table header; <td> table data
    posts = soup.select("tr>td>table>tr>td>font>a")
    # make a list of tuples: (post_title, post_link)
    title_link_list = [(p.text, p['href']) for p in posts]
    # turn it to a df
    essay_df = pd.DataFrame(title_link_list,
                            columns=("title", "partial_link"))
    essay_df = essay_df.drop_duplicates()  # some essays appear 2x (top, body)
    essay_df = essay_df.reset_index(drop=True)
    # drop RSS essay
    essay_df = essay_df.drop(essay_df[essay_df['title'] == 'RSS'].index)
    return essay_df


essay_df = extract_essay_df()
essay_df.index.set_names('essay_id', inplace=True)
essay_df.describe()  # 198 unique essays as of Feb 22
essay_df.head()
essay_df.to_csv('csv/essay_df.csv')
#
essay_df = pd.read_csv('csv/essay_df.csv', index_col='essay_id')


def url2soup(url):
    """Take an essay's url, turn it into a soup and extract the text"""
    essay_soup = tb.click_and_soup(url)
    try:
        essay_soup = essay_soup.select("table>tr>td>table>tr>td>font")[0]
    except IndexError:
        essay_soup = essay_soup.select("html>body>p")[0]
    # note: some essays have a paragraph tag and some don't
    # vb: "table>tr>td>table>tr>td>font"
    # ds: "table>tr>td>table>tr>td>font>p"
    return essay_soup


def soup2string(essay_soup):
    """Take an essay in soup form and turn it to a string"""
    return str(essay_soup)


def extract_essay_outlinks(essay_soup):
    """Extract all the outlinks in essay i (excluding footnotes)"""
    # three types of links: fXn_top, fXn_bottom, all other links
    all_links = essay_soup.select('a', href=True)
    # extract outlinks (exclude footnote-related links)
    real_links = []
    for link in all_links:
        if not bool(re.findall('f.n', str(link))):
            try:
                real_links.append(link['href'])
            except KeyError:
                # some tags that are not hrefs also exist, eg <a name>
                pass
    return real_links


def clean_essay_text(string_essay):
    """Take the soup from a given essay and return its formatted body"""
    # order of task preprocessing matters
    string_essay = re.sub("\n", " ", string_essay)  # line breaks for spaces
    string_essay = re.sub('<br/><br/>', ' \n\n', string_essay)
    string_essay = re.sub('<[^<]+?>', '', string_essay)
    # don't forget strip() to remove leading and trailing whitespaces
    string_essay = re.sub("  ", " ", string_essay).strip()
    return string_essay


def extract_body_and_features(essay_df):
    """Take a dataframe with essay links and return essay body and features"""
    data = []
    for i in essay_df.index:
        # i = 1
        print(i, essay_df.index[i], essay_df['title'].iloc[i])
        if essay_df['partial_link'][i][:5] != 'https':
            url = "http://paulgraham.com/" + essay_df['partial_link'][i]
        else:
            url = essay_df['partial_link'][i]
        essay_soup = url2soup(url)
        essay_string = soup2string(essay_soup)
        # append record-level features
        essay_body = clean_essay_text(essay_string)
        # write the essay to .txt
        # TODO create a new naming scheme for common lisp essays
        if '1 of Ansi Common' in essay_df['title'][i]:
            tb.save_as_txt(essay_body, 'common_lisp_1')
        elif '2 of Ansi Common' in essay_df['title'][i]:
            tb.save_as_txt(essay_body, 'common_lisp_2')
        else:
            name2save = essay_df['partial_link'][i].split('.')[0]
            tb.save_as_txt(essay_body, name2save)
        essay_outlinks = extract_essay_outlinks(essay_soup)
        data.append([
                    url,  # full_link
                    essay_outlinks,  # outlinks
                    len(essay_body.split())  # word count
                    ])
        time.sleep(0.3 + random.random())  # some server kindness

    feature_df = pd.DataFrame(data, columns=['full_link',
                                             'outlinks',
                                             'word_count'])
    return feature_df


# left join the original df with the feature df
feature_df = extract_body_and_features(essay_df)
feature_df.index.set_names('essay_id', inplace=True)
feature_df.head()
# full_df = pd.merge(essay_df, feature_df, how='left',
#                    left_index=True, right_index=True)
full_df = pd.merge(essay_df, feature_df, how='left', on='essay_id')
full_df.head()
full_df.to_csv('csv/full_df.csv')


def extract_essay_date(string_essay):
    """Take a cleaned string essay and return the date"""
    re.findall('.*\n', string_essay)[0]
    string_essay.split('\n')[0].strip()
    return


def main():
    """ """
    full_df = pd.read_csv('csv/full_df.csv')
    full_df.head()
    pass

