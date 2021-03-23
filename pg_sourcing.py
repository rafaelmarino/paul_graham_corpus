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
    title_link_list = [(p.text,
                        "http://paulgraham.com/" + p['href'],
                        p['href'],
                        )
                       for p in posts]
    # turn it to a df
    essay_df = pd.DataFrame(title_link_list,
                            columns=("title", "link", "file_name"))
    essay_df = essay_df.drop_duplicates()  # some essays appear 2x (top, body)
    return essay_df


essay_df = extract_essay_df()
essay_df.describe()  # 198 unique essays as of Feb 22
essay_df.head()


def url2soup(url):
    """Take an essay's url, turn it into a soup and extract the text"""
    essay_soup = tb.click_and_soup(url)
    essay_soup = essay_soup.select("table>tr>td>table>tr>td>font")[0]
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
            real_links.append(link['href'])
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
    for i in essay_df.index[:5]:
        # i = 1
        url = essay_df['link'][i]
        essay_soup = url2soup(url)
        essay_string = soup2string(essay_soup)
        # append record-level features
        essay_body = clean_essay_text(essay_string)
        essay_outlinks = extract_essay_outlinks(essay_soup)
        data.append([
                    essay_body,
                    essay_outlinks,
                    len(essay_body.split())
                    ])
        time.sleep(0.3 + random.random())  # some server kindness

    feature_df = pd.DataFrame(data, columns=['body', 'outlinks', 'word_count'])
    return feature_df


# left join the original df with the feature df
feature_df = extract_body_and_features(essay_df)
full_df = pd.merge(essay_df, feature_df, how='left',
                   left_index=True, right_index=True)
full_df.head()


    
    
    # save
    name2save = essay_df['file_name'][i].split('.')[0]
    tb.save_as_txt(processed_essay, name2save)
    tb.save_as_txt(processed_essay, 'vb_march23')
    tb.save_as_txt(processed_essay, 'ds_march23')
    tb.save_as_html(string_essay, name2save)
    tb.save_as_txt(string_essay, name2save)

# h2t_essay = h2t.handle(str(essay_soup).strip())
# tb.save_as_txt(h2t_essay, "ds_h2t")


outlink_vector_df = pd.DataFrame(outlink_vector, columns=['index', 'outlinks'])
outlink_vector_df.head()



extract_essay_outlinks(essay_soup)





def extract_essay_date(string_essay):
    """Take a cleaned string essay and return the date"""
    re.findall('.*\n', string_essay)[0]
    string_essay.split('\n')[0].strip()
    return


# extract_essay_outlinks
# clean_essay_text
# extract_essay_date





# TODO
# extract date: month_label
# extract date: month_number (MM)
# extract date: year (YYY)
# replace double breaks for line breaks "\n"






# # exploring an alternative: str(html_soup.text)
# string_essay2 = str(essay_soup.text)  # alternative method
# string_essay2 = essay_soup.text  # alternative method
# # re.findall('.\n.', string_essay2)
# re.sub('\n', ' ', string_essay2[:300])
# string_essay2[:300]
# # NOTE: it looks a bit difficult to extract paragraphs correctly like this

# second string literal in python is always displayed with backslash
# string_essay = re.sub("\'", "'", string_essay)
# print(string_essay)

# 'f1n' in string_essay
# partial_essay = ('Otherwise these people are literally\ntaking your '
#                  'life.\n<font color="#999999">[<a href="#f2n"><font '
#                  'color="#999999">2</font></a>]</font><br/><br/>Arguing '
#                  'online is only incidentally addictive.'
#                  )

# # test case with f1n : footnote 1
# f1n = ('<font color=\"#999999\">\[<a href=\"#f1n\"><font '
#        'color=\"#999999\">1</font></a>\]</font>'
#        )
# # build f1n test_case with double backslashes and test with re.sub()
# f1n_double = ('<font color=\\"#999999\\">\\[<a href=\\"#f1n\\"><font '
#               'color=\\"#999999\\">1</font></a>\\]</font>'
#               )
# generalize with wildcard to find all footnotes


# NOTE: the code below is deprecated, regular expressions are more powerful
# than finding and then constructing strings for removal.

fXn = ('<font color=\"#999999\">\[<a href=\"#f.n\"><font '
       'color=\"#999999\">.</font></a>\]</font>'
       )

# re.findall(f1n, string_essay)  # footnote1
all_footnotes = re.findall(fXn, string_essay)
print('{} footnotes found'.format(len(all_footnotes)))
print(all_footnotes)

# construct the regular expression for each footnote and sub it for a blank
for (key, fn) in enumerate(all_footnotes):
    # fn = all_footnotes[0]
    f1n_double_constructed = re.sub('"', '\\"', fn)
    f1n_double_constructed = re.sub('\[', '\\[', f1n_double_constructed)
    f1n_double_constructed = re.sub('\]', '\\]', f1n_double_constructed)
    # construct a new footnote 
    fn_symbol = '[' + str(key+1) + ']'
    string_essay = re.sub(f1n_double_constructed, fn_symbol, string_essay)

# save essay as .txt instead
with open("txt/vb.txt", "w") as text_file:
    text_file.write(string_essay)

# re.findall(f1n_double_constructed, string_essay)
# re.findall(f1n, string_essay)
# re.findall(f1n_double, string_essay)
# re.findall(f1n_double_constructed, string_essay)
# re.findall(fXn, partial_essay)

# save as html
# tb.save_as_html(essay_soup, "vb")
# tb.save_as_html(string_essay, "vb_cleaned")


# alternative txt file
# with open("txt/vb2.txt", "w") as text_file:
#     text_file.write(string_essay2)


type(essay_soup.text)
print(essay_soup.text)
# Isolating the essay
# Essay is wrapped by a <font> tag: "<font face="verdana" size="2">"
# 
# Essay ends after Thanks followed by closure of <font> tag

# below lie tests

# "<a href='vb.html'><u>Life is Short</u></a>"
# test_soup = BeautifulSoup("<a href='vb.html'><u>Life is Short</u></a>")
# test_soup.find("a", href=True)['href']
# eof