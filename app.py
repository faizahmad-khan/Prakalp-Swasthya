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
import requests

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
        
        # Check if image/media is attached
        if num_media > 0:
            logger.info(f"Processing {num_media} media file(s)")
            media_url = request.values.get('MediaUrl0', '')
            media_type = request.values.get('MediaContentType0', '')
            
            logger.info(f"Media URL: {media_url}, Type: {media_type}")
            
            # Download and process image
            try:
                # Download image from Twilio's media URL with authentication
                # Twilio requires HTTP Basic Auth to access media files
                auth = (Config.TWILIO_ACCOUNT_SID, Config.TWILIO_AUTH_TOKEN)
                media_response = requests.get(media_url, auth=auth, timeout=10)
                media_response.raise_for_status()
                image_data = media_response.content
                
                # Process image with caption/message
                bot_response = session_bot.process_image_message(image_data, incoming_msg, media_type)
                logger.info(f"Image processed successfully")
                
                resp = MessagingResponse()
                resp.message(bot_response)
                return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}
                
            except Exception as e:
                logger.error(f"Error processing image: {str(e)}", exc_info=True)
                resp = MessagingResponse()
                resp.message("छवि संसाधित करने में त्रुटि। कृपया पुनः प्रयास करें। / Error processing image. Please try again.")
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
        bot_response = session_bot.process_message(incoming_msg)
        logger.info(f"Bot response generated: {bot_response[:100]}...")
        
        # Create Twilio response
        resp = MessagingResponse()
        resp.message(bot_response)
        
        logger.info("Response sent successfully")
        return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}
        
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        
        # Send error message to user
        resp = MessagingResponse()
        resp.message("क्षमा करें, कुछ गलत हो गया। कृपया दोबारा प्रयास करें। / Sorry, something went wrong. Please try again.")
        return str(resp), 200, {'Content-Type': 'text/xml; charset=utf-8'}


if __name__ == '__main__':
    # Run Flask app locally for testing
    port = int(os.getenv('PORT', 5000))
    logger.info(f"Starting SwasthyaGuide on port {port}")
    app.run(debug=Config.DEBUG, host='0.0.0.0', port=port)
