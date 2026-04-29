import os
import joblib
import pandas as pd
from flask import Flask, request, jsonify
from flask_cors import CORS
from translator import deep_translate

from dietary_rules import (
    get_conditions,
    get_foods,
    get_avoid,
    get_nutrition,
    get_warnings,
    get_supplements,
    get_reminders,
    get_pregnancy_cravings
)

# ================= PATHS =================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# frontend folder is in project root
FRONTEND_FOLDER = os.path.join(BASE_DIR, "frontend")

# if app.py is inside backend folder use this instead:
# FRONTEND_FOLDER = os.path.join(BASE_DIR, "..", "frontend")

# ================= FLASK APP =================
app = Flask(
    __name__,
    static_folder=FRONTEND_FOLDER,
    static_url_path=""
)

CORS(app)

# ================= FRONTEND ROUTES =================
@app.route("/")
def home():
    return app.send_static_file("index.html")

@app.route("/<path:path>")
def frontend_files(path):
    return app.send_static_file(path)

CSV_PATH = os.path.join(BASE_DIR, "Final_Food.csv")

df = pd.read_csv(CSV_PATH)
df.columns = df.columns.str.strip()   

# convert to dictionary
FOOD_DB = df.set_index("name_en").to_dict(orient="index")

# ================= MODEL =================

try:
    model = joblib.load(os.path.join(BASE_DIR, "../model/rf_model.pkl"))
except:
    model = None

# ================= SAFE INPUT =================

def safe_int(value, default=0):
    try:
         return int(value)
    except:
         return default
def safe_float(value, default=0.0):
    try:
          return float(value)
    except:
          return default

# ================= LANGUAGE =================

def t(en, si, lang):
     return si if lang == "si" else en

# ================= BMI =================

def get_bmi_status(bmi, lang):
    if bmi < 18.5:
        return t("Underweight", "අඩු බර", lang)
    elif bmi < 25:
        return t("Normal", "සාමාන්‍ය", lang)
    elif bmi < 30:
        return t("Overweight", "වැඩි බර", lang)
    else:
        return t("Obese", "අධික බර", lang)

def get_message(risk, lang):
    if risk == 0:
        return t("💚 You are healthy", "💚 ඔබ සෞඛ්‍ය සම්පන්නයි", lang)
    elif risk == 1:
        return t("⚠ Improve lifestyle", "⚠ ජීවන රටාව හොඳ කරන්න", lang)
    else:

        return t("🚨 HIGH RISK – Take action now!",
                 "🚨 අධික අවදානම – ඉක්මනින් ක්‍රියා කරන්න!", lang)



# ================= 🔥 CALORIES =================
def calculate_calories(age, gender, height, weight, activity, pregnant=False):

    if gender == 0:
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    factors = [1.2, 1.375, 1.55, 1.725]
    tdee = bmr * factors[min(activity, 3)]

    if pregnant:
        tdee += 300

    return {
        "bmr": round(bmr),
        "tdee": round(tdee)
    }

# ================= 🆕 MACROS =================
def calculate_macros(calories):
    protein = (calories * 0.25) / 4
    carbs = (calories * 0.50) / 4
    fat = (calories * 0.25) / 9

    return {
        "Protein (g)": round(protein),
        "Carbs (g)": round(carbs),
        "Fat (g)": round(fat),
        "Fiber (g)": 25
    }
# ================= 🆕 FOOD RECOMMENDER =================

def recommend_foods(risk, gender, age, pregnant):
    foods = []
    if risk == 2:
        foods += ["Eat more vegetables", "Reduce rice portions", "Avoid oily food"]
    elif risk == 1:
        foods += ["Balanced meals", "Add green leaves daily"]
    else:
        foods += ["Maintain current healthy diet"]
    if pregnant:
        foods += ["Drink milk", "Eat fruits", "Eat eggs"]
    if gender == 1 and age > 40:
        foods += ["Calcium rich foods", "Leafy vegetables"]

    return foods

# ================= 🆕 WEEKLY CALORIE BALANCE =================

