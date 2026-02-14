# -*- coding: utf-8 -*-
"""
SwasthyaGuide Chatbot - Main Class
Orchestrates all modules and handles conversation flow
"""

import json
import logging
from datetime import datetime
from .language_detector import detect_language
from .emergency_handler import detect_emergency, get_emergency_response
from .symptom_checker import extract_symptoms
from .health_responses import get_symptom_response, get_general_health_tips
from .clinic_finder import check_for_clinic_request, extract_location, find_nearby_clinics
from .image_analyzer import ImageAnalyzer

# Database imports (optional, for conversation logging)
try:
    from database import get_db_manager, Conversation, UserProfile, Analytics
    DB_AVAILABLE = True
except ImportError:
    DB_AVAILABLE = False
    logger.warning("Database module not available - conversation logging disabled")

logger = logging.getLogger(__name__)


class SwasthyaGuide:
    """Main chatbot class for SwasthyaGuide healthcare assistant"""
    
    def __init__(self, session_id=None, user_phone=None):
        """
        Initialize the SwasthyaGuide chatbot
        
        Args:
            session_id: Unique session identifier (e.g., WhatsApp phone number)
            user_phone: User's phone number
        """
        self.load_config()
        self.conversation_history = []
        self.session_id = session_id or f"session_{datetime.now().timestamp()}"
        self.user_phone = user_phone
        self.user_context = {
            'language': None,
            'location': None,
            'symptoms': [],
            'emergency_detected': False,
            'waiting_for_location': False,
            'last_detected_symptoms': []
        }
        # Initialize image analyzer
        self.image_analyzer = ImageAnalyzer()
        
        # Initialize database connection if available
        if DB_AVAILABLE:
            try:
                self.db_manager = get_db_manager()
                self.db_enabled = True
                logger.info("Database connection established for conversation logging")
            except Exception as e:
                logger.warning(f"Database not available: {e}")
                self.db_enabled = False
        else:
            self.db_enabled = False
    
    def load_config(self):
        """Load configuration"""
        try:
            with open('config.json', 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except FileNotFoundError:
            self.config = {'default_language': 'hindi'}
    
    def log_conversation(self, user_message: str, bot_response: str, 
                        detected_intent: str = 'general', 
                        message_type: str = 'text',
                        image_analysis: dict = None):
        """
        Log conversation to database
        
        Args:
            user_message: User's message
            bot_response: Bot's response
            detected_intent: Type of intent detected (symptom_check, clinic_search, etc.)
            message_type: Type of message (text, image, voice)
            image_analysis: Image analysis results if applicable
        """
        if not self.db_enabled:
            logger.debug("Database logging disabled")
            return
        
        try:
            with self.db_manager.get_session() as session:
                conversation = Conversation(
                    session_id=self.session_id,
                    user_phone=self.user_phone,
                    language=self.user_context['language'],
                    message_type=message_type,
                    user_message=user_message[:5000],  # Limit length
                    bot_response=bot_response[:5000],  # Limit length
                    detected_intent=detected_intent,
                    detected_symptoms=self.user_context.get('symptoms'),
                    detected_location=self.user_context.get('location'),
                    is_emergency=self.user_context.get('emergency_detected', False),
                    image_analysis=image_analysis,
                    created_at=datetime.utcnow()
                )
                session.add(conversation)
                session.commit()
                logger.debug(f"Conversation logged: {detected_intent}")
        
        except Exception as e:
            logger.error(f"Failed to log conversation: {e}")
    
    def update_user_profile(self):
        """Update or create user profile in database"""
        if not self.db_enabled or not self.user_phone:
            return
        
        try:
            with self.db_manager.get_session() as session:
                # Check if profile exists
                profile = session.query(UserProfile).filter_by(
                    phone_number=self.user_phone
                ).first()
                
                if profile:
                    # Update existing profile
                    profile.total_conversations += 1
                    profile.last_active = datetime.utcnow()
                    if self.user_context['language']:
                        profile.preferred_language = self.user_context['language']
                    if self.user_context['location']:
                        profile.location = self.user_context['location']
                else:
                    # Create new profile
                    profile = UserProfile(
                        phone_number=self.user_phone,
                        preferred_language=self.user_context.get('language', 'hindi'),
                        location=self.user_context.get('location'),
                        total_conversations=1,
                        last_active=datetime.utcnow(),
                        created_at=datetime.utcnow()
                    )
                    session.add(profile)
                
                session.commit()
                logger.debug(f"User profile updated: {self.user_phone}")
        
        except Exception as e:
            logger.error(f"Failed to update user profile: {e}")
    
    def process_message(self, user_input: str) -> str:
        """
        Main method to process user message and generate response
        """
        # Detect language
        language = detect_language(user_input)
        
        # Override: If English is detected, respond in Hindi
        if language == 'english':
            language = 'hindi'
        
        self.user_context['language'] = language
        
        # Initialize intent
        detected_intent = 'general'
        
        # Check if we're waiting for location from previous conversation
        if self.user_context.get('waiting_for_location', False):
            # Check if user is declining the clinic search (use word boundaries)
            user_input_lower = user_input.lower()
            user_words = user_input_lower.split()
            negative_words = ['nahi', 'no', 'nai', 'naa', 'cancel', 'rehne', 'mat']
            if any(word in user_words for word in negative_words):
                self.user_context['waiting_for_location'] = False
                if language == 'hindi':
                    response = "Theek hai. Koi baat nahi!\n\nAgar aapko koi aur madad chahiye toh bataayein. 😊"
                else:
                    response = "Okay, no problem!\n\nLet me know if you need any other help. 😊"
                self.log_conversation(user_input, response, 'declined_clinic')
                return response
            
            # Check if user is saying yes/haan (confirming they want clinic info)
            affirmative_words = ['yes', 'haan', 'ha', 'ji', 'zaroor', 'chahiye', 'chahie', 
                                'sure', 'ok', 'okay', 'please', 'kripya', 'batao', 'bataye']
            if any(word in user_words for word in affirmative_words) and len(user_input.split()) <= 3:
                # User confirmed but didn't provide location yet
                if language == 'hindi':
                    response = "Kripya apna area, city, ya pincode clearly bataayein.\n\nUdaharan: 'Lucknow', 'Gomti Nagar', '226010'"
                else:
                    response = "Please clearly share your area, city, or pincode.\n\nExample: 'Lucknow', 'Gomti Nagar', '226010'"
                self.log_conversation(user_input, response, 'location_request')
                return response
            
            # Try to extract location
            location = extract_location(user_input)
            if location:
                logger.info(f"User provided location (continuation): {location}")
                self.user_context['location'] = location
                self.user_context['waiting_for_location'] = False
                response = find_nearby_clinics(location, language)
                detected_intent = 'clinic_search'
                self.log_conversation(user_input, response, detected_intent)
                self.update_user_profile()
                return response
            else:
                # Still waiting for valid location
                if language == 'hindi':
                    response = "Kripya apna area, city, ya pincode clearly bataayein.\n\nUdaharan: 'Lucknow', 'Gomti Nagar', '226010'"
                else:
                    response = "Please clearly share your area, city, or pincode.\n\nExample: 'Lucknow', 'Gomti Nagar', '226010'"
                self.log_conversation(user_input, response, 'location_request')
                return response
        
        # Check if user is asking about image analysis
        if self.image_analyzer.detect_image_request(user_input):
            response = self.image_analyzer.get_image_analysis_instructions(language)
            detected_intent = 'image_request'
            self.log_conversation(user_input, response, detected_intent)
            return response
        
        # Check if user wants skin condition info
        if any(word in user_input.lower() for word in ['skin', 'rash', 'daad', 'kharish', 'त्वचा', 'खुजली']):
            response = self.image_analyzer.get_common_skin_conditions_info(language)
            detected_intent = 'skin_info'
            self.log_conversation(user_input, response, detected_intent)
            return response
        
        # Check for emergency
        if detect_emergency(user_input):
            self.user_context['emergency_detected'] = True
            response = get_emergency_response(language)
            detected_intent = 'emergency'
            self.log_conversation(user_input, response, detected_intent)
            return response
        
        # Check for clinic request
        if check_for_clinic_request(user_input):
            detected_intent = 'clinic_search'
            location = extract_location(user_input)
            if location:
                self.user_context['location'] = location
                self.user_context['waiting_for_location'] = False
                response = find_nearby_clinics(location, language)
            else:
                # Ask for location and set state
                self.user_context['waiting_for_location'] = True
                if language == 'hindi':
                    response = "Kripya apna area, city, ya pincode bataayein toh main aapko najdeeki clinic suggest kar sakta/sakti hoon.\n\nUdaharan: 'Lucknow', 'Gomti Nagar', '226010'"
                else:
                    response = "Please share your area, city, or pincode so I can suggest nearby clinics.\n\nExample: 'Lucknow', 'Gomti Nagar', '226010'"
            self.log_conversation(user_input, response, detected_intent)
            self.update_user_profile()
            return response
        
        # Extract and handle symptoms
        symptoms = extract_symptoms(user_input)
        if symptoms:
            self.user_context['symptoms'] = symptoms
            self.user_context['last_detected_symptoms'] = symptoms
            detected_intent = 'symptom_check'
            response = get_symptom_response(symptoms, language)
            
            # Set flag to wait for location if response asks about clinic
            if ('najdeeki clinic' in response.lower() or 
                'nearby clinic' in response.lower() or
                'clinic suggest' in response.lower()):
                self.user_context['waiting_for_location'] = True
                logger.info("Symptom response includes clinic question - waiting for location")
        else:
            # Default: general health tips
            response = get_general_health_tips(language)
        
        # Log conversation
        self.log_conversation(user_input, response, detected_intent)
        self.update_user_profile()
        
        return response
    
    def process_image_message(self, image_data: bytes, caption: str = "", content_type: str = "image/jpeg") -> str:
        """
        Process image message with optional caption
        Returns formatted response with image analysis
        """
        # Detect language from caption if provided
        language = detect_language(caption) if caption else 'hindi'
        
        # Override: If English is detected, respond in Hindi
        if language == 'english':
            language = 'hindi'
        
        self.user_context['language'] = language
        
        # Analyze the image
        result = self.image_analyzer.analyze_skin_condition(image_data, language)
        
        if not result['success']:
            # Return error message
            error_responses = {
                'hindi': f"❌ छवि त्रुटि: {result['error']}\n\nकृपया:\n• एक स्पष्ट फोटो भेजें\n• अच्छी रोशनी में फोटो लें\n• 10MB से छोटी छवि भेजें",
                'english': f"❌ Image Error: {result['error']}\n\nPlease:\n• Send a clear photo\n• Take photo in good lighting\n• Send image smaller than 10MB"
            }
            response = error_responses.get(language, error_responses['english'])
            self.log_conversation(caption or "[Image]", response, 'image_analysis', 'image')
            return response
        
        # Format successful analysis response
        analysis = result['analysis']
        recommendations = '\n'.join(analysis['recommendations'])
        
        response = f"""
✅ Image analysis complete!

{recommendations}

{analysis['disclaimer']}

💬 Kuch aur puchhna chahenge? / Any other questions?
"""
        
        # Log conversation with image analysis
        self.log_conversation(
            caption or "[Image]", 
            response, 
            'image_analysis', 
            'image',
            image_analysis=result
        )
        self.update_user_profile()
        
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
