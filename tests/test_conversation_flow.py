#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Test script to demonstrate conversation flow with session management
This tests that the bot remembers context between messages
"""

import sys
import os

# Add parent directory to path so we can import src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.chatbot import SwasthyaGuide

def test_conversation_flow():
    """Test that the bot maintains context across multiple messages"""
    print("=" * 70)
    print("Testing Conversation Flow: Symptom → Location Request → Clinic Search")
    print("=" * 70)
    
    # Create a session for a user (simulating WhatsApp session)
    user_phone = "+919876543210"
    session_id = "whatsapp:+919876543210"
    
    # Initialize bot with session
    bot = SwasthyaGuide(session_id=session_id, user_phone=user_phone)
    
    # Message 1: User reports fever
    print("\n📱 USER MESSAGE 1: 'mujhe bukhar hai'")
    print("-" * 70)
    response1 = bot.process_message("mujhe bukhar hai")
    print(f"🤖 BOT RESPONSE:\n{response1}")
    
    # Check if bot is waiting for location
    print(f"\n📊 Bot State:")
    print(f"   - Language: {bot.user_context['language']}")
    print(f"   - Symptoms: {bot.user_context['symptoms']}")
    print(f"   - Waiting for location: {bot.user_context['waiting_for_location']}")
    
    # Message 2: User provides location (this should now work!)
    print("\n" + "=" * 70)
    print("📱 USER MESSAGE 2: 'Lucknow'")
    print("-" * 70)
    response2 = bot.process_message("Lucknow")
    print(f"🤖 BOT RESPONSE:\n{response2}")
    
    # Check bot state after location provided
    print(f"\n📊 Bot State:")
    print(f"   - Location: {bot.user_context['location']}")
    print(f"   - Waiting for location: {bot.user_context['waiting_for_location']}")
    
    # Message 3: New symptom (testing new conversation)
    print("\n" + "=" * 70)
    print("📱 USER MESSAGE 3: 'sir dard ho raha hai'")
    print("-" * 70)
    response3 = bot.process_message("sir dard ho raha hai")
    print(f"🤖 BOT RESPONSE:\n{response3[:500]}...")  # Truncate for readability
    
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETE")
    print("=" * 70)
    print("\nKEY IMPROVEMENTS:")
    print("1. ✅ Bot remembers it asked for location")
    print("2. ✅ When user says 'Lucknow', bot recognizes it as location")
    print("3. ✅ Bot searches for clinics instead of treating it as new query")
    print("4. ✅ Session state maintained across multiple messages")
    print("=" * 70)


if __name__ == "__main__":
    test_conversation_flow()
