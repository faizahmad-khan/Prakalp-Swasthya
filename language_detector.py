# -*- coding: utf-8 -*-
"""
Language Detection Module
Detects user's language from input text
"""

def detect_language(text: str) -> str:
    """
    Detect the language of user input
    Returns: Language code (hindi, english, marathi, etc.)
    """
    # Hindi/Hinglish detection
    hindi_patterns = ['hai', 'hain', 'mujhe', 'kya', 'aap', 'ko', 'se', 'mein', 'ka', 'ki']
    # English detection
    english_patterns = ['the', 'is', 'are', 'what', 'how', 'can', 'have', 'with', 'for']
    
    text_lower = text.lower()
    
    hindi_count = sum(1 for pattern in hindi_patterns if pattern in text_lower)
    english_count = sum(1 for pattern in english_patterns if pattern in text_lower)
    
    if hindi_count > english_count:
        return 'hindi'
    else:
        return 'english'