def calculate_weekly_balance(meal_plan, exercise_plan):
    weekly_intake = sum(
        day.get("calories", {}).get("total", 0)
        for day in meal_plan.values()
    )

    weekly_burn = sum(ex.get("calories_burn", 0) for ex in exercise_plan)

    return {
        "weekly_intake": round(weekly_intake, 1),
        "weekly_burn": round(weekly_burn, 1),
        "net": round(weekly_intake - weekly_burn, 1)
    }

# ================= 🧠 SMART MEAL ENGINE =================

def filter_foods_by_diet(diet_type):
    foods = []

    for name, data in FOOD_DB.items():
        if diet_type == 0 and data.get("diet") == "veg":
            foods.append((name, data))
        elif diet_type == 1:
            foods.append((name, data))

    return foods


def group_foods(foods):
    carbs, proteins, vegs = [], [], []

    for name, data in foods:
        if data.get("type") == "carb":
            carbs.append(name)
        elif data.get("type") == "protein":
            proteins.append(name)
        elif data.get("type") == "veg":
            vegs.append(name)

    return carbs, proteins, vegs


# ================= REQUIRED FUNCTIONS =================

def extract_foods(meal_text):
    meal_text = meal_text.lower()
    foods = []

    for food in FOOD_DB:
        # 🔥 flexible matching
        if any(word in meal_text for word in food.split()):
            foods.append(food)
    if not foods:
        if "rice" in meal_text:
            foods.append("red rice")
        elif "hoppers" in meal_text:
            foods.append("string hoppers")
        elif "pittu" in meal_text:
            foods.append("pittu")
        elif "roti" in meal_text:
            foods.append("kurakkan roti")
        else:
            foods.append("banana")  # safe fallback

    return foods

def generate_portions(foods, bmi):
    meal = []

    for food in foods:

        data = FOOD_DB.get(food, {})

        if "rice" in food:
            grams = 250 if bmi < 25 else 150

        elif data.get("type") == "protein":
            grams = 120

        elif data.get("type") == "veg":
            grams = 100

        else:
            grams = 120

        meal.append({
            "name": food,
            "grams": grams
        })

    return meal

def format_meal(meal):
    return " + ".join([item["name"] for item in meal])

# ================= PORTIONS =================

def get_portions(bmi, pregnant):
    if bmi < 18.5:
        rice = "2 cups"
    elif bmi < 25:
        rice = "1.5 cups"
    else:
        rice = "1 cup"

    protein = "1 piece"

    if pregnant:
        protein = "2 pieces"

    return rice, protein


# ================= PLATE GENERATOR =================

import random

def generate_plate_meal(diet_type, bmi, pregnant):
    foods = filter_foods_by_diet(diet_type)
    carbs, proteins, vegs = group_foods(foods)

    carb = random.choice(carbs) if carbs else "red rice"
    protein = random.choice(proteins) if proteins else "dhal"

    veg_choices = random.sample(vegs, 2) if len(vegs) >= 2 else vegs
    veg1 = veg_choices[0] if veg_choices else "vegetables"
    veg2 = veg_choices[1] if len(veg_choices) > 1 else veg1

    rice_portion, protein_portion = get_portions(bmi, pregnant)

    meal = f"""
🍚 {carb.title()} – {rice_portion}
🐟 {protein.title()} – {protein_portion}
🥬 {veg1.title()} curry
🥬 {veg2.title()} curry

(½ carbs • ¼ protein • ¼ vegetables)
"""

    return meal.strip()
# ================= 🌾 RURAL FOODS INFO =================
RURAL_FOODS = [
    {"name": "Gotukola Mallung", "benefit": "Iron rich, improves brain health"},
    {"name": "Kurakkan", "benefit": "High calcium, good for diabetes"},
    {"name": "Polos", "benefit": "High fiber, meat substitute"},
    {"name": "Fish Ambul Thiyal", "benefit": "High protein, low fat"},
    {"name": "Murunga", "benefit": "Rich in vitamins, boosts immunity"},
    {"name": "Dhal", "benefit": "Protein rich, affordable nutrition"},
    {"name": "Red Rice", "benefit": "High fiber, low GI"}
]
def calculate_meal_nutrition(meal_text):
    meal_text = meal_text.lower()

    total = {"cal": 0, "carbs": 0, "protein": 0, "fat": 0, "fiber": 0}

    for food, values in FOOD_DB.items():
        if food in meal_text:
            total["cal"] += values["cal"]
            total["carbs"] += values["carbs"]
            total["protein"] += values["protein"]
            total["fat"] += values["fat"]
            total["fiber"] += values["fiber"]

    return total
