import re
from collections import Counter
import string
import math

# Existing functions from v01 (keeping for compatibility)
def clean_word(word):
    """Clean a word by converting to lowercase and removing non-alphabetic characters from start and end"""
    word = word.lower()
    while len(word) > 0 and not word[0].isalpha():
        word = word[1:]
    while len(word) > 0 and not word[-1].isalpha():
        word = word[:-1]
    return word

def split_string(text):
    """Split a text string into a list of words using whitespace as delimiter"""
    return text.split()

def average_word_length(words):
    """Calculate the average length of words after cleaning"""
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

def different_to_total(words):
    """Calculate the ratio of different words to total words after cleaning"""
    cleaned_words = []
    for word in words:
        cleaned = clean_word(word)
        if cleaned != '':
            cleaned_words.append(cleaned)
    
    if len(cleaned_words) == 0:
        return 0
    
    unique_words = set(cleaned_words)
    return len(unique_words) / len(cleaned_words)

def exactly_once_to_total(words):
    """Calculate the ratio of words that appear exactly once to total words"""
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

# NEW ENHANCED FEATURE FUNCTIONS
def sentence_length_features(text):
    """Calculate sentence length related features
    Decision reason: Sentence length and structure are important indicators of author style
    """
    # Split text into sentences using regex
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    
    if not sentences:
        return 0, 0, 0
    
    # Calculate word count for each sentence
    sentence_lengths = [len(split_string(s)) for s in sentences]
    avg_sentence_length = sum(sentence_lengths) / len(sentence_lengths)
    max_sentence_length = max(sentence_lengths)
    
    # Calculate variance of sentence lengths
    if len(sentence_lengths) > 1:
        sentence_length_variance = sum((x - avg_sentence_length) ** 2 for x in sentence_lengths) / len(sentence_lengths)
    else:
        sentence_length_variance = 0
    
    return avg_sentence_length, max_sentence_length, sentence_length_variance

def punctuation_ratio(text):
    """Calculate punctuation usage frequency
    Decision reason: Punctuation habits are distinctive features of author style
    """
    if not text or len(text) == 0:
        return 0
    
    punct_count = sum(1 for char in text if char in string.punctuation)
    return punct_count / len(text)

def common_word_ratios(words):
    """Calculate the ratio of common function words
    Decision reason: Function word usage patterns are hard to consciously change, making them reliable author fingerprints
    """
    # Most common English function words
    common_words = {
        'the', 'and', 'to', 'of', 'a', 'in', 'that', 'is', 'it', 'with',
        'for', 'as', 'was', 'on', 'are', 'but', 'not', 'they', 'this', 'have'
    }
    
    cleaned_words = [clean_word(word) for word in words if clean_word(word)]
    
    if not cleaned_words:
        return 0
    
    common_count = sum(1 for word in cleaned_words if word in common_words)
    return common_count / len(cleaned_words)

def vocabulary_richness(words):
    """Calculate vocabulary richness using Honore's R measure
    Decision reason: Better reflects vocabulary diversity than simple type-token ratio
    """
    cleaned_words = [clean_word(word) for word in words if clean_word(word)]
    
    if not cleaned_words:
        return 0
    
    word_counts = Counter(cleaned_words)
    hapax_count = sum(1 for count in word_counts.values() if count == 1)  # Words appearing once
    V = len(word_counts)  # Number of unique words
    N = len(cleaned_words)  # Total number of words
    
    # Honore's R statistic: R = 100 * log(N) / (1 - (V1/V))
    if hapax_count == 0 or V == 0:
        return 0
    
    try:
        honor_r = 100 * (math.log(N) / (1 - (hapax_count / V)))
        return honor_r
    except (ValueError, ZeroDivisionError):
        return 0

def word_length_distribution(words):
    """Calculate word length distribution features
    Decision reason: Author preference for short vs long words is a stylistic feature
    """
    cleaned_words = [clean_word(word) for word in words if clean_word(word)]
    
    if not cleaned_words:
        return 0, 0
    
    word_lengths = [len(word) for word in cleaned_words]
    
    # Calculate ratio of long words (length > 6)
    long_words_ratio = sum(1 for length in word_lengths if length > 6) / len(word_lengths)
    
    # Calculate standard deviation of word lengths
    avg_length = sum(word_lengths) / len(word_lengths)
    length_variance = sum((length - avg_length) ** 2 for length in word_lengths) / len(word_lengths)
    length_std = math.sqrt(length_variance)
    
    return long_words_ratio, length_std

