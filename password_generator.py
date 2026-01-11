"""
Password generation module
"""

import secrets
import string
import random

class PasswordGenerator:
    def __init__(self):
        """Initialize password generator"""
        self.character_sets = {
            'lower': string.ascii_lowercase,
            'upper': string.ascii_uppercase,
            'digits': string.digits,
            'special': "!@#$%^&*()_+-=[]{}|;:,.<>?"
        }
    
    def generate(self, length=16, use_upper=True, use_lower=True, 
                use_digits=True, use_special=True):
        """
        Generate a random password
        
        Args:
            length: Password length (8-64)
            use_upper: Include uppercase letters
            use_lower: Include lowercase letters
            use_digits: Include digits
            use_special: Include special characters
            
        Returns:
            str: Generated password
        """
        # Validate length
        if length < 8:
            length = 8
        elif length > 64:
            length = 64
        
        # Determine which character sets to use
        char_sets = []
        if use_lower:
            char_sets.append(self.character_sets['lower'])
        if use_upper:
            char_sets.append(self.character_sets['upper'])
        if use_digits:
            char_sets.append(self.character_sets['digits'])
        if use_special:
            char_sets.append(self.character_sets['special'])
        
        # Ensure at least one character set is selected
        if not char_sets:
            char_sets = [self.character_sets['lower'] + self.character_sets['upper']]
        
        # Generate password
        password = []
        
        # Ensure at least one character from each selected set
        for char_set in char_sets:
            password.append(secrets.choice(char_set))
        
        # Fill remaining characters
        all_chars = ''.join(char_sets)
        for _ in range(length - len(password)):
            password.append(secrets.choice(all_chars))
        
        # Shuffle the password
        secrets.SystemRandom().shuffle(password)
        
        return ''.join(password)
    
    def estimate_strength(self, password):
        """
        Estimate password strength
        
        Args:
            password: Password to evaluate
            
        Returns:
            dict: Strength metrics
        """
        if not password:
            return {"score": 0, "strength": "Very Weak", "feedback": []}
        
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 12:
            score += 2
        elif len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
        # Character variety checks
        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)
        
        if has_upper:
            score += 1
        else:
            feedback.append("Add uppercase letters")
        
        if has_lower:
            score += 1
        else:
            feedback.append("Add lowercase letters")
        
        if has_digit:
            score += 1
        else:
            feedback.append("Add numbers")
        
        if has_special:
            score += 1
        else:
            feedback.append("Add special characters")
        
        # Common patterns check (simplified)
        common_patterns = ['123', 'abc', 'qwerty', 'password', 'admin']
        if any(pattern in password.lower() for pattern in common_patterns):
            score -= 1
            feedback.append("Avoid common patterns")
        
        # Determine strength level
        if score >= 6:
            strength = "Very Strong"
        elif score >= 5:
            strength = "Strong"
        elif score >= 4:
            strength = "Good"
        elif score >= 3:
            strength = "Fair"
        else:
            strength = "Weak"
        
        return {
            "score": score,
            "strength": strength,
            "feedback": feedback
        }
    
    def generate_memorable(self, word_count=4, separator="-", capitalize=True):
        """
        Generate a memorable passphrase
        
        Args:
            word_count: Number of words (3-6)
            separator: Word separator
            capitalize: Capitalize words
            
        Returns:
            str: Generated passphrase
        """
        # Common word list (you can expand this)
        word_list = [
            'apple', 'banana', 'cherry', 'dragon', 'elephant', 'forest',
            'garden', 'hammer', 'island', 'jungle', 'knight', 'lemon',
            'mountain', 'ninja', 'orange', 'penguin', 'quasar', 'river',
            'sunset', 'tiger', 'umbrella', 'volcano', 'water', 'xylophone',
            'yellow', 'zebra', 'airplane', 'basket', 'candle', 'desert'
        ]
        
        # Validate word count
        if word_count < 3:
            word_count = 3
        elif word_count > 6:
            word_count = 6
        
        # Select random words
        words = secrets.sample(word_list, word_count)
        
        # Apply formatting
        if capitalize:
            words = [w.capitalize() for w in words]
        
        # Add random digit at the end
        words.append(str(secrets.choice(string.digits)))
        
        return separator.join(words)