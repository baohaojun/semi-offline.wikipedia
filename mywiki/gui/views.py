from django.http import *
import os, re, urllib

def index(request):
    return article(request, "Wikipedia")

def article(request, article):
    article = article.encode('utf-8')
    if article.endswith("/"):
	article = article[:-1]
    result = "Not found"
    print "Searching for exact article", article
    print "./quickstartsearch db/ \"%s\"" % article.lower().replace('_', ' ')
    for line in os.popen("./quickstartsearch db/ \"%s\"" % article.lower().replace('_', ' ')):
	print line,
	res = re.match(r'^(\d+%)\s\[(rec[^:]+):(.+?)\]$', line)
	if res != None and res.group(3) == article.replace('_', ' '):
	    cmd = "./show.pl \"../wiki-splits/%s\" \"%s\"" % (res.group(2), res.group(3))
	    print cmd
	    os.system(cmd)
	    result = open("/var/tmp/result.html").read() 
	    print "Gotcha"
	    break
    else:
	return search(request, article)
    return HttpResponse(result)

def search(request, article):
    print "Searching for article", article
    lines = []
    print "./quickstartsearch db/ \"%s\"" % article.lower().replace('_', ' ')
    for line in os.popen("./quickstartsearch db/ \"%s\"" % article.lower().replace('_', ' ')):
	print line,
	lines.append(line[:])
    if len(lines) == 0:
	result = '<html><head><title>Wikipedia has nothing about this.</title>'
	result += '</head><body>Wikipedia has nothing about this.<br/>'
	result += 'You can keyword search about it  <a href="/keyword/%s">here</a>' % article
	result += '</body></html>'
    else:
	result = "<html><head><title>Choose one</title></head><body><h1>Choose one of the options below</h1>\n"
	for line in lines:
	    res = re.match(r'^(\d+%)\s\[(rec[^:]+):(.+?)\]$', line)
	    if res != None:
		result += "(%s) <A HREF=\"/article/%s\">%s</A><br/>\n" % (res.group(1), res.group(3), res.group(3))
	result += "</body></html>"
    return HttpResponse(result)

def keyword(request, article):
    print "Searching for keywords of article", article
    lines = []
    cmd = "./quickstartsearch db/ "
    for i in article.lower().replace('_', ' ').split():
	cmd += '"%s" ' % i
    print cmd
    for line in os.popen(cmd):
	print line,
	lines.append(line[:])
    if len(lines) == 0:
	result = '<html><head><title>No exact match for this article name found in Wikipedia (try a keyword search).</title>'
	result += '</body></html>'
    else:
	result = "<html><head><title>Choose one</title></head><body><h1>Choose one of the options below</h1>\n"
	for line in lines:
	    res = re.match(r'^(\d+%)\s\[(rec[^:]+):(.+?)\]$', line)
	    if res != None:
		result += "(%s) <A HREF=\"/article/%s/\">%s</A><br/>\n" % (res.group(1), urllib.quote(res.group(3)), res.group(3))
	result += "</body></html>"
    return HttpResponse(result)

def searchbar(request):
    searchData = request.GET['data'].encode('utf-8')
    return keyword(request, searchData)
