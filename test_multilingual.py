# -*- coding: utf-8 -*-
"""
Multilingual Support Test Script
Tests language detection and response generation in all 8 languages
"""

from language_detector import detect_language, get_language_name
from chatbot import SwasthyaGuide

# Test cases for each language
test_cases = {
    'hindi': [
        "Mujhe sir dard ho raha hai",
        "Bukhar hai aur kamzori mehsoos ho rahi hai",
        "Mumbai Andheri mein clinic chahiye"
    ],
    'english': [
        "I have a headache",
        "I have fever and feeling weak",
        "I need a clinic in Mumbai Andheri"
    ],
    'marathi': [
        "मला डोकेदुखी आहे",
        "मला ताप आहे आणि कमकुवत वाटत आहे",
        "मुंबई अंधेरी मध्ये क्लिनिक हवे आहे"
    ],
    'bengali': [
        "আমার মাথা ব্যথা আছে",
        "আমার জ্বর আছে এবং দুর্বল লাগছে",
        "মুম্বাই আন্ধেরিতে ক্লিনিক দরকার"
    ],
    'tamil': [
        "எனக்கு தலைவலி இருக்கிறது",
        "எனக்கு காய்ச்சல் மற்றும் பலவீனமாக உணர்கிறேன்",
        "மும்பை அந்தேரியில் கிளினிக் வேண்டும்"
    ],
    'telugu': [
        "నాకు తలనొప్పి ఉంది",
        "నాకు జ్వరం మరియు బలహీనంగా అనిపిస్తోంది",
        "ముంబై అంధేరిలో క్లినిక్ కావాలి"
    ],
    'punjabi': [
        "ਮੈਨੂੰ ਸਿਰ ਦਰਦ ਹੋ ਰਿਹਾ ਹੈ",
        "ਮੈਨੂੰ ਬੁਖ਼ਾਰ ਹੈ ਅਤੇ ਕਮਜ਼ੋਰ ਮਹਿਸੂਸ ਹੋ ਰਿਹਾ ਹੈ",
        "ਮੁੰਬਈ ਅੰਧੇਰੀ ਵਿੱਚ ਕਲੀਨਿਕ ਚਾਹੀਦੀ ਹੈ"
    ],
    'gujarati': [
        "મને માથાનો દુખાવો છે",
        "મને તાવ છે અને નબળાઈ લાગે છે",
        "મુંબઈ અંધેરીમાં ક્લિનિક જોઈએ છે"
    ]
}

def test_language_detection():
    """Test language detection for all languages"""
    print("=" * 70)
    print("TESTING LANGUAGE DETECTION")
    print("=" * 70)
    
    for expected_lang, messages in test_cases.items():
        print(f"\n📝 Testing {get_language_name(expected_lang)}:")
        print("-" * 70)
        
        for msg in messages:
            detected_lang = detect_language(msg)
            status = "✅" if detected_lang == expected_lang else "❌"
            print(f"{status} Input: {msg[:50]}...")
            print(f"   Expected: {expected_lang}, Detected: {detected_lang}")
            
            if detected_lang != expected_lang:
                print(f"   ⚠️  MISMATCH!")
        print()


def test_chatbot_responses():
    """Test chatbot responses in different languages"""
    print("\n" + "=" * 70)
    print("TESTING CHATBOT RESPONSES")
    print("=" * 70)
    
    bot = SwasthyaGuide()
    
    # Test specific messages in each language
    test_messages = {
        'hindi': "Mujhe bukhar hai",
        'english': "I have a fever",
        'marathi': "मला ताप आहे",
        'bengali': "আমার জ্বর আছে",
        'tamil': "எனக்கு காய்ச்சல் உள்ளது",
        'telugu': "నాకు జ్వరం ఉంది",
        'punjabi': "ਮੈਨੂੰ ਬੁਖ਼ਾਰ ਹੈ",
        'gujarati': "મને તાવ છે"
    }
    
    for lang, msg in test_messages.items():
        print(f"\n🗣️  Testing {get_language_name(lang)}:")
        print("-" * 70)
        print(f"Input: {msg}")
        
        response = bot.process_message(msg)
        
        # Show first 200 characters of response
        print(f"\nResponse preview:")
        print(response[:200] + "..." if len(response) > 200 else response)
        print()


