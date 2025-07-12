#!/usr/bin/perl
use strict;
use warnings;

use lib ("..");
use WebminCore;

our (%in, %text);
ReadParse();
init_config();

my $log_file = $in{'log'};

# Add headers to avoid cache and CORS issues
print "Content-type: text/plain; charset=utf-8\n";
print "Cache-Control: no-cache, no-store, must-revalidate\n";
print "Pragma: no-cache\n";
print "Expires: 0\n";
print "Access-Control-Allow-Origin: *\n";
print "Access-Control-Allow-Methods: GET\n";
print "Access-Control-Allow-Headers: Content-Type\n\n";

my $tmp_dir = tempname_dir();
unless (is_under_directory($tmp_dir, $log_file)) {
    print "$text{'error_access_denied'}\n";
    exit;
}

if (-e $log_file) {
    my $log_content = read_file_contents($log_file);
    print $log_content;
} else {
    print "$text{'error_waiting_migration'}";
}

exit; 