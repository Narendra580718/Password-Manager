"""
User Interface for SecurePass Manager
"""

import customtkinter as ctk
from tkinter import messagebox, filedialog
import os
import threading

class UIManager:
    def __init__(self, root, app):
        """
        Initialize UI manager
        """
        self.root = root
        self.app = app
        self.current_screen = None
        
        # Password display tracking
        self.password_labels = {}
        self.password_values = {}
        self.password_visible = {}
        
        # Show initial screen
        self.show_login_screen()
    
    def show_login_screen(self):
        """Show login/register screen"""
        self._clear_screen()
        self.current_screen = "login"
        
        # Main container
        container = ctk.CTkFrame(self.root, corner_radius=20)
        container.pack(pady=100, padx=200, fill="both", expand=True)
        
        # Title
        title = ctk.CTkLabel(
            container,
            text="🔐 SecurePass Manager",
            font=("Segoe UI", 32, "bold")
        )
        title.pack(pady=(40, 10))
        
        subtitle = ctk.CTkLabel(
            container,
            text="Secure Password Storage",
            font=("Segoe UI", 16),
            text_color="gray"
        )
        subtitle.pack(pady=(0, 40))
        
        # Password entry
        self.password_entry = ctk.CTkEntry(
            container,
            placeholder_text="Master Password",
            show="•",
            width=300,
            height=45,
            font=("Segoe UI", 14)
        )
        self.password_entry.pack(pady=10)
        self.password_entry.bind("<Return>", lambda e: self._on_login())
        
        # Confirm password (for registration)
        self.confirm_entry = ctk.CTkEntry(
            container,
            placeholder_text="Confirm Password",
            show="•",
            width=300,
            height=45,
            font=("Segoe UI", 14)
        )
        
        # Show password checkbox
        self.show_password_var = ctk.BooleanVar(value=False)
        show_cb = ctk.CTkCheckBox(
            container,
            text="Show Password",
            variable=self.show_password_var,
            command=self._toggle_password_visibility
        )
        show_cb.pack(pady=10)
        
        # Buttons
        btn_frame = ctk.CTkFrame(container, fg_color="transparent")
        btn_frame.pack(pady=30)
        
        login_btn = ctk.CTkButton(
            btn_frame,
            text="Login",
            command=self._on_login,
            width=140,
            height=45,
            font=("Segoe UI", 14, "bold")
        )
        login_btn.grid(row=0, column=0, padx=10)
        
        self.register_btn = ctk.CTkButton(
            btn_frame,
            text="Register",
            command=self._toggle_register,
            width=140,
            height=45,
            font=("Segoe UI", 14),
            fg_color="transparent",
            border_width=2
        )
        self.register_btn.grid(row=0, column=1, padx=10)
    
    def _toggle_register(self):
        """Toggle between login and register modes"""
        if self.confirm_entry.winfo_ismapped():
            self.confirm_entry.pack_forget()
            self.register_btn.configure(text="Register")
            self.root.geometry("1000x700")
        else:
            self.confirm_entry.pack(pady=10)
            self.register_btn.configure(text="Cancel")
            self.root.geometry("1000x750")
    
    def _toggle_password_visibility(self):
        """Toggle password visibility"""
        show = self.show_password_var.get()
        show_char = "" if show else "•"
        self.password_entry.configure(show=show_char)
        self.confirm_entry.configure(show=show_char)
    
    def _on_login(self):
        """Handle login/register button click"""
        password = self.password_entry.get()
        
        if not password:
            messagebox.showerror("Error", "Please enter a password")
            return
        
        # Check if in register mode
        is_register = self.confirm_entry.winfo_ismapped()
        
        if is_register:
            confirm = self.confirm_entry.get()
            if password != confirm:
                messagebox.showerror("Error", "Passwords do not match")
                return
        
        # Authenticate in a separate thread to prevent UI freeze
        def auth_thread():
            success = self.app.authenticate(password, is_new_account=is_register)
            if not success and not is_register:
                messagebox.showerror("Error", "Login failed")
        
        threading.Thread(target=auth_thread, daemon=True).start()
    
    def show_main_screen(self):
        """Show main application screen"""
        self._clear_screen()
        self.current_screen = "main"
        
        # Create sidebar
        self._create_sidebar()
        
        # Create main content area
        self._create_main_content()
        
        # Load initial content
        self.show_all_passwords()
    
    def _create_sidebar(self):
        """Create sidebar navigation"""
        self.sidebar = ctk.CTkFrame(self.root, width=200, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)
        
        # Logo
        logo = ctk.CTkLabel(
            self.sidebar,
            text="🔐 SecurePass",
            font=("Segoe UI", 20, "bold")
        )
        logo.pack(pady=(30, 20))
        
        # Navigation buttons
        nav_items = [
            ("📋 All Passwords", self.show_all_passwords),
            ("➕ Add New", self.show_add_password),
            ("🎲 Generator", self.show_generator),
            ("⚙️ Settings", self.show_settings),
        ]
        
        for text, command in nav_items:
            btn = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                anchor="w",
                font=("Segoe UI", 14),
                fg_color="transparent",
                hover_color=("gray70", "gray30")
            )
            btn.pack(pady=5, padx=20, fill="x")
        
        # Logout button
        logout_btn = ctk.CTkButton(
            self.sidebar,
            text="🚪 Logout",
            command=self.app.logout,
            font=("Segoe UI", 14),
            fg_color="transparent",
            hover_color=("gray70", "gray30")
        )
        logout_btn.pack(side="bottom", pady=20, padx=20, fill="x")
    
    def _create_main_content(self):
        """Create main content area"""
        self.main_content = ctk.CTkFrame(self.root, corner_radius=0)
        self.main_content.pack(side="right", fill="both", expand=True)
        
        # Header
        self.header = ctk.CTkFrame(self.main_content, height=80, corner_radius=0)
        self.header.pack(fill="x")
        self.header.pack_propagate(False)
        
        self.title_label = ctk.CTkLabel(
            self.header,
            text="All Passwords",
            font=("Segoe UI", 28, "bold")
        )
        self.title_label.pack(side="left", padx=30, pady=20)
        
        # Search
        search_frame = ctk.CTkFrame(self.header, fg_color="transparent")
        search_frame.pack(side="right", padx=30, pady=20)
        
        self.search_var = ctk.StringVar()
        self.search_entry = ctk.CTkEntry(
            search_frame,
            textvariable=self.search_var,
            placeholder_text="Search passwords...",
            width=250
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", self._on_search)
        
        # Content area
        self.content_area = ctk.CTkScrollableFrame(self.main_content)
        self.content_area.pack(fill="both", expand=True, padx=20, pady=20)
    
    def show_all_passwords(self):
        """Show all passwords"""
        self.title_label.configure(text="All Passwords")
        self._clear_content()
        
        passwords = self.app.get_all_passwords()
        
        if not passwords:
            label = ctk.CTkLabel(
                self.content_area,
                text="No passwords saved yet.\nClick 'Add New' to get started!",
                font=("Segoe UI", 16),
                text_color="gray"
            )
            label.pack(pady=100)
            return
        
        for password_data in passwords:
            self._create_password_card(password_data)
    
    def show_add_password(self):
        """Show add password form"""
        self.title_label.configure(text="Add New Password")
        self._clear_content()
        
        # Form container
        form_frame = ctk.CTkFrame(self.content_area, corner_radius=10)
        form_frame.pack(fill="x", padx=20, pady=20)
        
        # Form fields
        fields = [
            ("Website:", "website", "Enter website name"),
            ("Username:", "username", "Enter username or email"),
            ("Password:", "password", "Enter password"),
            ("URL:", "url", "Optional: Website URL"),
        ]
        
        self.form_entries = {}
        
        for label_text, field_name, placeholder in fields:
            frame = ctk.CTkFrame(form_frame, fg_color="transparent")
            frame.pack(fill="x", padx=30, pady=15)
            
            label = ctk.CTkLabel(
                frame,
                text=label_text,
                font=("Segoe UI", 14),
                width=100
            )
            label.pack(side="left")
            
            if field_name == "password":
                entry_frame = ctk.CTkFrame(frame, fg_color="transparent")
                entry_frame.pack(side="right", fill="x", expand=True)
                
                entry = ctk.CTkEntry(
                    entry_frame,
                    placeholder_text=placeholder,
                    show="•",
                    font=("Segoe UI", 14)
                )
                entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
                
                # Generate button
                gen_btn = ctk.CTkButton(
                    entry_frame,
                    text="Generate",
                    width=80,
                    command=lambda e=entry: self._generate_for_field(e)
                )
                gen_btn.pack(side="right", padx=(0, 10))
                
                # Show button
                show_btn = ctk.CTkButton(
                    entry_frame,
                    text="Show",
                    width=60,
                    command=lambda e=entry: self._toggle_field_visibility(e)
                )
                show_btn.pack(side="right")
                
                self.form_entries[field_name] = entry
            else:
                entry = ctk.CTkEntry(
                    frame,
                    placeholder_text=placeholder,
                    font=("Segoe UI", 14)
                )
                entry.pack(side="right", fill="x", expand=True)
                self.form_entries[field_name] = entry
        
        # Notes field
        notes_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        notes_frame.pack(fill="x", padx=30, pady=15)
        
        notes_label = ctk.CTkLabel(
            notes_frame,
            text="Notes:",
            font=("Segoe UI", 14),
            width=100
        )
        notes_label.pack(side="left", anchor="n")
        
        self.notes_text = ctk.CTkTextbox(notes_frame, height=100, font=("Segoe UI", 14))
        self.notes_text.pack(side="right", fill="x", expand=True)
        
        # Buttons
        button_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        button_frame.pack(pady=30)
        
        save_btn = ctk.CTkButton(
            button_frame,
            text="💾 Save Password",
            command=self._save_password,
            height=45,
            font=("Segoe UI", 14, "bold")
        )
        save_btn.pack(side="left", padx=20)
        
        clear_btn = ctk.CTkButton(
            button_frame,
            text="Clear",
            command=self._clear_form,
            height=45,
            font=("Segoe UI", 14)
        )
        clear_btn.pack(side="left", padx=20)
    
    def show_generator(self):
        """Show password generator"""
        self.title_label.configure(text="Password Generator")
        self._clear_content()
        
        # Generator container
        gen_frame = ctk.CTkFrame(self.content_area, corner_radius=10)
        gen_frame.pack(fill="x", padx=20, pady=20)
        
        # Length control
        length_frame = ctk.CTkFrame(gen_frame, fg_color="transparent")
        length_frame.pack(pady=20, padx=30, fill="x")
        
        length_label = ctk.CTkLabel(
            length_frame,
            text="Length:",
            font=("Segoe UI", 14)
        )
        length_label.pack(side="left")
        
        self.length_var = ctk.IntVar(value=16)
        length_slider = ctk.CTkSlider(
            length_frame,
            from_=8,
            to=32,
            variable=self.length_var,
            number_of_steps=24,
            command=self._update_length_label
        )
        length_slider.pack(side="left", padx=20, fill="x", expand=True)
        
        self.length_display = ctk.CTkLabel(
            length_frame,
            text="16",
            font=("Segoe UI", 14)
        )
        self.length_display.pack(side="right")
        
        # Character options
        self.use_upper = ctk.BooleanVar(value=True)
        self.use_lower = ctk.BooleanVar(value=True)
        self.use_digits = ctk.BooleanVar(value=True)
        self.use_special = ctk.BooleanVar(value=True)
        
        options = [
            ("Uppercase (A-Z)", self.use_upper),
            ("Lowercase (a-z)", self.use_lower),
            ("Digits (0-9)", self.use_digits),
            ("Special (!@#$%)", self.use_special)
        ]
        
        for text, var in options:
            cb = ctk.CTkCheckBox(
                gen_frame,
                text=text,
                variable=var,
                font=("Segoe UI", 14),
                command=self._generate_password
            )
            cb.pack(pady=5, padx=30, anchor="w")
        
        # Generated password display
        result_frame = ctk.CTkFrame(gen_frame, fg_color="transparent")
        result_frame.pack(pady=30, padx=30, fill="x")
        
        self.generated_password = ctk.StringVar()
        password_entry = ctk.CTkEntry(
            result_frame,
            textvariable=self.generated_password,
            font=("Consolas", 16),
            state="readonly"
        )
        password_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        copy_btn = ctk.CTkButton(
            result_frame,
            text="Copy",
            command=self._copy_generated,
            width=80
        )
        copy_btn.pack(side="right")
        
        # Generate button
        generate_btn = ctk.CTkButton(
            gen_frame,
            text="🔄 Generate New",
            command=self._generate_password,
            height=45,
            font=("Segoe UI", 14, "bold")
        )
        generate_btn.pack(pady=20, padx=50)
        
        # Generate initial password
        self._generate_password()
    
    def show_settings(self):
        """Show settings"""
        self.title_label.configure(text="Settings")
        self._clear_content()
        
        # Settings container
        settings_frame = ctk.CTkFrame(self.content_area, corner_radius=10)
        settings_frame.pack(fill="x", padx=20, pady=20)
        
        # Change password
        change_pass_btn = ctk.CTkButton(
            settings_frame,
            text="Change Master Password",
            command=self._change_password,
            height=45,
            font=("Segoe UI", 14)
        )
        change_pass_btn.pack(pady=20, padx=50, fill="x")
        
        # Export
        export_btn = ctk.CTkButton(
            settings_frame,
            text="Export Passwords",
            command=self._export_passwords,
            height=45,
            font=("Segoe UI", 14)
        )
        export_btn.pack(pady=20, padx=50, fill="x")
        
        # Import
        import_btn = ctk.CTkButton(
            settings_frame,
            text="Import Passwords",
            command=self._import_passwords,
            height=45,
            font=("Segoe UI", 14)
        )
        import_btn.pack(pady=20, padx=50, fill="x")
        
        # About
        about_btn = ctk.CTkButton(
            settings_frame,
            text="About",
            command=self._show_about,
            height=45,
            font=("Segoe UI", 14)
        )
        about_btn.pack(pady=20, padx=50, fill="x")
    
    def _create_password_card(self, password_data):
        """Create a password display card"""
        card = ctk.CTkFrame(self.content_area, corner_radius=10)
        card.pack(fill="x", padx=10, pady=5)
        
        # Card content
        content = ctk.CTkFrame(card, fg_color="transparent")
        content.pack(fill="x", padx=20, pady=15)
        
        # Left side - Info
        info_frame = ctk.CTkFrame(content, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True)
        
        # Website
        website = ctk.CTkLabel(
            info_frame,
            text=password_data.get('website', 'Unknown'),
            font=("Segoe UI", 18, "bold")
        )
        website.pack(anchor="w")
        
        # Username
        username = ctk.CTkLabel(
            info_frame,
            text=f"👤 {password_data.get('username', '')}",
            font=("Segoe UI", 14)
        )
        username.pack(anchor="w", pady=(5, 0))
        
        # Password (initially hidden)
        password_id = password_data.get('id', '')
        if password_id:
            password_label = ctk.CTkLabel(
                info_frame,
                text="🔒 ••••••••••",
                font=("Segoe UI", 14)
            )
            password_label.pack(anchor="w", pady=(5, 0))
            
            # Store for toggling
            self.password_labels[password_id] = password_label
            self.password_values[password_id] = password_data.get('password', '')
            self.password_visible[password_id] = False
        
        # Right side - Buttons
        btn_frame = ctk.CTkFrame(content, fg_color="transparent")
        btn_frame.pack(side="right")
        
        # Copy button
        copy_btn = ctk.CTkButton(
            btn_frame,
            text="Copy",
            width=80,
            command=lambda p=password_data.get('password', ''): self._copy_password(p)
        )
        copy_btn.grid(row=0, column=0, padx=5)
        
        # Show button
        if password_id:
            show_btn = ctk.CTkButton(
                btn_frame,
                text="Show",
                width=80,
                command=lambda pid=password_id: self._toggle_password_display(pid)
            )
            show_btn.grid(row=0, column=1, padx=5)
        
        # Delete button
        delete_btn = ctk.CTkButton(
            btn_frame,
            text="Delete",
            width=80,
            fg_color="red",
            hover_color="darkred",
            command=lambda pid=password_id: self._delete_password(pid)
        )
        delete_btn.grid(row=0, column=2, padx=5)
    
    def _on_search(self, event):
        """Handle search input"""
        search_term = self.search_var.get().lower()
        
        if not search_term:
            self.show_all_passwords()
            return
        
        # Filter passwords based on search term
        matching = self.app.search_passwords(search_term)
        
        self._clear_content()
        
        if not matching:
            label = ctk.CTkLabel(
                self.content_area,
                text=f"No passwords found for '{search_term}'",
                font=("Segoe UI", 16),
                text_color="gray"
            )
            label.pack(pady=100)
            return
        
        for password_data in matching:
            self._create_password_card(password_data)
    
    def refresh_password_list(self):
        """Refresh the password list display"""
        if self.current_screen == "main":
            if self.title_label.cget("text") == "All Passwords":
                self.show_all_passwords()
            elif "Search" in self.title_label.cget("text"):
                self._on_search(None)
    
    def _clear_screen(self):
        """Clear all widgets from screen"""
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def _clear_content(self):
        """Clear content area"""
        if hasattr(self, 'content_area'):
            for widget in self.content_area.winfo_children():
                widget.destroy()
        
        # Clear password tracking
        self.password_labels.clear()
        self.password_values.clear()
        self.password_visible.clear()
    
    def _save_password(self):
        """Save password from form"""
        password_data = {
            "website": self.form_entries["website"].get(),
            "username": self.form_entries["username"].get(),
            "password": self.form_entries["password"].get(),
            "url": self.form_entries["url"].get(),
            "notes": self.notes_text.get("1.0", "end-1c")
        }
        
        # Validate required fields
        if not password_data["website"] or not password_data["username"] or not password_data["password"]:
            messagebox.showerror("Error", "Please fill in website, username, and password")
            return
        
        success = self.app.save_password_entry(password_data)
        if success:
            messagebox.showinfo("Success", "Password saved successfully!")
            self.show_all_passwords()
    
    def _clear_form(self):
        """Clear the add password form"""
        for entry in self.form_entries.values():
            entry.delete(0, "end")
        self.notes_text.delete("1.0", "end")
    
    def _generate_for_field(self, entry_widget):
        """Generate password for a specific field"""
        password = self.app.generate_password()
        entry_widget.delete(0, "end")
        entry_widget.insert(0, password)
    
    def _toggle_field_visibility(self, entry_widget):
        """Toggle visibility of a password field"""
        current_show = entry_widget.cget("show")
        entry_widget.configure(show="" if current_show == "•" else "•")
    
    def _update_length_label(self, value):
        """Update length display label"""
        self.length_display.configure(text=str(int(float(value))))
    
    def _generate_password(self):
        """Generate a new password"""
        password = self.app.generate_password(
            length=self.length_var.get(),
            use_upper=self.use_upper.get(),
            use_lower=self.use_lower.get(),
            use_digits=self.use_digits.get(),
            use_special=self.use_special.get()
        )
        self.generated_password.set(password)
    
    def _copy_generated(self):
        """Copy generated password to clipboard"""
        password = self.generated_password.get()
        if password:
            self.app.copy_to_clipboard(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
    
    def _change_password(self):
        """Change master password"""
        dialog = ctk.CTkInputDialog(
            text="Enter new master password:",
            title="Change Master Password"
        )
        new_password = dialog.get_input()
        
        if new_password:
            self.app.change_master_password(new_password)
    
    def _export_passwords(self):
        """Export passwords"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".dat",
            filetypes=[("SecurePass files", "*.dat"), ("All files", "*.*")],
            title="Export Passwords"
        )
        
        if file_path:
            success = self.app.export_data(file_path)
            if success:
                messagebox.showinfo("Success", "Passwords exported successfully!")
    
    def _import_passwords(self):
        """Import passwords"""
        file_path = filedialog.askopenfilename(
            filetypes=[("SecurePass files", "*.dat"), ("All files", "*.*")],
            title="Import Passwords"
        )
        
        if file_path:
            if messagebox.askyesno("Confirm Import", "This will replace your current passwords. Continue?"):
                success = self.app.import_data(file_path)
                if success:
                    messagebox.showinfo("Success", "Passwords imported successfully!")
    
    def _show_about(self):
        """Show about dialog"""
        messagebox.showinfo(
            "About SecurePass Manager",
            "SecurePass Manager v1.0\n\n"
            "A secure password storage application\n"
            "with encryption and password generation.\n\n"
            "All data is encrypted locally with your master password."
        )
    
    def _copy_password(self, password):
        """Copy password to clipboard"""
        if password:
            self.app.copy_to_clipboard(password)
            messagebox.showinfo("Copied", "Password copied to clipboard!")
    
    def _toggle_password_display(self, password_id):
        """Toggle password visibility on card"""
        if password_id in self.password_labels and password_id in self.password_values:
            if self.password_visible.get(password_id, False):
                # Hide password
                self.password_labels[password_id].configure(text="🔒 ••••••••••")
                self.password_visible[password_id] = False
            else:
                # Show password
                password = self.password_values[password_id]
                self.password_labels[password_id].configure(text=password)
                self.password_visible[password_id] = True
    
    def _delete_password(self, password_id):
        """Delete a password"""
        if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this password?"):
            success = self.app.delete_password_entry(password_id)
            if success:
                messagebox.showinfo("Success", "Password deleted successfully!")