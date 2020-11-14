from bs4 import BeautifulSoup
import requests
import os
import sys
from collections import Counter
import datetime
import shelve


def GG_crawler(book_dict):

    sys.stdout.write(f'Downloading has begun, time is now: {datetime.datetime.now()}\n')
    sys.stdout.flush()

    try: 

        url = 'http://www.girlgeniusonline.com/comic.php?date=20021104'
        last_com = False
        book = ''
        init_url = requests.get(url)
        init_read = BeautifulSoup(init_url.content, 'html5lib')
        last_img = init_read.find(id = 'toplast')
        last_url = last_img.get('href') 

    except:
        sys.stdout.write(f'Unable to reach the Girl Genius server. Operation aborted.\n Time is now: {datetime.datetime.now()} \n')
        sys.stdout.flush()
        return 'Done!'

    gg_tracker = shelve.open('GG_tracker', writeback = True) 

    if 'url' in gg_tracker:
        url = gg_tracker['url']
        if url == last_url:
            sys.stdout.write(f'No new comics since this was last run.\n')
            last_com = True
        else:
            sys.stdout.write('Finding next comic...')
            sys.stdout.flush()
            gg_comic = requests.get(url)
            comic_soup = BeautifulSoup(gg_comic.content, 'html5lib')
            next_img = comic_soup.find(id = 'topnext')
            url = next_img.get('href')

    else:
        gg_tracker['url'] = url
        url = gg_tracker['url']

    if 'pages' in gg_tracker:
        pages = gg_tracker['pages']
        book = gg_tracker['book']

    else:
        gg_tracker['pages'] = Counter()
        pages = gg_tracker['pages']
    
    while last_com == False:

        try:
            gg_comic = requests.get(url)

            com_id = url[-8:]

            comic_soup = BeautifulSoup(gg_comic.content, 'html5lib')
            imgs = comic_soup.find_all('img', alt = 'Comic')

            if com_id in book_dict:
                book = book_dict[com_id]
                os.makedirs(book, exist_ok = True)
                sys.stdout.write(f'Switching to book {book}\n Time is now {datetime.datetime.now()} \n')
                sys.stdout.flush()

            if len(imgs) > 0: 
                for img in imgs:

                    com_down = img.get('src')

                    if com_down == None: 
                        sys.stdout.write(f'No comic found on page {com_id}. Continuing...\n')

                    else:
                        pages[book] += 1
                        image = requests.get(com_down)
                        com_name = f'{book} {str(pages[book]).zfill(3)}{com_down[-4:]}'
                        image_file = open(os.path.join(book, os.path.basename(com_name)), 'wb')

                        sys.stdout.write(f'Downloading {book} {pages[book]}\n')
                        sys.stdout.flush()

                        for chunk in image.iter_content(100_000):
                            image_file.write(chunk)

                        image_file.close()

            else:
                sys.stdout.write(f'No comics found on {url}\n')
                sys.stdout.flush()

        except:
            sys.stdout.write(f'Error in Downloading Process after {book} {pages[book]}. Ending process.')
            sys.stdout.flush()
            gg_tracker['book'] = book
            gg_tracker['url'] = old_url
            gg_tracker['pages'] = pages
            gg_tracker.close()
            return 'Done!'

        
        if url == last_url:
            sys.stdout.write(f'All done! \n Time is now: {datetime.datetime.now()}\n')
            gg_tracker['book'] = book
            gg_tracker['url'] = url
            gg_tracker['pages'] = pages
            gg_tracker.close()
            last_com = True

        else:
            old_url = url
            next_img = comic_soup.find(id = 'topnext')
            url = next_img.get('href')






        