# ENHANCED SIGNATURE FUNCTION
def make_signature(text):
    """Enhanced signature function with 8 text features
    Decision reason: Multi-dimensional features better distinguish different author styles
    """
    words = split_string(text)
    
    # Original 3 basic features (maintaining backward compatibility)
    avg_len = average_word_length(words)
    diff_ratio = different_to_total(words)
    once_ratio = exactly_once_to_total(words)
    
    # New 5 enhanced features
    avg_sent_len, max_sent_len, sent_var = sentence_length_features(text)
    punct_ratio = punctuation_ratio(text)
    common_ratio = common_word_ratios(words)
    vocab_rich = vocabulary_richness(words)
    long_words_ratio, word_length_std = word_length_distribution(words)
    
    # Return tuple with 8 features (maintaining v01 compatible format)
    return (
        avg_len,                    # 0: Average word length
        diff_ratio,                 # 1: Word variety ratio
        once_ratio,                 # 2: Hapax legomena ratio
        avg_sent_len,               # 3: Average sentence length (new)
        punct_ratio,                # 4: Punctuation ratio (new)
        common_ratio,               # 5: Common word ratio (new)
        vocab_rich,                 # 6: Vocabulary richness (new)
        long_words_ratio            # 7: Long words ratio (new)
    )

def get_all_signatures(authors_texts):
    """Get enhanced feature signatures for all authors"""
    signatures = {}
    for author, text in authors_texts.items():
        signatures[author] = make_signature(text)
    return signatures

def make_guess(mystery_text, author_signatures):
    """Enhanced guessing function using weighted Euclidean distance
    Decision reason: Different features have different importance, weighting improves accuracy
    """
    mystery_sig = make_signature(mystery_text)
    
    best_author = None
    best_distance = float('inf')
    
    # Feature weights (based on linguistic importance)
    weights = [
        1.0,   # Average word length
        1.5,   # Word variety ratio (important)
        1.2,   # Hapax legomena ratio
        1.0,   # Average sentence length
        0.8,   # Punctuation ratio
        1.3,   # Common word ratio (important)
        1.4,   # Vocabulary richness (important)
        1.1    # Long words ratio
    ]
    
    for author, signature in author_signatures.items():
        distance = 0
        for i in range(len(mystery_sig)):
            weight = weights[i] if i < len(weights) else 1.0
            diff = mystery_sig[i] - signature[i]
            distance += weight * (diff ** 2)
        distance = distance ** 0.5
        
        if distance < best_distance:
            best_distance = distance
            best_author = author
    
    return best_author, best_distance  # Return author and distance score

# TESTING FUNCTIONS
def test_functions():
    """Test individual functions with sample data"""
    print("Testing clean_word:")
    print(f"clean_word(\"'Hello!'\") = {clean_word("'Hello!'")}")
    print(f"clean_word('world.') = {clean_word('world.')}")
    print(f"clean_word('--test--') = {clean_word('--test--')}")
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
    print()
    
    # Test new features
    print("Testing new enhanced features:")
    test_text = "Hello world! This is a test. Another sentence here."
    words = split_string(test_text)
    print(f"sentence_length_features('{test_text}') = {sentence_length_features(test_text)}")
    print(f"punctuation_ratio('{test_text}') = {punctuation_ratio(test_text)}")
    print(f"common_word_ratios({words}) = {common_word_ratios(words)}")
    print(f"vocabulary_richness({words}) = {vocabulary_richness(words)}")
    print(f"word_length_distribution({words}) = {word_length_distribution(words)}")

def test_complete_program():
    """Test the complete enhanced authorship identification system"""
    known_authors = {
        "Author A": "The quick brown fox jumps over the lazy dog. This is a simple sentence for testing purposes.",
        "Author B": "Programming is fun and challenging. We enjoy writing code and solving complex problems with algorithms.",
        "Author C": "Data science and machine learning are fascinating fields. They involve statistics, programming, and domain knowledge to extract insights."
    }
    
    author_signatures = get_all_signatures(known_authors)
    
    print("=== Enhanced Author Signatures (8 Features) ===")
    feature_names = [
        "Avg Word Length",
        "Word Variety Ratio", 
        "Hapax Legomena Ratio",
        "Avg Sentence Length",
        "Punctuation Ratio",
        "Common Word Ratio",
        "Vocabulary Richness",
        "Long Words Ratio"
    ]
    
    for author, sig in author_signatures.items():
        print(f"\n{author}:")
        for i, (name, value) in enumerate(zip(feature_names, sig)):
            print(f"  {name}: {value:.4f}")
    
    print("\n" + "="*50)
    
    mystery_texts = [
        "A quick brown animal leaps over a sleepy canine.",
        "Coding brings joy and presents difficult puzzles for us to solve.",
        "Machine intelligence and data analysis captivate many researchers today."
    ]
    
    for i, mystery_text in enumerate(mystery_texts, 1):
        guess, distance = make_guess(mystery_text, author_signatures)
        print(f"\nMystery Text {i}: '{mystery_text}'")
        print(f"Predicted Author: {guess}")
        print(f"Confidence Distance: {distance:.4f}")
        print(f"Mystery Text Signature: {[f'{x:.4f}' for x in make_signature(mystery_text)]}")

if __name__ == "__main__":
    print("=== Testing Individual Functions ===")
    test_functions()
    print("\n=== Testing Complete Enhanced Program ===")
    test_complete_program()

