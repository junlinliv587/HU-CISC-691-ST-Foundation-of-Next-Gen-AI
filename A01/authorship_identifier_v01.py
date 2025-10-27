# Write a function called clean_word that takes a word as input and returns the word with all characters converted to lowercase and any non-alphabetic characters removed from the beginning and end of the word. For example, clean_word("'Hello!") should return "hello".
def clean_word(word):
    word = word.lower()
    while len(word) > 0 and not word[0].isalpha():
        word = word[1:]
    while len(word) > 0 and not word[-1].isalpha():
        word = word[:-1]
    return word

# Write a function called split_string that takes a text string as input and splits it into a list of words using whitespace as the delimiter.
def split_string(text):
    return text.split()

# Write a function called average_word_length that takes a list of words as input and returns the average length of all words after cleaning each word using the clean_word function. Skip any words that become empty after cleaning.
def average_word_length(words):
    total_chars = 0
    total_words = 0
    for word in words:
        cleaned = clean_word(word)
        if cleaned != '':
            total_chars += len(cleaned)
            total_words += 1
    if total_words == 0:
        return 0
    return total_chars / total_words

# Write a function called different_to_total that takes a list of words as input and returns the ratio of different words to total words after cleaning each word. Count how many unique cleaned words there are and divide by the total number of non-empty cleaned words.
def different_to_total(words):
    cleaned_words = []
    for word in words:
        cleaned = clean_word(word)
        if cleaned != '':
            cleaned_words.append(cleaned)
    
    if len(cleaned_words) == 0:
        return 0
    
    unique_words = set(cleaned_words)
    return len(unique_words) / len(cleaned_words)

# Write a function called exactly_once_to_total that takes a list of words as input and returns the ratio of words that appear exactly once to the total number of words after cleaning. Count how many cleaned words appear only one time in the entire list.
def exactly_once_to_total(words):
    from collections import Counter
    cleaned_words = []
    for word in words:
        cleaned = clean_word(word)
        if cleaned != '':
            cleaned_words.append(cleaned)
    
    if len(cleaned_words) == 0:
        return 0
    
    word_counts = Counter(cleaned_words)
    once_words = sum(1 for count in word_counts.values() if count == 1)
    return once_words / len(cleaned_words)

# Test functions
def test_functions():
    print("Testing clean_word:")
    print(f"clean_word("'Hello!'") = {clean_word("'Hello!'")}")  # Expected: "hello"
    print(f"clean_word('world.') = {clean_word('world.')}")      # Expected: "world"
    print(f"clean_word('--test--') = {clean_word('--test--')}")  # Expected: "test"
    print()
    
    print("Testing split_string:")
    test_text = "This is a test sentence."
    print(f"split_string('{test_text}') = {split_string(test_text)}")
    print()
    
    print("Testing average_word_length:")
    test_words = ["hello", "world", "python", "programming"]
    print(f"average_word_length({test_words}) = {average_word_length(test_words)}")
    print()
    
    print("Testing different_to_total:")
    test_words_dup = ["hello", "world", "hello", "python", "world"]
    print(f"different_to_total({test_words_dup}) = {different_to_total(test_words_dup)}")
    print()
    
    print("Testing exactly_once_to_total:")
    print(f"exactly_once_to_total({test_words_dup}) = {exactly_once_to_total(test_words_dup)}")

if __name__ == "__main__":
    test_functions()