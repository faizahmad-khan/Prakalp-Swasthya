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
from twilio.request_validator import RequestValidator
from chatbot import SwasthyaGuide
from config_loader import Config

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

# Initialize SwasthyaGuide bot instance globally
bot = SwasthyaGuide()
logger.info("SwasthyaGuide bot initialized")


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
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
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
        
        # Log incoming message (remove PII in production)
        logger.info(f"Received message: '{incoming_msg}' from {sender[:15]}...")
        
        # Validate message
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
        bot_response = bot.process_message(incoming_msg)
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
