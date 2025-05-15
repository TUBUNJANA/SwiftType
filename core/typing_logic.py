import time

class TypingSession:
    def __init__(self, lesson_text):
        self.lesson_text = lesson_text
        self.user_input = ""
        self.start_time = None
        self.end_time = None

    def start(self):
        self.start_time = time.time()  # Initialize start time when the session starts

    def end(self, user_input):
        self.end_time = time.time()  # Set the end time when the session ends
        self.user_input = user_input  # Capture the final user input

    def get_elapsed_time(self):
        if self.start_time is None:
            return 0  # If start_time is not set, return 0 to avoid error
        if self.end_time is None:
            return time.time() - self.start_time  # If session isn't finished, return elapsed time until now
        return max(self.end_time - self.start_time, 1)  # Elapsed time (min 1 second)

    def calculate_wpm(self):
        elapsed_time_in_minutes = self.get_elapsed_time() / 60  # Convert to minutes
        if elapsed_time_in_minutes == 0:  # Prevent division by zero
            return 0  # Return 0 WPM if no time has passed yet
        word_count = len(self.user_input.split())  # Split by spaces to count words
        return round(word_count / elapsed_time_in_minutes, 2)  # Words per minute

    def calculate_accuracy(self):
        correct_chars = 0
        total_chars = len(self.lesson_text)

        # Calculate the number of correct characters typed
        for i in range(min(len(self.lesson_text), len(self.user_input))):
            if self.lesson_text[i] == self.user_input[i]:
                correct_chars += 1

        # Calculate accuracy percentage
        return round((correct_chars / total_chars) * 100, 2)

    def get_error_count(self):
        # Count the number of characters that are incorrect
        incorrect_chars = 0
        for i in range(min(len(self.lesson_text), len(self.user_input))):
            if self.lesson_text[i] != self.user_input[i]:
                incorrect_chars += 1
        return incorrect_chars
