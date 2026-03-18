# -*- coding: utf-8 -*-
"""
SwasthyaGuide - Flask Web Application
Twilio WhatsApp webhook integration for healthcare assistance
"""

import os
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from twilio.twiml.messaging_response import MessagingResponse
from src.chatbot import SwasthyaGuide
from src.config_loader import Config
from src.voice_handler import get_voice_handler

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Validate configuration
try:
    Config.validate()
    logger.info("Configuration validated successfully")
except ValueError as e:
    logger.warning(f"Configuration warning: {e}")

# Initialize database
try:
    from database import init_db
    db_manager = init_db(Config.DATABASE_URL)
    logger.info("Database connection initialized successfully")
    
    # Optionally create tables on startup (recommended for first deployment)
    # db_manager.create_tables()
    
except Exception as e:
    logger.error(f"Database initialization failed: {e}")
    logger.warning("Application will continue without database logging")

# Session management - store bot instances per user session
user_sessions = {}
session_timestamps = {}
SESSION_TIMEOUT = 1800  # 30 minutes in seconds

logger.info("SwasthyaGuide session manager initialized")


def cleanup_old_sessions():
    """Remove sessions that haven't been used in SESSION_TIMEOUT seconds"""
    current_time = datetime.now()
    sessions_to_remove = []
    
    for session_id, timestamp in session_timestamps.items():
        if (current_time - timestamp).total_seconds() > SESSION_TIMEOUT:
            sessions_to_remove.append(session_id)
    
    for session_id in sessions_to_remove:
        logger.info(f"Cleaning up inactive session: {session_id[:15]}...")
        user_sessions.pop(session_id, None)
        session_timestamps.pop(session_id, None)
    
    if sessions_to_remove:
        logger.info(f"Cleaned up {len(sessions_to_remove)} inactive sessions")


def get_or_create_session(sender: str, user_phone: str) -> SwasthyaGuide:
    """Get existing session or create new one, with cleanup of old sessions"""
    # Clean up old sessions periodically
    if len(user_sessions) > 50:  # Only cleanup if we have many sessions
        cleanup_old_sessions()
    
    # Update or create session
    if sender not in user_sessions:
        logger.info(f"Creating new session for {sender[:15]}...")
        user_sessions[sender] = SwasthyaGuide(session_id=sender, user_phone=user_phone)
    else:
        logger.info(f"Reusing existing session for {sender[:15]}...")
    
    # Update timestamp
    session_timestamps[sender] = datetime.now()
    
    return user_sessions[sender]


@app.route('/')
def home():
    """Root route - health check"""
    return jsonify({
        'status': 'running',
        'app': Config.APP_NAME,
        'version': Config.APP_VERSION,
        'message': 'SwasthyaGuide is Running! 🏥'
    })


@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    db_health = {'status': 'not_initialized'}
    
    # Check database health if available
    try:
        from database import get_db_manager
        db_manager = get_db_manager()
        db_health = db_manager.health_check()
    except Exception as e:
        db_health = {'status': 'unavailable', 'error': str(e)}
    
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'database': db_health
    }), 200


