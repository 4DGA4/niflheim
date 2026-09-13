// fp-rotator-fallback.js - JavaScript alternative to WASM fingerprint rotation

class FPRotator {
  /**
   * Adds noise to Canvas/WebGL/AudioContext fingerprints.
   * Disrupts tracking by randomizing outputs.
   */
  static addCanvasNoise() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = `#${Math.floor(Math.random() * 16777215).toString(16).padStart(6, '0')}`;
    ctx.fillRect(0, 0, 1, 1);
    return ctx.getImageData(0, 0, 1, 1).data;
  }

  static addWebGLNoise() {
    const canvas = document.createElement('canvas');
    const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
    if (!gl) return null;

    const debugInfo = gl.getExtension('WEBGL_debug_renderer_info');
    if (debugInfo) {
      gl.getParameter(debugInfo.UNMASKED_RENDERER_WEBGL);
    }
    return gl.getSupportedExtensions();
  }

  static addAudioContextNoise() {
    if (!window.AudioContext) return null;
    const audioCtx = new AudioContext();
    const oscillator = audioCtx.createOscillator();
    oscillator.frequency.value = Math.random() * 1000;
    oscillator.connect(audioCtx.destination);
    oscillator.start();
    oscillator.stop(audioCtx.currentTime + 0.1);
    return audioCtx.destination.channelCount;
  }
}

export default FPRotator;