# -*- coding: utf-8 -*-
"""
Health Response Templates Module
Contains all health guidance responses for different symptoms
"""

from typing import List


def handle_headache(language: str) -> str:
    """Provide guidance for headache"""
    responses = {
        'hindi': """
1️⃣ **Sir dard ke samanya karan:**
Sir dard kai karan se ho sakta hai - kam neend, stress, dehydration, tension, aankh ki kamzori, ya long screen time.

2️⃣ **Ghar par aap ye try kar sakte hain:**
• Shaant aur andheri jagah mein aaram karein
• Pani zyada piyein (8-10 glass daily)
• Maatha par thanda pani ka patla kapda rakhein
• Aankh band karke 15-20 minute rest lein
• Screen time kam karein
• Halka stretching ya walk karein
• Proper neend lein (7-8 ghante)

3️⃣ **Doctor ko kab dikhaayein:**
⚠️ Agar dard bahut zyada ho
⚠️ 2-3 din se zyada chal raha ho
⚠️ Ulti, chakkar, ya dekhne mein dikkat ho
⚠️ Baar baar ho raha ho
⚠️ Ghar ke upay se aaraam nahi mil raha

4️⃣ **Kya aapko najdeeki clinic ki zaroorat hai?**
Agar haan, toh apna area, city, ya pincode bataayein.

5️⃣ **Disclaimer:**
Yeh medical diagnosis nahi hai. Agar condition serious lage toh turant doctor ko dikhaaye.
""",
        'english': """
1️⃣ **Common causes of headache:**
Headaches can be caused by lack of sleep, stress, dehydration, tension, eye strain, or prolonged screen time.

2️⃣ **Home care steps you can try:**
• Rest in a quiet, dark room
• Drink plenty of water (8-10 glasses daily)
• Apply a cool compress to your forehead
• Close your eyes and rest for 15-20 minutes
• Reduce screen time
• Do light stretching or take a walk
• Get proper sleep (7-8 hours)

3️⃣ **When to see a doctor:**
⚠️ If pain is very severe
⚠️ Lasts more than 2-3 days
⚠️ Accompanied by vomiting, dizziness, or vision problems
⚠️ Recurring frequently
⚠️ Home remedies don't provide relief

4️⃣ **Do you need nearby clinic information?**
If yes, please share your area, city, or pincode.

5️⃣ **Disclaimer:**
This is not a medical diagnosis. If the condition seems serious, please consult a doctor immediately.
"""
    }
    
    return responses.get(language, responses['hindi'])


def handle_fever(language: str) -> str:
    """Provide guidance for fever"""
    responses = {
        'hindi': """
1️⃣ **Bukhar ke bare mein:**
Bukhar ek lakshan hai jo batata hai ki aapka sharir kisi infection se lad raha hai. Normal temperature 98.6°F (37°C) hota hai.

2️⃣ **Ghar par aap ye try kar sakte hain:**
• Zyada se zyada aaram karein
• Pani, juice, ORS, coconut water piyein
• Halka aur nutritious khana khayein (dal, khichdi, soup)
• Loose aur comfortable kapde pehenein
• Maatha par thanda pani ka kapda rakhein
• Kamre ka temperature comfortable rakhein

3️⃣ **Doctor ko kab dikhaayein:**
⚠️ Bukhar 102°F se zyada ho
⚠️ 3 din se zyada ho
⚠️ Bahut kamzori, chakkar, ya body pain ho
⚠️ Chhote bachche ya buzurg vyakti ho
⚠️ Saans lene mein dikkat, rash, ya ulti ho

4️⃣ **Kya aapko najdeeki clinic ki zaroorat hai?**
Apna area bataayein, main clinic suggest kar dunga/dungi.

5️⃣ **Disclaimer:**
Yeh medical diagnosis nahi hai. Agar condition serious lage toh turant doctor ko dikhaaye.
""",
        'english': """
1️⃣ **About fever:**
Fever is a symptom indicating your body is fighting an infection. Normal temperature is 98.6°F (37°C).

2️⃣ **Home care steps you can try:**
• Get plenty of rest
• Drink lots of fluids (water, juice, ORS, coconut water)
• Eat light, nutritious food (lentils, khichdi, soup)
• Wear loose, comfortable clothes
• Apply cool compress to forehead
• Keep room temperature comfortable

3️⃣ **When to see a doctor:**
⚠️ Fever above 102°F
⚠️ Lasts more than 3 days
⚠️ Severe weakness, dizziness, or body pain
⚠️ In young children or elderly
⚠️ Breathing difficulty, rash, or vomiting

4️⃣ **Do you need nearby clinic information?**
Share your area, and I'll suggest clinics.

5️⃣ **Disclaimer:**
This is not a medical diagnosis. If the condition seems serious, please consult a doctor immediately.
"""
    }
    
    return responses.get(language, responses['hindi'])


