#!/usr/bin/perl
use JSON qw/decode_json/;
use XML::LibXML;

my $candXpath = "//*[self::div or self::p or self::span]";

my %features = (
  "parProd"  => 'number(contains(parent::*/@class,"prod"))',
  "selfProd" => 'number(contains(@class,"prod"))',
  "selfDesc" => 'number(contains(@class,"desc"))',
  "selfCurr" => 'number(contains(text(),"£") or contains(text(),"€"))',
  "selfDesc" => 'number(contains(text(),"Desc") or contains(text(),"desc"))',
  "selfEl"   => 'local-name()'
);

my $pn = 1;
foreach my $page (@ARGV) {
  my $nn = 1;
  my $parser = XML::LibXML->new( recover => 1);
  my $dom = $parser->load_html(location => $page);
  
  my @cands = $dom->findnodes($candXpath);
  foreach my $cand (@cands) {
#     print "=== $pn.$nn ===\n";
     my $label = $cand->getAttribute("data-tess-label");
     if(!$label) {
        $label = "other";
     }
     print $label. "\t";
     foreach $f (keys(%features)) {
        my $fxpath = $features{$f};
        my $fval = $cand->findvalue($fxpath);        
        print "$f=" . $fval . "\t";
     }  
     print "\n";
     $nn++;
  }  
  $pn++;
}

