"""
@auto iaglr_sess.py - one page program

Terry Brown, terrynbrown@gmail.com, Fri May 12 09:11:50 2017
"""

import json
import os
import re
import sys

from collections import namedtuple, defaultdict

import requests

from lxml import etree

json_state_file = "persistent.json"
if not os.path.exists(json_state_file):
    json.dump({'res':{}}, open(json_state_file, 'w'))
shelf = json.load(open(json_state_file))

def get_url(url):
    if url in shelf['res']:
        return shelf['res'][url]
    else:
        print("Fetching %s" % url)
        return shelf['res'].setdefault(url, requests.get(url).text)

def main():

    print(
        "<h1>Disclaimer</h1>\n"
        "<p>This is an unofficial snapshot of the IAGLR schedule as of\n"
        "Fri May 12 2017, check the official documents to verify</p>\n"
    )

    parser = etree.HTMLParser()
    base = "http://iaglr.org/conference/abstracts/"
    root = get_url(base+"listsession.php")
    session_ids = re.findall(r'href="./pub_sesspres_view.php\?session_id=(\d+)', root)
    for session_id in session_ids:
        details = get_url(base+"session_details.php?session_id=%s" % session_id)
        details = etree.fromstring(details, parser=parser)
        details.xpath("//h1")[0].text = 'Session %s' % session_id
        details = details.xpath("//*[@id='main']")[0]
        print(etree.tostring(details))
        listing = get_url(base+"pub_sesspres_view.php?session_id=%s" % session_id)
        listing = etree.fromstring(listing, parser=parser)
        for href in listing.xpath("//a"):
            href.set('href', base+href.get('href'))
        
        listing = listing.xpath("//*[@class='conftab']")[0]
        print(etree.tostring(listing))

if __name__ == '__main__':

    try:
        main()
    finally:
        json.dump(shelf, open(json_state_file, 'w'), indent=4)

