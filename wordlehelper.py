import string
import enchant
import itertools

PERMUTATION_CUTOFF = 200000


class Wordle:
    def __init__(self):
        self.remaining_letters = list(string.ascii_lowercase)
        self.incorrect_place = []
        self.correct_letters = []
        self.word = [None, None, None, None, None]
        self.dict = enchant.Dict("en_US")

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

    def update_incorrect_letters(self, letters):
        if letters is None:
            return
        for letter in letters:
            if letter.lower() in self.remaining_letters:
                self.remaining_letters.remove(letter)
        return

    def update_correct_place(self, letters):
        if letters is None:
            return

        if isinstance(letters, tuple):
            if isinstance(letters[0], int) and isinstance(letters[1], str):
                self.word[letters[0]] = letters[1]
                if letters[1] in self.correct_letters:
                    self.correct_letters.remove(letters[1])
                return
            else:
                raise ValueError

        for letter in letters:
            if (
                isinstance(letter, tuple)
                and isinstance(letter[0], int)
                and isinstance(letter[1], str)
            ):
                self.word[letter[0]] = letter[1]
                if letter[1] in self.correct_letters:
                    self.correct_letters.remove(letter[1])
            else:
                raise ValueError

        return

    def update_incorrect_place(self, letters):
        if letters is None:
            return

        if isinstance(letters, tuple):
            if isinstance(letters[0], int) and isinstance(letters[1], str):
                self.incorrect_place.append(letters)
                if letters[1] not in self.correct_letters:
                    self.correct_letters.append(letters[1])
                return
            else:
                raise ValueError

        for letter in letters:
            if (
                isinstance(letter, tuple)
                and isinstance(letter[0], int)
                and isinstance(letter[1], str)
            ):
                self.incorrect_place.append(letter)
                if letter[1] not in self.correct_letters:
                    self.correct_letters.append(letter[1])
            else:
                raise ValueError
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

        print(f"{permutations=}")

        if permutations > PERMUTATION_CUTOFF:
            print(f"Too many permutations to guess")
            return

        for base_word in self.base_words:
            empty_idx = [i for i, x in enumerate(base_word) if x == None]
            for i in itertools.product(self.remaining_letters, repeat=len(empty_idx)):
                test_word = base_word.copy()
                for idx, letter in zip(empty_idx, i):
                    test_word[idx] = letter
                if self.check_base_word(test_word):
                    test_word = "".join(test_word)
                    if self.dict.check(test_word):
                        output.append(test_word)
        return set(output)

    def update(self, incorrect_letters=None, incorrect_place=None, correct_place=None):
        self.update_incorrect_letters(incorrect_letters)
        self.update_incorrect_place(incorrect_place)
        self.update_correct_place(correct_place)
        return self.guess()
