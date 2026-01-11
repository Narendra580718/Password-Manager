"""
Main application class for SecurePass Manager
"""

import customtkinter as ctk
import os
from tkinter import messagebox

# Import local modules
import auth
import database
import ui
import password_generator
import clipboard
import utils

class SecurePassManager:
    def __init__(self):
        """Initialize the password manager application"""
        self.app = ctk.CTk()
        self.app.title("SecurePass Manager")
        self.app.geometry("1000x700")
        
        # Set window icon if exists
        if os.path.exists("app_icon.ico"):
            self.app.iconbitmap("app_icon.ico")
        
        # Initialize managers
        self.config = utils.ConfigManager()
        self.auth_manager = auth.AuthManager(self.config)
        self.db_manager = database.DatabaseManager()
        self.pass_generator = password_generator.PasswordGenerator()
        self.clipboard_manager = clipboard.ClipboardManager()
        self.ui_manager = ui.UIManager(self.app, self)
        
        # Application state
        self.is_authenticated = False
        
    def authenticate(self, password, is_new_account=False):
        """
        Authenticate user with master password
        """
        try:
            if is_new_account:
                success = self.auth_manager.create_account(password)
                if success:
                    messagebox.showinfo("Success", "Account created successfully!")
                    self.is_authenticated = True
                    self.ui_manager.show_main_screen()
                    return True
            else:
                success = self.auth_manager.authenticate(password)
                if success:
                    self.is_authenticated = True
                    self.ui_manager.show_main_screen()
                    return True
                else:
                    messagebox.showerror("Error", "Invalid password or corrupted data")
                    return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Authentication failed: {str(e)}")
            return False
    
    def save_password_entry(self, password_data):
        """
        Save a new password entry
        """
        try:
            if not self.is_authenticated:
                messagebox.showerror("Error", "Not authenticated")
                return False
                
            # Encrypt the password data
            encrypted_data = self.auth_manager.encrypt_data(password_data)
            
            # Save to database
            entry_id = self.db_manager.save_entry(encrypted_data)
            
            if entry_id:
                self.ui_manager.refresh_password_list()
                return True
            else:
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save password: {str(e)}")
            return False
    
    def get_all_passwords(self):
        """
        Get all password entries
        """
        try:
            if not self.is_authenticated:
                return []
                
            # Get encrypted entries from database
            encrypted_entries = self.db_manager.get_all_entries()
            decrypted_entries = []
            
            # Decrypt each entry
            for entry in encrypted_entries:
                try:
                    decrypted = self.auth_manager.decrypt_data(entry["data"])
                    decrypted["id"] = entry["id"]  # Add entry ID
                    decrypted_entries.append(decrypted)
                except:
                    continue  # Skip corrupted entries
                
            return decrypted_entries
            
        except Exception as e:
            print(f"Error loading passwords: {e}")
            return []
    
    def delete_password_entry(self, entry_id):
        """
        Delete a password entry
        """
        try:
            if not self.is_authenticated:
                return False
                
            success = self.db_manager.delete_entry(entry_id)
            
            if success:
                self.ui_manager.refresh_password_list()
                return True
            else:
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to delete password: {str(e)}")
            return False
    
    def search_passwords(self, search_term):
        """
        Search password entries
        """
        try:
            all_entries = self.get_all_passwords()
            search_term = search_term.lower()
            
            matching_entries = []
            for entry in all_entries:
                if (search_term in entry.get('website', '').lower() or 
                    search_term in entry.get('username', '').lower() or
                    search_term in entry.get('url', '').lower()):
                    matching_entries.append(entry)
                    
            return matching_entries
            
        except Exception as e:
            print(f"Search error: {e}")
            return []
    
    def generate_password(self, length=16, use_upper=True, use_lower=True, 
                         use_digits=True, use_special=True):
        """
        Generate a random password
        """
        return self.pass_generator.generate(
            length=length,
            use_upper=use_upper,
            use_lower=use_lower,
            use_digits=use_digits,
            use_special=use_special
        )
    
    def copy_to_clipboard(self, text):
        """
        Copy text to clipboard
        """
        return self.clipboard_manager.copy(text)
    
    def change_master_password(self, new_password):
        """
        Change master password
        """
        try:
            success = self.auth_manager.change_master_password(new_password)
            if success:
                messagebox.showinfo("Success", "Master password changed successfully!")
                return True
            else:
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to change password: {str(e)}")
            return False
    
    def export_data(self, file_path):
        """
        Export encrypted data to file
        """
        try:
            return self.db_manager.export_data(file_path)
        except Exception as e:
            messagebox.showerror("Error", f"Export failed: {str(e)}")
            return False
    
    def import_data(self, file_path):
        """
        Import encrypted data from file
        """
        try:
            success = self.db_manager.import_data(file_path)
            if success:
                self.ui_manager.refresh_password_list()
                return True
            else:
                return False
                
        except Exception as e:
            messagebox.showerror("Error", f"Import failed: {str(e)}")
            return False
    
    def logout(self):
        """Log out user"""
        self.is_authenticated = False
        self.auth_manager.logout()
        self.ui_manager.show_login_screen()
    
    def run(self):
        """Run the application"""
        self.app.mainloop()