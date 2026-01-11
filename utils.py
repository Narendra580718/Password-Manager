"""
Utility functions and classes
"""

import os
import json
import base64
import hashlib
from datetime import datetime

class ConfigManager:
    def __init__(self, config_dir="."):
        """
        Initialize configuration manager
        """
        self.config_dir = config_dir
        self.config_file = os.path.join(config_dir, "config.json")
        
        # Create config directory if it doesn't exist
        os.makedirs(config_dir, exist_ok=True)
        
        # Load or create config
        self.config = self._load_config()
    
    def _load_config(self):
        """
        Load configuration from file
        """
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading config: {e}")
                return self._create_default_config()
        else:
            return self._create_default_config()
    
    def _create_default_config(self):
        """
        Create default configuration
        """
        default_config = {
            "app": {
                "version": "1.0.0",
                "first_run": True,
                "theme": "dark",
                "language": "en"
            },
            "security": {
                "clear_clipboard": True,
                "clipboard_timeout": 30,
                "auto_lock": True,
                "lock_timeout": 300
            },
            "ui": {
                "font_size": 12,
                "font_family": "Segoe UI",
                "animations": True
            },
            "auth": {
                "salt": "",
                "password_hash": ""
            }
        }
        
        # Save default config
        self._save_config(default_config)
        
        return default_config
    
    def _save_config(self, config=None):
        """
        Save configuration to file
        """
        try:
            if config is None:
                config = self.config
            
            with open(self.config_file, 'w') as f:
                json.dump(config, f, indent=2)
            
            return True
            
        except IOError as e:
            print(f"Error saving config: {e}")
            return False
    
    def get(self, section, key, default=None):
        """
        Get configuration value
        """
        if section in self.config and key in self.config[section]:
            return self.config[section][key]
        return default
    
    def set(self, section, key, value):
        """
        Set configuration value
        """
        if section not in self.config:
            self.config[section] = {}
        
        self.config[section][key] = value
        return self._save_config()
    
    def delete(self, section, key):
        """
        Delete configuration key
        """
        if section in self.config and key in self.config[section]:
            del self.config[section][key]
            return self._save_config()
        return False
    
    def get_all(self):
        """
        Get all configuration
        """
        return self.config.copy()
    
    def reset(self):
        """Reset configuration to defaults"""
        self.config = self._create_default_config()
        return True


class SecurityUtils:
    @staticmethod
    def generate_salt(length=32):
        """
        Generate cryptographic salt
        """
        return os.urandom(length)
    
    @staticmethod
    def hash_data(data, algorithm='sha256'):
        """
        Hash data
        """
        if isinstance(data, str):
            data = data.encode('utf-8')
        
        if algorithm == 'sha256':
            return hashlib.sha256(data).hexdigest()
        elif algorithm == 'sha512':
            return hashlib.sha512(data).hexdigest()
        elif algorithm == 'blake2b':
            return hashlib.blake2b(data).hexdigest()
        else:
            raise ValueError(f"Unsupported algorithm: {algorithm}")
    
    @staticmethod
    def timing_safe_compare(a, b):
        """
        Timing-safe comparison
        """
        return hashlib.sha256(a.encode()).digest() == hashlib.sha256(b.encode()).digest()