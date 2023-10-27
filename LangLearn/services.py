from queue import Queue
from user_management.user_buffer import fetch_user_info, get_practice_buffer
from learning.services.generate_sentences import from_openai_chat
from languages.services import store_sentence

class RoundManager:
    def __init__(self):
        self.user_info = None
        self.user_practice_buffer = None
        self.buffer = Queue()
        self.history = []

    def set_user(self, username):
        # Load user information
        self.user_info = fetch_user_info(username)
        self.user_practice_buffer = get_practice_buffer(username)

        # Generate sentences and populate the buffer
        self.generate_sentences_and_fill_buffer()

    def generate_sentences_and_fill_buffer(self):
        generated_sentences = from_openai_chat(
            self.user_info['learning_language'],
            self.user_info['native_language'],
            self.user_info['proficiency'],
            self.user_practice_buffer
        )
        for sentence in generated_sentences:
            self.buffer.put(sentence)
            stored_sentence, message = store_sentence(sentence["sentence"], self.user_info['learning_language'])
            print(f"Stored Sentence: {stored_sentence}, Message: {message}")
            break

    def get_sentence(self):
        # If the buffer has less than 5 items, generate and add more sentences to the buffer
        if self.buffer.qsize() < 5:
            self.generate_sentences_and_fill_buffer()

        # Return a sentence from the buffer
        return self.buffer.get()

global_round_manager = RoundManager()
