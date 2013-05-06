from django.http import *
import os, re, urllib

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
    print "./quickstartsearch db/ \"%s\"" % article.replace('_', ' ')
    for line in os.popen("./quickstartsearch db/ \"%s\"" % article.replace('_', ' ')):
	print line,
	res = re.match(r'^(\d+%)\s\[([^\t]+)\t([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*\]$', line)
	if res != None and res.group(2) == article.replace('_', ' '):
	    cmd = """./show.pl "%s" %s %s %s %s %s %s %s %s %s""" % (
            res.group(2),
            res.group(3), 
            res.group(4),
            res.group(5),
            res.group(6),
            res.group(7),
            res.group(8),
            res.group(9),
            res.group(10),
            res.group(11),                                                                
            )
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
            print "line is ", line
            res = re.match(r'^(\d+%)\s\[([^\t]+)\t([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*\]$', line)
	    if res != None:
		result += "(%s) <A HREF=\"/article/%s\">%s</A><br/>\n" % (res.group(1), res.group(2), res.group(2))
            else:
                print "please check you regexp"
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
            print "line is ", line
            res = re.match(r'^(\d+%)\s\[([^\t]+)\t([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*([-0-9]+)\s*\]$', line)
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
 
