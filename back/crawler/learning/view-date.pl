#!/usr/bin/perl

use Text::CSV;
use Data::Dumper;

my @rows;

open(HEADERS,$ARGV[0]);
my @headers = split(/,/,<HEADERS>);
close(HEADERS);

open my $fh, "<:encoding(utf8)", $ARGV[1] or die "$ARGV[0]: $!";
my $yb = 0;
while ( my $row = <$fh>) {
	$y = $yb * 80;
	chomp $row;
	my @cells = split(/,/,$row);
	shift @cells;
	my $class = $cells[0];
	shift @cells;
	my $color = $class ? "green" : "red";
	
	
}
close $fh;