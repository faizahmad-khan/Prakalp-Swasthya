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
from image_analyzer import ImageAnalyzer


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
        # Initialize image analyzer
        self.image_analyzer = ImageAnalyzer()
    
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
        
        # Check if user is asking about image analysis
        if self.image_analyzer.detect_image_request(user_input):
            return self.image_analyzer.get_image_analysis_instructions(language)
        
        # Check if user wants skin condition info
        if any(word in user_input.lower() for word in ['skin', 'rash', 'daad', 'kharish', 'त्वचा', 'खुजली']):
            return self.image_analyzer.get_common_skin_conditions_info(language)
        
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
    
    def process_image_message(self, image_data: bytes, caption: str = "", content_type: str = "image/jpeg") -> str:
        """
        Process image message with optional caption
        Returns formatted response with image analysis
        """
        # Detect language from caption if provided
        language = detect_language(caption) if caption else 'english'
        self.user_context['language'] = language
        
        # Analyze the image
        result = self.image_analyzer.analyze_skin_condition(image_data, language)
        
        if not result['success']:
            # Return error message
            error_responses = {
                'hindi': f"❌ छवि त्रुटि: {result['error']}\n\nकृपया:\n• एक स्पष्ट फोटो भेजें\n• अच्छी रोशनी में फोटो लें\n• 10MB से छोटी छवि भेजें",
                'english': f"❌ Image Error: {result['error']}\n\nPlease:\n• Send a clear photo\n• Take photo in good lighting\n• Send image smaller than 10MB"
            }
            return error_responses.get(language, error_responses['english'])
        
        # Format successful analysis response
        analysis = result['analysis']
        recommendations = '\n'.join(analysis['recommendations'])
        
        response = f"""
✅ Image analysis complete!

{recommendations}

{analysis['disclaimer']}

💬 Kuch aur puchhna chahenge? / Any other questions?
"""
        
        return response.strip()
    
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
