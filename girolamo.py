import argparse, urllib2, utilities_lib
from bs4 import BeautifulSoup
# Import Bible translation expansion libraries
from ..translations import nab_expansion, njv_expansion, dr_expansion, sbt_expansion, sbs_expansion, jw_expansion

def split_locn(query):
    if query[0].isdigit():
        lead_num = query[0] + ' '
    else:
        lead_num = query[0]
    for i in xrange(1,len(query)):
        if query[i].isdigit():
            return (lead_num + query[1:i],query[i:])

def split_codes(query):
    return query.split(',')

def invalid_code_request(requests, valids):
    for request in requests:
        if request not in valids:
            return True

def sandbox():
    str = "'"
    # Strange quotation scheme in NJV - will look into this later

if __name__ == "__main__":
    # sandbox()
    # exit()
    parser = argparse.ArgumentParser(description='Welcome to Girolamo 1.0! '\
                                                 'Girolamo will read in a scriptural reference and retrieve it for you in a text file.')
    parser.add_argument('-t', '--translation', help='Type in a comma-separated list of the requested Bible translation code(s): '\
                                                    '"NAB" for the New American Bible (English), "NJV" for New Jerusalem Bible (English), '\
                                                    '"DR" for Douay-Rheims Bible (English), "SBT" for Studium Biblicum Bible (Trad. Chinese), '\
                                                    '"SBS" for Studium Biblicum Bible (Simp. Chinese), "JW" for John C.H. Wu translation (Class. Chinese)')
    parser.add_argument('-q', '--query', help='Type in the Book, Chapter, and Verse range of your Scriptural quotation without spaces, e.g. John3:14-17')
    args = parser.parse_args()
    locn = split_locn(args.query)
    requested_translations = split_codes(args.translation)
    valid_translation_codes = ['NAB','NJV','DR','SBT','SBS','JW']


    if invalid_code_request(requested_translations, valid_translation_codes):
        raise Exception("Invalid translation choice, please refer to the translation codes supported by typing 'python girolamo.py -h'")

    if 'NAB' in requested_translations:
        print "Girolamo is currently retrieving " + locn[0] + " " + locn[1] + " from the New American Bible (English)"
        nab_expansion.parse_nab(locn)
    if 'NJV' in requested_translations:
        print "Girolamo is currently retrieving " + locn[0] + " " + locn[1] + " from the New Jersulem Bible (English)"
        njv_expansion.parse_njv(locn)
    if 'DR' in requested_translations:
        print "Girolamo is currently retrieving " + locn[0] + " " + locn[1] + " from the Douay-Rheims Bible (English)"
        dr_expansion.parse_dr(locn)
    if 'SBT' in requested_translations:
        print "Girolamo is currently retrieving " + locn[0] + " " + locn[1] + " from the Studium Biblicum Bible (Trad. Chinese)"
        sbt_expansion.parse_sbt(locn)
    if 'SBS' in requested_translations:
        print "Girolamo currently doesn't support Studium Biblicum Bible (Simp. Chinese)"
        exit()
        #sbs_expansion.parse_sbs(locn)
    if 'JW' in requested_translations:
        print "Girolamo currently doesn't support John C.H. Wu Bible (Class. Chinese)"
        exit()
        #jw_expansion.parse_jw(locn)

    
    