# 🏥 SwasthyaGuide - Multilingual Healthcare Assistant

**SwasthyaGuide** is a compassionate, multilingual healthcare chatbot designed for urban and semi-urban users in India, including people with low literacy levels. It provides simple, safe health guidance via **WhatsApp** and helps users find nearby clinics when needed.

---

## 💬 Try It Now on WhatsApp!

**Want to experience SwasthyaGuide?** Send a message to our chatbot on WhatsApp:

### 📱 How to Get Started:

1. **Open WhatsApp** on your phone

2. **Save this number:** `+1 415 523 8886`

3. **Send this activation code:**
   ```
   join yellow-cheese
   ```

4. **Start chatting!** Try messages like:
   - `Mujhe sir dard ho raha hai` (Hindi)
   - `I have fever` (English)
   - `Mumbai mein clinic chahiye` (Find clinic)
   - `chest pain` (Emergency test)

### 🎯 Example Conversations:

```
You: Mujhe bukhar hai
Bot: [Provides fever guidance in Hindi]

You: Doctor chahiye Andheri
Bot: [Lists nearby clinics with addresses]

You: chest pain
Bot: [Sends emergency alert with 108 number]
```

**📲 WhatsApp Number:** +1 415 523 8886  
**🔑 Activation Code:** `join yellow-cheese`

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

## 🚀 Quick Start

### Option 1: Automated Setup (Recommended)
```bash
python setup.py
```

### Option 2: Manual Setup
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file
copy .env.example .env

# 3. Edit .env with your Twilio credentials
notepad .env

# 4. Run locally
python app.py
```

## 📁 Project Structure

```
Prakalp-Swasthya/
├── app.py                     # Flask web application (WhatsApp webhook)
├── main.py                    # CLI entry point
├── chatbot.py                 # Main orchestrator
├── config_loader.py           # Environment configuration
├── language_detector.py       # Language detection
├── emergency_handler.py       # Emergency detection & responses
├── symptom_checker.py         # Symptom extraction
├── health_responses.py        # Health guidance templates
├── clinic_finder.py          # Clinic search functionality
├── setup.py                   # Automated setup script
├── requirements.txt           # Python dependencies
├── Procfile                   # Render deployment config
├── .env.example              # Environment variables template
├── .gitignore                # Git ignore rules
├── config.json               # App configuration
├── README.md                 # This file
├── DEPLOYMENT_GUIDE.md       # Complete deployment guide
└── data/
    ├── clinics.json         # Clinic database
    └── translations.json    # Language translations
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

### Deploy to Render (Free)

**Full step-by-step guide:** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

**Quick steps:**
1. Push code to GitHub
2. Create Render web service
3. Add environment variables
4. Configure Twilio webhook
5. Test on WhatsApp!

## 🎯 Usage Examples

### 📱 Live WhatsApp Demo

**Try it yourself!**
1. WhatsApp: `+1 415 523 8886`
2. Send: `join yellow-cheese`
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

1. **Add to WhatsApp:** +1 415 523 8886
2. **Activate:** Send `join yellow-cheese`
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

### 💬 Try the Live Bot
- **WhatsApp:** +1 415 523 8886
- **Activation:** Send `join yellow-cheese`
- **Available:** 24/7

### 🐛 Report Issues
- **GitHub Issues**: [Open an issue](https://github.com/anubhavy-05/Prakalp-Swasthya/issues)
- **Documentation**: See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
- **Repository**: [github.com/anubhavy-05/Prakalp-Swasthya](https://github.com/anubhavy-05/Prakalp-Swasthya)

### 🌐 Live Demo
- **Web App**: https://prakalp-swasthya.onrender.com
- **Health Check**: https://prakalp-swasthya.onrender.com/health

## 🎉 Acknowledgments

- Built for accessible healthcare in India
- Inspired by the need for multilingual health information
- Thanks to Twilio for WhatsApp Business API
- Thanks to Render for free hosting

---

**Made with ❤️ for accessible healthcare guidance in India**

*"स्वास्थ्य सबका अधिकार है - Health is everyone's right"*

---

## 📚 Additional Resources

- [Twilio WhatsApp API Docs](https://www.twilio.com/docs/whatsapp)
- [Render Deployment Docs](https://render.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)

## 🆘 Troubleshooting

### Common Issues:

**Problem**: Import errors
```bash
# Solution
pip install -r requirements.txt
```

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
