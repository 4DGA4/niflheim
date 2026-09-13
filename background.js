// Background script for niflheim
import NetObfuscator from './net-obfuscator.js';

// Initialize NetObfuscator (background-only)
const netObfuscator = new NetObfuscator();
netObfuscator.start();

console.log('niflheim background script loaded');