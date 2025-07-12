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

# Process SSL/TLS configurations
my $source_ssl = $in{'source_ssl'} || 'none';
my $dest_ssl = $in{'dest_ssl'} || 'none';

my $source_pass_file = tempname();
write_file_contents($source_pass_file, $in{'source_pass'});
chmod(0600, $source_pass_file);

my $dest_pass_file = tempname();
write_file_contents($dest_pass_file, $in{'dest_pass'});
chmod(0600, $dest_pass_file);

my $log_file = tempname();

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

# Call header
ui_print_header(undef, $text{'migrate_title'}, "");

print "<h3>$text{'migrate_status_header'}</h3>";
print "<p>$text{'migrate_status_desc'}</p>";

print "<b>$text{'migrate_log_label'}</b><br>";

# Check if migrator debug is enabled
my $migrator_debug = defined($in{'migrator_debug'}) ? 1 : 0;

# Status indicator always visible
print "<div id='status-indicator' class='alert alert-info' style='margin-bottom: 10px;'><i class='fa fa-fw fa-info-circle'></i>&nbsp;<span>Status: $text{'status_awaiting_js'}</span></div>";

# Test buttons only if debug is enabled
if ($migrator_debug) {
    print "<div class='btn-group' style='margin-bottom: 10px;'>";
    print "<button class='btn btn-primary ui_submit' type='button' onclick='testJavaScript()'><i class='fa fa-fw fa-keyboard-o'></i>&nbsp;<span>$text{'test_js_button'}</span></button>";
    print "<button class='btn btn-success ui_submit' type='button' onclick='testServer()'><i class='fa fa-fw fa-server'></i>&nbsp;<span>$text{'test_server_button'}</span></button>";
    print "<button class='btn btn-warning ui_submit' type='button' onclick='testLogFile()'><i class='fa fa-fw fa-file-text'></i>&nbsp;<span>$text{'test_log_button'}</span></button>";
    print "</div><br>";
}

print "<pre id='log-container' data-logfile=\"$log_file\" class='xterm-helper-textarea' style='height: 400px;'>";
print "$text{'migration_starting'}";
print "</pre>";

print "<br>";
print ui_link("index.cgi", $text{'migrate_back'});

# Add CSS to ensure updates are visible
print "<style>\n";
print ".force-update { animation: flash 0.1s ease-in-out; }\n";
print "#log-container { transition: all 0.1s ease-in-out; }\n";
print "</style>\n";

# Add JavaScript variables with translations
print "<script type='text/javascript'>\n";
print "var translations = {\n";
print "  status_awaiting_js: '$text{'status_awaiting_js'}',\n";
print "  status_js_loaded: '$text{'status_js_loaded'}',\n";
print "  status_searching_updates: '$text{'status_searching_updates'}',\n";
print "  status_log_updated: '$text{'status_log_updated'}',\n";
print "  status_waiting_updates: '$text{'status_waiting_updates'}',\n";
print "  status_migration_complete: '$text{'status_migration_complete'}',\n";
print "  status_error_search: '$text{'status_error_search'}',\n";
print "  status_error_log_file: '$text{'status_error_log_file'}',\n";
print "  status_test_js: '$text{'status_test_js'}',\n";
print "  status_test_server: '$text{'status_test_server'}',\n";
print "  status_test_log: '$text{'status_test_log'}',\n";
print "  error_js_error: '$text{'error_js_error'}',\n";
print "  error_network_error: '$text{'error_network_error'}',\n";
print "  error_log_file_not_found: '$text{'error_log_file_not_found'}',\n";
print "  test_js_success: '$text{'test_js_success'}',\n";
print "  test_server_success: '$text{'test_server_success'}',\n";
print "  test_server_error: '$text{'test_server_error'}',\n";
print "  test_log_success: '$text{'test_log_success'}',\n";
print "  test_log_error: '$text{'test_log_error'}',\n";
print "  test_elements_not_found: '$text{'test_elements_not_found'}',\n";
print "  test_log_file_not_defined: '$text{'test_log_file_not_defined'}',\n";
print "  test_testing_server: '$text{'test_testing_server'}',\n";
print "  test_testing_log: '$text{'test_testing_log'}',\n";
print "  test_size: '$text{'test_size'}',\n";
print "  test_characters: '$text{'test_characters'}',\n";
print "  test_status: '$text{'test_status'}',\n";
print "  test_debug: '$text{'test_debug'}',\n";
print "  migration_complete: '$text{'migration_complete'}',\n";
print "  migrator_debug_enabled: " . ($migrator_debug ? 'true' : 'false') . "\n";
print "};\n";
print "</script>\n";

