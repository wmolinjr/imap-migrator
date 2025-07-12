#!/usr/bin/perl
use strict;
use warnings;

package imap_migrator;

# Function to find executable
sub find_executable {
    my ($cmd) = @_;
    my @paths = qw(/bin /usr/bin /sbin /usr/sbin /usr/local/bin);
    foreach my $path (@paths) {
        if (-x "$path/$cmd") { return "$path/$cmd"; }
    }
    return undef;
}

# Function to check if imapsync is installed
sub check_imapsync {
    my $imapsync_path = find_executable("imapsync");
    return $imapsync_path ? 1 : 0;
}

# Function to validate parameters
sub validate_params {
    my ($in) = @_;
    
    # Validate only required parameters
    unless ($in->{'source_host'} && $in->{'source_user'} && $in->{'source_pass'} &&
            $in->{'dest_host'} && $in->{'dest_user'} && $in->{'dest_pass'}) {
        return 0;
    }
    
    return 1;
}

# Function to build imapsync command
sub build_imapsync_command {
    my ($in, $source_pass_file, $dest_pass_file) = @_;
    
    my $imapsync_path = find_executable("imapsync");
    return undef unless $imapsync_path;
    
    my $cmd = "$imapsync_path \\
        --host1 $in->{'source_host'} --user1 $in->{'source_user'} --passfile1 $source_pass_file \\
        --host2 $in->{'dest_host'}   --user2 $in->{'dest_user'}   --passfile2 $dest_pass_file";
    
    # Add SSL/TLS parameters
    if ($in->{'source_ssl'} eq 'ssl') {
        $cmd .= " --ssl1";
    } elsif ($in->{'source_ssl'} eq 'tls') {
        $cmd .= " --tls1";
    }
    
    if ($in->{'dest_ssl'} eq 'ssl') {
        $cmd .= " --ssl2";
    } elsif ($in->{'dest_ssl'} eq 'tls') {
        $cmd .= " --tls2";
    }
    
    # Basic parameters
    $cmd .= " --automap --syncinternaldates --skipheader '^(Received|Date|From|To|Subject)\$'";
    
    # Folder parameters
    if ($in->{'folders_include'}) {
        $cmd .= " --include " . quotemeta($in->{'folders_include'});
    }
    if ($in->{'folders_exclude'}) {
        $cmd .= " --exclude " . quotemeta($in->{'folders_exclude'});
    }
    
    # Advanced parameters
    if ($in->{'max_size'}) {
        my $max_size_mb = $in->{'max_size'} * 1024 * 1024;
        $cmd .= " --maxsize " . quotemeta($max_size_mb);
    }
    if ($in->{'min_size'}) {
        my $min_size_mb = $in->{'min_size'} * 1024 * 1024;
        $cmd .= " --minsize " . quotemeta($min_size_mb);
    }
    
    # Message age parameters
    if ($in->{'max_age'}) {
        $cmd .= " --maxage " . quotemeta($in->{'max_age'});
    }
    if ($in->{'min_age'}) {
        $cmd .= " --minage " . quotemeta($in->{'min_age'});
    }
    
    if ($in->{'timeout1'}) {
        $cmd .= " --timeout1 " . quotemeta($in->{'timeout1'});
    }
    if ($in->{'timeout2'}) {
        $cmd .= " --timeout2 " . quotemeta($in->{'timeout2'});
    }

    if ($in->{'delete_source'}) {
        $cmd .= " --delete1";
    }

    
    # Email report parameters
    if ($in->{'email_report_source'} eq 'yes') {
        $cmd .= " --emailreport1";
    } else {
        $cmd .= " --noemailreport1";
    }
    
    if ($in->{'email_report_dest'} eq 'yes') {
        $cmd .= " --emailreport2";
    } else {
        $cmd .= " --noemailreport2";
    }
    
    if ($in->{'skip_empty_folders'}) {
        $cmd .= " --skipemptyfolders";
    }
    
    # Debug parameters
    if ($in->{'debug'}) {
        $cmd .= " --debug";
    }
    if ($in->{'show_commands'}) {
        $cmd .= " --showpasswords";
    }
    if ($in->{'skip_errors'}) {
        $cmd .= " --skipmess";
    }
    if ($in->{'dry_run'}) {
        $cmd .= " --dry";
    }
    if ($in->{'debug_folders'}) {
        $cmd .= " --debugfolders";
    }
    if ($in->{'debug_content'}) {
        $cmd .= " --debugcontent";
    }
    if ($in->{'debug_flags'}) {
        $cmd .= " --debugflags";
    }
    if ($in->{'debug_imap1'}) {
        $cmd .= " --debugimap1";
    }
    if ($in->{'debug_imap2'}) {
        $cmd .= " --debugimap2";
    }
    if ($in->{'debug_memory'}) {
        $cmd .= " --debugmemory";
    }
    if ($in->{'just_connect'}) {
        $cmd .= " --justconnect";
    }
    if ($in->{'debug_ssl'}) {
        $cmd .= " --debugssl " . quotemeta($in->{'debug_ssl'});
    }
    
    return $cmd;
}

1; 