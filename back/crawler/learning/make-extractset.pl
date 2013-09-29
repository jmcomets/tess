#!/usr/bin/perl
use JSON qw/decode_json/;
use XML::LibXML;

my $candXpath = "/*/*/*/*//*[self::div or self::p or self::span or self::h1 or self::h2 or self::h3]";

my %features = (
  "json"   => sub {
    my ($cand) = @_;
    my $v = $cand->textContent;
    $v =~ s/[\n\r]+//g;
    my $ln = length($v);
    if($ln < 50 || $ln <= 0) {    
      print "\t$v";
    }
  }
);

my $parser = XML::LibXML->new( recover => 1, verbose=> 0);

my $pn = 1;
foreach my $page (@ARGV) {
  my $nn = 1;
  my $dom = $parser->load_html(location => $page);
  
  my @cands = $dom->findnodes($candXpath);
  foreach my $cand (@cands) {
     my %fmap = ();
     print "$pn";
     foreach $f (keys(%features)) {
        my $fxpath = $features{$f};
        if(ref($fxpath) eq "CODE") {
          &$fxpath($cand);
        } else {
          my $fval = $cand->findvalue($fxpath);
          if($fval eq "") {
            $fval = 'null';
          }
          $fval =~ s/\n\r//g;
          $fval =~ s/\s+/_/g;
          print "\t$f=" . $fval;
          $fmap{$f} = $fval;
        }
     }  
     
     print "\n";
     $nn++;
  }  
  $pn++;
}
