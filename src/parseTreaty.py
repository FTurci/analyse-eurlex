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
        found = re.findall(r'href="(.*?)">',str(c))
        # print(found)
        if len(found)>0:
            result.append(found[0])
    return result

path = 'https://eur-lex.europa.eu/collection/eu-law/treaties/'
page = requests.get(path+'treaties-force.html')
parsed = BeautifulSoup(page.text,features="lxml")



print(path+'/treaties-force.html')
print(parsed.body.find_all('h2'))

divs = parsed.body.find_all('div', class_='collapse treatiesTableMobile')
print(divs)

# print(len(divs))

f = parse_div(divs[0])


treaty = {}
for i, article in enumerate(f):
    url = urljoin(path,article)
    print(url)
    article = requests.get(url).text
    # print(article)
    parsed_article = BeautifulSoup(article,features="lxml")
    divs = parsed_article.find_all('div', class_='tabContent')
    # only the second is relevany
    div = divs[1]
    children = div.children

    # print (''.join(text.strip() for text in parsed_article.p.find_all(text=True, recursive=False)))

    for c in children:
        paragraphs = re.findall(r'<p class="normal">(.*?)</p>',str(c))
        if len(paragraphs)>0:
            text =str(' '.join(paragraphs))
        for line in str(c).split('\n'):
            # print(line)
            if "\"ti-art\"" in line:
                name = str(re.search(r'">(.*?)</p>',line).group(1))
                print(name)

    treaty[name]={}
    paragraphs = list(filter(None,re.split(r'(?<!Article\xa0)\d\.',text)))
    for i,p in enumerate(paragraphs):
        treaty[name][i+1]=p
        # find references to other Articles in text
        try:
            pos = p.index('Article') # 'Article' has 6 letters
            # find the number
            print(pos)
            substring = p[pos+6:pos+6+200].split()
            ref_num = substring[0]
            print(p)
            if ''.join(substring[1:3]) =='of this' :
                print ("OFTHIS",p)
        except ValueError:
            print("Value error")#,sys.exc_info()[0])
        except:
            print("Unexpected error:", sys.exc_info()[0])
            raise

    
with open("treaty.json", 'w') as fw:
    json.dump(treaty, fw)   


        # pass
    # print(dir(c))
    # print(c)
   
    # print(bs)
#     print( ''.join(text.strip() for text in bs.find_all(text=True, recursive=False)))
# print(divs[1])
