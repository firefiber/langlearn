#TODO: Rework - lots of redundancy.


from queue import Queue
from user_management.user_buffer import fetch_user_info, get_practice_buffer
from learning.services.generate_sentences import from_openai_chat
from languages.services import store_sentence_translation_pair

# class RoundManager:
#     def __init__(self):
#         self.user_info = None
#         self.user_practice_buffer = None
#         self.buffer = Queue()
#         self.history = []
#
#     def set_user(self, username):
#         # Load user information
#         self.user_info = fetch_user_info(username)
#         self.user_practice_buffer = get_practice_buffer(username)
#
#         # Generate sentences and populate the buffer
#         self.generate_sentences_and_fill_buffer()
#
#     def generate_sentences_and_fill_buffer(self):
#         generated_sentences = from_openai_chat(
#             self.user_info['learning_language'],
#             self.user_info['native_language'],
#             self.user_info['proficiency'],
#             self.user_practice_buffer
#         )
#
#         for pair in generated_sentences:
#             self.buffer.put(pair)
#             stored_pair, message = store_sentence_translation_pair(pair)
#             # stored_sentence, message = store_sentence(pair["sentence"], self.user_info['learning_language'])
#             # print(f"Stored Sentence: {stored_sentence}, Message: {message}")
#
#     def get_sentence(self):
#         # If the buffer has less than 5 items, generate and add more sentences to the buffer
#         if self.buffer.qsize() < 5:
#             self.generate_sentences_and_fill_buffer()
#
#         # Return a sentence from the buffer
#         return self.buffer.get()
#
# global_round_manager = RoundManager()


from queue import Queue
from user_management.user_buffer import fetch_user_info, get_practice_buffer
from learning.services.generate_sentences import from_openai_chat
from languages.services import store_sentence_translation_pair

class Round:
    def __init__(self, user_info, buffer):
        self.user_info = user_info
        self.buffer = buffer
        self.history = []

class RoundManager:
    def __init__(self):
        self.current_round = None

    def initialize_round(self, username):
        user_info = fetch_user_info(username)
        user_practice_buffer = get_practice_buffer(username)

        generated_sentences = self._generate_sentences(user_info, user_practice_buffer)
        self.current_round = Round(user_info, generated_sentences)

    def _generate_sentences(self, user_info, user_practice_buffer):
        generated_sentences = from_openai_chat(
            user_info['learning_language'],
            user_info['native_language'],
            user_info['proficiency'],
            user_practice_buffer
        )

        buffer = Queue()
        for pair in generated_sentences:
            buffer.put(pair)
            stored_pair, message = store_sentence_translation_pair(pair)
            # Handle storage and messages as needed

        return buffer

    def get_next_sentence(self):
        if self.current_round and not self.current_round.buffer.empty():
            return self.current_round.buffer.get()
        return None  # Or handle empty buffer scenario

    def get_round_info(self):
        if self.current_round:
            return {
                "user_info": self.current_round.user_info,
                "buffer_size": self.current_round.buffer.qsize(),
                "history": self.current_round.history
            }
        return None
