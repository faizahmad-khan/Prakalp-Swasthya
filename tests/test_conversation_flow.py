# Test the exact conversation flow from WhatsApp
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from chatbot import SwasthyaGuide

print("=" * 60)
print("Simulating WhatsApp Conversation Flow")
print("=" * 60)

# Create bot instance
bot = SwasthyaGuide(session_id="test_user", user_phone="+919876543210")

# Step 1: User says they have fever
print("\n1. User: 'Mujhe bukhar hai'")
response1 = bot.process_message("Mujhe bukhar hai")
print(f"Bot: {response1[:200]}...")
print(f"waiting_for_location: {bot.user_context.get('waiting_for_location')}")

# Step 2: User confirms they want clinic info
print("\n2. User: 'Ha'")
response2 = bot.process_message("Ha")
print(f"Bot: {response2[:200]}...")
print(f"waiting_for_location: {bot.user_context.get('waiting_for_location')}")

# Step 3: User provides pincode
print("\n3. User: '226010'")
response3 = bot.process_message("226010")
print(f"Bot: {response3[:400]}...")
print(f"waiting_for_location: {bot.user_context.get('waiting_for_location')}")

if "najdeeki" in response3 and "clinics mil gaye" in response3:
    print("\n✅ SUCCESS: Bot found and returned clinics!")
else:
    print("\n❌ ISSUE: Bot did not return clinics properly")
    print(f"Full response: {response3}")