books = {'20021104' : 'Book One',
        '20030512' : 'Book Two',
        '20031231' : 'Book Three',
        '20041004' : 'Book Four',
        '20050627' : 'Book Five',
        '20051212' : 'Extra - FanFiction',
        '20051228' : 'Book Five',
        '20060310' : 'Book Six',
        '20060515' : 'Extra - Personal Trainer',
        '20060524' : 'Book Six',
        '20070226' : 'Book Seven',
        '20070827' : 'Radio Theater - Revenge of the Weasel Queen',
        '20071001' : 'Book Seven',
        '20071228' : 'Radio Theater - Revenge of the Weasel Queen',
        '20080204' : 'Book Eight',
        '20080507' : 'Extras',
        '20080512' : 'Book Eight',
        '20081121' : 'Extra - Cinderella',
        '20090114' : 'Book Nine',
        '20090601' : 'Radio Theater - Revenge of the Weasel Queen',
        '20090701' : 'Book Nine',
        '20090817' : 'Extras',
        '20090819' : 'Book Nine',
        '20091211' : 'Extras',
        '20091214' : 'Book Ten',
        '20100412' : 'Extras',
        '20100414' : 'Book Ten',
        '20100519' : 'Extra - Maxim Buys A Hat',
        '20100616' : 'Book Ten',
        '20101025' : 'Book Eleven',
        '20110105' : 'Extras',
        '20110107' : 'Book Eleven',
        '20110415' : 'Extras',
        '20110418' : 'Book Eleven',
        '20110831' : 'Extras',
        '20110902' : 'Book Eleven',
        '20111107' : 'Book Twelve',
        '20120410' : 'Extras',
        '20120411' : 'Book Twelve',
        '20121025' : 'Extras',
        '20121026' : 'Book Twelve',
        '20121221' : 'Book Thirteen',
        '20130419' : 'Extras',
        '20130422' : 'Book Thirteen',
        '20130717' : 'Extras',
        '20130729' : 'Book Thirteen',
        '20131023' : 'Extras',
        '20131028' : 'Book Thirteen',
        '20131230' : 'Radio Theater - Small Problems',
        '20140303' : 'Book Fourteen',
        '20140423' : 'Extras',
        '20140430' : 'Book Fourteen',
        '20140813' : 'Extra - Homecoming King',
        '20140827' : 'Extras',
        '20140829' : 'Book Fourteen',
        '20141231' : 'Extras', 
        '20150119' : 'Book Fifteen',
        '20150624' : 'Extras',
        '20150724' : 'Book Fifteen',
        '20150922' : 'Extras',
        '20150923' : 'Book Fifteen',
        '20151125' : 'Book Sixteen',
        '20151127' : 'Extras',
        '20151130' : 'Book Sixteen',
        '20151225' : 'Extras',
        '20151228' : 'Book Sixteen',
        '20160101' : 'Extras',
        '20160104' : 'Book Sixteen',
        '20160914' : 'Book Seventeen',
        '20161028' : 'Extras',
        '20161031' : 'Book Seventeen',
        '20161116' : 'Extras',
        '20161121' : 'Book Seventeen',
        '20161212' : 'Extras',
        '20161214' : 'Book Seventeen',
        '20170714' : 'Book Eighteen',
        '20170802' : 'Extras',
        '20170809' : 'Extra - Ivo Sharktooth',
        '20171106' : 'Book Eighteen',
        '20180101' : 'Extras',
        '20180103' : 'Book Eighteen',
        '20180119' : 'Extras',
        '20180122' : 'Book Eighteen',
        '20180219' : 'Extras',
        '20180221' : 'Book Eighteen',
        '20180305' : 'Extras',
        '20180307' : 'Book Eighteen',
        '20180402' : 'Extras',
        '20180430' : 'Book Eighteen',
        '20180907' : 'Extras',
        '20180910' : 'Book Nineteen',
        '20181005' : 'Extras',
        '20181012' : 'Book Nineteen',
        '20190102' : 'Extras',
        '20190104' : 'Book Nineteen',
        '20190701' : 'Book Twenty',
        '20190826' : 'Extras',
        '20190828' : 'Book Twenty',
        '20190927' : 'Extras',
        '20190930' : 'Book Twenty',
        '20191206' : 'Extras',
        '20191209' : 'Book Twenty',
        '20200203' : 'Extras',
        '20200207' : 'Book Twenty',
        '20200304' : 'Extras',
        '20200306' : 'Book Twenty',
        '20200401' : 'Extras',
        '20200403' : 'Book Twenty',
        '20200427' : 'Book Twenty-One',
        '20201023' : 'Extras',
        '20201026' : 'Book Twenty-One',
                }


def main():
    GG_crawler(books)

if __name__ == '__main__':
    main()