def calculate_meal_from_grams(meal):
    total = {"cal": 0, "carbs": 0, "protein": 0, "fat": 0, "fiber": 0}

    for item in meal:
        food = item["name"]
        grams = item["grams"]

        if food in FOOD_DB:
            factor = grams / 100   

            total["cal"] += FOOD_DB[food]["cal"] * factor
            total["carbs"] += FOOD_DB[food]["carbs"] * factor
            total["protein"] += FOOD_DB[food]["protein"] * factor
            total["fat"] += FOOD_DB[food]["fat"] * factor
            total["fiber"] += FOOD_DB[food]["fiber"] * factor

    return {
        "cal": round(total["cal"]),          
        "carbs": round(total["carbs"], 1),
        "protein": round(total["protein"], 1),
        "fat": round(total["fat"], 1),
        "fiber": round(total["fiber"], 1)
    }


# ================= 🍽️ PORTION CALCULATIONS =================
def get_smart_meal_plan(bmi, diet_type, lang, nutrition, pregnant=False, age=25):

    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]

    # 👶 BABIES 0-2 (Sri Lankan Rural)
    if age <= 2:
        base = [
            ("Breast milk / Formula", "Rice porridge", "Mashed banana", "Pumpkin puree"),
            ("Milk", "Soft dhal rice", "Papaya mash", "Vegetable soup"),
            ("Breast milk", "Rice porridge", "Banana mash", "Carrot mash"),
            ("Milk", "Soft rice + dhal", "Avocado mash", "Pumpkin puree"),
            ("Formula milk", "Soft kiri bath", "Papaya mash", "Vegetable soup"),
            ("Milk", "Soft rice", "Banana mash", "Potato mash"),
            ("Breast milk", "Rice porridge", "Watermelon mash", "Vegetable puree")
        ]

    # 👦 CHILDREN 3-5
    elif age <= 5:
        base = [
            ("Milk + banana", "Rice + dhal", "Curd", "Vegetable soup"),
            ("Bread + egg", "Rice + fish curry", "Papaya", "Soft noodles"),
            ("Milk rice", "Rice + chicken curry", "Banana", "Soft rice"),
            ("Milk", "Rice + dhal", "Avacado", "Soup"),
            ("Egg + bread", "Rice + fish", "Yoghurt", "Vegetables"),
            ("Milk + banana", "Rice + egg curry", "Orange", "Soup"),
            ("Bread + milk", "Rice + chicken", "Mangoes", "sweet potato mash")
        ]

    # 👧 CHILDREN 6-12
    elif age <= 12:
        base = [
            ("Egg sandwich", "Rice + chicken + vegetables", "Banana", "Soup"),
            ("Milk + bread", "Rice + fish curry", "Papaya", "Rice + dhal"),
            ("Bread + egg", "Rice + egg curry", "Fruit", "Vegetables"),
            ("String hoppers", "Rice + chicken", "Curd", "Soup"),
            ("Bread + omelette", "Rice + fish", "Banana", "Rice"),
            ("Milk + bread", "Rice + dhal", "Fruit", "Vegetables"),
            ("Egg sandwich", "Rice + chicken curry", "Papaya", "Soup")
        ]

    else:
        # ===== ADULT MEALS =====
        veg_meals = [
            ("Kurakkan roti", "Red rice + dhal + gotukola + Mashroom", "Papaya", "Vegetable soup"),
            ("String hoppers", "Red rice + dhal + beans + Cucumber salad", "Banana", "Red rice + Polos curry + Cucumber salad"),
            ("Kolakanda", "Red rice + dhal + mashroom + Mango curry", "Guava", "Vegetable roti"),
            ("Pittu", "Red rice + dhal + pumpkin + Gotukola", "Orange", "Soup"),
            ("Idli", "Red rice + dhal + brinjal + Mashroom", "Papaya", "Vegetables"),
            ("Kurakkan porridge", "Red rice + Polos + Green Piece curry + Tempered Soybeans", "Banana", "Soup"),
            ("String hoppers", "Red rice + dhal + Gotukola + Broccoli curry", "Guava", "Vegetable soup")
        ]

        nonveg_meals = [
            ("Egg + bread", "Red rice + fish curry + gotukola + Beans Curry", "Yogurt", "Soup"),
            ("String hoppers + egg", "Red rice + chicken + Gotukola Sambol + beans", "Papaya", "Red rice + Polos curry + Cucumber salad"),
            ("Kurakkan roti + Fish Curry", "Red rice + Egg + dhal + Tempered Brinjals", "Banana", "Chicken soup"),
            ("Pittu + egg", "Red rice + fish + murunga + Carrot Sambol", "Orange", "White rice + Dhal curry + Dried fish"),
            ("Coconut Rotti + Fish curry", "Red rice + chicken + beans + Gotukola", "Papaya", "String hoppers + Egg curry"),
            ("Bread + omelette", "Red rice + fish + Pumpkin curry + Broccoli curry", "Banana", "Chicken soup"),
            ("Kolakanda", "Red rice + fish + Ladies Fingers + Murunga", "Guava", "Fish curry + Red rice + dhal")
        ]

        # 🤰 Pregnancy meals
        if pregnant:
            veg_meals = [
                ("Milk + dates", "Red rice + dhal + spinach", "Fruit juice", "Vegetable soup"),
                ("String hoppers + milk", "Red rice + dhal + pumpkin", "Banana", "Vegetables"),
                ("Kolakanda + milk", "Red rice + dhal + gotukola", "Fruit", "Soup"),
                ("Pittu + milk", "Red rice + dhal + beans", "Orange", "Vegetables"),
                ("Idli + milk", "Red rice + dhal + spinach", "Papaya", "Soup"),
                ("Kurakkan porridge", "Red rice + dhal + murunga + Cucumber", "Banana", "Steamed Vegetables"),
                ("String hoppers", "Red rice + dhal + mallung", "Fruit", "Soup")
            ]

            nonveg_meals = [
                ("Milk + egg", "Red rice + fish + spinach + Pumpkin Curry", "Fruit juice", "Chicken soup"),
                ("String hoppers + egg", "Red rice + chicken + pumpkin", "Banana", "Fish curry"),
                ("Kurakkan roti + Fish Curry", "Red rice + Egg + dhal + Tempered Brinjals", "Banana", "Chicken soup"),
                ("Pittu + egg", "Red rice + chicken + beans", "Orange", "Chicken soup"),
                ("Idli + egg", "Red rice + fish + spinach", "Papaya", "Soup"),
                ("Bread + omelette", "Red rice + chicken + murunga", "Banana", "Fish curry"),
                ("Kolakanda + Egg", "Red rice + fish + mallung", "Fruit", "Soup")
            ]

        base = veg_meals if diet_type == 0 else nonveg_meals

    plan = {}

    for i, day in enumerate(days):
        b, l, s, d = base[i]

        plan[day] = {
            "Breakfast": {"meal": b},
            "Lunch": {"meal": l},
            "Snack": {"meal": s},
            "Dinner": {"meal": d}
        }

    return plan
