# -*- coding: utf-8 -*-
import time
import urllib2
import re
import gzip
import json
from StringIO import StringIO
from lxml import etree
from page import get_page, quote_safe
import HTMLParser
import re
import json
import sys

hparser = HTMLParser.HTMLParser()

def parse_list(text):
    try:
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(text), parser)
    except:
        raise    

    itemlists = tree.xpath('.//div[@class="itemtitle"]/a')
    if itemlists == []: return
    
    return itemlists[0].get('href')
    
    
def parse_no_catlog(text):
    try:
        parser = etree.HTMLParser()
        tree = etree.parse(StringIO(text), parser)
    except:
        raise
    trs = tree.xpath('.//div[@id="details2"]/table/tr')
    #print trs
    res = {}
    
    for tr in trs:
        tds = tr.xpath('./td')
        if len(tds) != 2: continue
        #html转义字符处理
        k = hparser.unescape(''.join(list(tds[0].itertext()))).strip()
        v = hparser.unescape(''.join(list(tds[1].itertext()))).strip()
        if k == '' or v == '': continue
        print k, v
        res[k] = v
    return res

def parse_catlog(text):
    content = re.search('aa\((.*?)\)', text)
    if content == None: return
    content = content.group(1)
    try:
        content = json.loads(content)
        catlog = content.get('result', {}).get('catlog', '')
    except:
        return
    return catlog
    
if __name__ == '__main__':
    search_wd = 'google'
    url = 'http://202.116.64.108:8991/F/-?func=find-b&find_code=WRD&request=%s&local_base=ZSU01' % quote_safe(search_wd)
    text = get_page(url)
    url = parse_list(text)
    if url == None:
        print 'No result for %s' % search_wd
        sys.exit()
    print 'top one search result url: ', url
    text = get_page(url)
    res = parse_no_catlog(text)
    if res.get('ISBN') != None:
        ts = int(time.time() * 1000)
        url = 'http://202.112.150.126/indexc.php?client=sysu&isbn=%s&callback=aa&t=%d' % (quote_safe(res['ISBN']), ts)
        text = get_page(url)
        catlog = parse_catlog(text)
        if catlog not in ['', None]:
            res[u'图书目录'] = catlog 
    print res
