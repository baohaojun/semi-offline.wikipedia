XMLBZ2 = enwiki-20070802-pages-articles.xml.bz2 


.PHONY:	inform wikipedia

all:	inform

inform:
	@echo Make sure you have Python, Perl, PHP5 and Xapian and Django installed
	@echo after that, put ${XMLBZ2} in the wiki-splits directory and \'make wikipedia\'

wikipedia: quickstartindex quickstartsearch index

quickstartindex: quickstartindex.cc
	@g++ -o $@ $^ -lxapian

quickstartsearch: quickstartsearch.cc
	@g++ -o $@ $^ -lxapian

index: quickstartindex
	@mkdir -p ~/wikipedia/db
	@rm -f db
	@ln -s ~/wikipedia/db . 
	@cat ~/wikipedia/enwiki-latest-pages-articles.idx|./quickstartindex
	@echo Index built - we are done
	@echo To run your local wikipedia, just
	@echo
	@echo cd mywiki
	@echo python manage.py runserver
	@echo
	@echo ... and point your browser to http://localhost:8000/
