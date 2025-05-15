import random
import os

class LessonManager:
    def __init__(self, lesson_folder='lessons/'):
        self.lesson_folder = lesson_folder
        self.lesson_files = [f for f in os.listdir(lesson_folder) if f.endswith('.txt')]
        

    def get_random_lesson(self):
        lesson_file = random.choice(self.lesson_files)
        with open(os.path.join(self.lesson_folder, lesson_file), 'r') as file:
            lesson_text = file.read().strip()
        return lesson_text
