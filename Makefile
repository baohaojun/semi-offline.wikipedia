XMLBZ2 = enwiki-20070802-pages-articles.xml.bz2 


.PHONY:	inform wikipedia split mediawiki

all:	inform

inform:
	@echo Make sure you have Python, Perl, PHP5 and Xapian and Django installed
	@echo after that, put ${XMLBZ2} in the wiki-splits directory and \'make wikipedia\'

wikipedia: quickstartindex quickstartsearch mediawiki split index

split:
	@mkdir -p wiki-splits
	@find wiki-splits -type f -iname rec\*  -exec rm -f '{}' ';'
	@cd wiki-splits && bzip2recover ${XMLBZ2} 
	@echo Perfect, spliting done

mediawiki:  
	@svn co http://fslab.de/svn/wpofflineclient/trunk/mediawiki_sa/ mediawiki_sa || echo Failed to get from svn...
	@cp testparser.php LocalSettings.php mediawiki_sa/
	@cp Math.php mediawiki_sa/includes/Math.php

quickstartindex: quickstartindex.cc
	@g++ -o $@ $^ -lxapian

quickstartsearch: quickstartsearch.cc
	@g++ -o $@ $^ -lxapian

index:
	@rm -rf db/
	@cd wiki-splits && rm -rf db && for i in rec*.bz2 ; do echo \#$$i ; bzcat $$i | grep '<title' | perl -ne 'm/<title>([^<]+)<\/title>/ && print $$1."\n";' ; done | ../quickstartindex
	@mv wiki-splits/db ./
	@echo Index built - we are done
	@echo To run your local wikipedia, just
	@echo
	@echo cd mywiki
	@echo python manage.py runserver
	@echo
	@echo ... and point your browser to http://localhost:8000/