def handle_stomach_pain(language: str) -> str:
    """Provide guidance for stomach pain"""
    responses = {
        'hindi': """
1️⃣ **Pet dard ke samanya karan:**
Pet dard kai karan se ho sakta hai - gas, acidity, indigestion, khane ki galti, constipation, ya infection.

2️⃣ **Ghar par aap ye try kar sakte hain:**
• Halka garam pani piyein
• Oily aur spicy khana avoid karein
• Chota meals, thodi-thodi der mein khayein
• Ajwain ya jeera pani piyein
• Light walk karein (heavy exercise nahi)
• Pet par halke haath se massage karein
• Proper neend lein

3️⃣ **Doctor ko kab dikhaayein:**
⚠️ Dard bahut tez ho ya 6-8 ghante se zyada ho
⚠️ Baar baar ulti ho rahi ho
⚠️ Pet bahut sakht ho ya chhune par dard ho
⚠️ Bukhar, khoon, ya kaale dast ho
⚠️ Pregnancy mein ho
⚠️ Dard badta ja raha ho

4️⃣ **Kya aapko najdeeki clinic ki zaroorat hai?**
Apna location share karein.

5️⃣ **Disclaimer:**
Yeh medical diagnosis nahi hai. Agar condition serious lage toh turant doctor ko dikhaaye.
""",
        'english': """
1️⃣ **Common causes of stomach pain:**
Stomach pain can be caused by gas, acidity, indigestion, food issues, constipation, or infection.

2️⃣ **Home care steps you can try:**
• Drink warm water
• Avoid oily and spicy food
• Eat small, frequent meals
• Drink ajwain or cumin water
• Take a light walk (no heavy exercise)
• Gently massage your stomach
• Get proper sleep

3️⃣ **When to see a doctor:**
⚠️ Pain is severe or lasts more than 6-8 hours
⚠️ Frequent vomiting
⚠️ Stomach is very hard or tender to touch
⚠️ Fever, blood in stool, or black stool
⚠️ If pregnant
⚠️ Pain is increasing

4️⃣ **Do you need nearby clinic information?**
Share your location.

5️⃣ **Disclaimer:**
This is not a medical diagnosis. If the condition seems serious, please consult a doctor immediately.
"""
    }
    
    return responses.get(language, responses['hindi'])


def get_general_symptom_advice(symptoms: List[str], language: str) -> str:
    """Provide general advice for multiple symptoms"""
    responses = {
        'hindi': """
Aapke symptoms sun kar lagta hai aapko proper medical check-up ki zaroorat hai.

**Abhi kya karein:**
• Aaram karein aur zyada exertion avoid karein
• Pani zyada piyein
• Halka aur nutritious khana khayein
• Apne symptoms ko note karein

**Doctor ko zaroor dikhaayein agar:**
• Symptoms 2-3 din se zyada rahein
• Condition bigad rahi ho
• Daily activities karne mein dikkat ho

Kya main aapke liye najdeeki clinic dhoondh doon? Apna area, city, ya pincode bataayein.

**Disclaimer:**
Yeh medical diagnosis nahi hai. Agar condition serious lage toh turant doctor ko dikhaaye.
""",
        'english': """
Based on your symptoms, it seems you need a proper medical check-up.

**What to do now:**
• Rest and avoid excessive exertion
• Drink plenty of water
• Eat light, nutritious food
• Note down your symptoms

**See a doctor if:**
• Symptoms persist for more than 2-3 days
• Condition is worsening
• Difficulty performing daily activities

Should I find nearby clinics for you? Please share your area, city, or pincode.

**Disclaimer:**
This is not a medical diagnosis. If the condition seems serious, please consult a doctor immediately.
"""
    }
    
    return responses.get(language, responses['hindi'])


def get_general_health_tips(language: str) -> str:
    """Provide general health tips"""
    responses = {
        'hindi': """
Namaste! Main SwasthyaGuide hoon. 🙏

**Mujhse aap ye pooch sakte hain:**
• Sir dard, bukhar, pet dard jaise common problems
• Ghar par kya kar sakte hain
• Doctor kab dikhana chahiye
• Najdeeki clinic kahan hai

**Kuch healthy tips:**
✅ Din mein 7-8 ghante soyein
✅ Pani zyada piyein (8-10 glass)
✅ Fruits aur vegetables khayein
✅ Thoda exercise ya walk daily karein
✅ Hand washing regularly karein

Aapki kya problem hai? Mujhe detail mein bataayein toh main better help kar sakta/sakti hoon.

**Yaad rakhein:**
Yeh medical diagnosis nahi hai. Serious problem ho toh doctor se zaroor milein.
""",
        'english': """
Hello! I'm SwasthyaGuide. 🙏

**You can ask me about:**
• Common problems like headache, fever, stomach pain
• What you can do at home
• When to see a doctor
• Where are nearby clinics

**Some healthy tips:**
✅ Sleep 7-8 hours daily
✅ Drink plenty of water (8-10 glasses)
✅ Eat fruits and vegetables
✅ Exercise or walk daily
✅ Wash hands regularly

What's troubling you? Please share details so I can help you better.

**Remember:**
This is not medical diagnosis. For serious issues, please consult a doctor.
"""
    }
    
    return responses.get(language, responses['hindi'])


def get_symptom_response(symptoms: List[str], language: str) -> str:
    """
    Generate response based on detected symptoms
    Returns formatted health guidance
    """
    if not symptoms:
        return get_general_health_tips(language)
    
    # Handle specific symptoms
    if 'headache' in symptoms:
        return handle_headache(language)
    elif 'fever' in symptoms:
        return handle_fever(language)
    elif 'stomach_pain' in symptoms:
        return handle_stomach_pain(language)
    else:
        return get_general_symptom_advice(symptoms, language)
