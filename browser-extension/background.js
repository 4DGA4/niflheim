/**
 * Niflheim - Background Service Worker
 * Manages tracker detection and data poisoning
 */

// Tracker patterns
const TRACKER_PATTERNS = {
  google: ['google-analytics.com', 'googletagmanager.com', 'googleadservices.com', 'doubleclick.net'],
  facebook: ['facebook.com', 'facebook.net', 'fbcdn.net', 'connect.facebook.net'],
  amazon: ['amazon-adsystem.com', 'amazonaws.com', 'amazon-adsystem.com'],
  microsoft: ['microsoft.com', 'live.com', 'bing.com', 'msn.com'],
  adobe: ['adobe.com', 'omtrdc.net', '2o7.net'],
  oracle: ['oracle.com', 'eloqua.com', 'addthis.com'],
  salesforce: ['salesforce.com', 'force.com', 'exacttarget.com'],
  twitter: ['twitter.com', 'twimg.com'],
  linkedin: ['linkedin.com', 'licdn.com'],
  criteo: ['criteo.com', 'criteo.net'],
  taboola: ['taboola.com'],
  outbrain: ['outbrain.com']
};

// State
let protectionEnabled = true;
let threadCount = 2;
let updateFrequency = 3600000; // 1 hour
let sharingEnabled = false;
let selectedCountry = 'USA';
let detectionLog = [];

// Identity store
let syntheticIdentities = [];

chrome.runtime.onInstalled.addListener(() => {
  console.log('Niflheim installed - initiating poisoning protocols');
  initializeIdentities();
  startPeriodicTasks();
});

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
  handleMessage(request, sender, sendResponse);
  return true; // Keep message channel open for async response
});

async function handleMessage(request, sender, sendResponse) {
  switch (request.action) {
    case 'toggleProtection':
      protectionEnabled = request.enabled;
      await saveSettings();
      sendResponse({ success: true, enabled: protectionEnabled });
      break;
      
    case 'getSettings':
      sendResponse({
        protectionEnabled,
        threadCount,
        updateFrequency,
        sharingEnabled,
        selectedCountry
      });
      break;
      
    case 'updateSettings':
      if (request.threadCount !== undefined) threadCount = request.threadCount;
      if (request.updateFrequency !== undefined) updateFrequency = request.updateFrequency;
      if (request.sharingEnabled !== undefined) sharingEnabled = request.sharingEnabled;
      if (request.selectedCountry !== undefined) selectedCountry = request.selectedCountry;
      await saveSettings();
      sendResponse({ success: true });
      break;
      
    case 'detectTracker':
      const tracker = detectTracker(request.url);
      sendResponse({ tracker, isTracker: tracker !== null });
      break;
      
    case 'generateIdentity':
      const identity = generateSyntheticIdentity();
      sendResponse({ identity });
      break;
      
    case 'poisonCookie':
      const poisoned = poisonCookie(request.name, request.value);
      sendResponse(poisoned);
      break;
      
    case 'getLog':
      sendResponse({ log: detectionLog.slice(-100) }); // Last 100 entries
      break;
      
    case 'clearLog':
      detectionLog = [];
      sendResponse({ success: true });
      break;
      
    default:
      sendResponse({ error: 'Unknown action' });
  }
}

function detectTracker(url) {
  const urlLower = url.toLowerCase();
  for (const [tracker, domains] of Object.entries(TRACKER_PATTERNS)) {
    for (const domain of domains) {
      if (urlLower.includes(domain)) {
        return tracker;
      }
    }
  }
  return null;
}

function initializeIdentities() {
  // Generate initial pool of synthetic identities
  syntheticIdentities = [];
  for (let i = 0; i < 50; i++) {
    syntheticIdentities.push(generateSyntheticIdentity());
  }
}

