// content-script.js - Inject BioNoiser and FPRotator into web pages
import BioNoiser from './bio-noiser.js';
import FPRotator from './fp-rotator-fallback.js';

// Initialize BioNoiser
const bioNoiser = new BioNoiser();
bioNoiser.start();

// Initialize FPRotator
FPRotator.addCanvasNoise();
FPRotator.addWebGLNoise();
FPRotator.addAudioContextNoise();

console.log('[niflheim] BioNoiser and FPRotator injected into page');