# ================= 🏃 EXERCISE =================
def get_exercise_plan(bmi, lang, pregnant=False, age=25, gender=0):

    # =================================================
    # 👶 BABIES / CHILDREN
    # =================================================
    if age <= 12:

        if bmi >= 30:
            return [
                {"day":"Monday","workout":"Nature Walk + Bubble Chase","time":"60 min","calories_burn":220},
                {"day":"Tuesday","workout":"Ball Play + Running","time":"55 min","calories_burn":210},
                {"day":"Wednesday","workout":"Playground Climb","time":"60 min","calories_burn":250},
                {"day":"Thursday","workout":"Water Play","time":"45 min","calories_burn":180},
                {"day":"Friday","workout":"Push Toy Walking","time":"50 min","calories_burn":220},
                {"day":"Saturday","workout":"Family Outdoor Walk","time":"60 min","calories_burn":240},
                {"day":"Sunday","workout":"Garden Free Play","time":"40 min","calories_burn":130}
            ]

        elif bmi >= 25:
            return [
                {"day":"Monday","workout":"Bubble Chase","time":"45 min","calories_burn":170},
                {"day":"Tuesday","workout":"Ball Play","time":"40 min","calories_burn":160},
                {"day":"Wednesday","workout":"Playground Time","time":"45 min","calories_burn":200},
                {"day":"Thursday","workout":"Nature Walk","time":"40 min","calories_burn":150},
                {"day":"Friday","workout":"Push Toy Walk","time":"40 min","calories_burn":170},
                {"day":"Saturday","workout":"Outdoor Games","time":"50 min","calories_burn":220},
                {"day":"Sunday","workout":"Family Walk","time":"30 min","calories_burn":100}
            ]

        else:
            return [
                {"day":"Monday","workout":"Bubble Play","time":"30 min","calories_burn":110},
                {"day":"Tuesday","workout":"Ball Play","time":"30 min","calories_burn":120},
                {"day":"Wednesday","workout":"Playground Fun","time":"35 min","calories_burn":140},
                {"day":"Thursday","workout":"Nature Explore","time":"30 min","calories_burn":100},
                {"day":"Friday","workout":"Push Toy Walk","time":"30 min","calories_burn":120},
                {"day":"Saturday","workout":"Outdoor Games","time":"40 min","calories_burn":170},
                {"day":"Sunday","workout":"Family Walk","time":"25 min","calories_burn":80}
            ]

    # =================================================
    # 🤰 PREGNANT WOMEN
    # =================================================
    if pregnant and gender == 1:

        return [
            {"day":"Monday","workout":"Pregnancy Walk","time":"30 min","calories_burn":120},
            {"day":"Tuesday","workout":"Prenatal Yoga","time":"25 min","calories_burn":100},
            {"day":"Wednesday","workout":"Stretching","time":"20 min","calories_burn":80},
            {"day":"Thursday","workout":"Village Walk","time":"30 min","calories_burn":120},
            {"day":"Friday","workout":"Breathing Exercise","time":"20 min","calories_burn":60},
            {"day":"Saturday","workout":"Slow Walk","time":"25 min","calories_burn":100},
            {"day":"Sunday","workout":"Rest","time":"-","calories_burn":0}
        ]

    # =================================================
    # 🔴 OBESE
    # =================================================
    if bmi >= 30:
        return [
            {"day":"Monday","workout":"Fast Walking","time":"60 min","calories_burn":350},
            {"day":"Tuesday","workout":"Farming Work","time":"60 min","calories_burn":400},
            {"day":"Wednesday","workout":"Cycling","time":"45 min","calories_burn":320},
            {"day":"Thursday","workout":"Hill Walking","time":"50 min","calories_burn":360},
            {"day":"Friday","workout":"Skipping + Walk","time":"45 min","calories_burn":300},
            {"day":"Saturday","workout":"Heavy Yard Work","time":"60 min","calories_burn":420},
            {"day":"Sunday","workout":"Light Walk","time":"30 min","calories_burn":150}
        ]

    # =================================================
    # 🟠 OVERWEIGHT
    # =================================================
    elif bmi >= 25:
        return [
            {"day":"Monday","workout":"Walking","time":"45 min","calories_burn":250},
            {"day":"Tuesday","workout":"Farming Work","time":"45 min","calories_burn":300},
            {"day":"Wednesday","workout":"Cycling","time":"35 min","calories_burn":240},
            {"day":"Thursday","workout":"Yoga","time":"30 min","calories_burn":150},
            {"day":"Friday","workout":"Fast Walking","time":"40 min","calories_burn":260},
            {"day":"Saturday","workout":"Outdoor Games","time":"45 min","calories_burn":280},
            {"day":"Sunday","workout":"Rest Walk","time":"25 min","calories_burn":100}
        ]

    # =================================================
    # 🟢 NORMAL
    # =================================================
    return [
        {"day":"Monday","workout":"Walking","time":"30 min","calories_burn":150},
        {"day":"Tuesday","workout":"Farming Work","time":"45 min","calories_burn":250},
        {"day":"Wednesday","workout":"House Work","time":"40 min","calories_burn":200},
        {"day":"Thursday","workout":"Yoga","time":"20 min","calories_burn":120},
        {"day":"Friday","workout":"Fast Walking","time":"30 min","calories_burn":250},
        {"day":"Saturday","workout":"Cycling","time":"30 min","calories_burn":280},
        {"day":"Sunday","workout":"Rest","time":"-","calories_burn":0}
    ]

