"""
Data Poisoning Toolkit - Core Module
Adversarial techniques for counter-surveillance operations
"""

import numpy as np
import hashlib
import json
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import random


@dataclass
class SyntheticIdentity:
    """Generate synthetic identities for data poisoning"""
    first_name: str
    last_name: str
    email: str
    phone: str
    address: str
    city: str
    state: str
    zip_code: str
    country: str
    birth_date: str
    ssn_partial: str  # Last 4 digits only
    credit_card: str
    occupation: str
    company: str
    
    def to_dict(self) -> Dict[str, str]:
        return {
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "phone": self.phone,
            "address": self.address,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "country": self.country,
            "birth_date": self.birth_date,
            "ssn_partial": self.ssn_partial,
            "credit_card": self.credit_card,
            "occupation": self.occupation,
            "company": self.company
        }


class IdentityGenerator:
    """Generate synthetic identities for form poisoning"""
    
    FIRST_NAMES = [
        "James", "Mary", "John", "Patricia", "Robert", "Jennifer", "Michael", "Linda",
        "William", "Elizabeth", "David", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
        "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Nancy", "Daniel", "Lisa",
        "Matthew", "Betty", "Anthony", "Margaret", "Donald", "Sandra", "Steven", "Ashley",
        "Paul", "Kimberly", "Andrew", "Emily", "Joshua", "Donna", "Kenneth", "Michelle",
        "Kevin", "Dorothy", "Brian", "Carol", "George", "Amanda", "Edward", "Melissa",
        "Ronald", "Deborah", "Timothy", "Stephanie", "Jason", "Rebecca", "Jeffrey", "Sharon"
    ]
    
    LAST_NAMES = [
        "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
        "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
        "Thomas", "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson",
        "White", "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker",
        "Young", "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
        "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
        "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker"
    ]
    
    STREETS = ["Main St", "Oak Ave", "Maple Dr", "Washington Blvd", "Park Ave", "Lake Rd",
               "Hill Ct", "River Rd", "Church St", "High St", "Mill Rd", "Union St"]
    
    CITIES = [
        "Springfield", "Franklin", "Clinton", "Madison", "Georgetown", "Salem",
        "Fairview", "Greenville", "Bristol", "Manchester", "Marion", "Oxford",
        "Dayton", "Richmond", "Auburn", "Concord", "Albany", "Lincoln"
    ]
    
    STATES = ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI",
              "NJ", "VA", "WA", "AZ", "MA", "TN", "IN", "MO", "MD", "WI"]
    
    OCCUPATIONS = [
        "Software Engineer", "Teacher", "Nurse", "Accountant", "Manager",
        "Sales Representative", "Analyst", "Consultant", "Designer", "Writer",
        "Marketing Specialist", "Project Manager", "Data Scientist", "Architect"
    ]
    
    COMPANIES = [
        "TechCorp", "Global Industries", "Innovative Solutions", "Digital Dynamics",
        "Advanced Systems", "Creative Works", "Strategic Partners", "Prime Services"
    ]
    
    def __init__(self, seed: Optional[int] = None):
        if seed is not None:
            random.seed(seed)
    
    def generate(self, count: int = 1) -> List[SyntheticIdentity]:
        """Generate synthetic identities"""
        identities = []
        for _ in range(count):
            identity = self._generate_single()
            identities.append(identity)
        return identities
    
    def _generate_single(self) -> SyntheticIdentity:
        first = random.choice(self.FIRST_NAMES)
        last = random.choice(self.LAST_NAMES)
        
        # Generate email
        email_domains = ["gmail.com", "yahoo.com", "outlook.com", "protonmail.com", "mail.com"]
        email = f"{first.lower()}.{last.lower()}{random.randint(1, 999)}@{random.choice(email_domains)}"
        
        # Generate phone (fake format)
        phone = f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
        
        # Generate address
        street_num = random.randint(100, 9999)
        street = random.choice(self.STREETS)
        city = random.choice(self.CITIES)
        state = random.choice(self.STATES)
        zip_code = f"{random.randint(10000, 99999)}"
        
        # Generate birth date
        year = random.randint(1950, 2000)
        month = random.randint(1, 12)
        day = random.randint(1, 28)
        birth_date = f"{year:04d}-{month:02d}-{day:02d}"
        
        # Generate SSN partial (last 4)
        ssn_partial = f"{random.randint(1000, 9999)}"
        
        # Generate fake credit card (Luhn-valid would be better, but this works for poisoning)
        cc_prefixes = ["4", "5", "3", "6"]  # Visa, MC, Amex, Discover
        cc = random.choice(cc_prefixes)
        for _ in range(15):
            cc += str(random.randint(0, 9))
        
        occupation = random.choice(self.OCCUPATIONS)
        company = random.choice(self.COMPANIES)
        
        return SyntheticIdentity(
            first_name=first,
            last_name=last,
            email=email,
            phone=phone,
            address=f"{street_num} {street}",
            city=city,
            state=state,
            zip_code=zip_code,
            country="USA",
            birth_date=birth_date,
            ssn_partial=ssn_partial,
            credit_card=cc,
            occupation=occupation,
            company=company
        )


