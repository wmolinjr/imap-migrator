#!/usr/bin/perl
# install_check.pl
# Retorna 0 se ok, 1 se as dependências não forem encontradas.

require 'web-lib-funcs.pl';

my $imapsync_path = &has_command('imapsync');

if (!$imapsync_path) {
    print "O comando 'imapsync' não foi encontrado em seu sistema. ",
          "Por favor, instale-o usando 'apt-get install imapsync' ou 'yum install imapsync' antes de usar este módulo.\n";
    exit 1;
}

exit 0; 