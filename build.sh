#!/bin/bash
#
# build.sh - Script para empacotar o módulo Webmin IMAPsync Migrator.
#

# Garante que o script pare se algum comando falhar.
set -e

MODULE_NAME="imap-migrator"
PACKAGE_FILE="${MODULE_NAME}.wbm.gz"

echo "Limpando pacotes antigos..."
rm -f *.wbm.gz

echo "Garantindo permissões corretas para os scripts..."
chmod +x ${MODULE_NAME}/*.cgi ${MODULE_NAME}/*.pl

echo "Criando o pacote do módulo '${PACKAGE_FILE}'..."
tar -czf ${PACKAGE_FILE} ${MODULE_NAME}

echo ""
echo "Pacote '${PACKAGE_FILE}' criado com sucesso!"
echo "Você pode instalá-lo via Webmin -> Configuração do Webmin -> Módulos do Webmin." 