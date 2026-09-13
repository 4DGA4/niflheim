/**
 * Niflheim - Content Script
 * Injected into web pages to detect and poison fingerprinting attempts
 */

(function() {
  'use strict';
  
  // Configuration
  const config = {
    enableCanvasPoisoning: true,
    enableWebGLPoisoning: true,
    enableAudioPoisoning: true,
    enableFontPoisoning: true,
    enableScreenPoisoning: true,
    enableNavigatorPoisoning: true,
    enableWebRTCPoisoning: true,
    enableBatteryPoisoning: true,
    enableMediaDevicePoisoning: true,
    enableTouchPoisoning: true,
    enableTimerJitter: true,
    jitterMs: 5.0
  };
  
  // Load config from background script
  chrome.runtime.sendMessage({ action: 'getSettings' }, (response) => {
    if (response && response.protectionEnabled !== undefined) {
      Object.assign(config, response);
    }
  });
  
  // Canvas fingerprinting protection
  if (config.enableCanvasPoisoning) {
    poisonCanvas();
  }
  
  // WebGL fingerprinting protection
  if (config.enableWebGLPoisoning) {
    poisonWebGL();
  }
  
  // Audio fingerprinting protection
  if (config.enableAudioPoisoning) {
    poisonAudio();
  }
  
  // Timer jitter for performance.now() and Date.now()
  if (config.enableTimerJitter) {
    poisonTimers();
  }
  
  // Navigator property poisoning
  if (config.enableNavigatorPoisoning) {
    poisonNavigator();
  }
  
  // Screen property poisoning
  if (config.enableScreenPoisoning) {
    poisonScreen();
  }
  
  // WebRTC protection
  if (config.enableWebRTCPoisoning) {
    poisonWebRTC();
  }
  
  // Battery API protection
  if (config.enableBatteryPoisoning) {
    poisonBattery();
  }
  
  // Media device enumeration protection
  if (config.enableMediaDevicePoisoning) {
    poisonMediaDevices();
  }
  
  // Touch event protection
  if (config.enableTouchPoisoning) {
    poisonTouch();
  }
  
  console.log('Niflheim content script initialized - fingerprinting protections active');
  
  // ============ Canvas Poisoning ============
  function poisonCanvas() {
    const originalToDataURL = HTMLCanvasElement.prototype.toDataURL;
    const originalGetImageData = CanvasRenderingContext2D.prototype.getImageData;
    
    HTMLCanvasElement.prototype.toDataURL = function(...args) {
      const result = originalToDataURL.apply(this, args);
      // Add subtle noise to the output
      return addNoiseToDataUrl(result);
    };
    
    CanvasRenderingContext2D.prototype.getImageData = function(sx, sy, sw, sh) {
      const imageData = originalGetImageData.apply(this, arguments);
      // Add noise to pixel data
      return addNoiseToImageData(imageData);
    };
  }
  
  function addNoiseToDataUrl(dataUrl) {
    // For actual implementation, would decode and modify the image data
    // For now, just log the attempt
    logFingerprintAttempt('canvas', 'toDataURL');
    return dataUrl;
  }
  
  function addNoiseToImageData(imageData) {
    const data = imageData.data;
    // Add subtle noise to every 10th pixel
    for (let i = 0; i < data.length; i += 40) {
      const noise = (Math.random() - 0.5) * 2;
      data[i] = Math.min(255, Math.max(0, data[i] + noise));
      data[i + 1] = Math.min(255, Math.max(0, data[i + 1] + noise));
      data[i + 2] = Math.min(255, Math.max(0, data[i + 2] + noise));
    }
    logFingerprintAttempt('canvas', 'getImageData');
    return imageData;
  }
  
  // ============ WebGL Poisoning ============
  function poisonWebGL() {
    const originalGetParameter = WebGLRenderingContext.prototype.getParameter;
    
    WebGLRenderingContext.prototype.getParameter = function(pname) {
      const result = originalGetParameter.apply(this, arguments);
      
      // Poison specific parameters
      if (pname === this.MAX_VIEWPORT_DIMS) {
        logFingerprintAttempt('webgl', 'MAX_VIEWPORT_DIMS');
        return [result[0] + randomInt(-10, 10), result[1] + randomInt(-10, 10)];
      }
      
      if (pname === this.EXTENSIONS) {
        logFingerprintAttempt('webgl', 'EXTENSIONS');
        const fakeExtensions = ['WEBGL_debug_renderer_info_FAKE', 'WEBGL_lose_context_FAKE'];
        return result.concat(fakeExtensions);
      }
      
      return result;
    };
  }
  
  // ============ Audio Poisoning ============
  function poisonAudio() {
    const originalGetChannelData = AudioBuffer.prototype.getChannelData;
    
    AudioBuffer.prototype.getChannelData = function(channel) {
      const data = originalGetChannelData.apply(this, arguments);
      logFingerprintAttempt('audio', 'getChannelData');
      
      // Add subtle noise
      const noisyData = new Float32Array(data.length);
      for (let i = 0; i < data.length; i++) {
        noisyData[i] = data[i] + (Math.random() - 0.5) * 0.001;
      }
      return noisyData;
    };
  }
  
  // ============ Timer Poisoning ============
  function poisonTimers() {
    const originalPerformanceNow = performance.now.bind(performance);
    const originalDateNow = Date.now.bind(Date);
    
    performance.now = function() {
      const baseTime = originalPerformanceNow();
      const jitter = (Math.random() - 0.5) * 2 * config.jitterMs;
      return baseTime + jitter;
    };
    
    Date.now = function() {
      const baseTime = originalDateNow();
      const jitter = (Math.random() - 0.5) * 2 * config.jitterMs;
      return baseTime + jitter;
    };
  }
  
  // ============ Navigator Poisoning ============
  function poisonNavigator() {
    // Override navigator properties with subtle variations
    const originalPlugins = navigator.plugins;
    const originalLanguages = navigator.languages;
    
    Object.defineProperty(navigator, 'plugins', {
      get: function() {
        logFingerprintAttempt('navigator', 'plugins');
        // Return fake plugins
        return createFakePlugins();
      }
    });
    
    Object.defineProperty(navigator, 'languages', {
      get: function() {
        logFingerprintAttempt('navigator', 'languages');
        const fakeLanguages = ['en-US', 'en', 'es', 'fr', 'de'];
        return fakeLanguages;
      }
    });
  }
  
  function createFakePlugins() {
    const fakePlugins = [
      { name: 'Chrome PDF Plugin', filename: 'internal-pdf-viewer' },
      { name: 'Chrome PDF Viewer', filename: 'mhjfbmdgcfjbbpaeojofohoefgiehjai' },
      { name: 'Native Client', filename: 'internal-nacl-plugin' }
    ];
    return {
      length: fakePlugins.length,
      item: (index) => fakePlugins[index] || null,
      namedItem: (name) => fakePlugins.find(p => p.name === name) || null,
      [Symbol.iterator]: function* () {
        for (const plugin of fakePlugins) {
          yield plugin;
        }
      }
    };
  }
  
  // ============ Screen Poisoning ============
  function poisonScreen() {
    const originalWidth = screen.width;
    const originalHeight = screen.height;
    
    Object.defineProperty(screen, 'width', {
      get: function() {
        logFingerprintAttempt('screen', 'width');
        return originalWidth + randomInt(-5, 5);
      }
    });
    
    Object.defineProperty(screen, 'height', {
      get: function() {
        logFingerprintAttempt('screen', 'height');
        return originalHeight + randomInt(-5, 5);
      }
    });
  }
  
  // ============ WebRTC Protection ============
  function poisonWebRTC() {
    const originalRTCPeerConnection = window.RTCPeerConnection || window.webkitRTCPeerConnection;
    
    if (originalRTCPeerConnection) {
      window.RTCPeerConnection = function(...args) {
        logFingerprintAttempt('webrtc', 'RTCPeerConnection');
        const pc = new originalRTCPeerConnection(...args);
        
        // Override createDataChannel to add noise
        const originalCreateDataChannel = pc.createDataChannel.bind(pc);
        pc.createDataChannel = function(label, options) {
          const channel = originalCreateDataChannel(label, options);
          // Could add noise to channel data here
          return channel;
        };
        
        return pc;
      };
    }
  }
  
  // ============ Battery API Protection ============
  function poisonBattery() {
    if (navigator.getBattery) {
      const originalGetBattery = navigator.getBattery.bind(navigator);
      
      navigator.getBattery = async function() {
        logFingerprintAttempt('battery', 'getBattery');
        const battery = await originalGetBattery();
        
        // Override battery properties
        Object.defineProperty(battery, 'level', {
          get: function() {
            return 0.5 + (Math.random() * 0.3); // Random level between 0.5 and 0.8
          }
        });
        
        Object.defineProperty(battery, 'charging', {
          get: function() {
            return Math.random() > 0.5;
          }
        });
        
        return battery;
      };
    }
  }
  
  // ============ Media Device Protection ============
  function poisonMediaDevices() {
    if (navigator.mediaDevices && navigator.mediaDevices.enumerateDevices) {
      const originalEnumerateDevices = navigator.mediaDevices.enumerateDevices.bind(navigator.mediaDevices);
      
      navigator.mediaDevices.enumerateDevices = async function() {
        logFingerprintAttempt('mediaDevices', 'enumerateDevices');
        const devices = await originalEnumerateDevices();
        
        // Add fake devices
        const fakeDevices = [
          {
            deviceId: 'fake_' + Math.random().toString(36).substr(2, 15),
            kind: 'audioinput',
            label: 'Fake Microphone',
            groupId: 'fake_group_' + Math.random().toString(36).substr(2, 8)
          },
          {
            deviceId: 'fake_' + Math.random().toString(36).substr(2, 15),
            kind: 'videoinput',
            label: 'Fake Camera',
            groupId: 'fake_group_' + Math.random().toString(36).substr(2, 8)
          }
        ];
        
        return devices.concat(fakeDevices);
      };
    }
  }
  
  // ============ Touch Event Protection ============
  function poisonTouch() {
    if (navigator.touchEnabled) {
      Object.defineProperty(navigator, 'touchEnabled', {
        get: function() {
          logFingerprintAttempt('touch', 'touchEnabled');
          return Math.random() > 0.5; // Random true/false
        }
      });
    }
    
    if (navigator.maxTouchPoints) {
      Object.defineProperty(navigator, 'maxTouchPoints', {
        get: function() {
          logFingerprintAttempt('touch', 'maxTouchPoints');
          return randomInt(0, 5);
        }
      });
    }
  }
  
  // ============ Utility Functions ============
  function randomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
  }
  
  function logFingerprintAttempt(type, method) {
    chrome.runtime.sendMessage({
      action: 'logFingerprintAttempt',
      type,
      method,
      url: window.location.href,
      timestamp: new Date().toISOString()
    });
  }
  
  // Listen for messages from background script
  chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'generateIdentity') {
      chrome.runtime.sendMessage({ action: 'generateIdentity' }, sendResponse);
      return true;
    }
  });
  
})();
