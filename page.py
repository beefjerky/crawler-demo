# -*- coding: utf-8 -*-
import urllib2
import gzip
from StringIO import StringIO
from urllib import quote_plus

def decode_safe(s):
    if type(s) == unicode: return s
    try: return s.decode('gbk')
    except: pass
    try: return s.decode('gb18030')
    except: pass
    try: return s.decode('utf-8')
    except: pass

def quote_safe(txt):
    if type(txt) == unicode:
        return quote_plus(txt.encode('utf-8'))
    else:
        return quote_plus(txt)

def get_page(url):
    for i in xrange(5):
        request = urllib2.Request(url)
        request.add_header('Accept-Encoding', 'gzip,deflate,sdch')
        request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8')
        request.add_header('Cache-Control', 'max-age=0')
        request.add_header('Accept-Language', 'zh-CN,en-US,en,zh;q=0.8')    
        request.add_header('Connection', 'keep-alive') 
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.94 Safari/537.36') 
        try:         
            rsp = urllib2.urlopen(request, timeout=10)
            rsp_text = rsp.read()
        except Exception, e:
            print str(e)
            continue
        if rsp.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(rsp_text)
            f = gzip.GzipFile(fileobj=buf)
            buf = decode_safe(f.read())
            text = buf
        else:
            text = rsp_text
        
        return text