def test_emergency_detection():
    """Test emergency detection in multiple languages"""
    print("\n" + "=" * 70)
    print("TESTING EMERGENCY DETECTION")
    print("=" * 70)
    
    bot = SwasthyaGuide()
    
    emergency_messages = {
        'hindi': "Mujhe chest pain ho raha hai",
        'english': "I have chest pain",
        'marathi': "मला छातीत दुखत आहे",
        'bengali': "আমার বুকে ব্যথা হচ্ছে",
        'tamil': "எனக்கு மார்பு வலி உள்ளது",
        'telugu': "నాకు ఛాతీ నొప్పి ఉంది",
        'punjabi': "ਮੈਨੂੰ ਛਾਤੀ ਵਿੱਚ ਦਰਦ ਹੈ",
        'gujarati': "મને છાતીમાં દુખાવો છે"
    }
    
    for lang, msg in emergency_messages.items():
        print(f"\n🚨 Testing {get_language_name(lang)}:")
        print("-" * 70)
        print(f"Input: {msg}")
        
        response = bot.process_message(msg)
        
        # Check if emergency response is triggered
        if "🚨" in response or "EMERGENCY" in response.upper():
            print("✅ Emergency detected correctly!")
        else:
            print("❌ Emergency NOT detected!")
        
        print(f"\nResponse preview:")
        print(response[:150] + "..." if len(response) > 150 else response)
        print()


def test_clinic_finder():
    """Test clinic finder in multiple languages"""
    print("\n" + "=" * 70)
    print("TESTING CLINIC FINDER")
    print("=" * 70)
    
    bot = SwasthyaGuide()
    
    clinic_messages = {
        'hindi': "Mumbai Andheri mein clinic chahiye",
        'english': "I need a clinic in Mumbai Andheri",
        'marathi': "मुंबई अंधेरी मध्ये क्लिनिक हवे",
        'bengali': "মুম্বাই আন্ধেরিতে ক্লিনিক দরকার",
        'tamil': "மும்பை அந்தேரியில் கிளினிக் வேண்டும்",
        'telugu': "ముంబై అంధేరిలో క్లినిక్ కావాలి",
        'punjabi': "ਮੁੰਬਈ ਅੰਧੇਰੀ ਵਿੱਚ ਕਲੀਨਿਕ ਚਾਹੀਦੀ ਹੈ",
        'gujarati': "મુંબઈ અંધેરીમાં ક્લિનિક જોઈએ"
    }
    
    for lang, msg in clinic_messages.items():
        print(f"\n🏥 Testing {get_language_name(lang)}:")
        print("-" * 70)
        print(f"Input: {msg}")
        
        response = bot.process_message(msg)
        
        # Check if clinic information is provided
        if "clinic" in response.lower() or "क्लिनिक" in response:
            print("✅ Clinic finder triggered!")
        else:
            print("❌ Clinic finder NOT triggered!")
        
        print(f"\nResponse preview:")
        print(response[:200] + "..." if len(response) > 200 else response)
        print()


def run_all_tests():
    """Run all multilingual tests"""
    print("\n" + "=" * 70)
    print("🌐 SWASTHYAGUIDE MULTILINGUAL SUPPORT TEST SUITE 🌐")
    print("=" * 70)
    print("\nTesting support for 8 languages:")
    print("Hindi, English, Marathi, Bengali, Tamil, Telugu, Punjabi, Gujarati")
    print("\n" + "=" * 70)
    
    try:
        # Run all test suites
        test_language_detection()
        test_chatbot_responses()
        test_emergency_detection()
        test_clinic_finder()
        
        print("\n" + "=" * 70)
        print("✅ ALL TESTS COMPLETED!")
        print("=" * 70)
        print("\n📊 Summary:")
        print("- Language Detection: TESTED")
        print("- Chatbot Responses: TESTED")
        print("- Emergency Detection: TESTED")
        print("- Clinic Finder: TESTED")
        print("\nℹ️  Review the output above for any ❌ failures.")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERROR during testing: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    run_all_tests()
