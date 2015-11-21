import codecs, urllib2, utilities_lib
from bs4 import BeautifulSoup
# Expansion library for New Jerusalem Bible
def njv_scrape(url, start, end):
    start = int(start)-1
    end = int(end)-1
    soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
    verse_soups = soup.findAll('div', {'id' : 'bibleBook'})[0].findAll('p')
    # Read in all the verse_nums
    verse_num_elems = soup.findAll('div', {'id' : 'bibleBook'})[0].findAll('p')
    verse_nums = []
    for verse_num_elem in verse_num_elems:
        verse_num = verse_num_elem.findAll('a')[0]['name'].encode('utf8')
        if verse_num.isdigit():
            verse_nums.append(verse_num)
    # Read in all the verse_texts
    verse_texts = utilities_lib.purify_text(verse_soups)
    if len(verse_nums) != len(verse_texts):
        raise Exception("Unequal lengths:"+str(len(verse_nums))+","+str(len(verse_texts)))
    return (verse_nums[start:end+1], verse_texts[start:end+1])

def njv_home(args):
    if len(args) != 2:
        raise Exception("Invalid number of args entered"+args)
    book = args[0]
    chapter = args[1].split(':')[0]
    start = args[1].split(':')[-1].split('-')[0]
    end = args[1].split(':')[-1].split('-')[-1]
    root_url = 'http://www.catholic.org/bible/'
    soup = BeautifulSoup(urllib2.urlopen(root_url), "html.parser")
    book_names = []
    index_urls = []
    chapter_num_lists = []
    chapter_url_lists = []
    a_elems = soup.findAll('a', {'class':'list-group-item'})
    for a_elem in a_elems:
        book_names.append(a_elem.contents[0].encode('utf8'))
        index_urls.append(root_url + a_elem['href'].split('/')[-1].encode('utf8'))
        chapter_nums = []
        chapter_urls = []
        chapter_soup = BeautifulSoup(urllib2.urlopen(index_urls[-1]), "html.parser")
        chapter_elems = chapter_soup.findAll('ul', {'class' : 'pagination Chapters'})[0].findAll('li')[1:-1]
        for chapter_elem in chapter_elems:
            chapter_nums.append(chapter_elem.find('a').contents[0].encode('utf8'))
            chapter_urls.append(root_url + chapter_elem.findAll('a')[0]['href'].split('/')[-1].encode('utf8'))
        chapter_num_lists.append(chapter_nums)
        chapter_url_lists.append(chapter_urls)
    request_url = ''

    for book_i in xrange(0,len(book_names)):
        if len(chapter_num_lists[book_i]) != len(chapter_url_lists[book_i]):
            raise Exception("Unequal lengths:"+str(len(chapter_num_lists[book_i]))+","+str(len(chapter_url_lists[book_i])))
        if book_names[book_i] != book:
            continue
        for chapter_i in xrange(0,len(chapter_num_lists[book_i])):
            if chapter_num_lists[book_i][chapter_i] != chapter:
                continue
            request_url = chapter_url_lists[book_i][chapter_i]
            break
        break

    if request_url:
        nums = []
        texts = []
        (nums, texts) = njv_scrape(request_url, start, end)
        return (nums, texts)
    else:
        raise Exception("Requested URL not found")

def parse_njv(args):
    (verse_nums, verse_texts) = njv_home(args)
    with open("njv_plain.txt",'w') as out_njv:
        out_njv.write(utilities_lib.remove_leading_space(' '.join(verse_texts)))
    with open("njv_lines.txt",'w') as out_njv2:
        for i in xrange(0,len(verse_nums)):
            out_njv2.write(verse_nums[i] + ',' + verse_texts[i] + '\n')