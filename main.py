import itertools
import re
import sys
from threading import Thread
from unicodedata import category


def convert_text_to_word_list(text):
    # remove case sensitivity
    case_insensitive_text = text.lower()
    # remove apostrophes and hyphens for contractions and compound words
    removed_contraction_punctuation_text = re.sub(r"[\'’-]", "", case_insensitive_text)
    # replace all other punctuation with whitespace (words will incorrectly join if you just remove the punctuation)
    replaced_punctuation_text = removed_contraction_punctuation_text.translate(
        dict.fromkeys((i for i in range(sys.maxunicode)
                      if category(chr(i)).startswith('P')  # P = Unicode punctuation
                      or category(chr(i)).startswith('S')),  # S = Unicode symbols
                      ' ')
    )
    # create a list of words based on characters between whitespaces
    word_list = replaced_punctuation_text.split()
    return word_list


def count_sequential_word_counts(word_list, sequence_dict):
    # loop through all words except last two
    for index, first_word in enumerate(word_list[:-2]):
        # create three-word sequence by taking current word plus the next two, separated by spaces
        word_sequence = first_word + " " + word_list[index + 1] + " " + word_list[index + 2]
        # keep track of how often the sequence shows up
        if sequence_dict.get(word_sequence):
            sequence_dict[word_sequence] += 1
        else:
            sequence_dict[word_sequence] = 1


def get_top_100_sequences(sequence_dict):
    # sort the sequence-count dict from greatest count to least and return the first 100 entries
    sorted_dict = dict(sorted(sequence_dict.items(), key=lambda item: item[1], reverse=True))
    top_100_sequences = dict(itertools.islice(sorted_dict.items(), 100))
    return top_100_sequences

# prep text from a file for processing
def read_and_count_sequences_from_file(file_path, sequence_dict):
    try:
        with open(file_path, encoding="utf-8-sig") as text_file:
            text = text_file.read()
    except FileNotFoundError:
        print("File not found at path: " + file_path)
    read_and_count_sequences(text, sequence_dict)

# prep text from stdin for processing
def read_and_count_sequences_from_stdin(sequence_dict):
    sys.stdin.reconfigure(encoding='utf-8')
    text = ''.join(sys.stdin.readlines())
    read_and_count_sequences(text, sequence_dict)

def read_and_count_sequences(text, sequence_dict):
    word_list = convert_text_to_word_list(text)
    count_sequential_word_counts(word_list, sequence_dict)


if __name__ == '__main__':
    threads = []
    sequence_dict = {}
    # read through the files and map the three-word sequences to how often they appear
    # each file will be mapped to a thread for processing
    if len(sys.argv) > 1:
        for file_path in sys.argv[1:]:
            thread = Thread(target=read_and_count_sequences_from_file, args=(file_path, sequence_dict))
            thread.start()
            threads.append(thread)
    else:
        thread = Thread(target=read_and_count_sequences_from_stdin, args=(sequence_dict,))
        thread.start()
        threads.append(thread)
    for thread in threads:
        thread.join()
    # once the files are read and processed, get the top 100 three-word sequences and print them
    most_common_word_sequences = get_top_100_sequences(sequence_dict)
    for sequence, count in most_common_word_sequences.items():
        print(sequence + " - " + str(count))

