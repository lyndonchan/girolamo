import codecs, urllib2, utilities_lib
from bs4 import BeautifulSoup
# Expansion library for Douay-Rheims Bible
def dr_scrape(url, start, end):
    start = int(start)-1
    end = int(end)-1
    soup = BeautifulSoup(urllib2.urlopen(url), "html.parser")
    verse_base_elems = soup.findAll('td', {'class' : 'verses'})[0].findAll('p', class_=lambda x: (x != 'note' and x != 'desc'))
    verse_nums = []
    verse_texts = []
    temp_text = ''
    for verse_base_elem in verse_base_elems:
        for base_cont in verse_base_elem.contents:
            if base_cont == u'\n':
                continue
            if base_cont.name == 'a':
                if temp_text:
                    verse_texts.append(temp_text)
                verse_nums.append(utilities_lib.remove_brackets(base_cont.contents[0]).encode('utf8'))
                temp_text = ''
            elif not base_cont.name:
                temp_text += utilities_lib.remove_leading_space(base_cont.encode('utf8')).replace('\n','').replace('\t','')
            elif base_cont.name == 'u':
                temp_text += utilities_lib.remove_leading_space(base_cont.contents[0].encode('utf8')).replace('\n','').replace('\t','')
    verse_texts.append(temp_text)
    if len(verse_nums) != len(verse_texts):
        raise Exception("Unequal lengths:"+str(len(verse_nums))+","+str(len(verse_texts)))
    return (verse_nums[start:end+1], verse_texts[start:end+1])

def dr_home(args):
    if len(args) != 2:
        raise Exception("Invalid number of args entered"+args)
    book = args[0]
    chapter = args[1].split(':')[0]
    start = args[1].split(':')[-1].split('-')[0]
    end = args[1].split(':')[-1].split('-')[-1]
    root_url = 'http://www.drbo.org/'
    soup = BeautifulSoup(urllib2.urlopen(root_url), "html.parser")
    index_urls = []
    chapter_num_lists = []
    chapter_url_lists = []
    a_elems = soup.findAll('a', {'class':'b'})
    book_names = utilities_lib.purify_text(a_elems)
    book_names[-1] = "Apocalypse"
    for a_elem in a_elems:
        index_urls.append(root_url + 'chapter/' + a_elem['href'].split('/')[-1].encode('utf8'))
        chapter_nums = ['1']
        chapter_urls = [index_urls[-1]]
        chapter_soup = BeautifulSoup(urllib2.urlopen(index_urls[-1]), "html.parser")
        chapter_elems = chapter_soup.findAll('td', {'class' : 'chapnum'})[0].findAll('a')   # Doesn't include elem. for chapter 1
        for chapter_elem in chapter_elems:
            chapter_nums.append(utilities_lib.remove_leading_zeroes(chapter_elem.contents[0].encode('utf8')))
            chapter_urls.append(root_url + 'chapter/' + chapter_elem['href'].split('/')[-1].encode('utf8'))
        chapter_num_lists.append(chapter_nums)
        chapter_url_lists.append(chapter_urls)
    request_url = ''

    for book_i in xrange(0,len(book_names)):
        if len(chapter_num_lists[book_i]) != len(chapter_url_lists[book_i]):
            raise Exception("Unequal lengths:"+str(len(chapter_num_lists[book_i]))+","+str(len(chapter_url_lists[book_i])))
        if book_names[book_i] != book:
            continue
        print "Found book: " + book
        for chapter_i in xrange(0,len(chapter_num_lists[book_i])):
            print chapter_num_lists[book_i][chapter_i]
            if chapter_num_lists[book_i][chapter_i] != chapter:
                continue
            print "Found chapter: " + chapter
            request_url = chapter_url_lists[book_i][chapter_i]
            break
        break

    if request_url:
        nums = []
        texts = []
        (nums, texts) = dr_scrape(request_url, start, end)
        return (nums, texts)
    else:
        raise Exception("Requested URL not found")

def parse_dr(args):
    (verse_nums, verse_texts) = dr_home(args)
    with open("dr_plain.txt",'w') as out_dr:
        out_dr.write(utilities_lib.remove_leading_space(' '.join(verse_texts)))
    with open("dr_lines.txt",'w') as out_dr2:
        for i in xrange(0,len(verse_nums)):
            out_dr2.write(verse_nums[i] + ',' + verse_texts[i] + '\n')