#!/usr/bin/perl
use strict;
use warnings;

use lib ("..");
use WebminCore;

our (%in, %text);
ReadParse();
init_config();

# Get log file path from parameters
my $log_file = $in{'log'};

# Validate log file path
my $tmp_dir = tempname_dir();
unless ($log_file && is_under_directory($tmp_dir, $log_file)) {
    error($text{'error_access_denied'} || "Access denied to log file");
}

# Set headers
print "Content-Type: text/html\n";
print "Cache-Control: no-cache, no-store, must-revalidate\n";
print "Pragma: no-cache\n";
print "Expires: 0\n";

# Check if migration is complete before setting refresh header
my $refresh_interval = 3; # Refresh every 3 seconds
my $is_migration_complete = 0;

if (-e $log_file) {
    # Check if the log file contains the completion marker
    my $log_content = read_file_contents($log_file);
    if ($log_content =~ /Exiting with return value/) {
        $is_migration_complete = 1;
    }
}

# Only add refresh header if migration is not complete
unless ($is_migration_complete) {
    print "Refresh: $refresh_interval\n";
}
print "\n";

# Start HTML output
print "<!DOCTYPE html>\n";
print "<html>\n";
print "<head>\n";
print "<meta charset=\"utf-8\">\n";
print "<title>Log Viewer</title>\n";
print "<link rel=\"stylesheet\" type=\"text/css\" href=\"assets/terminal.min.css\">\n";
print "</head>\n";
print "<body>\n";

# Add terminal header
print "<div class=\"terminal-header\">";
print "<div class=\"terminal-title\"><span class=\"terminal-text\">" . ($text{'imap_migration_log'} || "IMAP Migration Log") . " - </span>" . localtime() . "</div>";
print "</div>";

# Display log content
print "<pre>";
if (-e $log_file) {
    # Read the log file content
    my $log_content = "";

    # Try to use tail command if available for better performance with large logs
    my $tail_cmd = "tail -n 1000 " . quotemeta($log_file);
    my $tail_output = `$tail_cmd 2>/dev/null`;

    if ($? == 0 && $tail_output) {
        $log_content = $tail_output;
    } else {
        # Fallback to reading the entire file
        $log_content = read_file_contents($log_file);
    }

    # Convert special characters to HTML entities
    $log_content =~ s/&/&amp;/g;
    $log_content =~ s/</&lt;/g;
    $log_content =~ s/>/&gt;/g;

    # Split the log content into lines for processing
    my @lines = split(/\n/, $log_content);
    my @processed_lines;

    foreach my $line (@lines) {
        if ($line =~ /^DEBUG:/) {
            # For DEBUG lines, only apply the DEBUG pattern and skip all other patterns
            $line =~ s/^(DEBUG:.*)$/<span class="info">$1<\/span>/;
            push @processed_lines, $line;
        } elsif ($line =~ /^\+\+\+\+ /) {
            # For section header lines, only apply the section header pattern and skip all other patterns
            $line =~ s/^(\+\+\+\+ .+)$/<span class="section-header">$1<\/span>/;
            push @processed_lines, $line;
        } elsif ($line =~ /^(Host2-Host1\s+)(\d+)(\s+)(\d+)(\s+)(\d+)(.*)$/){
            $line = "$1<span class=\"number\">$2</span>$3<span class=\"message-count\">$4</span>$5<span class=\"biggest\">$6</span>$7";
            push @processed_lines, $line;
        } else {

            # Progress indicators (ETA lines)
            $line =~ s/(ETA:.+)/<span class="eta">$1<\/span>/g;

            # Timestamps
            $line =~ s/(Sunday|Monday|Tuesday|Wednesday|Thursday|Friday|Saturday) (\d+ [A-Za-z]+ \d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})/<span class="timestamp">$1 $2<\/span>/g;

            # Box Sizes
            $line =~ s/(Size:\s+)(\d+)/$1<span class="number">$2<\/span>/g;
            $line =~ s/(Messages:\s+)(\d+)/$1<span class="message-count">$2<\/span>/g;
            $line =~ s/(Biggest:\s+)(\d+)/$1<span class="biggest">$2<\/span>/g;

            # Command arguments
            $line =~ s/(--[a-zA-Z0-9_-]+)/<span class="command-arg">$1<\/span>/g;

            # Numbers with slashes (like 10/10)
            $line =~ s/(\s|^)(\d+)(\/)(\d+)(\s|$)/$1<span class="number">$2<\/span><span class="bracket">$3<\/span><span class="number">$4<\/span>$5/g;

            $line =~ s/(\s|>|\()(\d+(?:\.\d+)?%?)(\s|\)|$)/$1<span class="number">$2<\/span>$3/g;
            $line =~ s/\[([^\]]*)\]/<span class="bracket">[<\/span><span class="folder">$1<\/span><span class="bracket">]<\/span>/g;
            $line =~ s/\(([^\)]*)\)/<span class="bracket">(<\/span>$1<span class="bracket">)<\/span>/g;

            # Statistics sections
            $line =~ s/^(Transfer (started|ended|time).+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Messages (transferred|skipped|found|deleted|void).+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Total bytes.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Message rate.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Average bandwidth.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Reconnections.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Memory consumption.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Load end.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Folders (synced).+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(CPU time.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Biggest message.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Memory\/biggest.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Start difference.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Final difference.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(There is.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(The sync.+)$/<span class="stat">$1<\/span>/g;
            $line =~ s/^(Detected.+errors)$/<span class="stat">$1<\/span>/g;

            push @processed_lines, $line;
        }
    }

    # Join the processed lines back together
    $log_content = join("\n", @processed_lines);

    # Process each line to add appropriate CSS classes based on content
    my @lines_with_classes;
    foreach my $line (split(/\n/, $log_content)) {
        if ($line =~ /^Host2-Host1/) {
            push @lines_with_classes, "<p class=\"host_1_2\">$line</p>";
        } elsif ($line =~ /^Host1/) {
            push @lines_with_classes, "<p class=\"host_1\">$line</p>";
        } elsif ($line =~ /^Host2/) {
            push @lines_with_classes, "<p class=\"host_2\">$line</p>";
        } elsif ($line =~ /^Err /) {
            push @lines_with_classes, "<p class=\"error\">$line</p>";
        } else {
            push @lines_with_classes, "<p class=\"single_line\">$line</p>";
        }
    }

    # Join the lines with classes
    $log_content = join("", @lines_with_classes);

    # Remove empty paragraphs
    $log_content =~ s/<p class="[^"]*"><\/p>//g;

    print $log_content;

    # Add a message if migration is complete
    if ($log_content =~ /Exiting with return value/) {
        print "<p class=\"success\"><b>" . ($text{'migration_complete'} || "Migration Complete.") . "</b></p>";
    } else {
        # Add a refreshing indicator with a blinking cursor
        print "<p class=\"info\"><i>--- " . ($text{'log_refreshing'} || "Log refreshing automatically every $refresh_interval seconds...") . " ---</i><span class=\"cursor\"></span></p>";
    }
} else {
    # Add a terminal prompt and starting message
    print "<p class=\"info\">" . ($text{'migration_starting'} || "Migration starting...") . "<span class=\"cursor\"></span></p>";
}
print "</pre>";

# Add script to scroll to bottom
print "<script src=\"assets/terminal.min.js\"></script>\n";

print "</body>\n";
print "</html>\n";

exit;
