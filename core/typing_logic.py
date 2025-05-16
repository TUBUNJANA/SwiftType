import time

class TypingSession:
    def __init__(self, lesson_text):
        """
        Initializes a typing session with the given lesson text.
        """
        self.lesson_text = lesson_text
        self.user_input = ""
        self.start_time = None
        self.end_time = None

    def start(self):
        """
        Starts the timer for the typing session.
        """
        self.start_time = time.time()

    def end(self, user_input):
        """
        Ends the typing session, records user input and stops the timer.
        """
        self.end_time = time.time()
        self.user_input = user_input

    def get_elapsed_time(self):
        """
        Returns the elapsed time in seconds. If not ended, returns time so far.
        """
        if self.start_time is None:
            return 0
        if self.end_time is None:
            return time.time() - self.start_time
        return max(self.end_time - self.start_time, 1)  # Avoid division by zero

    def calculate_wpm(self):
        """
        Calculates and returns words per minute.
        """
        elapsed_minutes = self.get_elapsed_time() / 60
        if elapsed_minutes == 0:
            return 0
        word_count = len(self.user_input.split())
        return round(word_count / elapsed_minutes, 2)

    def calculate_accuracy(self):
        """
        Calculates and returns accuracy as a percentage.
        """
        if not self.lesson_text:
            return 0.0

        correct_chars = sum(
            1 for i in range(min(len(self.lesson_text), len(self.user_input)))
            if self.lesson_text[i] == self.user_input[i]
        )

        return round((correct_chars / len(self.lesson_text)) * 100, 2)

    def get_error_count(self):
        """
        Returns the total number of character mismatches between lesson and input.
        """
        return sum(
            1 for i in range(min(len(self.lesson_text), len(self.user_input)))
            if self.lesson_text[i] != self.user_input[i]
        )
