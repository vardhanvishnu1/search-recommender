# trie.py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False
        self.frequency = 0

class AutocompleteTrie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, frequency=1):
        """Inserts a word into the Trie with its frequency."""
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True
        node.frequency = frequency

    def _find_all_words_from_node(self, node, prefix):
        """A recursive helper to find all words and their frequencies."""
        suggestions = []
        if node.is_end_of_word:
            suggestions.append((prefix, node.frequency))
        
        for char, child_node in node.children.items():
            suggestions.extend(self._find_all_words_from_node(child_node, prefix + char))
        return suggestions

    def suggest(self, prefix, num_suggestions=10):
        """Suggests words for a given prefix, ranked by frequency."""
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        
        suggestions_with_freq = self._find_all_words_from_node(node, prefix)
        
        suggestions_with_freq.sort(key=lambda item: item[1], reverse=True)
        
        final_suggestions = [word for word, freq in suggestions_with_freq]
        
        return final_suggestions[:num_suggestions]