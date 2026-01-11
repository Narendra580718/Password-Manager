#!/usr/bin/env python3
"""
SecurePass Manager - Main Entry Point
"""

import customtkinter as ctk
from app import SecurePassManager

# Configure appearance
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def main():
    """Main application entry point"""
    try:
        app = SecurePassManager()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()