# ================= 💧 WATER =================
def get_water(weight, age, gender, activity, pregnant, lang):
    total = (weight * 35) / 1000

    if pregnant:
        total += 0.3

    total = round(total, 1)

    return {
        "total": total,
        "message": t("Stay hydrated 💧", "ජලය පානය කරන්න 💧", lang),
        "schedule": [
            {"time": t("Morning (empty stomach)", "උදේ හිස්බඩ", lang), "amount": round(total * 0.25, 1)},
            {"time": t("After breakfast", "උදේ ආහාරයෙන් පසු", lang), "amount": round(total * 0.15, 1)},
            {"time": t("Before lunch", "දිවා ආහාරයට පෙර", lang), "amount": round(total * 0.20, 1)},
            {"time": t("After lunch", "දිවා ආහාරයෙන් පසු", lang), "amount": round(total * 0.15, 1)},
            {"time": t("Evening", "සවස", lang), "amount": round(total * 0.15, 1)},
            {"time": t("Before sleep", "නිදියට පෙර", lang), "amount": round(total * 0.10, 1)}
        ]
    }
# ================= 🧬 PCOS =================
def get_pcos(gender, age, bmi, pregnant, lang):
    if gender == 1 and 12 <= age <= 45 and not pregnant:
        return {
            "show": True,
            "risk": bmi >= 25,
            "message": t("Monitor PCOS symptoms",
                         "PCOS ලක්ෂණ සලකන්න", lang)
        }
    return {"show": False}


