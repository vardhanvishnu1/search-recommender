# spell_checker.py
from spellchecker import SpellChecker

class Corrector:
    def __init__(self, language='en'):
        self.spell = SpellChecker(language)
        # You can add your own custom words (like catering service names)
        # self.spell.word_frequency.load_words(['mycateringbiz', 'eventify'])

    def correct_word(self, word):
        """Returns the most likely correction for a word."""
        return self.spell.correction(word)

    def correct_sentence(self, sentence):
        """Corrects all words in a sentence."""
        words = sentence.split()
        corrected_words = [self.spell.correction(word) for word in words]
        return " ".join(corrected_words)

# --- Example Usage ---
if __name__ == '__main__':
    corrector = Corrector()

    word1 = "cataogorie"
    print(f"Correction for '{word1}': {corrector.correct_word(word1)}")
    # Output: Correction for 'cataogorie': catalogue

    word2 = "bithday"
    print(f"Correction for '{word2}': {corrector.correct_word(word2)}")
    # Output: Correction for 'bithday': birthday

    sentence = "i need a catring service for my bithday evnt"
    print(f"Corrected sentence: {corrector.correct_sentence(sentence)}")
    # Output: Corrected sentence: i need a catering service for my birthday event