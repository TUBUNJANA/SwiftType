import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from core.typing_logic import TypingSession
from core.lesson_manager import LessonManager
from core.user_manager import UserManager
import datetime
import os
import sys  # ✅ Added for resource_path support

# ✅ Add this utility for PyInstaller-safe path resolution
def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.abspath("."))
    return os.path.join(base_path, relative_path)

class TypingTutorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("SwiftType")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f0f4f8")

        self.lesson_manager = LessonManager()
        self.user_manager = UserManager()
        self.session = None
        self.username = ""
        self.lesson_text = ""

        # ✅ Use resource_path for the icon
        icon_path = resource_path("assets/favicon.ico")
        if os.path.exists(icon_path):
            self.root.iconbitmap(icon_path)
        else:
            print(f"Icon not found at {icon_path}")

        self.tab_control = ttk.Notebook(self.root)
        self.practice_tab = tk.Frame(self.tab_control, bg="#f0f4f8")
        self.dashboard_tab = tk.Frame(self.tab_control, bg="#f0f4f8")

        self.tab_control.add(self.practice_tab, text='Practice')
        self.tab_control.add(self.dashboard_tab, text='Dashboard')
        self.tab_control.pack(expand=1, fill="both")

        self.manage_lessons_tab = tk.Frame(self.tab_control, bg="#f0f4f8")
        self.tab_control.add(self.manage_lessons_tab, text='Manage Lessons')
        self.create_manage_lessons_tab()

        self.setup_styles()
        self.create_practice_widgets()
        self.create_dashboard()
        
        self.about_tab = tk.Frame(self.tab_control, bg="#f0f4f8")
        self.tab_control.add(self.about_tab, text='About')
        self.create_about_tab()

    def create_about_tab(self):
        frame = self.about_tab

        # Style and padding
        frame.configure(bg="#f0f4f8")

        # Main title
        ttk.Label(frame, text="About SwiftType", font=("Helvetica", 20, "bold")).pack(pady=(30, 10))

        # App Info Section
        info_frame = ttk.Frame(frame, padding=20)
        info_frame.pack(pady=5)

        info_text = (
            "App Name: SwiftType - Typing Tutor\n"
            "Version: 1.0.0\n"
            "Developer: TUBUN JANA(Computer Science Student)\n"
            "Email: tubun.official@gmail.com\n"
            "Website: https://SwiftType.com\n"
            "License: MIT License\n"
        )
        ttk.Label(info_frame, text=info_text, font=("Arial", 10), justify="left").pack()

        # Logo section
        logo_path = resource_path("assets/logo.png")
        if os.path.exists(logo_path):
            img = Image.open(logo_path)
            img = img.resize((100, 100), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(img)
            logo_label = tk.Label(frame, image=photo, bg="#f0f4f8")
            logo_label.image = photo  # Keep a reference
            logo_label.pack(pady=5)

        # Separator
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=30, pady=5)

        # Description
        desc_text = (
            "SwiftType is a lightweight and interactive typing tutor that helps improve speed and accuracy.\n"
            "Track your progress, set time goals, and view detailed dashboards tailored to your performance."
        )
        ttk.Label(frame, text=desc_text, font=("Arial", 11), justify="center", wraplength=700).pack(pady=10)

        # Separator
        ttk.Separator(frame, orient='horizontal').pack(fill='x', padx=30, pady=2)

        # Support Section
        support_frame = ttk.LabelFrame(frame, text="Support", padding=20)
        support_frame.pack(pady=2, padx=20, fill="x")

        ttk.Label(support_frame, text="Need help or want to report a bug?", font=("Arial", 11)).pack(anchor="w", pady=2)
        ttk.Label(support_frame, text="📧 Email: support.swifttype@swifttype.com", font=("Arial", 11)).pack(anchor="w", pady=2)
        ttk.Label(support_frame, text="🌐 Visit: https://swifttype.com/support", font=("Arial", 11)).pack(anchor="w", pady=2)
        ttk.Label(support_frame, text="💬 Join our Community Forum: https://forum.swifttype.com", font=("Arial", 11)).pack(anchor="w", pady=2)

        # Footer
        ttk.Label(frame, text="© 2025 SwiftType. All rights reserved.", font=("Arial", 10, "italic")).pack()
        ttk.Label(frame, text="Thank you for using SwiftType!", font=("Arial", 10, "italic")).pack()


    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("TButton", font=('Arial', 12), padding=6, background="#0078D7", foreground="white")
        style.map("TButton", background=[('active', '#005A9E')])
        style.configure("TLabel", font=('Arial', 12), background="#f0f4f8")
        style.configure("Treeview", rowheight=25, font=('Arial', 11))
        style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))


    def create_practice_widgets(self):
        frame = self.practice_tab

        ttk.Label(frame, text="Welcome to SwiftType Tutor", font=("Arial", 16)).pack(pady=10)

        self.user_listbox = tk.Listbox(frame, height=5)
        self.user_listbox.pack()
        for user in self.user_manager.list_users():
            self.user_listbox.insert(tk.END, user)

        ttk.Button(frame, text="Select User", command=self.select_existing_user).pack(pady=5)
        ttk.Button(frame, text="Delete User", command=self.delete_selected_user).pack(pady=5)

        ttk.Label(frame, text="Or enter a new username:").pack()
        self.username_entry = ttk.Entry(frame)
        self.username_entry.pack(pady=5)
        ttk.Button(frame, text="Start", command=self.start_session).pack(pady=10)

    def start_session(self):
        self.create_dashboard()
        if not self.username:
            self.username = self.username_entry.get().strip()
        if not self.username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return

        self.lesson_text = self.lesson_manager.get_random_lesson()
        if self.lesson_text.startswith("No valid lessons available"):
            messagebox.showwarning(
                "Invalid Lessons",
                "No valid lessons found. Please add a proper lesson first from the 'Manage Lessons' tab.\n\n"
                "Rules:\n"
                "- At least 50 characters\n"
                "- No double spaces or blank lines\n"
                "- Must start with a capital letter and end with proper punctuation."
            )
            return

        self.clear_practice_tab()
        self.ask_for_time_limit()



    def ask_for_time_limit(self):
        self.time_limit_window = tk.Toplevel(self.root)
        self.time_limit_window.title("Set Time Limit")

        ttk.Label(self.time_limit_window, text="Enter time limit in minutes:").pack(pady=5)
        self.time_limit_entry = ttk.Entry(self.time_limit_window)
        self.time_limit_entry.pack(pady=5)

        ttk.Button(self.time_limit_window, text="Start Typing", command=self.begin_typing).pack(pady=10)

    def begin_typing(self):
        try:
            self.time_limit = int(self.time_limit_entry.get()) * 60
            self.time_limit_window.destroy()

            self.session = TypingSession(self.lesson_text)
            self.session.start()
            self.create_typing_ui()
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number.")

    def create_typing_ui(self):
        frame = self.practice_tab

        self.lesson_display = tk.Text(frame, height=6, width=90, font=("Arial", 14))
        self.lesson_display.pack(pady=10)
        self.lesson_display.insert(tk.END, self.lesson_text)
        self.lesson_display.config(state=tk.DISABLED)

        self.text_entry = tk.Text(frame, height=6, width=90, font=("Arial", 14))
        self.text_entry.pack(pady=10)
        self.text_entry.bind("<KeyRelease>", self.on_key_release)

        self.stats_label = ttk.Label(frame, text="", font=("Arial", 12))
        self.stats_label.pack(pady=10)

        self.timer_label = ttk.Label(frame, text=f"Time Left: {self.time_limit // 60} minutes", font=("Arial", 12))
        self.timer_label.pack(pady=10)

        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=10)

        ttk.Button(button_frame, text="Restart", command=self.restart_session).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="End Session", command=self.end_session_by_button_click).pack(side=tk.LEFT, padx=10)

        self.update_timer()
        

    def end_session_by_button_click(self):
        if self.time_limit > 0:
            if messagebox.askyesno("Confirm", "Are you sure you want to end the session early?"):
                # Stop the timer
                self.time_limit = 0
        else:
            messagebox.showinfo("Info", "No session is currently running.")


    def restart_session(self):
        self.clear_practice_tab()
        self.username = ""  # Reset username to allow new or same user
        self.create_practice_widgets()



    def update_timer(self):
        if self.time_limit > 0:
            self.time_limit -= 1
            minutes, seconds = divmod(self.time_limit, 60)
            self.timer_label.config(text=f"Time Left: {minutes} minutes {seconds} seconds")
            self.root.after(1000, self.update_timer)
        else:
            self.end_session()

    def on_key_release(self, event):
        user_input = self.text_entry.get("1.0", "end-1c")
        self.session.user_input = user_input
        self.update_text_display()

    def update_text_display(self):
        self.lesson_display.config(state=tk.NORMAL)
        self.lesson_display.tag_remove("correct", "1.0", tk.END)
        self.lesson_display.tag_remove("incorrect", "1.0", tk.END)

        for i, char in enumerate(self.lesson_text):
            if i < len(self.session.user_input):
                tag = "correct" if char == self.session.user_input[i] else "incorrect"
                self.lesson_display.tag_add(tag, f"1.{i}", f"1.{i+1}")

        self.lesson_display.tag_configure("correct", foreground="green")
        self.lesson_display.tag_configure("incorrect", foreground="red")
        self.lesson_display.config(state=tk.DISABLED)

        self.stats_label.config(
            text=f"WPM: {self.session.calculate_wpm()} | "
                f"Accuracy: {self.session.calculate_accuracy()}% | "
                f"Errors: {self.session.get_error_count()}"
        )

    
    def end_session(self):
        print("Ending session... Time is :",self.time_limit)

        # Disable typing
        self.text_entry.config(state='disabled')

        # Mark session as ended
        typed_text = self.text_entry.get("1.0", "end-1c")
        self.session.end(typed_text)

        # Collect session data
        session_data = {
            'lesson': self.lesson_text,
            'wpm': self.session.calculate_wpm(),
            'accuracy': self.session.calculate_accuracy(),
            'errors': self.session.get_error_count(),
            'time': self.time_limit,
            'timestamp': datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }

        # Save to user history
        self.user_manager.save_user_history(self.username, session_data)

        # Show warning popup
        messagebox.showwarning(
            "Session Ended",
            f"Session was manually ended.\n\n"
            f"WPM: {session_data['wpm']}\n"
            f"Accuracy: {session_data['accuracy']}%\n"
            f"Errors: {session_data['errors']}"
        )

        # Redirect to dashboard
        self.create_dashboard()


    def select_existing_user(self):
        selected = self.user_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a user.")
            return
        self.username = self.user_listbox.get(selected[0])
        self.start_session()


    def delete_selected_user(self):
        selected = self.user_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a user to delete.")
            return
        username = self.user_listbox.get(selected[0])
        confirm = messagebox.askyesno("Confirm Delete", f"Delete user '{username}' and all history?")
        if confirm:
            self.user_manager.delete_user(username)
            self.user_listbox.delete(selected[0])
            messagebox.showinfo("Deleted", f"User '{username}' has been deleted.")
            self.create_dashboard()

    def create_dashboard(self):
        for widget in self.dashboard_tab.winfo_children():
            widget.destroy()

        if not self.username:
            ttk.Label(self.dashboard_tab, text="Please select or create a user to see the dashboard.").pack()
            return

        user_data = self.user_manager.load_user_data(self.username)
        history = user_data.get("history", [])

        if not history:
            ttk.Label(self.dashboard_tab, text=f"No data available for user '{self.username}'.").pack()
            return

        # Create a frame to hold the dashboard content
        frame = ttk.Frame(self.dashboard_tab)
        frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Cumulative Stats
        avg_wpm = sum(h['wpm'] for h in history) / len(history)
        avg_errors = sum(h['errors'] for h in history) / len(history)
        avg_accuracy = sum(h['accuracy'] for h in history) / len(history)

        ttk.Label(frame, text=f"Dashboard for: {self.username}", font=("Arial", 16)).pack(pady=10)
        ttk.Label(frame, text=f"Average WPM: {avg_wpm:.2f}").pack()
        ttk.Label(frame, text=f"Average Accuracy: {avg_accuracy:.2f}%").pack()
        ttk.Label(frame, text=f"Average Errors: {avg_errors:.2f}").pack()

        # Individual History Table
        ttk.Label(frame, text="\nSession History:", font=("Arial", 14)).pack(pady=5)

        columns = ("timestamp", "wpm", "accuracy", "errors")
        tree = ttk.Treeview(frame, columns=columns, show='headings')
        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, anchor="center")

        for session in history:
            tree.insert("", tk.END, values=(
                session.get("timestamp", "N/A"),
                session["wpm"],
                session["accuracy"],
                session["errors"]
            ))
        tree.pack(expand=True, fill='both', pady=10)

        # Clear History Button
        ttk.Button(frame, text="Clear History", command=self.clear_user_history).pack(pady=1)

    def clear_user_history(self):
        self.user_manager.clear_user_history(self.username)
        messagebox.showinfo("History Cleared", "User history has been cleared.")
        self.create_dashboard()

    def clear_practice_tab(self):
        for widget in self.practice_tab.winfo_children():
            widget.destroy()
    
    def create_manage_lessons_tab(self):
        frame = self.manage_lessons_tab

        ttk.Label(
            frame, 
            text="⚠️ Lesson text must be 50–5000 characters, no blank lines, no double spaces, start with a capital letter and end with a punctuation.",
            wraplength=800,
            foreground="red",
            font=("Arial", 10, "italic")
        ).pack(pady=5)


        self.lesson_listbox = tk.Listbox(frame, height=10, width=50)
        self.lesson_listbox.pack(pady=5)

        self.refresh_lesson_list()

        # Buttons for delete and select
        button_frame = ttk.Frame(frame)
        button_frame.pack(pady=5)
        ttk.Button(button_frame, text="Delete Selected", command=self.delete_selected_lesson).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Refresh List", command=self.refresh_lesson_list).pack(side=tk.LEFT, padx=5)

        # Text area to add new lesson
        ttk.Label(frame, text="Add New Lesson Text Below:", font=("Arial", 12)).pack(pady=10)
        self.new_lesson_textbox = tk.Text(frame, height=6, width=80)
        self.new_lesson_textbox.pack(pady=5)

        # Warning note
        ttk.Label(frame, text="Note: Keep lesson text between 50 and 5000 characters.", foreground="red").pack()

        # Save new lesson
        ttk.Button(frame, text="Save Lesson", command=self.save_new_lesson).pack(pady=10)

    def refresh_lesson_list(self):
        self.lesson_listbox.delete(0, tk.END)
        for lesson_file in self.lesson_manager.lesson_files:
            self.lesson_listbox.insert(tk.END, lesson_file)

    def delete_selected_lesson(self):
        selected = self.lesson_listbox.curselection()
        if not selected:
            messagebox.showerror("Error", "Please select a lesson to delete.")
            return
        lesson_file = self.lesson_listbox.get(selected[0])
        full_path = os.path.join(self.lesson_manager.lesson_folder, lesson_file)
        if os.path.exists(full_path):
            os.remove(full_path)
            self.lesson_manager.lesson_files.remove(lesson_file)
            self.refresh_lesson_list()
            messagebox.showinfo("Deleted", f"Lesson '{lesson_file}' has been deleted.")
        else:
            messagebox.showerror("Error", "File does not exist.")

    def save_new_lesson(self):
        text = self.new_lesson_textbox.get("1.0", tk.END).strip()

        # Validation checks
        if not (50 <= len(text) <= 5000):
            messagebox.showwarning("Invalid Length", "Lesson text must be between 50 and 5000 characters.")
            return

        if "  " in text:
            messagebox.showwarning("Spacing Error", "Lesson text contains extra spaces. Please use only one space between words.")
            return

        if "\n\n" in text:
            messagebox.showwarning("Paragraph Error", "Lesson should not contain blank lines. Use a single paragraph only.")
            return

        if not text[0].isupper() or not text.endswith(('.', '!', '?')):
            messagebox.showwarning("Formatting Warning", "Lesson should start with a capital letter and end with proper punctuation (e.g., period).")
            return

        # Save lesson
        filename = f"custom_{len(self.lesson_manager.lesson_files)+1}.txt"
        filepath = os.path.join(self.lesson_manager.lesson_folder, filename)
        with open(filepath, 'w') as file:
            file.write(text)
        self.lesson_manager.lesson_files.append(filename)
        self.new_lesson_textbox.delete("1.0", tk.END)
        self.refresh_lesson_list()
        messagebox.showinfo("Saved", f"Lesson saved as '{filename}'.")
