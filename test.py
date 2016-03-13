from bs4 import BeautifulSoup

soup = BeautifulSoup(open('/Users/Barry/Documents/test.html'), 'html.parser')

for x in soup.select('#WikiModule_Characters ul.li_6 li a'):
    print x.string