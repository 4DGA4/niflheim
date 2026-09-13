# NIFLHEIM Browser Extension

**Educational browser extension demonstrating client-side data poisoning concepts**

## Overview

This browser extension provides a practical demonstration of how data poisoning concepts can be applied at the browser level. It intercepts web requests and provides educational overlays about data collection practices.

## Features

- **Request Interception**: Monitors outgoing requests to demonstrate data flows
- **Educational Overlays**: Shows real-time information about tracking
- **Privacy Indicators**: Visual feedback on privacy implications
- **Manifest V3**: Compatible with modern browser extension standards

## Installation

### Chrome/Chromium

1. Open Chrome and navigate to `chrome://extensions/`
2. Enable "Developer mode" in the top right
3. Click "Load unpacked"
4. Select the `browser-extension` directory
5. The extension icon should appear in your toolbar

### Firefox

1. Open Firefox and navigate to `about:debugging`
2. Click "This Firefox" in the left sidebar
3. Click "Load Temporary Add-on"
4. Select `manifest.json` from the `browser-extension` directory
5. The extension will be loaded until Firefox is restarted

## Usage

Once installed:

1. Click the extension icon in your browser toolbar
2. Navigate to a website to see tracking indicators
3. Open the popup to view intercepted requests
4. Review educational information about data collection

## Files

- `manifest.json` - Extension configuration (Manifest V3)
- `background.js` - Background service worker for request interception
- `content.js` - Content script for page interaction
- `popup.html` - Extension popup interface
- `popup.js` - Popup logic and UI handling
- `README.md` - This file

## Development

### Testing Changes

1. Make changes to extension files
2. Go to `chrome://extensions/` or `about:debugging`
3. Click the refresh/reload button on the extension
4. Test the changes

### Debugging

- **Background Script**: Open `chrome://extensions/` → Inspect "service worker"
- **Content Script**: Open DevTools on any webpage → Console tab
- **Popup**: Right-click extension icon → Inspect popup

## Privacy & Security

This extension is designed for **educational purposes only**:

- Does not collect or transmit any user data
- All processing happens locally in the browser
- No external API calls or telemetry
- Open source for transparency

## Limitations

- Temporary installation in Firefox (resets on browser close)
- May not work on all websites due to CSP restrictions
- Educational demo, not a production privacy tool

## Troubleshooting

### Extension not loading

- Ensure you're in Developer mode
- Check that manifest.json is valid JSON
- Verify all referenced files exist

### No requests showing

- Navigate to websites with tracking scripts
- Check browser console for errors
- Ensure extension has necessary permissions

### Popup not working

- Reload the extension
- Check for JavaScript errors in popup inspector
- Clear browser cache and reload

## Contributing

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## License

AGPL-3.0 - See main [LICENSE](../LICENSE)

---

**Educational Use Only**: This extension demonstrates concepts for awareness and learning. Not intended for production use.
