@echo off
REM
REM build.bat - Script to package the Webmin IMAPsync Migrator module on Windows.
REM

SET MODULE_NAME=imap-migrator
SET PACKAGE_FILE=%MODULE_NAME%.wbm.gz
SET TEMP_DIR=temp_build

echo Cleaning old packages...
del /f /q *.wbm.gz 2>nul

echo Cleaning previous temporary directory (if exists)...
if exist %TEMP_DIR% rmdir /s /q %TEMP_DIR%

echo Ensuring correct permissions for scripts...
REM On Windows chmod is not needed, but we ensure the files exist
IF NOT EXIST %MODULE_NAME%\*.cgi (
    echo ERROR: .cgi files not found in folder %MODULE_NAME%
    exit /b 1
)
IF NOT EXIST %MODULE_NAME%\*.pl (
    echo ERROR: .pl files not found in folder %MODULE_NAME%
    exit /b 1
)

echo Creating temporary structure for the build...
mkdir %TEMP_DIR%
mkdir %TEMP_DIR%\%MODULE_NAME%

echo Copying files to the temporary structure...
xcopy /E /I /Y %MODULE_NAME%\* %TEMP_DIR%\%MODULE_NAME%\

echo Removing non-minified files from assets folder...
del /f /q %TEMP_DIR%\%MODULE_NAME%\assets\terminal.css
del /f /q %TEMP_DIR%\%MODULE_NAME%\assets\terminal.js

echo Creating the module package '%PACKAGE_FILE%'...
REM Uses tar from Git Bash or Windows (if tar is supported in PATH)
tar -czf %PACKAGE_FILE% -C %TEMP_DIR% %MODULE_NAME%
IF ERRORLEVEL 1 (
    echo ERROR: Failed to create .wbm.gz package
    rmdir /s /q %TEMP_DIR%
    exit /b 1
)

echo Cleaning temporary directory...
rmdir /s /q %TEMP_DIR%

echo.
echo Package '%PACKAGE_FILE%' created successfully!
echo You can install it via Webmin

pause
