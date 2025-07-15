#!/bin/bash
#
# build.sh - Script to package the Webmin IMAPsync Migrator module.
#

# Ensures the script stops if any command fails.
set -e

MODULE_NAME="imap-migrator"
PACKAGE_FILE="${MODULE_NAME}.wbm.gz"
TEMP_DIR="temp_build"

echo "Cleaning old packages..."
rm -f *.wbm.gz

echo "Cleaning previous temporary directory (if exists)..."
if [ -d "${TEMP_DIR}" ]; then
    rm -rf "${TEMP_DIR}"
fi

echo "Ensuring correct permissions for scripts..."
chmod +x ${MODULE_NAME}/*.cgi ${MODULE_NAME}/*.pl

echo "Creating temporary structure for the build..."
mkdir -p "${TEMP_DIR}/${MODULE_NAME}"

echo "Copying files to the temporary structure..."
cp -r ${MODULE_NAME}/* "${TEMP_DIR}/${MODULE_NAME}/"

echo "Removing non-minified files from assets folder..."
rm -f "${TEMP_DIR}/${MODULE_NAME}/assets/terminal.css"
rm -f "${TEMP_DIR}/${MODULE_NAME}/assets/terminal.js"

echo "Creating the module package '${PACKAGE_FILE}'..."
tar -czf ${PACKAGE_FILE} -C ${TEMP_DIR} ${MODULE_NAME}

echo "Cleaning temporary directory..."
rm -rf "${TEMP_DIR}"

echo ""
echo "Package '${PACKAGE_FILE}' created successfully!"
echo "You can install it via Webmin -> Webmin Configuration -> Webmin Modules."