@app.route('/whatsapp', methods=['GET', 'POST'])
def whatsapp_webhook():
    """
    WhatsApp webhook endpoint
    GET: For Twilio webhook verification
    POST: Receives messages from Twilio and responds with health guidance
    """
    # Handle GET request for webhook verification
    if request.method == 'GET':
        logger.info("GET request received - webhook verification")
        return jsonify({
            'status': 'webhook active',
            'message': 'WhatsApp webhook is ready to receive messages'
        }), 200
    
    # Handle POST request for incoming messages
    try:
        # Log the incoming request for debugging
        logger.info(f"Webhook triggered - Method: {request.method}")
        logger.info(f"Request data: {request.values}")
        
        # Extract incoming message from Twilio request
        incoming_msg = request.values.get('Body', '').strip()
        sender = request.values.get('From', '')
        num_media = int(request.values.get('NumMedia', 0))
        
        # Extract phone number (remove whatsapp: prefix)
        user_phone = sender.replace('whatsapp:', '') if sender.startswith('whatsapp:') else sender
        
        # Get or create session-specific bot instance (maintain conversation context)
        session_bot = get_or_create_session(sender, user_phone)
        
        # Log incoming message (remove PII in production)
        logger.info(f"Received message: '{incoming_msg}' from {sender[:15]}... (Media: {num_media})")
        
        # Handle media messages (voice only supported for now)
        if num_media > 0:
            logger.info(f"Processing {num_media} media file(s)")
            media_type = request.values.get('MediaContentType0', '')
            media_url = request.values.get('MediaUrl0', '')
            
            logger.info(f"Media URL: {media_url}, Type: {media_type}")
            
            # --- VOICE MESSAGE HANDLING ---
            # Check if it's a voice/audio message
            if media_type and ('audio' in media_type.lower() or 'ogg' in media_type.lower()):
                logger.info(f"🎤 Voice message detected! Type: {media_type}")
                
                try:
                    # Get voice handler
                    voice_handler = get_voice_handler()
                    
                    # Verify Twilio credentials
                    if not Config.TWILIO_ACCOUNT_SID or Config.TWILIO_ACCOUNT_SID.startswith('your_'):
                        logger.error("Twilio credentials not configured!")
                        raise ValueError("Server configuration error")
                    
                    auth = (Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
                    
                    # Get user's language preference from session
                    user_language = session_bot.user_context.get('language', 'hindi')
                    
                    # Process voice message: download -> convert -> transcribe
                    logger.info("Processing voice message...")
                    transcribed_text, detected_language = voice_handler.process_voice_message(
                        media_url, 
                        auth, 
                        language_hint=user_language
                    )
                    
                    if not transcribed_text:
                        # Voice transcription failed
                        error_msg = voice_handler.get_error_message('unclear', user_language)
                        resp = MessagingResponse()
                        resp.message(error_msg)
                        return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}
                    
                    logger.info(f"✅ Voice transcribed: '{transcribed_text}'")
                    
                    # Process transcribed text through chatbot
                    bot_text_response = session_bot.process_message(transcribed_text, message_type='voice')
                    
                    # Log what we heard from user
                    logger.info(f"📝 Sending text response: {bot_text_response[:100]}...")
                    
                    # Convert bot's text response to speech
                    logger.info("🔊 Converting response to speech...")
                    audio_response = voice_handler.synthesize_speech(
                        bot_text_response, 
                        language=session_bot.user_context.get('language', 'hindi'),
                        voice_gender='FEMALE'
                    )
                    
                    resp = MessagingResponse()
                    msg = resp.message()
                    
                    # Send both text and audio response
                    # First, add transcription confirmation (so user knows we understood)
                    confirmation = f"🎤 आपने कहा: {transcribed_text}\n\n" if user_language == 'hindi' else f"🎤 You said: {transcribed_text}\n\n"
                    msg.body(confirmation + bot_text_response)
                    
                    # Attach audio response if synthesis succeeded
                    if audio_response:
                        # Save audio to temporary file and get URL
                        # Note: In production, upload to cloud storage (S3, GCS) and get public URL
                        # For now, send text response only
                        # TODO: Implement audio file upload to cloud storage
                        logger.info("✅ Audio response generated (upload to cloud storage required)")
                        msg.body(msg.body() + "\n\n🔊 [Audio response generated - cloud storage integration pending]")
                    
                    return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}
                    
                except Exception as voice_error:
                    logger.error(f"Voice message processing failed: {voice_error}", exc_info=True)
                    user_language = session_bot.user_context.get('language', 'hindi')
                    error_msg = voice_handler.get_error_message('service_unavailable', user_language)
                    resp = MessagingResponse()
                    resp.message(error_msg)
                    return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}

            # Non-audio media fallback (image analysis disabled)
            logger.info("Non-audio media received while image analysis is disabled")
            resp = MessagingResponse()
            resp.message(
                "Image analysis is temporarily disabled. Please send a text query.\n"
                "Image analysis filhaal disabled hai. Kripya text message bhejein."
            )
            return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}
        
        # Validate text message
        if not incoming_msg:
            logger.warning("Empty message received")
            resp = MessagingResponse()
            resp.message("कृपया अपना संदेश भेजें। / Please send your message.")
            return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}
        
        # Check message length
        if len(incoming_msg) > Config.MAX_MESSAGE_LENGTH:
            logger.warning(f"Message too long: {len(incoming_msg)} characters")
            resp = MessagingResponse()
            resp.message("संदेश बहुत लंबा है। कृपया छोटा संदेश भेजें। / Message too long. Please send a shorter message.")
            return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}
        
        # Process message through SwasthyaGuide bot
        logger.info(f"Processing message through bot...")
        try:
            bot_response = session_bot.process_message(incoming_msg)
            logger.info(f"Bot response generated successfully: {len(bot_response)} characters")
            logger.info(f"Bot response preview: {bot_response[:150]}...")
        except Exception as bot_error:
            logger.error(f"Error in bot.process_message(): {str(bot_error)}", exc_info=True)
            raise  # Re-raise to be caught by outer handler
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(bot_response)
        
        logger.info("Response sent successfully")
        return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}
        
    except Exception as e:
        logger.error(f"CRITICAL ERROR in whatsapp_webhook: {str(e)}", exc_info=True)
        logger.error(f"Error type: {type(e).__name__}")
        logger.error(f"Error occurred while processing: '{incoming_msg if 'incoming_msg' in locals() else 'N/A'}'")
        
        # Send error message to user
        resp = MessagingResponse()
        resp.message("क्षमा करें, कुछ गलत हो गया। कृपया दोबारा प्रयास करें। / Sorry, something went wrong. Please try again.")
        return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}


if __name__ == '__main__':
    # Run Flask app locally for testing
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting SwasthyaGuide on port {port}")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
