#!/usr/bin/perl

use Text::CSV;
use Data::Dumper;

my @rows;
print "<svg xmlns='http://www.w3.org/2000/svg' version='1.1'>\n";

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
	my %data = map { split(/:/) } @cells;
	my $xb = 0;
	foreach my $h (@headers) {
		my $s = $data{$h};
		if($s eq "") {
			$s = 0;
		}
		my $x = $xb * 6;
		print <<END;
<rect x='$x' y='$y'  width='5' height="$s" style="fill: $color"></rect>
END
    $xb++;
	}
	$yb++;
}
close $fh;
print "</svg>\n";