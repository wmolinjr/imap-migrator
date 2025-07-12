# IMAPsync Migrator for Webmin/Virtualmin

A simple and effective Webmin/Virtualmin module to migrate email accounts between IMAP servers using the power of `imapsync`. It provides a clean user interface within Webmin and a real-time log viewer to monitor the migration process.

## ✨ Features

- **🖥️ User-Friendly Interface:** Clean and intuitive form to configure source and destination server details
- **📊 Real-Time Monitoring:** Live log viewer that updates automatically every 2 seconds, showing `imapsync` output in real-time
- **🔒 Secure Password Handling:** Passwords are stored in temporary files with secure permissions and automatically deleted after migration
- **🎛️ Advanced Options:** Support for SSL/TLS connections, folder filtering, size/age restrictions, and email reports
- **🐛 Debug Mode:** Built-in debugging tools for troubleshooting migration issues
- **🌐 Multi-language Support:** Available in English and Portuguese
- **⚡ Self-Contained:** Robust and independent of specific Webmin theme configurations

## 📋 Prerequisites

Before installing this module, you **must** have `imapsync` installed on your server.

### Installing imapsync

**For Debian/Ubuntu:**

```bash
sudo apt-get update && sudo apt-get install imapsync
```

**For Red Hat/CentOS:**

```bash
sudo yum install epel-release && sudo yum install imapsync
```

**For other distributions:**
Check your package manager or install from [source](https://github.com/imapsync/imapsync).

## 🚀 Installation

### Quick Install (Recommended)

1. Go to the [Releases page](https://github.com/wmolinjr/imap-migrator/releases) of this repository
2. Download the latest `imap-migrator.wbm.gz` file
3. In Webmin, navigate to **Webmin → Webmin Configuration → Webmin Modules**
4. Select **From local file** or **From uploaded file**
5. Choose the `imap-migrator.wbm.gz` file you downloaded
6. Click **Install Module**

The module will be available under the **Tools** category in the left-hand menu.

### Manual Installation

1. Download the module files
2. Extract to `/usr/share/webmin/imap-migrator/`
3. Set proper permissions: `chmod 755 /usr/share/webmin/imap-migrator/`
4. Restart Webmin

## 🛠️ Usage

### Basic Migration

1. Navigate to **Tools → IMAP Migrator** in Webmin
2. Fill in the source server details:
   - **IMAP Server:** Your source server address
   - **User:** Email account username
   - **Password:** Email account password
   - **Security:** Choose SSL/TLS if required
3. Fill in the destination server details (same fields)
4. Click **Start Migration**
5. Monitor the real-time log for progress

### Advanced Options

The module includes several advanced features accessible through tabs:

- **Credentials:** Basic server configuration
- **Advanced:** Size limits, age filters, folder inclusion/exclusion, email reports
- **Debug:** Debugging options and real-time testing tools

## 🔧 For Developers

### Building from Source

If you want to modify the module or build the package from source:

1. Clone this repository:

   ```bash
   git clone https://github.com/wmolinjr/imap-migrator.git
   cd imap-migrator
   ```

2. Run the build script:

   ```bash
   ./build.sh
   ```

3. The `imap-migrator.wbm.gz` package will be created in the root directory

### Development Setup

```bash
# Clone the repository
git clone https://github.com/wmolinjr/imap-migrator.git
cd imap-migrator

# Make build script executable
chmod +x build.sh

# Build the module
./build.sh
```

## 📁 Project Structure

```
imap-migrator/
├── index.cgi              # Main interface
├── migrate.cgi            # Migration execution
├── status.cgi             # Real-time log status
├── imap-migrator.js       # Frontend JavaScript
├── imap-migrator-lib.pl   # Backend library
├── lang/                   # Translation files
│   ├── en                 # English translations
│   └── pt                 # Portuguese translations
├── help/                   # Help documentation
└── build.sh               # Build script
```

## 🐛 Troubleshooting

### Common Issues

**Module not appearing in Webmin:**

- Ensure proper file permissions
- Check Webmin error logs
- Verify module installation path

**imapsync not found:**

- Install imapsync package for your distribution
- Verify imapsync is in PATH: `which imapsync`

**Migration fails:**

- Check server connectivity
- Verify credentials
- Review real-time logs for specific errors
- Enable debug mode for detailed information

### Debug Mode

Enable debug mode in the **Debug** tab to access:

- Real-time testing tools
- Detailed console logging
- Server connectivity tests
- Log file verification

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

### How to Contribute

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 💖 Support the Project

If this project helped you, consider supporting:

- 💸 [GitHub Sponsors](https://github.com/sponsors/wmolinjr)
- ☕ [Buy Me a Coffee](https://www.buymeacoffee.com/wmolinjr)
- 📢 Share with friends and colleagues!

All help is welcome to keep the project alive 🚀

## 🙏 Acknowledgments

- [imapsync](https://github.com/imapsync/imapsync) - The powerful tool that makes this all possible
- [Webmin](https://webmin.com/) - The excellent web-based system administration tool
- All contributors and users who help improve this module

---

**Made with ❤️ for the Webmin community**
