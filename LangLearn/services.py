import threading
from queue import Queue
from user_management.user_buffer import fetch_user_info, get_practice_buffer
from learning.services.generate_sentences import from_openai_chat
import time

class RoundManager:
    def __init__(self, username):
        # Load user information
        self.user_info = fetch_user_info(username)
        self.user_practice_buffer = get_practice_buffer(username)

        # Initialize buffer and history
        self.buffer = Queue()
        self.history = []

        # Flag to indicate the session status
        self.session_active = False

        # Initialize buffer loader thread
        self.buffer_loader = threading.Thread(target=self.load_additional_sentences, daemon=True)

        # Start the session
        self.start_session()

    def start_session(self):
        # Generate sentences and populate the buffer
        self.generate_sentences_and_fill_buffer()

        # Mark session as active
        self.session_active = True

        # Start the buffer loader thread
        self.buffer_loader.start()

    def generate_sentences_and_fill_buffer(self):
        generated_sentences = from_openai_chat(
            self.user_info['learning_language'],
            self.user_info['native_language'],
            self.user_info['proficiency'],
            self.user_practice_buffer
        )
        for sentence in generated_sentences:
            self.buffer.put(sentence)
            print(sentence)

    def load_additional_sentences(self):
        while self.session_active:
            # If the buffer has less than 5 items
            if self.buffer.qsize() < 5:
                # Generate sentences and fill the buffer
                self.generate_sentences_and_fill_buffer()
            time.sleep(1)  # wait for 1 second before checking again

    def get_sentence(self):
        # Return a sentence from the buffer
        return self.buffer.get()

    def end_session(self):
        # Mark session as inactive
        self.session_active = False
        # If the buffer loader thread is running, wait for it to finish
        if self.buffer_loader.is_alive():
            self.buffer_loader.join()

global_round_manager = RoundManager("adrian")
