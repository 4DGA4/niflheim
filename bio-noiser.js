// bio-noiser.js - Keystroke/mouse/scroll timing perturbation

class BioNoiser {
  constructor() {
    this.jitterRange = {
      keystroke: { min: 50, max: 200 },   // ms
      mouse: { min: 1, max: 5 },         // px
      scroll: { min: 50, max: 300 }      // ms
    };
    this.eventListeners = [];
  }

  start() {
    // Keystroke noise
    this.addEventListener(document, 'keydown', (event) => this.perturbKeystroke(event));
    this.addEventListener(document, 'keyup', (event) => this.perturbKeystroke(event));

    // Mouse noise
    this.addEventListener(document, 'mousemove', (event) => this.perturbMouse(event));
    this.addEventListener(document, 'click', (event) => this.perturbMouse(event));

    // Scroll noise
    this.addEventListener(window, 'scroll', (event) => this.perturbScroll(event));
  }

  stop() {
    this.eventListeners.forEach(({ element, event, handler }) => {
      element.removeEventListener(event, handler);
    });
    this.eventListeners = [];
  }

  addEventListener(element, event, handler) {
    element.addEventListener(event, handler);
    this.eventListeners.push({ element, event, handler });
  }

  perturbKeystroke(event) {
    const jitter = this.getRandomJitter('keystroke');
    const originalTimeStamp = event.timeStamp;

    // Override timeStamp with jitter
    Object.defineProperty(event, 'timeStamp', {
      value: originalTimeStamp + jitter,
      writable: false
    });
    console.log(`[BioNoiser] Keystroke jitter: +${jitter}ms`);
  }

  perturbMouse(event) {
    if (event.type === 'mousemove') {
      const jitterX = this.getRandomJitter('mouse');
      const jitterY = this.getRandomJitter('mouse');

      // Perturb clientX/clientY
      Object.defineProperty(event, 'clientX', {
        value: event.clientX + jitterX,
        writable: false
      });
      Object.defineProperty(event, 'clientY', {
        value: event.clientY + jitterY,
        writable: false
      });
      console.log(`[BioNoiser] Mouse jitter: +${jitterX}px, +${jitterY}px`);
    }
  }

  perturbScroll(event) {
    const jitter = this.getRandomJitter('scroll');
    const originalTimeStamp = event.timeStamp;

    // Override timeStamp with jitter
    Object.defineProperty(event, 'timeStamp', {
      value: originalTimeStamp + jitter,
      writable: false
    });
    console.log(`[BioNoiser] Scroll jitter: +${jitter}ms`);
  }

  getRandomJitter(type) {
    const range = this.jitterRange[type];
    return Math.floor(Math.random() * (range.max - range.min + 1)) + range.min;
  }
}

// Export for module systems
export default BioNoiser;