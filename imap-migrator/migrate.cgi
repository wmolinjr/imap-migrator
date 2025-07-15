#!/usr/bin/perl
use strict;
use warnings;

use lib ("..");
use WebminCore;

init_config();

# Load module library
require "./imap-migrator-lib.pl";

our (%in, %text);
ReadParse();

unless (imap_migrator::validate_params(\%in)) {
    error($text{'error_missing_params'});
}

my $source_pass_file = tempname();
write_file_contents($source_pass_file, $in{'source_pass'});
chmod(0600, $source_pass_file);

my $dest_pass_file = tempname();
write_file_contents($dest_pass_file, $in{'dest_pass'});
chmod(0600, $dest_pass_file);

my $log_file = tempname();
# Add initial content to log file for debugging
write_file_contents($log_file, "Log file created at " . localtime() . "\n");

# Check if imapsync is available
unless (imap_migrator::check_imapsync()) {
    write_file_contents($log_file, "$text{'error_imapsync_not_found'}\n");
} else {
    # Build command using library
    my $imapsync_cmd = imap_migrator::build_imapsync_command(\%in, $source_pass_file, $dest_pass_file);

    if ($imapsync_cmd) {
        my $full_shell_cmd = "unset REMOTE_ADDR REMOTE_HOST HTTP_REFERER HTTP_USER_AGENT SERVER_SOFTWARE SERVER_NAME SERVER_PORT HTTP_COOKIE GATEWAY_INTERFACE; $imapsync_cmd ; rm -f $source_pass_file $dest_pass_file";
        $full_shell_cmd =~ s/'/'\\''/g;

        my $cmd = "nohup bash -c '$full_shell_cmd' > $log_file 2>&1 &";
        system($cmd);
    } else {
        write_file_contents($log_file, "$text{'error_command_build'}\n");
    }
}

# Call header without auto-refresh (iframe will handle refreshing)
my $encoded_log_file = urlize($log_file);
ui_print_header(undef, $text{'migrate_title'}, "");

print "<h3>$text{'migrate_status_header'}</h3>";
print "<p>$text{'migrate_status_desc'}</p>";

# Check if we're refreshing an existing migration
if ($in{'log'}) {
    $log_file = un_urlize($in{'log'});

    # Validate log file path
    my $tmp_dir = tempname_dir();
    unless (is_under_directory($tmp_dir, $log_file)) {
        error($text{'error_access_denied'} || "Access denied to log file");
    }

    # Append refresh timestamp to log file for debugging
    if (-e $log_file && -w $log_file) {
        open(my $fh, ">>", $log_file) or warn "Cannot open log file for appending: $!";
        print $fh "Page refreshed at " . localtime() . "\n";
        close($fh);
    }
}

# Display log content in an iframe that auto-refreshes
# Add a timestamp to prevent caching
print "<iframe id=\"log-container\" src=\"log_viewer.cgi?log=$encoded_log_file\" style=\"width: 100%; height: 400px; border: 1px solid #ccc; border-radius: 4px;\"></iframe>";

print ui_link("index.cgi", $text{'migrate_back'});

ui_print_footer(); 
