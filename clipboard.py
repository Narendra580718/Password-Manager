"""
Clipboard management module
"""

import pyperclip
import time
from threading import Thread

class ClipboardManager:
    def __init__(self, clear_timeout=30):
        """
        Initialize clipboard manager
        """
        self.clear_timeout = clear_timeout
        self.clear_thread = None
        self.stop_clear = False
    
    def copy(self, text, clear_after=True):
        """
        Copy text to clipboard
        """
        try:
            pyperclip.copy(text)
            
            # Start clear thread if enabled
            if clear_after and self.clear_timeout > 0:
                self._start_clear_thread()
            
            return True
            
        except Exception as e:
            print(f"Error copying to clipboard: {e}")
            return False
    
    def paste(self):
        """
        Get text from clipboard
        """
        try:
            return pyperclip.paste()
        except Exception as e:
            print(f"Error pasting from clipboard: {e}")
            return ""
    
    def clear(self):
        """Clear clipboard"""
        try:
            pyperclip.copy("")
            return True
        except Exception as e:
            print(f"Error clearing clipboard: {e}")
            return False
    
    def _start_clear_thread(self):
        """Start thread to clear clipboard after timeout"""
        if self.clear_thread and self.clear_thread.is_alive():
            self.stop_clear = True
            self.clear_thread.join(timeout=1)
        
        self.stop_clear = False
        self.clear_thread = Thread(target=self._clear_after_timeout)
        self.clear_thread.daemon = True
        self.clear_thread.start()
    
    def _clear_after_timeout(self):
        """
        Clear clipboard after timeout
        """
        start_time = time.time()
        
        while time.time() - start_time < self.clear_timeout:
            if self.stop_clear:
                return
            time.sleep(0.1)
        
        if not self.stop_clear:
            self.clear()
    
    def cancel_clear(self):
        """Cancel scheduled clipboard clearing"""
        self.stop_clear = True
        if self.clear_thread and self.clear_thread.is_alive():
            self.clear_thread.join(timeout=1)