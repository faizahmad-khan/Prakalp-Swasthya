# Debug language detection scoring
import sys
import re
sys.path.insert(0, 'src')

text = "mujhe bukhar hai"
text_lower = text.lower()

# Check if has Devanagari
has_devanagari = any(0x0900 <= ord(char) <= 0x097F for char in text)
print(f"Text: '{text}'")
print(f"Has Devanagari: {has_devanagari}")
print()

language_patterns = {
    'hinglish': {
        'patterns': ['hai', 'hain', 'mujhe', 'kya', 'aap', 'ko', 'se', 'mein', 
                    'ka', 'ki', 'ho', 'thi', 'tha', 'main', 'aapko', 'mere',
                    'tumhe', 'usko', 'yeh', 'woh', 'kaise', 'kahan', 'kab',
                    'bukhar', 'dard', 'sir', 'pet', 'kripya', 'zaroor', 'chahiye',
                    'najdeeki', 'batao', 'bataye', 'dijiye', 'karein', 'hona'],
        'weight': 1.2 if not has_devanagari else 0
    },
    'english': {
        'patterns': ['the', 'is', 'are', 'was', 'were', 'what', 'how', 'can', 
                    'have', 'has', 'with', 'for', 'from', 'this', 'that',
                    'my', 'your', 'his', 'her', 'their', 'pain', 'fever',
                    'headache', 'stomach', 'need', 'help', 'please', 'want'],
        'weight': 1
    },
}

scores = {}
for lang, data in language_patterns.items():
    count = 0
    matched_words = []
    for pattern in data['patterns']:
        if re.search(r'\b' + re.escape(pattern) + r'\b', text_lower):
            count += 1
            matched_words.append(pattern)
    scores[lang] = count * data['weight']
    print(f"{lang}:")
    print(f"  Weight: {data['weight']}")
    print(f"  Matched words: {matched_words}")
    print(f"  Count: {count}")
    print(f"  Score: {scores[lang]}")
    print()

print(f"Winner: {max(scores, key=scores.get)}")
