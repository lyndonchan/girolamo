import codecs, urllib2,utilities_lib
from bs4 import BeautifulSoup
# Expansion library for John C.H. Wu Bible (Class. Chinese)
def jw_home(args):
    if len(args) != 2:
        raise Exception("Invalid number of args entered")
    book = args[0]
    chapter = args[1].split(':')[0]
    start = int(args[1].split(':')[-1].split('-')[0])
    end = int(args[1].split(':')[-1].split('-')[-1])
    nt_books = ['Matthew','Mark','Luke','John','Acts','Romans','1 Corinthians','2 Corinthians',
                'Galatians','Ephesians','Philippians','Colossians','1 Thessalonians','2 Thessalonians',
                '1 Timothy','2 Timothy','Titus','Philemon','Hebrews','James','1 Peter','2 Peter',
                '1 John','2 John','3 John','Jude','Revelation']
    if book in nt_books or book == 'Psalms':
        root_url = 'http://jesus.tw'
    else:
        raise Exception("You requested '"+book+"' but John C.H. Wu Bible only includes Psalms and the New Testament")
    chapter_url = root_url + '/' + book.replace(' ','_') + '/' + chapter
    soup = BeautifulSoup(urllib2.urlopen(chapter_url), "html.parser")
    try:
        verse_elems = soup.findAll('table',{'class':'bible'})[0].findAll('tr')
    except:
        raise Exception("Error loading your requested page: "+chapter_url)
    verse_nums = [str(x) for x in xrange(1,len(verse_elems)+1)]
    verse_texts = []
    i = 1
    for verse_elem in verse_elems:
        verse_texts.append(utilities_lib.purify_contents(verse_elem.findAll('td')[1].contents).replace('\n',''))
        i += 1
    return (verse_nums[start:end+1], verse_texts[start:end+1])

def parse_jw(args):
    # John C.H. Wu Bible (Class. Chinese)
    (verse_nums, verse_texts) = jw_home(args)
    with open('jw_plain.txt','w') as out_jw:
        out_jw.write((''.join(verse_texts)))
    with open('jw_lines.txt','w') as out_jw2:
        for i in xrange(0,len(verse_nums)):
            out_jw2.write(verse_nums[i] + ',' + verse_texts[i] + '\n')