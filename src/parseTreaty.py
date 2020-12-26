try:
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup
import re
import requests
from urllib.parse import urljoin
import json
import sys


def parse_div(div):
    children = div.children
    result = []
    for c in children:
        # print(c)
        found = re.findall(r'href="(.*?)">', str(c))
        # print(found)
        if len(found) > 0:
            result.append(found[0])
    return result


# def find_references_to_other(text):

path = "https://eur-lex.europa.eu/collection/eu-law/treaties/"
page = requests.get(path + "treaties-force.html")
parsed = BeautifulSoup(page.text, features="lxml")

print(path + "/treaties-force.html")
# print(parsed.body.find_all('h2'))

divs = parsed.body.find_all("div", class_="collapse treatiesTableMobile")
# print(divs)

print("Number of divs", len(divs))

f = parse_div(divs[0])


treaty = {}
for i, article in enumerate(f):
    url = urljoin(path, article)
    # print(url)
    article = requests.get(url).text
    # print(article)
    parsed_article = BeautifulSoup(article, features="lxml")
    divs = parsed_article.find_all("div", class_="tabContent")
    # only the second is relevant
    # print(divs)
    div = divs[1]
    children = div.children

    # print (''.join(text.strip() for text in parsed_article.p.find_all(text=True, recursive=False)))

    for c in children:
        paragraphs = re.findall(r'<p class="normal">(.*?)</p>', str(c))
        if len(paragraphs) > 0:
            text = str(" ".join(paragraphs))
        for line in str(c).split("\n"):
            # print(line)
            if '"ti-art"' in line:
                name = str(re.search(r'">(.*?)</p>', line).group(1))
                print("Element", name)

    treaty[name] = {}
    paragraphs = list(filter(None, re.split(r"(?<!Article\xa0)\d\.", text)))

    for i, par in enumerate(paragraphs):
        treaty[name][i + 1] = par
        # find references to other Articles in text
        try:
            refs = []
            # exclude "this Article"
            par = par.replace("this Article", "")  
            # find all occurrencies of "Article":
            idxs =[i for i in range(len(par)) if par.startswith('Article', i)]
            print(idxs)
            for i,idx in enumerate(idxs):
                if idxs.index(idx)<len(idxs)-1:
                    p = par[idxs[i]:idxs[i+1]]
                else:
                    p = par[idx:]
                print(p)
                pos = p.index("Article")  # 'Article' has 7 letters
                # find the number
                # print(pos)
                substring = p[pos + 7 : pos + 7 + 200].split()
                ss = " ".join(substring)

                # check if it refers to multiple articles:
                if substring[0]=='s': # if 'Articles', plural
                    if substring[2]=='to': #if "Articles x to y"
                        for k in range(int(substring[1]), int(substring[3])+1):
                            refs.append(k)
                    # elif substring[2]=='and': #if "Articles x and y"

                ref_num = substring[0]
                print("==> Paragraph\n", p)

                print("===> sub\n", ss)
                print(substring[:10])

            # print(" ".join(substring))
            # if ''.join(substring[0:2]) =='of' :
            # print ("===> of",substring[0:20])

        # except ValueError:
            # pass
            # print("Value error (it may be expected.)")  # ,sys.exc_info()[0])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise


with open("treaty.json", "w") as fw:
    json.dump(treaty, fw)

    # pass
    # print(dir(c))
    # print(c)

    # print(bs)
#     print( ''.join(text.strip() for text in bs.find_all(text=True, recursive=False)))
# print(divs[1])
