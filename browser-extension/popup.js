/**
 * Niflheim Popup UI Controller
 */

document.addEventListener('DOMContentLoaded', async () => {
  // Load settings
  await loadSettings();
  
  // Load activity log
  await loadActivityLog();
  
  // Setup event listeners
  setupEventListeners();
});

async function loadSettings() {
  const response = await chrome.runtime.sendMessage({ action: 'getSettings' });
  
  if (response) {
    document.getElementById('protectionToggle').checked = response.protectionEnabled;
    document.getElementById('sharingToggle').checked = response.sharingEnabled;
    document.getElementById('threadSlider').value = response.threadCount;
    document.getElementById('threadValue').textContent = response.threadCount;
    document.getElementById('countrySelect').value = response.selectedCountry;
    
    updateStatusIndicator(response.protectionEnabled);
  }
}

async function loadActivityLog() {
  const response = await chrome.runtime.sendMessage({ action: 'getLog' });
  
  if (response && response.log) {
    renderActivityLog(response.log);
    updateStats(response.log);
  }
}

function renderActivityLog(log) {
  const logContainer = document.getElementById('activityLog');
  
  if (log.length === 0) {
    logContainer.innerHTML = '<div class="log-entry"><div class="log-timestamp">No activity yet</div></div>';
    return;
  }
  
  logContainer.innerHTML = '';
  
  // Show last 20 entries, newest first
  const recentLog = log.slice(-20).reverse();
  
  for (const entry of recentLog) {
    const entryDiv = document.createElement('div');
    entryDiv.className = 'log-entry';
    
    const timestamp = new Date(entry.timestamp).toLocaleTimeString();
    const type = entry.type || entry.operation || 'unknown';
    const data = JSON.stringify(entry.data).substring(0, 50);
    
    entryDiv.innerHTML = `
      <div class="log-timestamp">${timestamp}</div>
      <div>${type}: ${data}...</div>
    `;
    
    logContainer.appendChild(entryDiv);
  }
}

function updateStats(log) {
  let trackersDetected = 0;
  let cookiesPoisoned = 0;
  let formsPoisoned = 0;
  let fingerprintsBlocked = 0;
  
  for (const entry of log) {
    const type = entry.type || entry.operation || '';
    
    if (type.includes('tracker')) trackersDetected++;
    if (type.includes('cookie')) cookiesPoisoned++;
    if (type.includes('form')) formsPoisoned++;
    if (type.includes('fingerprint')) fingerprintsBlocked++;
  }
  
  document.getElementById('trackersDetected').textContent = trackersDetected;
  document.getElementById('cookiesPoisoned').textContent = cookiesPoisoned;
  document.getElementById('formsPoisoned').textContent = formsPoisoned;
  document.getElementById('fingerprintsBlocked').textContent = fingerprintsBlocked;
}

function updateStatusIndicator(enabled) {
  const dot = document.getElementById('statusDot');
  const text = document.getElementById('statusText');
  
  if (enabled) {
    dot.classList.remove('inactive');
    text.textContent = 'Protection Active';
  } else {
    dot.classList.add('inactive');
    text.textContent = 'Protection Disabled';
  }
}

function setupEventListeners() {
  // Protection toggle
  document.getElementById('protectionToggle').addEventListener('change', async (e) => {
    await chrome.runtime.sendMessage({
      action: 'toggleProtection',
      enabled: e.target.checked
    });
    updateStatusIndicator(e.target.checked);
  });
  
  // Sharing toggle
  document.getElementById('sharingToggle').addEventListener('change', async (e) => {
    await chrome.runtime.sendMessage({
      action: 'updateSettings',
      sharingEnabled: e.target.checked
    });
  });
  
  // Thread slider
  document.getElementById('threadSlider').addEventListener('input', (e) => {
    document.getElementById('threadValue').textContent = e.target.value;
  });
  
  document.getElementById('threadSlider').addEventListener('change', async (e) => {
    await chrome.runtime.sendMessage({
      action: 'updateSettings',
      threadCount: parseInt(e.target.value)
    });
  });
  
  // Country select
  document.getElementById('countrySelect').addEventListener('change', async (e) => {
    await chrome.runtime.sendMessage({
      action: 'updateSettings',
      selectedCountry: e.target.value
    });
  });
  
  // Refresh log
  document.getElementById('refreshLogBtn').addEventListener('click', loadActivityLog);
  
  // Clear log
  document.getElementById('clearLogBtn').addEventListener('click', async () => {
    await chrome.runtime.sendMessage({ action: 'clearLog' });
    loadActivityLog();
  });
  
  // Generate identity
  document.getElementById('generateIdentityBtn').addEventListener('click', async () => {
    const response = await chrome.runtime.sendMessage({ action: 'generateIdentity' });
    
    if (response && response.identity) {
      const identity = response.identity;
      const identityText = `
Name: ${identity.first_name} ${identity.last_name}
Email: ${identity.email}
Phone: ${identity.phone}
Address: ${identity.address}, ${identity.city}, ${identity.state} ${identity.zip_code}
DOB: ${identity.birth_date}
CC: ${identity.credit_card}
      `.trim();
      
      alert('Synthetic Identity Generated:\n\n' + identityText);
    }
  });
}
