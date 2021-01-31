from fuzzywuzzy import fuzz

class Node(object):
    def __init__(self):
        self.children = {}
        self.isend = False


class Trie(object):
    def __init__(self):
        self.root = self.getTrieNode()
        self.suggestions = []
        self.search_keywords_counter = {}

    def getTrieNode(self):
        return Node()

    def insert(self, key):
        crawl = self.root
        for l in range(len(key)):
            if key[l] not in crawl.children:
                crawl.children[key[l]] = self.getTrieNode()
            crawl = crawl.children[key[l]]
        crawl.isend = True

    def search(self, key):
        self.search_keywords_counter[key] += 1
        crawl = self.root
        for l in range(len(key)):
            if key[l] not in crawl.children:
                return False
            crawl = crawl.children[key[l]]
        return crawl != None and crawl.isend

    def print_top_suggestions(self, key):
        self.search_keywords_counter[key] += 1
        self.get_auto_suggestions_from_input_word(key)
        return [word for word in self.suggestions if fuzz.ratio(word, key) > 20]

    def get_auto_suggestions_from_input_word(self, prefix):
        crawl = self.root
        search_word = ""
        self.suggestions = []
        for c in prefix:
            if c not in crawl.children:
                break
            search_word += c
            crawl = crawl.children.get(c)
        self.all_words(crawl, search_word)

    def all_words(self, node, search_word):
        if node.isend:
            self.suggestions.append(search_word)
        for letter, child in node.children.items():
            self.all_words(child, search_word + letter)


t = Trie()

keys = ["the", "a", "there", "analysis", "any",
        "by", "their", "amazon", "amazon food", "amaze", "amaze industries"]

for key in keys:
    t.insert(key)

print(t.search("the"))
print(t.search("theif"))
print(t.print_top_suggestions("a"))
print(t.print_top_suggestions("anime"))
print(t.print_top_suggestions("amaz"))
print(t.print_top_suggestions("an"))
