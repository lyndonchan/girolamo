import codecs, urllib2, utilities_lib
#from .. import utilities_lib
from bs4 import BeautifulSoup
# Expansion library for New American Bible
def nab_scrape_chapter(url,start,end):
    start = int(start)
    end = int(end)
    chapter = url.split('+')[-1].split('&')[0]
    soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
    chapter_abbrev = soup.find('a',{'class':'bibleref'})['data-bibleref'].split('.')[0]
    # Read in all the verse_nums and verse_texts
    verse_nums = []
    verse_texts = []
    verse_num_elems = soup.findAll('sup',{'class':'versenum'})
    for i in xrange(1,len(verse_num_elems)+1):
        search_key = 'text '+chapter_abbrev+'-'+chapter+'-'+str(i)
        these_spans = soup.findAll('span',{'class':search_key})
        if len(these_spans) > 1:
            these_spans = [x for x in these_spans if x.findAll('sup',{'class':'versenum'})]
        if len(these_spans) > 1:
            raise Exception("This should never be raised - we can't have two duplicate verses!")
        raw_contents = these_spans[0].contents[1:]
        verse_nums.append(str(i))
        verse_texts.append(utilities_lib.correct_quotes(utilities_lib.rem_lead_end_spaces(''.join([x for x in raw_contents if x.name == None]).encode('utf8'))))
    return (verse_nums[start:end+1], verse_texts[start:end+1])

def nab_home(args):
    if len(args) != 2:
        raise Exception("Invalid number of args entered"+args)
    book = args[0]
    chapter = args[1].split(':')[0]
    start = args[1].split(':')[-1].split('-')[0]
    end = args[1].split(':')[-1].split('-')[-1]
    root_url = 'https://www.biblegateway.com/passage/?search='
    index_url = root_url + book + '+' + chapter + '&version=NABRE'
    return nab_scrape_chapter(index_url,start,end)

def parse_nab(args):
    (verse_nums, verse_texts) = nab_home(args)
    with open("nab_plain.txt",'w') as out_nab:
        out_nab.write(utilities_lib.remove_leading_space(' '.join(verse_texts)))
    with open("nab_lines.txt",'w') as out_nab2:
        for i in xrange(0,len(verse_nums)):
            out_nab2.write(verse_nums[i] + ',' + verse_texts[i] + '\n')