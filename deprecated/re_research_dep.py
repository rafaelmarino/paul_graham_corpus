import re

# exploring an alternative: str(html_soup.text)
string_essay2 = str(essay_soup.text)  # alternative method
string_essay2 = essay_soup.text  # alternative method
# re.findall('.\n.', string_essay2)
re.sub('\n', ' ', string_essay2[:300])
string_essay2[:300]
# NOTE: it looks a bit difficult to extract paragraphs correctly like this

# second string literal in python is always displayed with backslash
# string_essay = re.sub("\'", "'", string_essay)
# print(string_essay)

'f1n' in string_essay
partial_essay = ('Otherwise these people are literally\ntaking your '
                 'life.\n<font color="#999999">[<a href="#f2n"><font '
                 'color="#999999">2</font></a>]</font><br/><br/>Arguing '
                 'online is only incidentally addictive.'
                 )

# test case with f1n : footnote 1
f1n = ('<font color=\"#999999\">\[<a href=\"#f1n\"><font '
       'color=\"#999999\">1</font></a>\]</font>'
       )
# build f1n test_case with double backslashes and test with re.sub()
f1n_double = ('<font color=\\"#999999\\">\\[<a href=\\"#f1n\\"><font '
              'color=\\"#999999\\">1</font></a>\\]</font>'
              )
generalize with wildcard to find all footnotes


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