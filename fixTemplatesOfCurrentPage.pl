#!/usr/bin/perl -w
use strict;
use Digest::MD5;

sub LooseEntities {
    $_ = $_[0];
    s/&lt;/</g;
    s/&gt;/>/g;
    s/&apos;/'/g;
    s/&quot;/"/g;
    s/&amp;/\&/g;
    return $_;
}

my %templates;
open RES, "/var/tmp/result.html" || die "No page currently rendered\n";
while(<RES>) {
    if (/"\/(article\/Template:[^"]*)".*title="Template:([^"]*)"/) {
	$templates{$2}=$1;
    }
}
close RES;
for my $template (keys %templates) {
    print "Fixing $template...\n";
    if ($template =~ m/^Pp-/i) {
	print "Not allowed\n";
	next;
    }

    my $md5s = Digest::MD5::md5_hex(lc($template));
    if ( ! -e "./mediawiki_sa/templates/$md5s.mwt") {
	#system("wget -O /var/tmp/fixup.html http://localhost:8000/article/Template:".$template."/");
	my $url = $templates{$template};
	system("wget -O /var/tmp/fixup.html http://localhost:8000/$url/ >/dev/null 2>&1");
	if ($? == -1) {
        }
        elsif ($? & 127) {
        }
        else {
            if (0 == ($? >> 8)) {
		open HTML, "/var/tmp/fixup.html" || die "What! No HTML generated!\n";
		my $foundBadMsg = 0;
		while(<HTML>) {
		    if (/<h1>Choose one of the options below/) {
			$foundBadMsg = 1;
			last;
		    } elsif (/head><body>Wikipedia has nothing about this/) {
			$foundBadMsg = 1;
			last;
		    } elsif (/Warning.*::require.*failed to open stream/) {
			$foundBadMsg = 1;
			last;
		    }
		}
		close HTML;
		if ($foundBadMsg == 0) {
		    open DATA, "tail +2 /var/tmp/result |";
		    open TEMPLATE, ">./mediawiki_sa/templates/$md5s.mwt";   
		    while(<DATA>) {
			print TEMPLATE LooseEntities($_);
		    }
		    close DATA;
		    close TEMPLATE;
		} else {
		    print "Don't know how to fix $template\n";
		}
	    }
        }
    }
}