class AdversarialPerturbation:
    """Generate adversarial perturbations for image/audio poisoning"""
    
    @staticmethod
    def add_noise(image: np.ndarray, epsilon: float = 0.01, 
                  method: str = "random") -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Add adversarial noise to an image
        
        Args:
            image: Input image as numpy array (normalized to [0, 1])
            epsilon: Maximum perturbation magnitude
            method: "random", "gradient", or "square"
            
        Returns:
            Perturbed image and metadata
        """
        if method == "random":
            noise = np.random.uniform(-epsilon, epsilon, image.shape).astype(np.float32)
            perturbed = np.clip(image + noise, 0, 1)
            
        elif method == "gradient":
            # Simplified gradient-based attack (would need model access in practice)
            gradient = np.random.randn(*image.shape).astype(np.float32)
            gradient = gradient / (np.linalg.norm(gradient) + 1e-8)
            perturbed = np.clip(image + epsilon * gradient, 0, 1)
            
        elif method == "square":
            # Square attack - perturb random square regions
            perturbed = image.copy()
            h, w = image.shape[:2]
            square_size = max(int(min(h, w) * 0.2), 10)
            
            for _ in range(10):
                x = random.randint(0, max(0, w - square_size))
                y = random.randint(0, max(0, h - square_size))
                noise = np.random.uniform(-epsilon, epsilon, (square_size, square_size))
                if len(image.shape) == 3:
                    noise = np.repeat(noise[:, :, np.newaxis], image.shape[2], axis=2)
                perturbed[y:y+square_size, x:x+square_size] += noise
            
            perturbed = np.clip(perturbed, 0, 1)
        else:
            raise ValueError(f"Unknown method: {method}")
        
        metadata = {
            "method": method,
            "epsilon": epsilon,
            "noise_magnitude": float(np.mean(np.abs(perturbed - image))),
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        
        return perturbed, metadata
    
    @staticmethod
    def create_adversarial_patch(image_shape: Tuple[int, ...], 
                                 patch_size: int = 50,
                                 pattern: str = "checkerboard") -> np.ndarray:
        """
        Create an adversarial patch that can be overlaid on images
        
        Args:
            image_shape: Shape of target image (H, W, C) or (H, W)
            patch_size: Size of the patch
            pattern: "checkerboard", "random", or "gradient"
            
        Returns:
            Adversarial patch as numpy array
        """
        if len(image_shape) == 2:
            h, w = image_shape
            channels = 1
        else:
            h, w, channels = image_shape
        
        if pattern == "checkerboard":
            patch = np.zeros((patch_size, patch_size, channels))
            block_size = max(patch_size // 4, 4)
            for i in range(0, patch_size, block_size):
                for j in range(0, patch_size, block_size):
                    if (i // block_size + j // block_size) % 2 == 0:
                        patch[i:i+block_size, j:j+block_size] = 1.0
                        
        elif pattern == "random":
            patch = np.random.uniform(0, 1, (patch_size, patch_size, channels))
            
        elif pattern == "gradient":
            x = np.linspace(0, 1, patch_size)
            y = np.linspace(0, 1, patch_size)
            xx, yy = np.meshgrid(x, y)
            patch = np.stack([xx, yy, np.ones_like(xx)], axis=-1)[:,:,:channels]
        else:
            raise ValueError(f"Unknown pattern: {pattern}")
        
        return patch


class FingerprintPoisoner:
    """Poison browser fingerprinting attempts"""
    
    @staticmethod
    def poison_canvas_fingerprint(ctx_hash: str) -> str:
        """
        Generate alternative canvas hash to poison fingerprinting
        
        Args:
            ctx_hash: Original canvas context hash
            
        Returns:
            Modified hash that appears legitimate
        """
        # Add deterministic but unpredictable noise
        noise = hashlib.sha256(
            (ctx_hash + str(datetime.utcnow().timestamp())).encode()
        ).hexdigest()[:16]
        
        # XOR first 16 chars with noise
        original = ctx_hash[:16]
        poisoned = ''.join(
            chr(ord(a) ^ ord(b)) for a, b in zip(original, noise)
        )
        
        return poisoned + ctx_hash[16:]
    
    @staticmethod
    def poison_webgl_params(params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Poison WebGL fingerprinting parameters
        
        Args:
            params: Original WebGL parameters
            
        Returns:
            Modified parameters
        """
        poisoned = params.copy()
        
        # Add small variations to numeric values
        if "MAX_VIEWPORT_DIMS" in poisoned:
            dims = poisoned["MAX_VIEWPORT_DIMS"]
            if isinstance(dims, (list, tuple)) and len(dims) == 2:
                poisoned["MAX_VIEWPORT_DIMS"] = [
                    dims[0] + random.randint(-10, 10),
                    dims[1] + random.randint(-10, 10)
                ]
        
        # Add fake extensions
        fake_extensions = [
            "WEBGL_debug_renderer_info_FAKE",
            "WEBGL_lose_context_FAKE",
            "OES_texture_float_FAKE"
        ]
        if "EXTENSIONS" in poisoned:
            poisoned["EXTENSIONS"] = list(poisoned["EXTENSIONS"]) + fake_extensions
        
        return poisoned
    
    @staticmethod
    def poison_audio_fingerprint(audio_hash: str) -> str:
        """
        Poison audio context fingerprinting
        
        Args:
            audio_hash: Original audio fingerprint hash
            
        Returns:
            Modified hash
        """
        # Reverse and add timestamp noise
        reversed_hash = audio_hash[::-1]
        timestamp_noise = hashlib.md5(
            str(datetime.utcnow().timestamp()).encode()
        ).hexdigest()[:8]
        
        return timestamp_noise + reversed_hash[8:]
    
    @staticmethod
    def generate_timer_jitter(base_time: float, jitter_ms: float = 5.0) -> float:
        """
        Add jitter to timer measurements to poison timing-based fingerprinting
        
        Args:
            base_time: Base timestamp in milliseconds
            jitter_ms: Maximum jitter in milliseconds
            
        Returns:
            Jittered timestamp
        """
        jitter = random.uniform(-jitter_ms, jitter_ms)
        return base_time + jitter


