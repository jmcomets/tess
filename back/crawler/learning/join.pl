#!/usr/bin/perl

open($fhOne,$ARGV[0]);
my ($curOne, $keyOne) = nextToken($fhOne);

open($fhTwo,$ARGV[1]);
my ($curTwo, $keyTwo) = nextToken($fhTwo);

my $header = '{ "index" : { "_index" : "object", "_type" : "test" } }';
my $previd = undef;
while($curOne && $curTwo) {
  if($keyOne == $keyTwo) {
    if($curOne !~ m/other/) {
      my ($label) = ($curOne =~ m/([a-z]+)/);
      my ($jid,$content) = ($curTwo =~ m/[0-9]+\s+([0-9]+)\s*(.*)\s*$/);
      if(!defined($previd)) {
        print $header,"\n";;
        print "{ ";
      } else {
        if($previd != $jid) {
          print "}\n$header\n{ ";
        } else {
          print ",";
        }
      }
      $previd = $jid;
#      print "[",$label,"] ", $curOne, " ", $curTwo,"\n";
      print ' "', $label,'": "',$content,'"';
    }
    ($curOne, $keyOne) = nextToken($fhOne);
    ($curTwo, $keyTwo) = nextToken($fhTwo);    
  } else {
    if($keyOne > $keyTwo) {
    } else {
      ($curTwo, $keyTwo) = nextToken($fhTwo);    
    }
  }
}
print "}\n";
  
sub nextToken {
  my ($fh) = @_;
  my $line = <$fh>;
  chomp $line;
  my ($key)  = ($line =~ m/^\s*([0-9]+)/);
  return ($line, $key);
}
