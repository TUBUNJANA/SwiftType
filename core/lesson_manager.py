import random
import os
import sys

class LessonManager:
    def __init__(self, lesson_folder='lessons'):
        self.lesson_folder = self.get_resource_path(lesson_folder)
        self.lesson_files = [
            f for f in os.listdir(self.lesson_folder) if f.endswith('.txt')
        ]

    def get_resource_path(self, relative_path):
        """
        Get absolute path to resource, works for dev and for PyInstaller.
        """
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller stores temp path in _MEIPASS
            return os.path.join(sys._MEIPASS, relative_path)
        return os.path.join(os.path.abspath("."), relative_path)

    def get_random_lesson(self):
        valid_lessons = []

        for lesson_file in self.lesson_files:
            with open(os.path.join(self.lesson_folder, lesson_file), 'r') as file:
                text = file.read().strip()
                if self.is_valid_lesson(text):
                    valid_lessons.append(text)

        if not valid_lessons:
            return "No valid lessons available. Please add a valid lesson from the 'Manage Lessons' tab."
        
        return random.choice(valid_lessons)
    
    def is_valid_lesson(self, text):
        if not (50 <= len(text) <= 500):
            return False
        if "  " in text:
            return False
        if "\n\n" in text or text.strip() == "":
            return False
        if not text[0].isupper() or not text.endswith(('.', '!', '?')):
            return False
        return True


