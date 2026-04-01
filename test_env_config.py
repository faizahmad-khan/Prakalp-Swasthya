# -*- coding: utf-8 -*-
"""
Test script to verify .env file is properly configured
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

print("=" * 70)
print("🔍 CHECKING .ENV FILE CONFIGURATION")
print("=" * 70)

def check_env_var(var_name, required=True):
    """Check if environment variable exists and is not a placeholder"""
    value = os.getenv(var_name)
    
    if not value:
        status = "❌ MISSING"
        message = f"Not found in .env file"
    elif "your_" in value.lower() or "here" in value.lower() or "change" in value.lower():
        status = "⚠️  PLACEHOLDER"
        message = f"Needs to be replaced: {value[:30]}..."
    elif len(value) > 10:
        status = "✅ CONFIGURED" if required else "✅ SET"
        message = f"Value set: {value[:15]}..."
    else:
        status = "⚠️  SHORT"
        message = f"Value seems too short: {value}"
    
    print(f"\n{status} {var_name}")
    print(f"   └─ {message}")
    return status == "✅ CONFIGURED" or status == "✅ SET"

print("\n📋 REQUIRED FOR WHATSAPP BOT:")
check_env_var("TWILIO_ACCOUNT_SID")
check_env_var("TWILIO_AUTH_TOKEN")
check_env_var("TWILIO_PHONE_NUMBER")

print("\n\n⚙️  APPLICATION SETTINGS:")
check_env_var("FLASK_SECRET_KEY", required=False)
check_env_var("DATABASE_URL", required=False)
check_env_var("APP_NAME", required=False)

print("\n\n🔗 OPTIONAL (Alternative AI Services):")
check_env_var("ANTHROPIC_API_KEY", required=False)
check_env_var("OPENAI_API_KEY", required=False)

print("\n" + "=" * 70)
print("📝 SUMMARY:")
print("=" * 70)

print("\n💡 NEXT STEPS:")
print("   1. For WhatsApp: Get Twilio credentials from https://console.twilio.com")
print("   2. Update your .env file with actual credentials")
print("   3. Save the .env file and run this test again")
print("\n" + "=" * 70)
