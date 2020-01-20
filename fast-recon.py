#!/usr/bin/env python2
# -*- coding: utf8 -*-

import sys
import time
import random
import argparse

from selenium import webdriver
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.common.exceptions import NoSuchFrameException
from selenium.webdriver.common.keys import Keys

import os

os.environ['MOZ_FORCE_DISABLE_E10S'] = '1'

# If this script no longer fetches any results check the XPath

def parse_args():
    """ Script arguments """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--domain', help='Enter the domain')
    return parser.parse_args()

def start_browser():
    """ Start the browser """
    br = webdriver.Firefox()
    br.implicitly_wait(10)
    return br

def get_ua():
    """ Get a random user agent form this list for each request """
    ua_list = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:29.0) Gecko/20100101 Firefox/29.0',
               'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36',
               'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:28.0) Gecko/20100101 Firefox/28.0']
    ua = random.choice(ua_list)
    return ua

def open_page(br, domain):
    """ Open URLs each in its own tab """
    g_search_base = 'https://www.google.com/webhp?#num=100&start=0&q='
    google_queries = ('+intitle:index.of', # Dir indexing
                      '+ext:xml+|+ext:conf+|+ext:cnf+|+ext:reg+|+ext:inf+|+ext:rdp+|+ext:cfg+|+ext:txt+|+ext:ora+|+ext:ini', # config
                      '+ext:sql+|+ext:dbf+|+ext:mdb', #d db files
                      '+ext:log', # logs
                      '+ext:bkf+|+ext:bkp+|+ext:bak+|+ext:old+|+ext:backup', # backups
                      '+intext:"sql+syntax+near"+|+intext:"syntax+error+has+occurred"+|+intext:"incorrect+syntax+near"+|+intext:\
                      "unexpected+end+of+SQL+command"+|+intext:"Warning:+mysql_connect()"+|+intext:"Warning:+mysql_query()"+|+intext:"Warning:+pg_connect()"', # sql errors
                      '+filetype:asmx+|+inurl:jws?wsdl+|+filetype:jws+|+inurl:asmx?wsdl', # wsdls
                      '+ext:doc+|+ext:docx+|+ext:odt+|+ext:pdf+|+ext:rtf+|+ext:sxw+|+ext:psw+|+ext:ppt+|+ext:pptx+|+ext:pps+|+ext:csv') # docs
    # Make Google queries
    urls = [g_search_base+'site:'+domain+q for q in google_queries]
    # Make pastebin searches
    urls.append(g_search_base+'site:pastebin.com+'+domain)
    # Add quotes around domain for pastebin search
    urls.append(g_search_base+'site:pastebin.com+"'+domain+'"')

    tabHandle = 0
    for u in urls:
        br.switch_to_window(br.window_handles[tabHandle])
        br.get(u)
        # Just grab an element that exists in all pages
        html_elem = br.find_element_by_tag_name('html')
        if u != urls[-1]:
            html_elem.send_keys(Keys.CONTROL + 't')
        tabHandle+=1
	# time.sleep(10) # Optional
    br.switch_to_window(br.window_handles[0])

def main():
    args = parse_args()
    if args.domain.startswith('http'):
        sys.exit('[*] Do: -d example.com  Do not: -d http://example.com')
    br = start_browser()
    if not args.domain:
        sys.exit('[!] Enter a domain to perform the recon on: ./fast-recon.py -d "danmcinerney.org"')
    domain = args.domain
    open_page(br, domain)

main()
