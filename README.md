# 🏥 SwasthyaGuide - Multilingual Healthcare Assistant

**SwasthyaGuide** is a compassionate, multilingual healthcare chatbot designed for urban and semi-urban users in India, including people with low literacy levels. It provides simple, safe health guidance and helps users find nearby clinics when needed.

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
