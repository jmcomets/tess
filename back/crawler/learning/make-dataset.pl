#!/usr/bin/perl
use JSON qw/decode_json/;
use XML::LibXML;

my $candXpath = "/*/*/*/*//*[self::div or self::p or self::span]";

my %features = (
  "parProd"   => 'number(contains(parent::*/@class,"prod"))',
  "ancProd"   => 'count(ancestor::*[contains(@class,"prod")])',
  "ancDesc"   => 'count(ancestor::*[contains(@class,"desc")])',
  "selfProd"  => 'number(contains(@class,"prod"))',
  "selfDesc"  => 'number(contains(@class,"desc"))',
  "selfCurr"  => 'number(contains(text(),"£") or contains(text(),"€") or contains(text(), "EUR"))',
  "selfDesc"  => 'number(contains(text(),"Desc") or contains(text(),"desc"))',
  "selfEl"    => 'local-name(.)',
  "parEl"     => 'local-name(..)',
  "selfIP"    => '@itemprop',
  "selfClass" => '@class',
  "parClass"  => '../@class',
  "selfDepth" => 'count(ancestor::*)',
  "selfDesc"  => 'count(descendant::*)',
  "gpClass"   => sub {
     my ($cand) = @_;
     my @n = $cand->findnodes('../../@class');
     my $i = 0;
     foreach my $n (@n) {
        foreach my $c (split(/\s+/,$n->value())) {
           if($c ne "") {
             $i++;
             print "\t" . "gpClass[" .$i . "]=",$c;
           }
        }
     }
  },
);

my @links = (
  ["selfProd","parProd"],
  ["parProd","ancProd"],
  ["selfClass","parClass"],
  ["selfEl","parEl"]
);

my $parser = XML::LibXML->new( recover => 1, verbose=> 0);

my $pn = 1;
foreach my $page (@ARGV) {
  my $nn = 1;
  my $dom = $parser->load_html(location => $page);
  
  my @cands = $dom->findnodes($candXpath);
  foreach my $cand (@cands) {
     my $label = $cand->getAttribute("data-tess-label");
     if(!$label) {
        $label = "other";
     }
     print $label;
     my %fmap = ();
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
     
     foreach $a (@links) {
       print "\t", join('|',@{$a}),"=", join("|",map {$fmap{$_}} @{$a}); 
     }
     print "\n";
     $nn++;
  }  
  $pn++;
}