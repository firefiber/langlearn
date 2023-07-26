from utils.language_codes import LANGUAGE_MAP
from spellchecker import SpellChecker
import spacy
# import language_tool_python


class LanguageCodeManager:
    def __init__(self, language_code):
        self.language_code = language_code
        self.language_map = LANGUAGE_MAP.get(self.language_code)
        self.nlp = None
        self.spell = None
        # self.tool = None

    def load_spacy_model(self):
        model_name = self.language_map.get("spacy", "es_core_news_sm")
        self.nlp = spacy.load(model_name)

    def set_spellchecker_language(self):
        language = self.language_map.get("spellchecker", "es")
        self.spell = SpellChecker(language=language)

    # def set_language_tool_language(self):
    #     language = self.language_map.get("language_tool", "es-ES")
    #     self.tool = language_tool_python.LanguageTool(language)

    def initialize_tools(self):
        self.load_spacy_model()
        self.set_spellchecker_language()
        # self.set_language_tool_language()