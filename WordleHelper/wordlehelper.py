import string
import itertools
import os
from IPython.display import display
from IPython.display import HTML as ipyHTML


DICT_PATH = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "dictionary.txt"))
PERMUTATION_CUTOFF = 200000

class Wordle:
    def __init__(self, dict_path = DICT_PATH):
        self.remaining_letters = list(string.ascii_lowercase)
        self.incorrect_place = []
        self.correct_letters = []
        self.word = [None, None, None, None, None]
        self.dict = self._import_dictionary(dict_path)

    @property
    def empty_idx(self):
        return [i for i, x in enumerate(self.word) if x == None]

    @property
    def base_words(self):
        correct_letters = self.correct_letters.copy()
        if len(correct_letters) == 0:
            return [self.word]
        else:
            while len(correct_letters) < len(self.empty_idx):
                correct_letters.append(None)
            base_words_list = []
            for i in itertools.permutations(correct_letters):

                base_word = self.word.copy()
                for idx, letter in zip(self.empty_idx, i):
                    base_word[idx] = letter
                if all(item in base_word for item in self.correct_letters):
                    base_words_list.append(base_word)
            return [i for i in base_words_list if self.check_base_word(i)]

    def update(self, incorrect_letters=None, incorrect_place=None, correct_place=None):
        self.update_incorrect_letters(incorrect_letters)
        self.update_all_incorrect_places(incorrect_place)
        self.update_all_correct_places(correct_place)
        return self.guess()

    def reset(self):
        self.__init__()
        return

    def update_incorrect_letters(self, letters):
        if letters is None:
            return
        for letter in letters:
            if self._check_letter(letter):
                if letter.lower() in self.remaining_letters:
                    self.remaining_letters.remove(letter)
            else:
                return
        return

    def update_all_incorrect_places(self, letters):
        if letters is None:
            return

        if isinstance(letters, tuple):
            self._update_incorrect_place(letters)

        else:
            for letter in letters:
                self._update_incorrect_place(letter)
        return

    def update_all_correct_places(self, letters):
        if letters is None:
            return

        if isinstance(letters, tuple):
            self._update_correct_place(letters)

        else:
            for letter in letters:
                self._update_correct_place(letter)

        return

    def check_base_word(self, base_word):
        for letter in self.incorrect_place:
            if base_word[letter[0]] == letter[1]:
                return False
        return True

    def guess(self):
        output = []

        permutations = sum(
            [
                len(self.remaining_letters) ** len([i for i in j if i == None])
                for j in self.base_words
            ]
        )

        display(ipyHTML(f"<h4>There are {permutations} permutations</h4>"))

        if permutations > PERMUTATION_CUTOFF:
            display(ipyHTML(f"<i>There are too many permutations to compute</i>"))
            return

        for base_word in self.base_words:
            empty_idx = [i for i, x in enumerate(base_word) if x == None]
            for i in itertools.product(self.remaining_letters, repeat=len(empty_idx)):
                test_word = base_word.copy()
                for idx, letter in zip(empty_idx, i):
                    test_word[idx] = letter
                if self.check_base_word(test_word):
                    test_word = "".join(test_word)
                    if test_word in self.dict:
                        output.append(test_word)
        return set(output)

    def _check_letter(self, letter):
        if letter not in list(string.ascii_lowercase):
            display(ipyHTML(f"<i>{letter} is not a valid letter</i>"))
            return False
        return True

    def _update_incorrect_place(self, letter):
        if (
            isinstance(letter, tuple)
            and isinstance(letter[0], int)
            and isinstance(letter[1], str)
        ):
            if self._check_letter(letter[1]):
                self.incorrect_place.append(letter)
                if letter[1] not in self.correct_letters:
                    self.correct_letters.append(letter[1])
            else:
                return
        else:
            raise ValueError

    def _update_correct_place(self, letter):
        if (
            isinstance(letter, tuple)
            and isinstance(letter[0], int)
            and isinstance(letter[1], str)
        ):
            if self._check_letter(letter[1]):
                self.word[letter[0]] = letter[1]
                if letter[1] in self.correct_letters:
                    self.correct_letters.remove(letter[1])
                return
            else:
                return
        else:
            raise ValueError


    def _import_dictionary(self, dict_path):
        dictionary = []
        with open(dict_path, "r") as f:
            for line in f:
                dictionary.append(line.strip())
        return dictionary