# Add JavaScript test functions only if debug is enabled
if ($migrator_debug) {
    print "<script type='text/javascript'>\n";
    print "function testJavaScript() {\n";
    print "  var logContainer = document.getElementById('log-container');\n";
    print "  var statusIndicator = document.getElementById('status-indicator');\n";
    print "  if (logContainer && statusIndicator) {\n";
    print "    logContainer.innerHTML = '<div class=\"alert alert-success\"><i class=\"fa fa-fw fa-check-circle\"></i>&nbsp;<strong>' + translations.test_js_success + '</strong> ' + new Date().toLocaleTimeString() + '</div>';\n";
    print "    statusIndicator.innerHTML = '<i class=\"fa fa-fw fa-check-circle\"></i>&nbsp;<span>' + translations.test_status + ': [' + translations.test_debug + '] ' + translations.status_test_js + ' ' + new Date().toLocaleTimeString() + '</span>';\n";
    print "    statusIndicator.className = 'alert alert-success';\n";
    print "    console.log('Teste JavaScript executado com sucesso');\n";
    print "  } else {\n";
    print "    alert(translations.test_elements_not_found);\n";
    print "  }\n";
    print "}\n";
    print "function testServer() {\n";
    print "  var logContainer = document.getElementById('log-container');\n";
    print "  var statusIndicator = document.getElementById('status-indicator');\n";
    print "  if (logContainer && statusIndicator) {\n";
    print "    statusIndicator.innerHTML = '<i class=\"fa fa-fw fa-info-circle\"></i>&nbsp;<span>' + translations.test_status + ': [' + translations.test_debug + '] ' + translations.test_testing_server + '</span>';\n";
    print "    statusIndicator.className = 'alert alert-info';\n";
    print "    // Testa apenas a conectividade básica do servidor\n";
    print "    fetch('index.cgi')\n";
    print "      .then(response => {\n";
    print "        console.log('Teste servidor - Status:', response.status);\n";
    print "        if (response.ok) {\n";
    print "          logContainer.innerHTML = '<div class=\"alert alert-success\"><i class=\"fa fa-fw fa-check-circle\"></i>&nbsp;<strong>' + translations.test_server_success + '</strong><br>' + translations.test_status + ': ' + response.status + '<br>URL: ' + response.url + '</div>';\n";
    print "          statusIndicator.innerHTML = '<i class=\"fa fa-fw fa-check-circle\"></i>&nbsp;<span>' + translations.test_status + ': [' + translations.test_debug + '] ' + translations.status_test_server + ' ' + new Date().toLocaleTimeString() + '</span>';\n";
    print "          statusIndicator.className = 'alert alert-success';\n";
    print "        } else {\n";
    print "          throw new Error('Status: ' + response.status);\n";
    print "        }\n";
    print "      })\n";
    print "      .catch(error => {\n";
    print "        logContainer.innerHTML = '<div class=\"alert alert-danger\"><i class=\"fa fa-fw fa-exclamation-triangle\"></i>&nbsp;<strong>' + translations.test_server_error + ' -</strong> ' + error.message + '</div>';\n";
    print "        statusIndicator.innerHTML = '<i class=\"fa fa-fw fa-exclamation-triangle\"></i>&nbsp;<span>' + translations.test_status + ': [' + translations.test_debug + '] ' + translations.status_test_error + ' ' + new Date().toLocaleTimeString() + '</span>';\n";
    print "        statusIndicator.className = 'alert alert-danger';\n";
    print "      });\n";
    print "  } else {\n";
    print "    alert(translations.test_elements_not_found);\n";
    print "  }\n";
    print "}\n";
    print "function testLogFile() {\n";
    print "  var logContainer = document.getElementById('log-container');\n";
    print "  var statusIndicator = document.getElementById('status-indicator');\n";
    print "  var logFile = logContainer.dataset.logfile;\n";
    print "  if (logContainer && statusIndicator && logFile) {\n";
    print "    statusIndicator.innerHTML = '<i class=\"fa fa-fw fa-info-circle\"></i>&nbsp;<span>' + translations.test_status + ': [' + translations.test_debug + '] ' + translations.test_testing_log + '</span>';\n";
    print "    statusIndicator.className = 'alert alert-info';\n";
    print "    fetch('status.cgi?log=' + logFile)\n";
    print "      .then(response => {\n";
    print "        console.log('Teste log - ' + translations.test_status + ':', response.status);\n";
    print "        return response.text();\n";
    print "      })\n";
    print "      .then(data => {\n";
    print "        logContainer.innerHTML = '<div class=\"alert alert-success\"><i class=\"fa fa-fw fa-check-circle\"></i>&nbsp;<strong>' + translations.test_log_success + '</strong><br>' + translations.test_size + ': ' + data.length + ' ' + translations.test_characters + '</div><pre>' + data + '</pre>';\n";
    print "        statusIndicator.innerHTML = '<i class=\"fa fa-fw fa-check-circle\"></i>&nbsp;<span>' + translations.test_status + ': [' + translations.test_debug + '] ' + translations.status_test_log + ' ' + new Date().toLocaleTimeString() + '</span>';\n";
    print "        statusIndicator.className = 'alert alert-success';\n";
    print "      })\n";
    print "      .catch(error => {\n";
    print "        logContainer.innerHTML = '<div class=\"alert alert-danger\"><i class=\"fa fa-fw fa-exclamation-triangle\"></i>&nbsp;<strong>' + translations.test_log_error + ' -</strong> ' + error.message + '</div>';\n";
    print "        statusIndicator.innerHTML = '<i class=\"fa fa-fw fa-exclamation-triangle\"></i>&nbsp;<span>' + translations.test_status + ': [' + translations.test_debug + '] ' + translations.status_test_error + ' ' + new Date().toLocaleTimeString() + '</span>';\n";
    print "        statusIndicator.className = 'alert alert-danger';\n";
    print "      });\n";
    print "  } else {\n";
    print "    alert(translations.test_log_file_not_defined);\n";
    print "  }\n";
    print "}\n";
    print "</script>\n";
}

# Load JavaScript at the end of the page with a small delay to avoid conflicts with the theme
print "<script type='text/javascript'>\n";
print "setTimeout(function() {\n";
print "  var script = document.createElement('script');\n";
print "  script.src = 'imap-migrator.js';\n";
print "  document.head.appendChild(script);\n";
print "}, 1000);\n";
print "</script>\n";

ui_print_footer(); 