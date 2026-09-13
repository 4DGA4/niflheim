# NIFLHEIM - Data Poisoning Browser Extension

**Version:** 1.0.0  
**Manifest:** V3 (Chrome/Edge/Brave compatible)

## Overview

NIFLHEIM is a privacy protection browser extension that detects surveillance mechanisms and poisons collected data with synthetic identities and false information. It provides 11 comprehensive fingerprinting protections to defend against modern tracking techniques.

## Installation

### Chrome/Edge/Brave

1. Open browser and navigate to:
   - Chrome: `chrome://extensions/`
   - Edge: `edge://extensions/`
   - Brave: `brave://extensions/`

2. Enable **Developer mode** (toggle in top-right corner)

3. Click **Load unpacked**

4. Select the `browser-extension` directory:
   ```
   C:\Users\cgill\DarkEmpire_Systems\browser-extension\
   ```

5. The extension icon (pink with "NIFLHEIM") should appear in your toolbar

## Features

### 11 Fingerprinting Protections

1. **Canvas Fingerprinting** - Adds noise to canvas rendering
2. **WebGL Fingerprinting** - Po WebGL renderer information
3. **Audio Fingerprinting** - Modifies audio context output
4. **Font Detection** - Randomizes font availability detection
5. **Screen Resolution** - Reports false screen dimensions
6. **Timezone** - Spoofs timezone information
7. **Language** - Randomizes navigator languages
8. **Platform** - Masks OS detection
9. **Hardware Concurrency** - False CPU core count
10. **Device Memory** - False memory reporting
11. **Touch Support** - Modifies touch capability detection

### Surveillance Detection

- Cookie tracking detection
- LocalStorage monitoring
- SessionStorage tracking
- IndexedDB surveillance
- Beacon API monitoring
- Fetch API interception
- XMLHttpRequest monitoring

### Data Poisoning

- Synthetic identity injection
- False demographic data
- Randomized behavioral patterns
- Noise injection in analytics

## Usage

### Viewing Protection Status

1. Click the extension icon in the toolbar
2. The popup displays:
   - Active protections count
   - Trackers detected
   - Poisoning events
   - Real-time status

### Console Monitoring

Open browser DevTools (F12) → Console to see:
- `[NIFLHEIM]` prefixed logs
- Tracker detection alerts
- Protection activation confirmations
- Poisoning event reports

## File Structure

```
browser-extension/
├── manifest.json       # Extension configuration (MV3)
├── background.js       # Service worker (tracker detection)
├── content.js          # Content script (11 protections)
├── popup.html          # Extension UI
├── popup.js            # Popup controller
├── alerts.js           # Alert system stub
├── icons/
│   ├── icon16.png      # Toolbar icon (small)
│   ├── icon48.png      # Extension page icon
│   └── icon128.png     # Chrome Web Store icon
└── README.md           # This file
```

## Troubleshooting

### Extension Not Loading

**Error:** "Could not load extension"
- **Solution:** Verify all files are present in the directory
- Check manifest.json for syntax errors
- Ensure icon files exist in `icons/` subdirectory

### Icons Not Showing

**Error:** Missing icon errors in console
- **Solution:** Verify icons directory exists
- Check file names match manifest (icon16.png, icon48.png, icon128.png)
- Reload extension from chrome://extensions/

### Protections Not Working

**Issue:** Trackers not being detected
- **Solution:** Refresh the target webpage after extension loads
- Check browser console for `[NIFLHEIM]` logs
- Verify content.js is injecting (check Sources panel)

### Conflicts with Other Extensions

**Issue:** Ad blockers or privacy extensions interfering
- **Solution:** Disable conflicting extensions temporarily
- NIFLHEIM is designed to work alongside uBlock Origin, Privacy Badger
- If issues persist, whitelist NIFLHEIM in other extensions

## Browser Compatibility

| Browser | Version | Status |
|---------|---------|--------|
| Chrome | 88+ | ✅ Tested |
| Edge | 88+ | ✅ Tested |
| Brave | 1.20+ | ✅ Tested |
| Firefox | 100+ | ⚠️ Requires manifest adjustments |
| Opera | 74+ | ✅ Should work |

## Permissions

The extension requires the following permissions:

- **storage** - Store protection settings and tracker counts
- **cookies** - Detect and monitor cookie-based tracking
- **webRequest** - Intercept network requests for tracker detection
- **tabs** - Access tab information for per-site protection
- **alarms** - Periodic cleanup and maintenance tasks
- **<all_urls>** - Apply protections across all websites

## Development

### Reloading During Development

1. Make code changes
2. Go to `chrome://extensions/`
3. Click the refresh icon on the NIFLHEIM card
4. Refresh target webpages to apply content script changes

### Debugging

**Background Script:**
- Go to `chrome://extensions/`
- Click "service worker" link under NIFLHEIM
- Opens DevTools for background.js

**Content Script:**
- Open target webpage
- Press F12 → Console
- Filter by `[NIFLHEIM]` prefix

**Popup:**
- Right-click extension icon → "Inspect popup"
- Opens DevTools for popup.html/popup.js

## Integration with NIFLHEIM Core

This extension works as part of the broader NIFLHEIM surveillance poisoning framework. For full integration:

1. Install browser extension (this package)
2. Deploy NIFLHEIM core modules from `DarkEmpire_Systems\`
3. Configure shared identity pools
4. Enable cross-module coordination

See `INTEGRATION_GUIDE.md` for detailed integration instructions.

## License

Part of the Dark Empire NIFLHEIM project. All rights reserved.

## Support

For issues or questions:
- Check `INTEGRATION_GUIDE.md` for detailed documentation
- Review browser console logs for error messages
- Verify file permissions and directory structure

---

**Last Updated:** 2026-09-13  
**Migration Status:** Complete (DarkEmpire_Intelligence-Operations → DarkEmpire_Systems)
