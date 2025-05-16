# core/custom_lesson_manager.py

import json
import os

class CustomLessonManager:
    def __init__(self, file_path='data/custom_lessons.json'):
        self.file_path = file_path
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        if not os.path.exists(file_path):
            with open(file_path, 'w') as f:
                json.dump([], f)

    def load_lessons(self):
        with open(self.file_path, 'r') as f:
            return json.load(f)

    def save_lessons(self, lessons):
        with open(self.file_path, 'w') as f:
            json.dump(lessons, f, indent=4)

    def add_lesson(self, title, text):
        if len(text) < 20:
            raise ValueError("Lesson must be at least 20 characters long.")
        lessons = self.load_lessons()
        if any(l['title'] == title for l in lessons):
            raise ValueError("A lesson with this title already exists.")
        lessons.append({'title': title, 'text': text})
        self.save_lessons(lessons)

    def delete_lesson(self, title):
        lessons = self.load_lessons()
        lessons = [l for l in lessons if l['title'] != title]
        self.save_lessons(lessons)

    def get_lesson_text(self, title):
        for l in self.load_lessons():
            if l['title'] == title:
                return l['text']
        return None