function generateSyntheticIdentity() {
  const firstNames = ['James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda', 'William', 'Elizabeth'];
  const lastNames = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Rodriguez', 'Martinez'];
  const domains = ['gmail.com', 'yahoo.com', 'outlook.com', 'protonmail.com'];
  const streets = ['Main St', 'Oak Ave', 'Maple Dr', 'Washington Blvd', 'Park Ave'];
  const cities = ['Springfield', 'Franklin', 'Clinton', 'Madison', 'Georgetown'];
  const states = ['CA', 'TX', 'FL', 'NY', 'PA', 'IL', 'OH', 'GA', 'NC', 'MI'];
  
  const firstName = firstNames[Math.floor(Math.random() * firstNames.length)];
  const lastName = lastNames[Math.floor(Math.random() * lastNames.length)];
  const domain = domains[Math.floor(Math.random() * domains.length)];
  const email = `${firstName.toLowerCase()}.${lastName.toLowerCase()}${Math.floor(Math.random() * 999)}@${domain}`;
  
  const phone = `(${200 + Math.floor(Math.random() * 799)}) ${200 + Math.floor(Math.random() * 799)}-${1000 + Math.floor(Math.random() * 8999)}`;
  
  const streetNum = 100 + Math.floor(Math.random() * 9899);
  const street = streets[Math.floor(Math.random() * streets.length)];
  const city = cities[Math.floor(Math.random() * cities.length)];
  const state = states[Math.floor(Math.random() * states.length)];
  const zip = 10000 + Math.floor(Math.random() * 89999);
  
  const year = 1950 + Math.floor(Math.random() * 50);
  const month = 1 + Math.floor(Math.random() * 12);
  const day = 1 + Math.floor(Math.random() * 28);
  const birthDate = `${year}-${String(month).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
  
  const ssnPartial = 1000 + Math.floor(Math.random() * 8999);
  
  // Fake credit card (not Luhn valid, just for poisoning)
  const ccPrefixes = ['4', '5', '3', '6'];
  let cc = ccPrefixes[Math.floor(Math.random() * ccPrefixes.length)];
  for (let i = 0; i < 15; i++) {
    cc += Math.floor(Math.random() * 10);
  }
  
  return {
    first_name: firstName,
    last_name: lastName,
    email,
    phone,
    address: `${streetNum} ${street}`,
    city,
    state,
    zip_code: String(zip),
    country: 'USA',
    birth_date: birthDate,
    ssn_partial: String(ssnPartial),
    credit_card: cc
  };
}

function poisonCookie(name, value) {
  const poisonedName = `_poison_${name}`;
  const poisonedValue = hashWithNoise(value);
  
  return {
    original: name,
    poisoned: poisonedName,
    value: poisonedValue
  };
}

function hashWithNoise(input) {
  // Simple hash with random component
  const timestamp = Date.now();
  const random = Math.random();
  const combined = `${input}-${timestamp}-${random}`;
  
  // Simple hash function
  let hash = 0;
  for (let i = 0; i < combined.length; i++) {
    const char = combined.charCodeAt(i);
    hash = ((hash << 5) - hash) + char;
    hash = hash & hash;
  }
  
  return Math.abs(hash).toString(16).padStart(32, '0');
}

async function saveSettings() {
  await chrome.storage.local.set({
    protectionEnabled,
    threadCount,
    updateFrequency,
    sharingEnabled,
    selectedCountry
  });
}

async function loadSettings() {
  const result = await chrome.storage.local.get([
    'protectionEnabled',
    'threadCount',
    'updateFrequency',
    'sharingEnabled',
    'selectedCountry'
  ]);
  
  if (result.protectionEnabled !== undefined) protectionEnabled = result.protectionEnabled;
  if (result.threadCount !== undefined) threadCount = result.threadCount;
  if (result.updateFrequency !== undefined) updateFrequency = result.updateFrequency;
  if (result.sharingEnabled !== undefined) sharingEnabled = result.sharingEnabled;
  if (result.selectedCountry !== undefined) selectedCountry = result.selectedCountry;
}

function startPeriodicTasks() {
  // Clean up old log entries every hour
  chrome.alarms.create('cleanupLog', { periodInMinutes: 60 });
}

chrome.alarms.onAlarm.addListener((alarm) => {
  if (alarm.name === 'cleanupLog') {
    // Keep only last 1000 entries
    if (detectionLog.length > 1000) {
      detectionLog = detectionLog.slice(-1000);
    }
  }
});

function logDetection(type, data) {
  const entry = {
    timestamp: new Date().toISOString(),
    type,
    data
  };
  
  detectionLog.push(entry);
  
  // Limit log size
  if (detectionLog.length > 1000) {
    detectionLog = detectionLog.slice(-1000);
  }
}

// Load settings on startup
loadSettings();
