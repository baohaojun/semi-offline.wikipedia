from django.http import *
import os, re, urllib, subprocess

def index(request):
    return article(request, "Wikipedia")

def article(request, article):
    article = article.encode('utf-8')
    if article.endswith("/"):
        article = article[:-1]
    if article.endswith("/&redlink=1"):
        article = article[:-11]
    result = "Not found"
    print "Searching for exact article", article
    print "wiki-sorted-idx-title-query \"%s\"" % article.replace('_', ' ')
    for line in subprocess.Popen(("wiki-sorted-idx-title-query", article.replace('_', ' ')), stdout=subprocess.PIPE).communicate()[0].split('\n'):
        print line,
        res = re.match(r'^(\d+%)\s\[([^\t]+)\t' + r'(0x[0-9A-Fa-f]+)\s+' * 9 + r'\]$', line)
        if res != None and res.group(2) == article.replace('_', ' '):
            cmd = ["./show.pl"]
            for i in range(2, 12):
                cmd.append(res.group(i))
            
            print cmd
            subprocess.Popen(cmd).communicate()
            result = open("/var/tmp/result.html").read() 
            break
    else:
        return search(request, article)
    return HttpResponse(result)

def search(request, article):
    print "Searching for article", article
    lines = []
    cmd = ['wiki-query-keywords']
    cmd.extend(article.replace('_', ' ').split())
    print cmd
    for line in subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].split('\n'):
        if line:
            lines.append(line[:]) 
    if len(lines) == 0:
        result = '<html><head><title>Wikipedia has nothing about this.</title>'
        result += '</head><body>Wikipedia has nothing about this.<br/>'
        result += 'You can keyword search about it  <a href="/keyword/%s">here</a>' % article
        result += '</body></html>'
    else:
        result = "<html><head><title>Choose one</title></head><body><h1>Choose one of the options below</h1>\n"
        for line in lines:
            print "line is ", line
            res = re.match(r'^(\d+%)\s\[([^\t]+)\t' + r'(0x[0-9A-Fa-f]+)\s+' * 9 + r'\]$', line)
            if res != None:
                result += "(%s) <A HREF=\"/article/%s\">%s</A><br/>\n" % (res.group(1), urllib.quote(res.group(2)), res.group(2))
                print "regexp is matched ok:"
            else:
                print "please check your regexp"
        result += "</body></html>"
    return HttpResponse(result)

def keyword(request, article):
    print "Searching for keywords of article", article
    lines = []
    cmd = ["wiki-query-keywords"]
    for i in article.replace('_', ' ').split():
        cmd.append(i)
    print cmd
    for line in subprocess.Popen(cmd, stdout=subprocess.PIPE).communicate()[0].split('\n'):
        print line,
        lines.append(line[:])
    if len(lines) == 0:
        result = '<html><head><title>No exact match for this article name found in Wikipedia (try a keyword search).</title>'
        result += '</body></html>'
    else:
        result = "<html><head><title>Choose one</title></head><body><h1>Choose one of the options below</h1>\n"
        for line in lines:
            print "line is ", line
            res = re.match(r'^(\d+%)\s\[([^\t]+)\t' + r'(0x[0-9A-Fa-f]+)\s+' * 9 + r'\]$', line)
            if res != None:
                result += "(%s) <A HREF=\"/article/%s/\">%s</A><br/>\n" % (res.group(1), urllib.quote(res.group(2)), res.group(2))
            else:
                print "res is null"
        result += "</body></html>"
    return HttpResponse(result)

def searchbar(request):
    searchData = request.GET['data'].encode('utf-8')
    return keyword(request, searchData)
# Local Variables: #
# tab-width: 4 #
# python-indent: 4 #
# End: #
 
