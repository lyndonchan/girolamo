import codecs, urllib2
from .. import utilities_lib
from bs4 import BeautifulSoup
# Expansion library for Studium Biblicum Bible (Trad. Chinese)
def sbt_scrape(url, start, end):
    start = int(start)-1
    end = int(end)-1
    soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
    verse_elems = soup.findAll('table', {'style' : 'align=center'})[1].findAll('tr')
    verse_nums = []
    verse_texts = []
    for verse_elem in verse_elems:
        verse_nums.append(verse_elem.find('td').find('sup').contents[0].encode('utf8'))
        verse_texts.append(verse_elem.find('td').find('sup').nextSibling)
    return (verse_nums[start:end+1], verse_texts[start:end+1])

def sbt_home(args):
    if len(args) != 2:
        raise Exception("Invalid number of args entered")
    book = args[0]
    chapter = args[1].split(':')[0]
    start = args[1].split(':')[-1].split('-')[0]
    end = args[1].split(':')[-1].split('-')[-1]
    root_url = 'http://www.ccreadbible.org/Chinese%20Bible/sigao'
    soup = BeautifulSoup(urllib2.urlopen(root_url), "html.parser")
    book_names = []
    chapter_num_lists = []
    chapter_url_lists = []
    table_elems = soup.find('div', {'id' : 'content-core'}).find('div').findAll('table')
    for table_elem in table_elems:
        for book_elem in table_elem.find('tbody').findAll('tr'):  
            if not book_elem.findAll('td'):
                continue
            if book_elem.findAll('td')[0].find('a').nextSibling:
                book_names.append(utilities_lib.remove_leading_space(str(book_elem.findAll('td')[0].find('a').nextSibling)))
            else:
                book_names.append(utilities_lib.remove_leading_space(str(book_elem.findAll('td')[0].find('a').contents[0].split('/')[-1])))
            chapter_nums = []
            for chapter_num in book_elem.findAll('td')[1].findAll('a'):
                chapter_nums.append(chapter_num.contents[0].replace('[','').replace(']','').encode('utf-8'))
            chapter_num_lists.append(chapter_nums)
            url_list = []
            for url in book_elem.findAll('td')[1].findAll('a'):
                url_list.append(url['href'].encode('utf-8'))
            chapter_url_lists.append(url_list)  
            
    request_url = ''
    for book_i in xrange(0,len(book_names)):
        if book_names[book_i] != book:
            continue
        for chapter_i in xrange(0,len(chapter_num_lists[book_i])):
            if chapter_num_lists[book_i][chapter_i] != chapter:
                continue
            request_url = chapter_url_lists[book_i][chapter_i]
        
    if request_url:
        nums = []
        texts = []
        (nums, texts) = sbt_scrape(request_url, start, end)
        return (nums, texts)
    else:
        raise Exception("Requested URL not found")

def parse_sbt(args):
    # Studium Biblicum Bible (Trad. Chinese)
    (verse_nums, verse_texts) = sbt_home(args)
    with open('sbt_plain.txt','w') as out_sbt:
        out_sbt.write((''.join(verse_texts)).encode('utf8'))
    with open('sbt_lines.txt','w') as out_sbt2:
        for i in xrange(0,len(verse_nums)):
            out_sbt2.write(verse_nums[i] + ',' + verse_texts[i].encode('utf8') + '\n')