class TrackerPoisoner:
    """Detect and poison common tracking mechanisms"""
    
    TRACKER_DOMAINS = {
        "google": ["google-analytics.com", "googletagmanager.com", "googleadservices.com"],
        "facebook": ["facebook.com", "facebook.net", "fbcdn.net"],
        "amazon": ["amazon-adsystem.com", "amazonaws.com"],
        "microsoft": ["microsoft.com", "live.com", "bing.com"],
        "adobe": ["adobe.com", "omtrdc.net"],
        "oracle": ["oracle.com", "eloqua.com"],
        "salesforce": ["salesforce.com", "force.com"],
    }
    
    @staticmethod
    def detect_tracker(url: str) -> Optional[str]:
        """
        Detect which tracker service a URL belongs to
        
        Args:
            url: URL to check
            
        Returns:
            Tracker name or None
        """
        url_lower = url.lower()
        for tracker, domains in TrackerPoisoner.TRACKER_DOMAINS.items():
            for domain in domains:
                if domain in url_lower:
                    return tracker
        return None
    
    @staticmethod
    def poison_cookie(name: str, value: str) -> Tuple[str, str]:
        """
        Poison tracking cookies
        
        Args:
            name: Cookie name
            value: Cookie value
            
        Returns:
            Modified name and value
        """
        # Add prefix to indicate poisoned
        poisoned_name = f"_poison_{name}"
        
        # Generate fake value with same structure
        if len(value) > 16:
            # Likely a tracking ID - replace with fake UUID-like string
            poisoned_value = hashlib.sha256(
                (value + str(random.random())).encode()
            ).hexdigest()
        else:
            # Short value - just hash it
            poisoned_value = hashlib.md5(
                (value + str(random.random())).encode()
            ).hexdigest()[:len(value)]
        
        return poisoned_name, poisoned_value
    
    @staticmethod
    def generate_link_walking_targets(base_domain: str, count: int = 10) -> List[str]:
        """
        Generate fake URLs for link walking (noise generation)
        
        Args:
            base_domain: Base domain to generate paths for
            count: Number of URLs to generate
            
        Returns:
            List of fake URLs
        """
        fake_paths = [
            "/about", "/contact", "/products", "/services", "/blog",
            "/news", "/careers", "/privacy", "/terms", "/faq",
            "/support", "/documentation", "/api", "/status", "/metrics"
        ]
        
        urls = []
        for i in range(count):
            path = random.choice(fake_paths)
            query = f"?session={random.randint(1000, 9999)}&ref={random.randint(100, 999)}"
            urls.append(f"https://{base_domain}{path}{query}")
        
        return urls


