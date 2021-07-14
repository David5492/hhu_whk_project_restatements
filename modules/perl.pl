#!/usr/bin/perl
use strict;
use warnings;

my $satz = $ARGV[0]
   or die "usage: $0 <input file> <output file>\n";
my $key = $ARGV[1]
   or die "usage: $0 <input file> <output file>\n";
my $number = () = $satz =~ m{$key}gi;
print($number);


# ERKLÄRUNG:
# Perl bekommt hier 2 Parameter übergeben: Satz und Schlüssel. 
# Beides wird als solches eingelesen und es wird die Anzahl der 
# Regex-Matches des Schlüssels im Satz ausgegeben.