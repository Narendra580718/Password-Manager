"""
Build script for creating Password Manager executable
"""

import PyInstaller.__main__
import os
import shutil
import sys

def clean_build_dirs():
    """Clean up previous build directories"""
    dirs_to_remove = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_remove:
        if os.path.exists(dir_name):
            try:
                shutil.rmtree(dir_name)
                print(f"Removed {dir_name}/")
            except Exception as e:
                print(f"Error removing {dir_name}: {e}")
    
    # Remove spec files
    for file in os.listdir('.'):
        if file.endswith('.spec'):
            try:
                os.remove(file)
                print(f"Removed {file}")
            except Exception as e:
                print(f"Error removing {file}: {e}")

def create_exe():
    """Create the executable file"""
    
    # Define PyInstaller arguments
    args = [
        'main.py',  # Main script
        '--name=PasswordManager',  # Name of executable
        '--windowed',  # No console window
        '--onefile',  # Single executable file
        '--icon=app_icon.ico',  # Icon file (optional)
        '--add-data=config.json;.',  # Include config file
        '--add-data=data;data',  # Include data directory
        '--hidden-import=customtkinter',
        '--hidden-import=cryptography',
        '--hidden-import=pyperclip',
        '--hidden-import=json',
        '--hidden-import=hashlib',
        '--hidden-import=base64',
        '--hidden-import=os',
        '--hidden-import=sys',
        '--hidden-import=datetime',
        '--hidden-import=uuid',
        '--hidden-import=pickle',
        '--hidden-import=threading',
        '--hidden-import=tkinter',
        '--clean',  # Clean PyInstaller cache
        '--noconfirm',  # Replace output directory without confirmation
    ]
    
    print("Building executable...")
    PyInstaller.__main__.run(args)

def create_icon():
    """Create a simple icon file if it doesn't exist"""
    if not os.path.exists('app_icon.ico'):
        print("Creating default icon...")
        # Create a simple ICO file using PIL if available
        try:
            from PIL import Image, ImageDraw
            # Create a simple 64x64 icon
            img = Image.new('RGBA', (64, 64), (59, 89, 152))  # Blue background
            draw = ImageDraw.Draw(img)
            
            # Draw a lock symbol
            draw.rectangle([20, 25, 44, 45], fill=(255, 255, 255, 255))
            draw.ellipse([25, 15, 39, 29], fill=(255, 255, 255, 255))
            
            # Save as ICO
            img.save('app_icon.ico', format='ICO')
            print("Created app_icon.ico")
        except ImportError:
            print("PIL not available, skipping icon creation")
            print("You can create your own app_icon.ico file")

def create_config_template():
    """Create config template if it doesn't exist"""
    if not os.path.exists('config.json'):
        config = {
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
        
        import json
        with open('config.json', 'w') as f:
            json.dump(config, f, indent=2)
        print("Created config.json template")

def create_data_dir():
    """Create data directory if it doesn't exist"""
    if not os.path.exists('data'):
        os.makedirs('data')
        print("Created data/ directory")

def main():
    """Main build function"""
    print("=" * 50)
    print("Password Manager - Build Script")
    print("=" * 50)
    
    # Create necessary files and directories
    create_icon()
    create_config_template()
    create_data_dir()
    
    # Clean previous builds
    clean_build_dirs()
    
    # Create executable
    create_exe()
    
    print("\n" + "=" * 50)
    print("Build completed successfully!")
    print("=" * 50)
    print("\nYour executable is in the 'dist' folder:")
    print("→ dist/PasswordManager.exe")
    print("\nTo run the application, double-click PasswordManager.exe")
    
    # Offer to test the executable
    if sys.platform == 'win32' and os.path.exists('dist/PasswordManager.exe'):
        response = input("\nDo you want to test the executable now? (y/n): ")
        if response.lower() == 'y':
            print("\nLaunching PasswordManager.exe...")
            os.system('start dist/PasswordManager.exe')

if __name__ == "__main__":
    main()