// NIFLHEIM Alerts Stub
// Placeholder for web accessible alerts module

const alerts = {
  show: function(message, type = 'info') {
    console.log(`[NIFLHEIM Alert][${type}]: ${message}`);
  },
  warn: function(message) {
    this.show(message, 'warning');
  },
  error: function(message) {
    this.show(message, 'error');
  }
};

// Export for content script access
if (typeof window !== 'undefined') {
  window.NiflheimAlerts = alerts;
}
