#!/usr/bin/perl
use JSON qw/decode_json/;

use XML::LibXML;

my $rStr = "";
open(JSON,$ARGV[0]);
while(<JSON>) {
  $rStr .= $_;
}
close(JSON);

my $wrapper = decode_json($rStr);
my $rules = $wrapper->{"rules"};

my $page = $ARGV[1];
my $parser = XML::LibXML->new( recover => 1);
my $dom = $parser->load_html(location => $page);

foreach my $r (keys($rules)) {
  my $x = $rules->{$r};
  if($x) {
    my $n = $dom->findvalue($x);
    print "$r => ". $n . "\n";
  }
}