class DataPoisoningPipeline:
    """Main pipeline for coordinating data poisoning operations"""
    
    def __init__(self, seed: Optional[int] = None):
        self.identity_gen = IdentityGenerator(seed=seed)
        self.adv_perturbation = AdversarialPerturbation()
        self.fingerprint_poisoner = FingerprintPoisoner()
        self.tracker_poisoner = TrackerPoisoner()
        self.log: List[Dict[str, Any]] = []
    
    def poison_form_data(self, form_fields: Dict[str, str], 
                         use_synthetic: bool = True) -> Dict[str, str]:
        """
        Poison form submission data
        
        Args:
            form_fields: Original form data
            use_synthetic: If True, replace with synthetic identity
            
        Returns:
            Poisoned form data
        """
        if use_synthetic:
            identity = self.identity_gen.generate(1)[0]
            poisoned = {
                "first_name": identity.first_name,
                "last_name": identity.last_name,
                "email": identity.email,
                "phone": identity.phone,
                "address": identity.address,
                "city": identity.city,
                "state": identity.state,
                "zip": identity.zip_code,
                "country": identity.country
            }
        else:
            # Just add noise to existing data
            poisoned = form_fields.copy()
            for key, value in poisoned.items():
                if "email" in key.lower():
                    poisoned[key] = hashlib.md5(value.encode()).hexdigest() + "@fake.com"
                elif "phone" in key.lower():
                    poisoned[key] = f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}"
        
        self._log_operation("form_poisoning", len(poisoned))
        return poisoned
    
    def poison_image(self, image: np.ndarray, 
                     method: str = "random",
                     epsilon: float = 0.01) -> Tuple[np.ndarray, Dict[str, Any]]:
        """
        Poison an image with adversarial perturbations
        
        Args:
            image: Input image
            method: Perturbation method
            epsilon: Perturbation magnitude
            
        Returns:
            Poisoned image and metadata
        """
        perturbed, metadata = self.adv_perturbation.add_noise(image, epsilon, method)
        self._log_operation("image_poisoning", metadata)
        return perturbed, metadata
    
    def detect_and_poison(self, url: str, cookies: Dict[str, str] = None) -> Dict[str, Any]:
        """
        Detect trackers and poison them
        
        Args:
            url: URL to check
            cookies: Optional cookies to poison
            
        Returns:
            Detection and poisoning results
        """
        tracker = self.tracker_poisoner.detect_tracker(url)
        result = {
            "url": url,
            "tracker_detected": tracker,
            "cookies_poisoned": []
        }
        
        if tracker and cookies:
            for name, value in cookies.items():
                poisoned_name, poisoned_value = self.tracker_poisoner.poison_cookie(name, value)
                result["cookies_poisoned"].append({
                    "original": name,
                    "poisoned": poisoned_name,
                    "value_hash": hashlib.md5(poisoned_value.encode()).hexdigest()
                })
        
        self._log_operation("tracker_detection", result)
        return result
    
    def _log_operation(self, operation: str, data: Any):
        """Log poisoning operation"""
        self.log.append({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "operation": operation,
            "data": data
        })
    
    def get_log(self) -> List[Dict[str, Any]]:
        """Get operation log"""
        return self.log
    
    def export_log(self, filepath: str):
        """Export log to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(self.log, f, indent=2)


# Convenience function
def create_pipeline(seed: Optional[int] = None) -> DataPoisoningPipeline:
    """Create a new data poisoning pipeline"""
    return DataPoisoningPipeline(seed=seed)
