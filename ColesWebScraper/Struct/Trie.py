"""
 This is a Trie implementation
"""
__author__ = "Chaluka Salgado"
__copyright__ = "Copyright 2021 @ Kamikaze"
__email__ = "chaluka.salgado@gmail.com"
__docformat__ = 'reStructuredText'

from typing import TypeVar


class Node:
    DOMAIN_SIZE = 27
    SPECIAL_CHAR = '$'
    SPECIAL_CHAR_INDEX = 26
    INIT_CHAR = 'a'

    def __init__(self, char: chr) -> None:
        self.array = [None for i in range(self.DOMAIN_SIZE)]
        self.char = char
        self.count = 0

    def _get_index(self, char: chr) -> int:
        return ord(char) - ord(self.INIT_CHAR) if char != self.SPECIAL_CHAR else self.SPECIAL_CHAR_INDEX

    def _insert(self, char: chr):
        index = self._get_index(char)

        if not self.array[index]:
            self.array[index] = Node(char)

        self.count += 1
        return self.array[index]

    def _get_next_node(self, char: chr):
        return self.array[self._get_index(char)]

    def _traversal(self, word, lst):
        if self.array[self.SPECIAL_CHAR_INDEX]:
            lst.append(word)

        for i in range(self.DOMAIN_SIZE):
            if self.array[i]:
                self.array[i]._traversal(word + str(self.array[i]), lst)

    def __str__(self) -> str:
        return str(self.char)


class PrefixTrie:

    def __init__(self):
        self.root = Node('$')
        self.count = 0

    def insert_word(self, word: str):
        # print(word)
        word = word + Node.SPECIAL_CHAR
        self.count += 1
        self._insert_aux(self.root, word, 0)

    def _insert_aux(self, node, word: str, index: int):
        if index < len(word):
            node = node._insert(word[index])
            self._insert_aux(node, word, index + 1)

    def prefix_search(self, prefix: str) -> bool:
        return self._prefix_search_aux(self.root, prefix, 0)

    def _prefix_search_aux(self, cur_node, prefix: str, index: int) -> bool:

        # prefix found
        if index > len(prefix) - 1 and cur_node:
            return True

        if cur_node:
            node = cur_node._get_next_node(prefix[index])
            return self._prefix_search_aux(node, prefix, index + 1)

        return False

    def __str__(self):
        lst = []
        self.root._traversal("", lst)
        return str(lst)


if __name__ == "__main__":
    pre_trie = PrefixTrie()
    pre_trie.insert_word("abcd")
    pre_trie.insert_word("abxd")
    pre_trie.insert_word("zde")
    pre_trie.insert_word("aaaazde")
    # print(pre_trie.prefix_search("abcd$"))
    print(pre_trie)