# ================= 🆕 NUTRITION BREAKDOWN =================
def generate_nutrition_breakdown(meal_plan):

    totals = {
        "cal": 0,
        "carbs": 0,
        "protein": 0,
        "fat": 0,
        "fiber": 0
    }

    for day in meal_plan.values():
        for meal_type in day.values():

            meal_text = meal_type["meal"]

            nutrients = calculate_meal_nutrition(meal_text)

            for key in totals:
                totals[key] += nutrients.get(key, 0)

    # average per day
    for key in totals:
        totals[key] = round(totals[key] / 7, 1)

    return totals

def calculate_meal_nutrition(meal_text):
    meal_text = meal_text.lower()

    total = {
        "cal": 0,
        "carbs": 0,
        "protein": 0,
        "fat": 0,
        "fiber": 0
    }

    foods_in_meal = [f.strip() for f in meal_text.split("+")]

    for item in foods_in_meal:
        for food, values in FOOD_DB.items():
            if food.lower() in item:
                total["cal"] += values["cal"]
                total["carbs"] += values["carbs"]
                total["protein"] += values["protein"]
                total["fat"] += values["fat"]
                total["fiber"] += values["fiber"]

    return total

def generate_daily_analysis(meal_plan, exercise_plan, target):
    days_data = []

    for day, meals in meal_plan.items():

        # ❗ your meal_plan currently has NO calories → so we simulate
        intake = target * 0.9   # assume 90% intake (you can improve later)

        burn = 0
        for ex in exercise_plan:
            if ex["day"] == day:
                burn = ex["calories_burn"]

        days_data.append({
            "day": day,
            "intake": round(intake),
            "burn": burn,
            "target": target
        })

    return days_data
