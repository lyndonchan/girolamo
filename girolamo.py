import codecs, urllib2, argparse, bs4
from bs4 import BeautifulSoup

def is_text(elem):
    text = str(elem)
    if '<' in text or '>' in text:
        return False
    return True

def rem_lead_end_spaces(text):
    ret = text
    if text[0] == ' ':
        ret = ret[1:]
    if text[-1] == ' ':
        ret = ret[:-1]
    return ret
    
def remove_leading_space(text):
    if text[0] == ' ':
        return text[1:]
    return text
    
def va_scrape(url, start, end):
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
            if is_text(cont):
                verse_text+=' ' + str(rem_lead_end_spaces(cont).replace('\n',' ').replace('\r',''))
        verse_texts.append(remove_leading_space(verse_text.replace('  ',' ')))
        i += 1
    if len(verse_nums) != len(verse_texts):
        raise Exception("Unequal lengths:"+str(len(verse_nums))+","+str(len(verse_texts)))
    return (verse_nums[start:end+1], verse_texts[start:end+1])

def va_home(args):
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
        if list_elem.findAll('font') and is_text(list_elem.find('font').contents[0]):
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
        (nums, texts) = va_scrape(request_url, start, end)
        return (nums, texts)
    else:
        raise Exception("Requested URL not found")

def ccread_scrape(url, start, end):
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

def ccread_home(args):
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
                book_names.append(remove_leading_space(str(book_elem.findAll('td')[0].find('a').nextSibling)))
            else:
                book_names.append(remove_leading_space(str(book_elem.findAll('td')[0].find('a').contents[0].split('/')[-1])))
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
        (nums, texts) = ccread_scrape(request_url, start, end)
        return (nums, texts)
    else:
        raise Exception("Requested URL not found")
        
def parse_en(args):
    # English
    print "Currently parsing " + args[0] + " " + args[1] + " in English"
    (verse_nums, verse_texts) = va_home(args)
    with open("en_plain.txt",'w') as out_en:
        out_en.write(remove_leading_space(' '.join(verse_texts)))
    with open("en_lines.txt",'w') as out_en2:
        for i in xrange(0,len(verse_nums)):
            out_en2.write(verse_nums[i] + ',' + verse_texts[i] + '\n')

def parse_zh(args):
    # Chinese
    print "Currently parsing " + args[0] + " " + args[1] + " in Chinese"
    (verse_nums, verse_texts) = ccread_home(args)
    with open('zh_plain.txt','w') as out_zh:
        out_zh.write((''.join(verse_texts)).encode('utf8'))
    with open('zh_lines.txt','w') as out_zh2:
        for i in xrange(0,len(verse_nums)):
            out_zh2.write(verse_nums[i] + ',' + verse_texts[i].encode('utf8') + '\n')
            
def split_locn(query):
    if query[0].isdigit():
        lead_num = query[0] + ' '
    else:
        lead_num = query[0]
    for i in xrange(1,len(query)):
        if query[i].isdigit():
            return (lead_num + query[1:i],query[i:])
            
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Welcome to Girolamo 1.0! '\
                                                 'Girolamo will read in a scriptural reference and retrieve it for you in a text file. '\
									'English text is from the Vatican website\'s New American Bible, Chinese text is from the John Duns Scotus Bible Reading '\
									'Promotion Center\'s Studium Biblicum translation')
    parser.add_argument('-l', '--language', help='"E" for English, "C" for Chinese, "B" for English and Chinese')
    parser.add_argument('-q', '--query', help='Type in the Book, Chapter, and Verse range of your Scriptural quotation without spaces, e.g. John3:14-17')
    args = parser.parse_args()
    locn = split_locn(args.query)
    if args.language == 'E':
        parse_en(locn)
    elif args.language == 'C':
        parse_zh(locn)
    elif args.language == 'B':
        parse_en(locn)
        parse_zh(locn)
    else:
        raise Exception("Invalid language choice, please use only 'E', 'C', or 'B'")
    
    