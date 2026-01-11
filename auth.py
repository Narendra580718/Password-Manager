"""
Authentication and encryption module
"""

import base64
import os
import json
import hashlib
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC  # Fixed import
from cryptography.exceptions import InvalidKey

class AuthManager:
    def __init__(self, config_manager):
        """
        Initialize authentication manager
        """
        self.config = config_manager
        self.cipher_suite = None
        
    def derive_key(self, password, salt=None):
        """
        Derive encryption key from password
        """
        if salt is None:
            salt = os.urandom(16)
        
        # Use PBKDF2HMAC for key derivation
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        return key, salt
    
    def hash_password(self, password):
        """
        Create password hash for verification
        """
        salt = os.urandom(32)
        key = hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            salt,
            100000
        )
        return base64.b64encode(salt + key).decode('utf-8')
    
    def verify_password(self, stored_hash, password):
        """
        Verify password against stored hash
        """
        try:
            decoded = base64.b64decode(stored_hash)
            salt = decoded[:32]
            key = decoded[32:]
            
            new_key = hashlib.pbkdf2_hmac(
                'sha256',
                password.encode('utf-8'),
                salt,
                100000
            )
            return key == new_key
        except:
            return False
    
    def create_account(self, password):
        """
        Create new user account
        """
        try:
            # Derive encryption key
            key, salt = self.derive_key(password)
            self.cipher_suite = Fernet(key)
            
            # Save salt to config
            self.config.set('auth', 'salt', base64.b64encode(salt).decode())
            
            # Hash and store password
            password_hash = self.hash_password(password)
            self.config.set('auth', 'password_hash', password_hash)
            
            # Save config
            self.config._save_config()
            
            return True
            
        except Exception as e:
            print(f"Error creating account: {e}")
            return False
    
    def authenticate(self, password):
        """
        Authenticate existing user
        """
        try:
            # Load salt from config
            salt_b64 = self.config.get('auth', 'salt')
            if not salt_b64:
                return False
                
            salt = base64.b64decode(salt_b64)
            
            # Verify password hash
            stored_hash = self.config.get('auth', 'password_hash')
            if not self.verify_password(stored_hash, password):
                return False
            
            # Derive key and create cipher suite
            key, _ = self.derive_key(password, salt)
            self.cipher_suite = Fernet(key)
            
            # Test encryption/decryption
            test_data = b"test"
            encrypted = self.cipher_suite.encrypt(test_data)
            decrypted = self.cipher_suite.decrypt(encrypted)
            
            return decrypted == test_data
                
        except (InvalidKey, Exception) as e:
            print(f"Authentication error: {e}")
            return False
    
    def encrypt_data(self, data):
        """
        Encrypt data
        """
        if not self.cipher_suite:
            raise ValueError("Not authenticated")
            
        if isinstance(data, dict):
            data_str = json.dumps(data)
        else:
            data_str = str(data)
            
        return self.cipher_suite.encrypt(data_str.encode())
    
    def decrypt_data(self, encrypted_data):
        """
        Decrypt data
        """
        if not self.cipher_suite:
            raise ValueError("Not authenticated")
            
        decrypted = self.cipher_suite.decrypt(encrypted_data)
        return json.loads(decrypted.decode())
    
    def change_master_password(self, new_password):
        """
        Change master password
        """
        try:
            # Derive new key
            key, salt = self.derive_key(new_password)
            
            # Update config
            self.config.set('auth', 'salt', base64.b64encode(salt).decode())
            
            # Update password hash
            password_hash = self.hash_password(new_password)
            self.config.set('auth', 'password_hash', password_hash)
            
            # Update cipher suite
            self.cipher_suite = Fernet(key)
            
            # Save config
            self.config._save_config()
            
            return True
            
        except Exception as e:
            print(f"Error changing password: {e}")
            return False
    
    def logout(self):
        """Log out user (clear sensitive data)"""
        self.cipher_suite = None