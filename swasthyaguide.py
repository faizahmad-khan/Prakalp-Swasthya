#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SwasthyaGuide - Multilingual Healthcare Assistant
A compassionate chatbot for accessible health guidance in India
"""

import json
import re
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class SwasthyaGuide:
    """Main chatbot class for SwasthyaGuide healthcare assistant"""
    
    def __init__(self):
        """Initialize the SwasthyaGuide chatbot"""
        self.load_data()
        self.conversation_history = []
        self.user_context = {
            'language': None,
            'location': None,
            'symptoms': [],
            'emergency_detected': False
        }
        
    def load_data(self):
        """Load clinic data, translations, and configuration"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {'default_language': 'hindi'}
            
        try:
            with open('data/clinics.json', 'r', encoding='utf-8') as f:
                self.clinics = json.load(f)
        except FileNotFoundError:
            self.clinics = {}
            
        try:
            with open('data/translations.json', 'r', encoding='utf-8') as f:
                self.translations = json.load(f)
        except FileNotFoundError:
            self.translations = {}
    
    def detect_language(self, text: str) -> str:
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
    
    def detect_emergency(self, text: str) -> bool:
        """
        Detect emergency keywords in user input
        Returns: True if emergency detected
        """
        emergency_keywords = {
            'hindi': [
                'chest pain', 'seene mein dard', 'dil ka dard', 'saans nahi aa rahi',
                'bahut bleeding', 'khoon bah raha', 'behosh', 'accident',
                'stroke', 'paralysis', 'lakwa', 'heart attack'
            ],
            'english': [
                'chest pain', 'heart attack', 'can\'t breathe', 'breathing difficulty',
                'heavy bleeding', 'fainting', 'fainted', 'severe accident',
                'stroke', 'paralysis', 'unconscious'
            ]
        }
        
        text_lower = text.lower()
        
        for lang in emergency_keywords:
            for keyword in emergency_keywords[lang]:
                if keyword in text_lower:
                    return True
        
        return False
    
    def get_emergency_response(self, language: str) -> str:
        """Generate emergency response message"""
        responses = {
            'hindi': """
🚨 YEH EMERGENCY JAISA LAG RAHA HAI!

KRIPYA TURANT:
✅ Apne najdeeki hospital ya emergency service se sampark karein
✅ 108 (Ambulance) dial karein
✅ Kisi ko saath mein rakhein

Agar sambhav ho toh turant hospital jayein. Der na karein!
""",
            'english': """
🚨 THIS SEEMS LIKE AN EMERGENCY!

PLEASE IMMEDIATELY:
✅ Contact your nearest hospital or emergency service
✅ Call 108 (Ambulance)
✅ Have someone stay with you

If possible, go to the hospital right away. Don't delay!
"""
        }
        
        return responses.get(language, responses['hindi'])
    
    def extract_symptoms(self, text: str) -> List[str]:
        """Extract common symptoms from user input"""
        symptom_keywords = {
            'headache': ['sir dard', 'headache', 'head pain', 'sar dard'],
            'fever': ['bukhar', 'fever', 'tap', 'badan garam'],
            'cough': ['khansi', 'cough', 'khaansi'],
            'cold': ['sardi', 'cold', 'zukam', 'nazla'],
            'stomach_pain': ['pet dard', 'stomach pain', 'pet mein dard', 'paet dard'],
            'vomiting': ['ulti', 'vomit', 'vomiting', 'qai'],
            'diarrhea': ['dast', 'loose motion', 'diarrhea', 'pतला pakhana'],
            'body_pain': ['badan dard', 'body pain', 'body ache', 'sharir dard'],
            'weakness': ['kamzori', 'weakness', 'thakan', 'fatigue']
        }
        
        text_lower = text.lower()
        detected_symptoms = []
        
        for symptom, keywords in symptom_keywords.items():
            for keyword in keywords:
                if keyword in text_lower:
                    detected_symptoms.append(symptom)
                    break
        
        return detected_symptoms
    
    def get_symptom_response(self, symptoms: List[str], language: str) -> str:
        """
        Generate response based on detected symptoms
        Returns formatted health guidance
        """
        if not symptoms:
            return self.get_general_health_tips(language)
        
        # For this example, we'll handle headache
        if 'headache' in symptoms:
            return self.handle_headache(language)
        elif 'fever' in symptoms:
            return self.handle_fever(language)
        elif 'stomach_pain' in symptoms:
            return self.handle_stomach_pain(language)
        else:
            return self.get_general_symptom_advice(symptoms, language)
    
    def handle_headache(self, language: str) -> str:
        """Provide guidance for headache"""
        responses = {
            'hindi': """
1️⃣ **Sir dard ke samanya karan:**
Sir dard kai karan se ho sakta hai - kam neend, stress, dehydration, tension, aankh ki kamzori, ya long screen time.

2️⃣ **Ghar par aap ye try kar sakte hain:**
• Shaant aur andheri jagah mein aaram karein
• Pani zyada piyein (8-10 glass daily)
• Maatha par thanda pani ka patla kapda rakhein
• Aankh band karke 15-20 minute rest lein
• Screen time kam karein
• Halka stretching ya walk karein
• Proper neend lein (7-8 ghante)

3️⃣ **Doctor ko kab dikhaayein:**
⚠️ Agar dard bahut zyada ho
⚠️ 2-3 din se zyada chal raha ho
⚠️ Ulti, chakkar, ya dekhne mein dikkat ho
⚠️ Baar baar ho raha ho
⚠️ Ghar ke upay se aaraam nahi mil raha

4️⃣ **Kya aapko najdeeki clinic ki zaroorat hai?**
Agar haan, toh apna area, city, ya pincode bataayein.

5️⃣ **Disclaimer:**
Yeh medical diagnosis nahi hai. Agar condition serious lage toh turant doctor ko dikhaaye.
""",
            'english': """
1️⃣ **Common causes of headache:**
Headaches can be caused by lack of sleep, stress, dehydration, tension, eye strain, or prolonged screen time.

2️⃣ **Home care steps you can try:**
• Rest in a quiet, dark room
• Drink plenty of water (8-10 glasses daily)
• Apply a cool compress to your forehead
• Close your eyes and rest for 15-20 minutes
• Reduce screen time
• Do light stretching or take a walk
• Get proper sleep (7-8 hours)

3️⃣ **When to see a doctor:**
⚠️ If pain is very severe
⚠️ Lasts more than 2-3 days
⚠️ Accompanied by vomiting, dizziness, or vision problems
⚠️ Recurring frequently
⚠️ Home remedies don't provide relief

4️⃣ **Do you need nearby clinic information?**
If yes, please share your area, city, or pincode.

5️⃣ **Disclaimer:**
This is not a medical diagnosis. If the condition seems serious, please consult a doctor immediately.
"""
        }
        
        return responses.get(language, responses['hindi'])
    
    def handle_fever(self, language: str) -> str:
        """Provide guidance for fever"""
        responses = {
            'hindi': """
1️⃣ **Bukhar ke bare mein:**
Bukhar ek lakshan hai jo batata hai ki aapka sharir kisi infection se lad raha hai. Normal temperature 98.6°F (37°C) hota hai.

2️⃣ **Ghar par aap ye try kar sakte hain:**
• Zyada se zyada aaram karein
• Pani, juice, ORS, coconut water piyein
• Halka aur nutritious khana khayein (dal, khichdi, soup)
• Loose aur comfortable kapde pehenein
• Maatha par thanda pani ka kapda rakhein
• Kamre ka temperature comfortable rakhein

3️⃣ **Doctor ko kab dikhaayein:**
⚠️ Bukhar 102°F se zyada ho
⚠️ 3 din se zyada ho
⚠️ Bahut kamzori, chakkar, ya body pain ho
⚠️ Chhote bachche ya buzurg vyakti ho
⚠️ Saans lene mein dikkat, rash, ya ulti ho

4️⃣ **Kya aapko najdeeki clinic ki zaroorat hai?**
Apna area bataayein, main clinic suggest kar dunga/dungi.

5️⃣ **Disclaimer:**
Yeh medical diagnosis nahi hai. Agar condition serious lage toh turant doctor ko dikhaaye.
""",
            'english': """
1️⃣ **About fever:**
Fever is a symptom indicating your body is fighting an infection. Normal temperature is 98.6°F (37°C).

2️⃣ **Home care steps you can try:**
• Get plenty of rest
• Drink lots of fluids (water, juice, ORS, coconut water)
• Eat light, nutritious food (lentils, khichdi, soup)
• Wear loose, comfortable clothes
• Apply cool compress to forehead
• Keep room temperature comfortable

3️⃣ **When to see a doctor:**
⚠️ Fever above 102°F
⚠️ Lasts more than 3 days
⚠️ Severe weakness, dizziness, or body pain
⚠️ In young children or elderly
⚠️ Breathing difficulty, rash, or vomiting

4️⃣ **Do you need nearby clinic information?**
Share your area, and I'll suggest clinics.

5️⃣ **Disclaimer:**
This is not a medical diagnosis. If the condition seems serious, please consult a doctor immediately.
"""
        }
        
        return responses.get(language, responses['hindi'])
    
    def handle_stomach_pain(self, language: str) -> str:
        """Provide guidance for stomach pain"""
        responses = {
            'hindi': """
1️⃣ **Pet dard ke samanya karan:**
Pet dard kai karan se ho sakta hai - gas, acidity, indigestion, khane ki galti, constipation, ya infection.

2️⃣ **Ghar par aap ye try kar sakte hain:**
• Halka garam pani piyein
• Oily aur spicy khana avoid karein
• Chota meals, thodi-thodi der mein khayein
• Ajwain ya jeera pani piyein
• Light walk karein (heavy exercise nahi)
• Pet par halke haath se massage karein
• Proper neend lein

3️⃣ **Doctor ko kab dikhaayein:**
⚠️ Dard bahut tez ho ya 6-8 ghante se zyada ho
⚠️ Baar baar ulti ho rahi ho
⚠️ Pet bahut sakht ho ya chhune par dard ho
⚠️ Bukhar, khoon, ya kaale dast ho
⚠️ Pregnancy mein ho
⚠️ Dard badta ja raha ho

4️⃣ **Kya aapko najdeeki clinic ki zaroorat hai?**
Apna location share karein.

5️⃣ **Disclaimer:**
Yeh medical diagnosis nahi hai. Agar condition serious lage toh turant doctor ko dikhaaye.
""",
            'english': """
1️⃣ **Common causes of stomach pain:**
Stomach pain can be caused by gas, acidity, indigestion, food issues, constipation, or infection.

2️⃣ **Home care steps you can try:**
• Drink warm water
• Avoid oily and spicy food
• Eat small, frequent meals
• Drink ajwain or cumin water
• Take a light walk (no heavy exercise)
• Gently massage your stomach
• Get proper sleep

3️⃣ **When to see a doctor:**
⚠️ Pain is severe or lasts more than 6-8 hours
⚠️ Frequent vomiting
⚠️ Stomach is very hard or tender to touch
⚠️ Fever, blood in stool, or black stool
⚠️ If pregnant
⚠️ Pain is increasing

4️⃣ **Do you need nearby clinic information?**
Share your location.

5️⃣ **Disclaimer:**
This is not a medical diagnosis. If the condition seems serious, please consult a doctor immediately.
"""
        }
        
        return responses.get(language, responses['hindi'])
    
    def get_general_symptom_advice(self, symptoms: List[str], language: str) -> str:
        """Provide general advice for multiple symptoms"""
        responses = {
            'hindi': """
Aapke symptoms sun kar lagta hai aapko proper medical check-up ki zaroorat hai.

**Abhi kya karein:**
• Aaram karein aur zyada exertion avoid karein
• Pani zyada piyein
• Halka aur nutritious khana khayein
• Apne symptoms ko note karein

**Doctor ko zaroor dikhaayein agar:**
• Symptoms 2-3 din se zyada rahein
• Condition bigad rahi ho
• Daily activities karne mein dikkat ho

Kya main aapke liye najdeeki clinic dhoondh doon? Apna area, city, ya pincode bataayein.

**Disclaimer:**
Yeh medical diagnosis nahi hai. Agar condition serious lage toh turant doctor ko dikhaaye.
""",
            'english': """
Based on your symptoms, it seems you need a proper medical check-up.

**What to do now:**
• Rest and avoid excessive exertion
• Drink plenty of water
• Eat light, nutritious food
• Note down your symptoms

**See a doctor if:**
• Symptoms persist for more than 2-3 days
• Condition is worsening
• Difficulty performing daily activities

Should I find nearby clinics for you? Please share your area, city, or pincode.

**Disclaimer:**
This is not a medical diagnosis. If the condition seems serious, please consult a doctor immediately.
"""
        }
        
        return responses.get(language, responses['hindi'])
    
    def get_general_health_tips(self, language: str) -> str:
        """Provide general health tips"""
        responses = {
            'hindi': """
Namaste! Main SwasthyaGuide hoon. 🙏

**Mujhse aap ye pooch sakte hain:**
• Sir dard, bukhar, pet dard jaise common problems
• Ghar par kya kar sakte hain
• Doctor kab dikhana chahiye
• Najdeeki clinic kahan hai

**Kuch healthy tips:**
✅ Din mein 7-8 ghante soyein
✅ Pani zyada piyein (8-10 glass)
✅ Fruits aur vegetables khayein
✅ Thoda exercise ya walk daily karein
✅ Hand washing regularly karein

Aapki kya problem hai? Mujhe detail mein bataayein toh main better help kar sakta/sakti hoon.

**Yaad rakhein:**
Yeh medical diagnosis nahi hai. Serious problem ho toh doctor se zaroor milein.
""",
            'english': """
Hello! I'm SwasthyaGuide. 🙏

**You can ask me about:**
• Common problems like headache, fever, stomach pain
• What you can do at home
• When to see a doctor
• Where are nearby clinics

**Some healthy tips:**
✅ Sleep 7-8 hours daily
✅ Drink plenty of water (8-10 glasses)
✅ Eat fruits and vegetables
✅ Exercise or walk daily
✅ Wash hands regularly

What's troubling you? Please share details so I can help you better.

**Remember:**
This is not medical diagnosis. For serious issues, please consult a doctor.
"""
        }
        
        return responses.get(language, responses['hindi'])
    
    def find_nearby_clinics(self, location: str, language: str) -> str:
        """Find and return nearby clinics based on location"""
        location_lower = location.lower()
        
        # Search in clinic database
        matching_clinics = []
        for area, clinic_list in self.clinics.items():
            if area.lower() in location_lower or location_lower in area.lower():
                matching_clinics = clinic_list
                break
        
        if not matching_clinics:
            # No clinics found
            responses = {
                'hindi': f"""
Maaf kijiye, mere database mein "{location}" ke liye clinic information nahi hai.

**Aap ye kar sakte hain:**
• Google Maps par "clinic near me" search karein
• Local hospital ka helpline number call karein
• Kisi aur najdeeki area ka naam try karein

Ya fir doctor ko urgent dekhna hai toh:
• Najdeeki government hospital jayein
• 108 (Ambulance/Health helpline) dial karein

Koi aur area ka naam bataana chahenge?
""",
                'english': f"""
Sorry, I don't have clinic information for "{location}" in my database.

**You can try:**
• Search "clinic near me" on Google Maps
• Call local hospital helpline
• Try a different nearby area name

If urgent doctor visit needed:
• Visit nearest government hospital
• Dial 108 (Ambulance/Health helpline)

Would you like to try a different area?
"""
            }
            return responses.get(language, responses['hindi'])
        
        # Format clinic information
        clinic_text = ""
        
        if language == 'hindi':
            clinic_text = f"**{location} ke najdeeki clinics:**\n\n"
            for i, clinic in enumerate(matching_clinics[:3], 1):
                clinic_text += f"{i}. **{clinic['name']}**\n"
                clinic_text += f"   📍 Address: {clinic['address']}\n"
                if 'timing' in clinic:
                    clinic_text += f"   🕐 Timing: {clinic['timing']}\n"
                if 'phone' in clinic:
                    clinic_text += f"   📞 Phone: {clinic['phone']}\n"
                clinic_text += "\n"
            
            clinic_text += "**Yaad rakhein:** Jaane se pehle ek baar phone kar lein.\n"
        else:
            clinic_text = f"**Nearby clinics in {location}:**\n\n"
            for i, clinic in enumerate(matching_clinics[:3], 1):
                clinic_text += f"{i}. **{clinic['name']}**\n"
                clinic_text += f"   📍 Address: {clinic['address']}\n"
                if 'timing' in clinic:
                    clinic_text += f"   🕐 Timing: {clinic['timing']}\n"
                if 'phone' in clinic:
                    clinic_text += f"   📞 Phone: {clinic['phone']}\n"
                clinic_text += "\n"
            
            clinic_text += "**Remember:** Please call before visiting.\n"
        
        return clinic_text
    
    def check_for_clinic_request(self, text: str) -> bool:
        """Check if user is requesting clinic information"""
        clinic_keywords = [
            'clinic', 'hospital', 'doctor', 'clinic chahiye', 'doctor dikhaana',
            'najdeeki', 'nearby', 'paas mein', 'clinic dhundo', 'hospital kahan'
        ]
        
        text_lower = text.lower()
        return any(keyword in text_lower for keyword in clinic_keywords)
    
    def extract_location(self, text: str) -> Optional[str]:
        """Extract location from user input"""
        # Simple location extraction - looks for common patterns
        # In production, you'd use NER or location API
        
        # Remove common words
        words = text.split()
        location_words = []
        
        skip_words = ['mein', 'ka', 'ki', 'hai', 'hain', 'the', 'in', 'at', 'near']
        
        for word in words:
            if word.lower() not in skip_words and len(word) > 2:
                location_words.append(word)
        
        if location_words:
            return ' '.join(location_words[:3])  # Take first few words as location
        
        return None
    
    def process_message(self, user_input: str) -> str:
        """
        Main method to process user message and generate response
        """
        # Detect language
        language = self.detect_language(user_input)
        self.user_context['language'] = language
        
        # Check for emergency
        if self.detect_emergency(user_input):
            self.user_context['emergency_detected'] = True
            return self.get_emergency_response(language)
        
        # Check for clinic request
        if self.check_for_clinic_request(user_input):
            location = self.extract_location(user_input)
            if location:
                self.user_context['location'] = location
                return self.find_nearby_clinics(location, language)
            else:
                # Ask for location
                if language == 'hindi':
                    return "Kripya apna area, city, ya pincode bataayein toh main aapko najdeeki clinic suggest kar sakta/sakti hoon."
                else:
                    return "Please share your area, city, or pincode so I can suggest nearby clinics."
        
        # Extract and handle symptoms
        symptoms = self.extract_symptoms(user_input)
        if symptoms:
            self.user_context['symptoms'] = symptoms
            return self.get_symptom_response(symptoms, language)
        
        # Default: general health tips
        return self.get_general_health_tips(language)
    
    def run_cli(self):
        """Run the chatbot in command-line interface mode"""
        print("=" * 60)
        print("🏥 SwasthyaGuide - Multilingual Healthcare Assistant")
        print("=" * 60)
        print("\nNamaste! Main aapki health ki madad karne ke liye yahan hoon.")
        print("Hello! I'm here to help with your health questions.\n")
        print("Type 'exit' or 'quit' to end the conversation.\n")
        
        while True:
            try:
                user_input = input("You: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ['exit', 'quit', 'bye', 'alvida']:
                    print("\nSwasthyaGuide: Dhanyavaad! Swasth rahein! 🙏")
                    print("SwasthyaGuide: Thank you! Stay healthy! 🙏\n")
                    break
                
                # Process message
                response = self.process_message(user_input)
                print(f"\nSwasthyaGuide:\n{response}\n")
                
                # Store in conversation history
                self.conversation_history.append({
                    'timestamp': datetime.now().isoformat(),
                    'user': user_input,
                    'bot': response
                })
                
            except KeyboardInterrupt:
                print("\n\nSwasthyaGuide: Conversation ended. Take care! 🙏\n")
                break
            except Exception as e:
                print(f"\nError: {e}")
                print("Please try again.\n")


def main():
    """Main entry point for the application"""
    chatbot = SwasthyaGuide()
    chatbot.run_cli()


if __name__ == "__main__":
    main()
