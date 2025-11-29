# -*- coding: utf-8 -*-
"""
SwasthyaGuide Chatbot - Main Class
Orchestrates all modules and handles conversation flow
"""

import json
from datetime import datetime
from language_detector import detect_language
from emergency_handler import detect_emergency, get_emergency_response
from symptom_checker import extract_symptoms
from health_responses import get_symptom_response, get_general_health_tips
from clinic_finder import check_for_clinic_request, extract_location, find_nearby_clinics


class SwasthyaGuide:
    """Main chatbot class for SwasthyaGuide healthcare assistant"""
    
    def __init__(self):
        """Initialize the SwasthyaGuide chatbot"""
        self.load_config()
        self.conversation_history = []
        self.user_context = {
            'language': None,
            'location': None,
            'symptoms': [],
            'emergency_detected': False
        }
    
    def load_config(self):
        """Load configuration"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {'default_language': 'hindi'}
    
    def process_message(self, user_input: str) -> str:
        """
        Main method to process user message and generate response
        """
        # Detect language
        language = detect_language(user_input)
        self.user_context['language'] = language
        
        # Check for emergency
        if detect_emergency(user_input):
            self.user_context['emergency_detected'] = True
            return get_emergency_response(language)
        
        # Check for clinic request
        if check_for_clinic_request(user_input):
            location = extract_location(user_input)
            if location:
                self.user_context['location'] = location
                return find_nearby_clinics(location, language)
            else:
                # Ask for location
                if language == 'hindi':
                    return "Kripya apna area, city, ya pincode bataayein toh main aapko najdeeki clinic suggest kar sakta/sakti hoon."
                else:
                    return "Please share your area, city, or pincode so I can suggest nearby clinics."
        
        # Extract and handle symptoms
        symptoms = extract_symptoms(user_input)
        if symptoms:
            self.user_context['symptoms'] = symptoms
            return get_symptom_response(symptoms, language)
        
        # Default: general health tips
        return get_general_health_tips(language)
    
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
