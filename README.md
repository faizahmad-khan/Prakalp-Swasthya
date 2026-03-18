# 🏥 SwasthyaGuide - Multilingual Healthcare Assistant

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green.svg)](https://flask.palletsprojects.com/)
[![Twilio](https://img.shields.io/badge/Twilio-WhatsApp-red.svg)](https://www.twilio.com/whatsapp)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15+-blue.svg)](https://www.postgresql.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**A compassionate, multilingual healthcare chatbot for accessible health guidance in India 🇮🇳**

[Try on WhatsApp](#-try-it-now) • [Features](#-features) • [Deploy Your Own](#-deployment) • [Documentation](#-documentation)

</div>

---

## 🆕 What's New in v2.0

### ⚡ PostgreSQL Database Integration
SwasthyaGuide has been upgraded with enterprise-grade PostgreSQL database:

- **✅ Conversation History** - Track all user interactions
- **✅ User Profiles** - Personalized experience with preferences
- **✅ Analytics & Metrics** - Usage statistics and insights
- **✅ Scalable Search** - Fast clinic lookup with indexing
- **✅ Cloud Ready** - Production deployment on Render/Railway/Heroku

**Quick Setup:** See [PostgreSQL Migration Guide](POSTGRESQL_MIGRATION.md) or [Quick Start (5 min)](POSTGRESQL_QUICKSTART.md)

---

## 📱 Try It Now on WhatsApp!

**Experience SwasthyaGuide in action:**

### Quick Start (30 seconds):

1. **Open WhatsApp** on your phone 📲

2. **Message this number:** [**+1 415 523 8886**](https://wa.me/14155238886?text=join%20dinner-brief)

3. **Send activation code:**
   ```
   join dinner-brief
   ```

4. **Start chatting!** Try:
   - `Mujhe sir dard ho raha hai` (Hindi - Headache)
   - `I have fever` (English)
   - `Mumbai mein clinic chahiye` (Find clinic)
   - `chest pain` (Emergency detection)

### 🎯 Example Conversations:

```
You: Mujhe bukhar hai
Bot: [Provides fever guidance in Hindi]

You: Doctor chahiye Andheri
Bot: [Lists nearby clinics with addresses]

You: chest pain
Bot: [Sends emergency alert with 108 number]
```

**📲 WhatsApp Number:** [+1 415 523 8886](https://wa.me/14155238886?text=join%20dinner-brief)  
**🔑 Activation Code:** `join dinner-brief`

---

## ✨ Features

### 🌐 Multilingual Support
- **Languages Supported**: Hindi, Hinglish, English, Marathi, Bengali, Tamil, Telugu, Punjabi, Gujarati
- Automatic language detection and response in the same language
- Simple, everyday words - no medical jargon

### 🩺 Health Guidance
- Basic health information and common causes
- Safe home-care steps
- Nutrition tips and hygiene guidance
- Lifestyle advice
- Warning signs recognition

### 🚨 Emergency Protocol
Immediate alerts for severe symptoms:
- Chest pain
- Breathing difficulty
- Heavy bleeding
- Fainting
- Stroke symptoms
- Severe accidents

### 🏥 Clinic Finder
- Location-based clinic search
- Nearby clinic suggestions with addresses
- Timing information
- Works with area name, city, or pincode

### 👩‍⚕️ Women's Health Mode
- Safe guidance on periods and cramps
- Pregnancy nutrition advice
- Hygiene tips
- PCOS basics
- Breast health information

### 🔍 Symptom Checker
Interactive symptom assessment:
- Duration of symptoms
- Pain intensity
- Fever check
- Additional symptoms
- Safe home care recommendations
- Red-flag symptom warnings

## 🛡️ Safety Features

**What SwasthyaGuide DOES:**
- ✅ Provide basic health information
- ✅ Suggest safe home care steps
- ✅ Identify warning signs
- ✅ Recommend doctor visits when needed
- ✅ Find nearby clinics

**What SwasthyaGuide DOES NOT DO:**
- ❌ Diagnose diseases
- ❌ Prescribe medicines
- ❌ Mention drug doses
- ❌ Recommend antibiotics
- ❌ Give harmful home remedies
- ❌ Make unsupported medical claims

---

## 📁 Project Structure

```
Prakalp-Swasthya/
├── app.py                    # Flask web server (WhatsApp webhook)
├── main.py                   # CLI interface entry point
├── requirements.txt          # Python dependencies
├── config.json              # Application configuration
├── Procfile                 # Heroku deployment config
├── render.yaml              # Render deployment config
├── README.md                # This file
│
├── src/                     # 📦 Source code modules
│   ├── chatbot.py          # Main chatbot orchestrator
│   ├── clinic_finder.py    # Clinic search & recommendations
│   ├── config_loader.py    # Configuration management
│   ├── emergency_handler.py # Emergency detection & response
│   ├── health_responses.py # Health guidance responses
│   ├── language_detector.py # Language detection
│   └── symptom_checker.py  # Symptom extraction & checking
│
├── database/                # 🗄️ Database layer (PostgreSQL)
│   ├── models.py           # SQLAlchemy ORM models
│   ├── connection.py       # Database connection manager
│   └── __init__.py         # Package initialization
│
├── scripts/                 # 🛠️ Utility scripts
│   ├── init_database.py    # Database initialization
│   └── migrate_to_postgres.py # JSON to PostgreSQL migration
│
├── docs/                    # 📚 Documentation
│   ├── README.md           # Documentation index
│   ├── QUICK_START.md      # 5-minute setup guide
│   ├── POSTGRESQL_QUICKSTART.md # Database setup
│   ├── POSTGRESQL_MIGRATION.md  # Complete migration guide
│   ├── DEPLOYMENT_GUIDE.md # Cloud deployment
│   ├── ARCHITECTURE.md     # System architecture
│   └── ... (more docs)
│
├── tests/                   # 🧪 Test suite
│   ├── unit/               # Unit tests
│   ├── integration/        # Integration tests
│   └── test_*.py           # Test files
│
└── data/                    # 📊 Data files
    ├── clinics.json        # Clinic database (467 clinics)
    └── translations.json   # Multilingual translations
```

### Quick Navigation
- 📖 **[Complete Documentation](docs/README.md)**
- 🚀 **[Quick Start Guide](docs/QUICK_START.md)**
- 🏗️ **[Architecture Details](docs/ARCHITECTURE.md)**
- ☁️ **[Deployment Guide](docs/DEPLOYMENT_GUIDE.md)**
- 🗄️ **[PostgreSQL Setup](docs/POSTGRESQL_QUICKSTART.md)**

---

## 🚀 Quick Start Guide

### For Users: Try the Live Bot
👉 **[Click here to chat on WhatsApp](https://wa.me/14155238886?text=join%20dinner-brief)** 👈

### For Developers: Deploy Your Own

#### Option 1: One-Click Deploy to Render (Recommended)

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

1. Click the button above
2. Connect your GitHub account
3. Add environment variables:
   - `TWILIO_ACCOUNT_SID` - Get from [Twilio Console](https://console.twilio.com)
   - `TWILIO_AUTH_TOKEN` - Get from [Twilio Console](https://console.twilio.com)
   - `FLASK_SECRET_KEY` - Generate: `python -c "import secrets; print(secrets.token_hex(32))"`
4. Deploy! ✨

#### Option 2: Local Development

```bash
# Clone the repository
git clone https://github.com/anubhavy-05/Prakalp-Swasthya.git
cd Prakalp-Swasthya

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
copy .env.example .env

# Edit .env with your credentials
notepad .env

# Test the bot locally
python test_webhook.py

# Run the web server
python app.py
```

**Visit:** http://localhost:5000 to see if it's running

## 📁 Project Structure

```
Prakalp-Swasthya/
├── 🚀 Core Application
│   ├── app.py                     # Flask webhook server (WhatsApp integration)
│   ├── main.py                    # CLI entry point for testing
│   ├── chatbot.py                 # Main orchestrator & conversation flow
│   └── test_webhook.py            # Local testing script
│
├── 🧠 Intelligence Modules
│   ├── language_detector.py       # Automatic language detection
│   ├── emergency_handler.py       # Critical symptom detection
│   ├── symptom_checker.py         # Symptom extraction & analysis
│   ├── health_responses.py        # Medical guidance templates
│   └── clinic_finder.py           # Location-based clinic search
│
├── ⚙️ Configuration
│   ├── config_loader.py           # Environment variable management
│   ├── config.json                # App settings & features
│   ├── .env.example               # Template for secrets
│   └── .gitignore                 # Git exclusion rules
│
├── 🗂️ Data
│   ├── data/clinics.json          # Medical facility database
│   └── data/translations.json     # Multilingual content
│
├── 🚢 Deployment
│   ├── requirements.txt           # Python dependencies
│   ├── Procfile                   # Heroku/Render config
│   ├── render.yaml                # Render deployment config
│   └── setup.py                   # Automated setup script
│
└── 📖 Documentation
    ├── README.md                  # Main documentation (you are here)
    ├── DEPLOYMENT_GUIDE.md        # Step-by-step deployment
    ├── WHY_NOT_WORKING.md         # Troubleshooting guide
    ├── WEBHOOK_FIX.md             # Webhook configuration help
    ├── ARCHITECTURE.md            # System architecture
    ├── PROJECT_SUMMARY.md         # Project overview
    └── QUICK_START.md             # Quick reference
```

## 📋 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Twilio account (for WhatsApp)
- Render account (for hosting)

### Setup Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/anubhavy-05/Prakalp-Swasthya.git
   cd Prakalp-Swasthya
   ```

2. **Run setup script**
   ```bash
   python setup.py
   ```

3. **Configure Twilio credentials**
   - Edit `.env` file
   - Add your Twilio Account SID and Auth Token
   - Get these from: https://console.twilio.com

4. **Test locally**
   ```bash
   python app.py
   # Visit: http://localhost:5000
   ```

## 🌐 Deployment

### Deploy to Render (FREE - Recommended)

**📖 Complete Guide:** [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) | **🆘 Troubleshooting:** [WHY_NOT_WORKING.md](WHY_NOT_WORKING.md)

**Quick Deploy Steps:**

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Deploy SwasthyaGuide"
   git push origin main
   ```

2. **Create Render Service**
   - Go to [render.com](https://render.com)
   - New Web Service → Connect your repo
   - Branch: `deployment-ready` or `main`
   - Build: `pip install -r requirements.txt`
   - Start: `gunicorn app:app`

3. **Add Environment Variables in Render**
   ```
   TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   TWILIO_AUTH_TOKEN=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
   FLASK_SECRET_KEY=[generated random key]
   ```

4. **Configure Twilio Webhook**
   - Twilio Console → WhatsApp Sandbox
   - Webhook URL: `https://your-app.onrender.com/whatsapp`
   - Method: POST
   - Save!

5. **Test It! 🎉**
   - Send WhatsApp message
   - Bot should respond immediately

**⚠️ Important:** First deployment takes 2-3 minutes. Free tier sleeps after 15 minutes of inactivity.

## 🎯 Usage Examples

### 📱 Live WhatsApp Demo

**Try it yourself!**
1. WhatsApp: `+1 415 523 8886`
2. Send: `join dinner-brief`
3. Start asking health questions!

---

### WhatsApp Interaction Examples:

**Example 1: Hindi Query**
```
You: Mujhe sir dard ho raha hai

Bot: 
1️⃣ Sir dard ke samanya karan:
Sir dard kai karan se ho sakta hai - kam neend, stress, dehydration...

2️⃣ Ghar par aap ye try kar sakte hain:
• Shaant aur andheri jagah mein aaram karein
• Pani zyada piyein...

[Full response with disclaimer]
```

**Example 2: Emergency**
```
You: Chest pain

Bot: 
🚨 YEH EMERGENCY JAISA LAG RAHA HAI!
KRIPYA TURANT:
✅ 108 (Ambulance) dial karein
...
```

**Example 3: Clinic Search**
```
You: Doctor chahiye Andheri

Bot:
**Andheri ke najdeeki clinics:**

1. Dr. Sharma Clinic
   📍 Address: ...
   🕐 Timing: 10 AM - 8 PM
   📞 Phone: ...
```

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with:

```env
# Flask Configuration
FLASK_ENV=production
FLASK_SECRET_KEY=your-secret-key
FLASK_DEBUG=False

# Twilio Configuration
TWILIO_ACCOUNT_SID=your_account_sid
TWILIO_AUTH_TOKEN=your_auth_token
TWILIO_PHONE_NUMBER=whatsapp:+14155238886

# Application Settings
APP_NAME=SwasthyaGuide
LOG_LEVEL=INFO
```

**⚠️ NEVER commit `.env` to Git!**

## 🧪 Testing

### Local CLI Testing
```bash
python main.py
```

### Web API Testing
```bash
# Start server
python app.py

# Test endpoints
curl http://localhost:5000/
curl http://localhost:5000/health
```

### WhatsApp Testing
**Try the live bot right now!**

1. **Add to WhatsApp:** [+1 415 523 8886](https://wa.me/14155238886?text=join%20dinner-brief)
2. **Activate:** Send `join dinner-brief`
3. **Start chatting:** Try `Mujhe sir dard ho raha hai`

Or deploy your own:
1. Deploy to Render
2. Configure Twilio webhook
3. Set up your WhatsApp number
4. Start helping users!

## 🔒 Security

- ✅ Environment variables for secrets
- ✅ `.gitignore` protects `.env`
- ✅ Input validation
- ✅ Error handling
- ✅ Request logging
- ✅ Message length limits

## 📊 Monitoring

### Health Check Endpoint
```bash
GET /health
```

Returns:
```json
{
  "status": "healthy",
  "timestamp": "2025-11-29T12:00:00"
}
```

### Logs
View logs in Render dashboard:
- Service → Logs
- Real-time monitoring
- Error tracking

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## ⚠️ Disclaimer

**SwasthyaGuide is an informational assistant only.**

- This is NOT a replacement for professional medical advice
- Always consult a qualified doctor for diagnosis and treatment
- In emergencies, call 108 or visit the nearest hospital immediately
- This chatbot cannot prescribe medications or diagnose conditions

## 📄 License

This project is licensed under the MIT License.

## 📞 Support & Contact

### 💬 Live Bot Demo
- **WhatsApp:** [**+1 415 523 8886**](https://wa.me/14155238886?text=join%20dinner-brief) 👈 Click to chat!
- **Activation Code:** `join dinner-brief`
- **Available:** 24/7 (may take 30s to wake from sleep)

### 🐛 Issues & Contributions
- **Report Bugs:** [GitHub Issues](https://github.com/anubhavy-05/Prakalp-Swasthya/issues)
- **Contribute:** Fork → Branch → PR
- **Documentation:** [Full Deployment Guide](DEPLOYMENT_GUIDE.md)
- **Source Code:** [github.com/anubhavy-05/Prakalp-Swasthya](https://github.com/anubhavy-05/Prakalp-Swasthya)

### 🔗 Links
- **Web Health Check:** `https://[your-app].onrender.com/health`
- **Twilio Console:** https://console.twilio.com
- **Render Dashboard:** https://dashboard.render.com

## 🎉 Acknowledgments

- Built for accessible healthcare in India
- Inspired by the need for multilingual health information
- Thanks to Twilio for WhatsApp Business API
- Thanks to Render for free hosting
Bot Not Responding on WhatsApp?

**📖 Read:** [WHY_NOT_WORKING.md](WHY_NOT_WORKING.md) - Complete troubleshooting guide

**Quick Checks:**

✅ **Is your app deployed?**
- Visit: `https://your-app.onrender.com/health`
- Should return: `{"status": "healthy", ...}`
- If 404 or error → App not deployed properly

✅ **Is Twilio webhook configured?**
- Twilio Console → WhatsApp Sandbox → Settings
- Webhook URL should be: `https://your-app.onrender.com/whatsapp`
- Method: POST
- If empty → Configure it!

✅ **Check logs:**
```bash
# In Render Dashboard
Service → Logs → Watch for incoming requests

# Should see:
"Webhook triggered - Method: POST"
"Received message: 'Mujhe sir dard...'"
"Response sent successfully"
```

### Common Issues:

| Problem | Solution |
|---------|----------|
| **Import errors** | Run: `pip install -r requirements.txt` |
| **`.env` not loaded** | Ensure `.env` exists and contains valid values |
| **Webhook 500 error** | Check Render logs for Python errors |
| **No response from bot** | Verify Twilio webhook URL is correct |
| **App sleeping** | Free tier sleeps after 15 min - first message wakes it (30s delay) |

**Still stuck?** Open an [issue on GitHub](https://github.com/anubhavy-05/Prakalp-Swasthya/issues

**Problem**: `.env` not loaded
```bash
# Solution
pip install python-dotenv
# Make sure .env file exists
```

**Problem**: Twilio webhook not working
```bash
# Solution
1. Check Render logs
2. Verify webhook URL in Twilio
3. Test /health endpoint
```

For more help, see [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)


## ✨ Features

### 🌐 Multilingual Support
- **Languages Supported**: Hindi, Hinglish, English, Marathi, Bengali, Tamil, Telugu, Punjabi, Gujarati
- Automatic language detection and response in the same language
- Simple, everyday words - no medical jargon

### 🩺 Health Guidance
- Basic health information and common causes
- Safe home-care steps
- Nutrition tips and hygiene guidance
- Lifestyle advice
- Warning signs recognition

### 🚨 Emergency Protocol
Immediate alerts for severe symptoms:
- Chest pain
- Breathing difficulty
- Heavy bleeding
- Fainting
- Stroke symptoms
- Severe accidents

### 🏥 Clinic Finder
- Location-based clinic search
- Nearby clinic suggestions with addresses
- Timing information
- Works with area name, city, or pincode

### 👩‍⚕️ Women's Health Mode
- Safe guidance on periods and cramps
- Pregnancy nutrition advice
- Hygiene tips
- PCOS basics
- Breast health information

### 🔍 Symptom Checker
Interactive symptom assessment:
- Duration of symptoms
- Pain intensity
- Fever check
- Additional symptoms
- Safe home care recommendations
- Red-flag symptom warnings

## 🛡️ Safety Features

**What SwasthyaGuide DOES:**
- ✅ Provide basic health information
- ✅ Suggest safe home care steps
- ✅ Identify warning signs
- ✅ Recommend doctor visits when needed
- ✅ Find nearby clinics

**What SwasthyaGuide DOES NOT DO:**
- ❌ Diagnose diseases
- ❌ Prescribe medicines
- ❌ Mention drug doses
- ❌ Recommend antibiotics
- ❌ Give harmful home remedies
- ❌ Make unsupported medical claims

## 📋 Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup Steps

1. **Clone or download this repository**
   ```bash
   cd chaboo
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure clinic data**
   - Edit `data/clinics.json` to add local clinic information
   - Update `config.json` for your settings

4. **Run the chatbot**
   ```bash
   python swasthyaguide.py
   ```

## 🎯 Usage Examples

### Example 1: Basic Query (Hindi)
**User:** "Mujhe sir dard ho raha hai"

**SwasthyaGuide:**
1️⃣ Sir dard kai karan se ho sakta hai - kam neend, stress, dehydration, ya aankh ki kamzori.

2️⃣ Aap ye try karein:
- Thoda aaram karein, shaant jagah mein baith jayein
- Pani piyein
- Halka khana khayein
- Aankh band karke 15-20 minute rest lein

3️⃣ Doctor ko dikhaayein agar:
- Dard bahut zyada ho
- 2-3 din se zyada ho
- Ulti ya chakkar aaye
- Dekhne mein dikkat ho

4️⃣ Kya aapko najdeeki clinic ki zaroorat hai? Apna area bataayein.

5️⃣ Yeh medical diagnosis nahi hai. Agar condition serious lage toh turant doctor ko dikhaaye.

### Example 2: Emergency (English)
**User:** "I'm having severe chest pain"

**SwasthyaGuide:**
🚨 Yeh emergency jaisa lag raha hai. Kripya turant apne najdeeki hospital ya emergency service se sampark karein.

Call 108 (Ambulance) immediately!

### Example 3: Clinic Search
**User:** "Doctor dekhna hai, Andheri area mein"

**SwasthyaGuide:**
Aapko doctor dekhna zaroori lag raha hai. Yahaan Andheri ke najdeeki clinics hain:

1. **Dr. Sharma Clinic**
   - Address: Shop 5, Andheri West, Mumbai
   - Timing: 10 AM - 8 PM
   
2. **HealthFirst Medical Center**
   - Address: Link Road, Andheri East, Mumbai
   - Timing: 9 AM - 9 PM

## 📁 Project Structure

```
chaboo/
├── swasthyaguide.py          # Main chatbot application
├── requirements.txt           # Python dependencies
├── config.json               # Configuration settings
├── data/
│   ├── clinics.json         # Clinic database
│   └── translations.json    # Language translations
└── README.md                 # This file
```

## ⚙️ Configuration

Edit `config.json` to customize:
- Default language
- Clinic search radius
- Emergency keywords
- API keys (if using external services)

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Add your improvements
4. Test thoroughly
5. Submit a pull request

## ⚠️ Disclaimer

**SwasthyaGuide is an informational assistant only.**

- This is NOT a replacement for professional medical advice
- Always consult a qualified doctor for diagnosis and treatment
- In emergencies, call 108 or visit the nearest hospital immediately
- This chatbot cannot prescribe medications or diagnose conditions

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For questions or issues, please open an issue on the repository.

---

**Made with ❤️ for accessible healthcare guidance in India**

*"स्वास्थ्य सबका अधिकार है - Health is everyone's right"*
