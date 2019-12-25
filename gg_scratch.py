

from bs4 import BeautifulSoup
import requests
import os
import sys
from collections import Counter
import datetime



url = 'http://www.girlgeniusonline.com/comic.php?date=20091027'
test_get = requests.get(url)
soup_read = BeautifulSoup(test_get.content, 'html5lib')
imgs = soup_read.find_all('img', alt = 'Comic')
for img in imgs:
    com_down = img.get('src')
    print(com_down)
    if com_down == None:
        sys.stdout.write('Worked!')
        sys.stdout.flush()
    else:
        sys.stdout.write("Didn't work!")
        sys.stdout.flush()


print(soup_read)
print(imgs)
print(len(imgs))