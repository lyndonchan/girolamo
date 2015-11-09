import codecs, urllib2
from .. import utilities_lib
from bs4 import BeautifulSoup
# Expansion library for New American Bible
def nab_scrape(url, start, end):
    start = int(start)-1
    end = int(end)-1
    soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
    # Read in all the verse_nums
    verse_num_elems = soup.findAll('p', {'class' : 'MsoNormal', 'style' : False})
    verse_nums = []
    for verse_num_elem in verse_num_elems:
        verse_num = verse_num_elem.contents[0].encode('utf8').strip()
        if verse_num.isdigit():
            verse_nums.append(verse_num)
    # Read in all the verse_texts
    verse_text_elems = soup.findAll('p', {'class' : 'MsoNormal', 'style' : 'margin-left:36.0pt'})
    verse_texts = []
    i = 0
    for verse_text_elem in verse_text_elems:
        verse_text = ''
        for cont in verse_text_elem.contents:
            if utilities_lib.is_text(cont):
                verse_text+=' ' + str(utilities_lib.rem_lead_end_spaces(cont).replace('\n',' ').replace('\r',''))
        verse_texts.append(utilities_lib.remove_leading_space(verse_text.replace('  ',' ')))
        i += 1
    if len(verse_nums) != len(verse_texts):
        raise Exception("Unequal lengths:"+str(len(verse_nums))+","+str(len(verse_texts)))
    return (verse_nums[start:end+1], verse_texts[start:end+1])

def nab_home(args):
    if len(args) != 2:
        raise Exception("Invalid number of args entered"+args)
    book = args[0]
    chapter = args[1].split(':')[0]
    start = args[1].split(':')[-1].split('-')[0]
    end = args[1].split(':')[-1].split('-')[-1]
    root_url = 'http://www.vatican.va/archive/ENG0839/'
    index_url = root_url + '_INDEX.HTM'
    soup = BeautifulSoup(urllib2.urlopen(index_url), "html.parser")
    book_names = []
    chapter_num_lists = []
    chapter_url_lists = []
    list_elems = soup.findAll('li')
    for list_elem in list_elems:
        if list_elem.findAll('font') and utilities_lib.is_text(list_elem.find('font').contents[0]):
            book_names.append(list_elem.find('font').contents[0].encode('utf8'))
            book_elem = list_elem
            try:
                chapter_elems = book_elem.find('ul').find('li').find('font').findAll('a')
            except:
                pass
                # Psalms are buggy on the vatican website; script probably fails for single-chapter books, like Jude
            chapter_nums = []
            chapter_urls = []
            for chapter_elem in chapter_elems:
                chapter_nums.append(chapter_elem.contents[0].encode('utf8'))
                chapter_urls.append((root_url + chapter_elem['href']).encode('utf8'))
            chapter_num_lists.append(chapter_nums)
            chapter_url_lists.append(chapter_urls)
    
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
        (nums, texts) = nab_scrape(request_url, start, end)
        return (nums, texts)
    else:
        raise Exception("Requested URL not found")

def parse_nab(args):
    (verse_nums, verse_texts) = nab_home(args)
    with open("nab_plain.txt",'w') as out_nab:
        out_nab.write(utilities_lib.remove_leading_space(' '.join(verse_texts)))
    with open("nab_lines.txt",'w') as out_nab2:
        for i in xrange(0,len(verse_nums)):
            out_nab2.write(verse_nums[i] + ',' + verse_texts[i] + '\n')