def get_plate_distribution(risk, pregnant):
    if pregnant:
        return {
            "carbs": "45%",
            "protein": "30%",
            "vegetables": "25%",
            "extra": "+ milk / fruits"
        }

    if risk == 0:
        return {
            "carbs": "50%",
            "protein": "25%",
            "vegetables": "25%"
        }

    elif risk == 1:
        return {
            "carbs": "40%",
            "protein": "30%",
            "vegetables": "30%"
        }

    else:
        return {
            "carbs": "35%",
            "protein": "35%",
            "vegetables": "30%"
        }
  

@app.route("/predict", methods=["POST"])
def predict():
    try:
        data = request.get_json(force=True)

        lang = data.get("lang", "en")

        age = safe_int(data.get("age"))
        height = safe_float(data.get("height"))
        weight = safe_float(data.get("weight"))

        gender_map = {"Male":0, "Female":1}
        gender = gender_map.get(data.get("gender"), 0)

        pregnant_value = str(data.get("pregnant")).strip().lower()
        pregnant = pregnant_value in ["yes", "true", "1"]

        gender = safe_int(data.get("gender"))
        activity = safe_int(data.get("activity"))
        addiction = safe_int(data.get("tobacco_alcohol"))
        diet_type = safe_int(data.get("diet_type"))

        # ================= BMI =================
        bmi = round(weight / ((height / 100) ** 2), 2)
        risk = 2 if bmi >= 30 else 1 if bmi >= 25 else 0

        # ================= CALORIES =================
        cal_data = calculate_calories(age, gender, height, weight, activity, pregnant)
        target_calories = cal_data["tdee"]

        nutrition = get_nutrition(risk, gender, age, pregnant, lang) or {}

        macros = nutrition["macros"]

        # ================= PLANS =================
        meal_plan = get_smart_meal_plan(
            bmi, diet_type, lang, nutrition, pregnant, age
        )

        exercise_plan = get_exercise_plan(
             bmi, lang, pregnant, age, gender

        )

        # ================= RESPONSE =================
        response = {
            "risk": risk,
            "bmi": bmi,
            "bmi_status": get_bmi_status(bmi, lang),
            "message": get_message(risk, lang),

            # ✅ NEW CALORIE CARD DATA
            "calorie_target": {
                "daily": target_calories,
                "macros": macros,
                "plate": get_plate_distribution(risk, pregnant)
            },

            "calories": cal_data,

            "conditions": get_conditions(bmi, activity, addiction, gender, age, pregnant, lang),
            "foods": get_foods(risk, lang, age),
            "avoid": get_avoid(risk, lang, age),
            "supplements": get_supplements(bmi, gender, age, pregnant, lang),
            "nutrition": nutrition,
            "weekly_meal_plan": meal_plan,
            "exercise_plan": exercise_plan,

            "food_recommendations": recommend_foods(
                risk, gender, age, pregnant
            ),

            "calorie_balance": calculate_weekly_balance(
                meal_plan, exercise_plan
            ),
            "daily_analysis": generate_daily_analysis(
                meal_plan,
                exercise_plan,
                target_calories
            ),
            "nutrition_breakdown": generate_nutrition_breakdown(meal_plan),
            "warnings": get_warnings(
                pregnant,
                addiction,
                risk,
                activity,
                bmi,
                lang,
                age
            ),
            "reminders": get_reminders(
                risk, activity, lang, pregnant, age
            ),
            "water": get_water(weight, age, gender, activity, pregnant, lang),
            "pcos": get_pcos(gender, age, bmi, pregnant, lang),
            "rural_foods": RURAL_FOODS,
            "pregnancy_cravings": get_pregnancy_cravings(pregnant),
        }

        response = deep_translate(response, lang)
        return jsonify(response)

    except Exception as e:
        print("ERROR:", str(e))
        return jsonify({"error": "Server crash"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)