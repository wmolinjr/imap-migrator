#!/usr/bin/perl
use strict;
use warnings;

use lib ("..");
use WebminCore;

our %text;

init_config();
foreign_require("virtual-server");

ui_print_header($text{'index_desc'}, $text{'index_title'}, undef, 'help', undef);

print ui_form_start("migrate.cgi", "post");

# Definir as tabs usando formato correto do Webmin
my @tabs = (
    [ 'credentials', $text{'tab_credentials'} ],
    [ 'advanced', $text{'tab_advanced'} ],
    [ 'debug', $text{'tab_debug'} ]
);

print ui_tabs_start(\@tabs, "tab", "credentials", 1);

# Tab Credentials
print ui_tabs_start_tab("tab", "credentials");
print ui_table_start($text{'index_header'}, "width=100%", 2);

print ui_table_row(undef, "<b>$text{'index_source_header'}</b>", 2, "width=100%");
print ui_table_row("$text{'index_host'}:",
    ui_textbox("source_host", undef, 50), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'index_user'}:",
    ui_textbox("source_user", undef, 50), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'index_pass'}:",
    ui_password("source_pass", undef, 50), undef, ["width=20%", "width=80%"]);

print ui_table_row("$text{'index_ssl_label'}",
    ui_radio_table("source_ssl", "none",
        [ [ "none", $text{'index_ssl_none'} ],
          [ "ssl", $text{'index_ssl_ssl'} ],
          [ "tls", $text{'index_ssl_tls'} ] ], 3), undef, ["width=20%", "width=80%"]);

print ui_table_row(undef, "<b>$text{'index_dest_header'}</b>", 2, "width=100%");
print ui_table_row("$text{'index_host'}:",
    ui_textbox("dest_host", "localhost", 50), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'index_user'}:",
    ui_textbox("dest_user", undef, 50), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'index_pass'}:",
    ui_password("dest_pass", undef, 50), undef, ["width=20%", "width=80%"]);

print ui_table_row("$text{'index_ssl_label'}",
    ui_radio_table("dest_ssl", "none",
        [ [ "none", $text{'index_ssl_none'} ],
          [ "ssl", $text{'index_ssl_ssl'} ],
          [ "tls", $text{'index_ssl_tls'} ] ], 3), undef, ["width=20%", "width=80%"]);

print ui_table_end();
print ui_tabs_end_tab();

# Tab Advanced
print ui_tabs_start_tab("tab", "advanced");
print ui_table_start($text{'advanced_header'}, "width=100%", 2);

print ui_table_row("$text{'advanced_max_size'}:",
    ui_textbox("max_size", undef, 10), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_min_size'}:",
    ui_textbox("min_size", undef, 10), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_max_age'}:",
    ui_textbox("max_age", undef, 10), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_min_age'}:",
    ui_textbox("min_age", undef, 10), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_age_selection'}:",
    ui_radio_table("age_selection", "default",
        [ [ "default", $text{'advanced_age_default'} ],
          [ "intersection", $text{'advanced_age_intersection'} ],
          [ "union", $text{'advanced_age_union'} ] ], 3), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_delete_source'}:",
    ui_checkbox("delete_source", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_skip_empty_folders'}:",
    ui_checkbox("skip_empty_folders", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_timeout1'}:",
    ui_textbox("timeout1", "120", 10), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_timeout2'}:",
    ui_textbox("timeout2", "120", 10), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_email_report_source'}:",
    ui_radio_table("email_report_source", "no",
        [ [ "yes", $text{'advanced_email_report_yes'} ],
          [ "no", $text{'advanced_email_report_no'} ] ], 2), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_email_report_dest'}:",
    ui_radio_table("email_report_dest", "yes",
        [ [ "yes", $text{'advanced_email_report_yes'} ],
          [ "no", $text{'advanced_email_report_no'} ] ], 2), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'folders_include'}:",
    ui_textbox("folders_include", undef, 50), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'folders_exclude'}:",
    ui_textbox("folders_exclude", undef, 50), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'advanced_skip_errors'}:",
    ui_checkbox("skip_errors", 1, undef), undef, ["width=20%", "width=80%"]);

print ui_table_end();
print ui_tabs_end_tab();

# Tab Debug
print ui_tabs_start_tab("tab", "debug");
print ui_table_start($text{'debug_header'}, "width=100%", 2);

print ui_table_row("$text{'debug_debug'}:",
    ui_checkbox("debug", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_just_connect'}:",
    ui_checkbox("just_connect", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_dry_run'}:",
    ui_checkbox("dry_run", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_show_commands'}:",
    ui_checkbox("show_commands", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_debug_folders'}:",
    ui_checkbox("debug_folders", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_debug_content'}:",
    ui_checkbox("debug_content", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_debug_flags'}:",
    ui_checkbox("debug_flags", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_debug_imap1'}:",
    ui_checkbox("debug_imap1", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_debug_imap2'}:",
    ui_checkbox("debug_imap2", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_debug_memory'}:",
    ui_checkbox("debug_memory", undef, undef), undef, ["width=20%", "width=80%"]);
print ui_table_row("$text{'debug_debug_ssl'}:",
    ui_textbox("debug_ssl", undef, 5), undef, ["width=20%", "width=80%"]);

print ui_table_end();
print ui_tabs_end_tab();

print ui_tabs_end(1);

print ui_form_end([ [ undef, $text{'index_migrate_button'} ] ]);

ui_print_footer(); 