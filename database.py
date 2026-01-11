"""
Database management for password storage
"""

import os
import json
import uuid
from datetime import datetime
import pickle

class DatabaseManager:
    def __init__(self, data_dir="data"):
        """
        Initialize database manager
        """
        self.data_dir = data_dir
        self.data_file = os.path.join(data_dir, "passwords.dat")
        
        # Create data directory if it doesn't exist
        os.makedirs(data_dir, exist_ok=True)
        
        # Initialize database
        self._init_database()
    
    def _init_database(self):
        """Initialize database files"""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'wb') as f:
                pickle.dump({}, f)
    
    def save_entry(self, encrypted_data):
        """
        Save encrypted password entry
        """
        try:
            # Generate unique ID
            entry_id = str(uuid.uuid4())
            timestamp = datetime.now().isoformat()
            
            # Load current data
            with open(self.data_file, 'rb') as f:
                data = pickle.load(f)
            
            # Add new entry
            data[entry_id] = {
                "data": encrypted_data,
                "created": timestamp,
                "modified": timestamp
            }
            
            # Save data
            with open(self.data_file, 'wb') as f:
                pickle.dump(data, f)
            
            return entry_id
            
        except Exception as e:
            print(f"Error saving entry: {e}")
            return None
    
    def get_all_entries(self):
        """
        Get all entries
        """
        try:
            if not os.path.exists(self.data_file):
                return []
                
            with open(self.data_file, 'rb') as f:
                data = pickle.load(f)
            
            entries = []
            for entry_id, entry_data in data.items():
                entries.append({
                    "id": entry_id,
                    "data": entry_data["data"],
                    "created": entry_data["created"],
                    "modified": entry_data["modified"]
                })
            
            return entries
            
        except Exception as e:
            print(f"Error getting all entries: {e}")
            return []
    
    def delete_entry(self, entry_id):
        """
        Delete entry by ID
        """
        try:
            # Load current data
            with open(self.data_file, 'rb') as f:
                data = pickle.load(f)
            
            # Delete entry
            if entry_id in data:
                del data[entry_id]
                
                # Save updated data
                with open(self.data_file, 'wb') as f:
                    pickle.dump(data, f)
                
                return True
            else:
                return False
                
        except Exception as e:
            print(f"Error deleting entry: {e}")
            return False
    
    def export_data(self, export_path):
        """
        Export database to file
        """
        try:
            if not os.path.exists(self.data_file):
                return False
                
            # Copy data file
            import shutil
            shutil.copy2(self.data_file, export_path)
            return True
            
        except Exception as e:
            print(f"Error exporting data: {e}")
            return False
    
    def import_data(self, import_path):
        """
        Import database from file
        """
        try:
            if not os.path.exists(import_path):
                return False
            
            # Backup current data
            backup_path = self.data_file + ".backup"
            if os.path.exists(self.data_file):
                import shutil
                shutil.copy2(self.data_file, backup_path)
            
            # Import new data
            import shutil
            shutil.copy2(import_path, self.data_file)
            
            return True
            
        except Exception as e:
            print(f"Error importing data: {e}")
            
            # Restore backup if exists
            if os.path.exists(backup_path):
                import shutil
                shutil.copy2(backup_path, self.data_file)
            
            return False