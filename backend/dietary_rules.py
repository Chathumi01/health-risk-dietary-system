# ================= 🌐 LANGUAGE =================
def t(en, si, lang="en"):
    return si if lang == "si" else en


# ================= ⚠ CONDITIONS =================
def get_conditions(bmi, activity, addiction, gender, age, pregnant, lang):

    conditions = []

    # ==================================================
    # 👶 BABIES (0-2)
    # ==================================================
    if age <= 2:

        conditions.append("Rapid growth stage → nutrition is very important")
        conditions.append("Low iron may affect brain development")
        conditions.append("Low calcium may affect bone growth")
        conditions.append("Too much sugar may harm teeth")

        if bmi >= 25:
            conditions.append("High weight for age → monitor feeding portions")

        return conditions

    # ==================================================
    # 👦 CHILDREN (3-12)
    # ==================================================
    elif age <= 12:

        conditions.append("Growth stage → needs balanced nutrition")
        conditions.append("Too much junk food may cause obesity")
        conditions.append("Low activity may reduce fitness")
        conditions.append("Low calcium may weaken bones")

        if bmi >= 25:
            conditions.append("High BMI → childhood obesity risk")

        return conditions

    # ==================================================
    # 🤰 PREGNANT WOMEN
    # ==================================================
    elif pregnant:

        conditions.append("Pregnancy needs extra iron & folic acid")
        conditions.append("Low nutrition may affect baby growth")
        conditions.append("Hydration is important during pregnancy")

        if bmi >= 25:
            conditions.append("High BMI may increase pregnancy complications")

        return conditions

    # ==================================================
    # 👨 ADULTS
    # ==================================================
    if activity == 0:
        conditions.append("Sedentary lifestyle → increases obesity risk")

    if bmi >= 25:
        conditions.append("High BMI → increases diabetes & heart disease risk")

    if addiction == 2:
        conditions.append("Smoking → increases lung disease risk")

    if addiction == 1:
        conditions.append("Alcohol use → increases liver disease risk")

    if addiction == 3:
        conditions.append("Smoking + alcohol → very high health risk")

    conditions.append("Low fiber intake → poor digestion")
    conditions.append("High sugar foods → diabetes risk")
    conditions.append("Low water intake → kidney stress")
    conditions.append("High salt intake → blood pressure risk")

    if gender == 1:
        conditions.append("Poor nutrition may affect thyroid health")

    return conditions
# ================= 🍎 FOODS =================
def get_foods(risk, lang, age=25):

    # ================= BABIES 0-2 =================
    if age <= 2:
        return [
            "Breast milk / Formula",
            "Mashed banana",
            "Rice porridge",
            "Vegetable puree",
            "Soft boiled egg yolk",
            "Mashed papaya"
        ]

    # ================= CHILDREN 3-5 =================
    elif age <= 5:
        return [
            "Milk",
            "Banana",
            "Rice + dhal",
            "Soft vegetables",
            "Scrambled egg",
            "Yogurt"
        ]

    # ================= CHILDREN 6-12 =================
    elif age <= 12:
        return [
            "Milk / Curd",
            "Rice + fish",
            "Egg",
            "Fruits",
            "Vegetables",
            "Peanut butter bread"
        ]

    # ================= ADULT =================
    if risk == 2:
        return [
            "Leafy greens",
            "Fish",
            "Oats",
            "Papaya",
            "Kurakkan"
        ]

    return [
        "Balanced meals",
        "Rice",
        "Vegetables",
        "Protein foods"
    ]

# ================= 🚫 AVOID =================
def get_avoid(risk, lang, age=25):

    # babies
    if age <= 2:
        return [
            "Honey",
            "Hard nuts",
            "Popcorn",
            "Too much sugar",
            "Soft drinks",
            "Spicy food"
        ]

    # children
    elif age <= 12:
        return [
            "Chocolates daily",
            "Fast food",
            "Soft drinks",
            "Too much sugar",
            "Deep fried food"
        ]

    # adults
    if risk == 2:
       return [
            "Burger",
            "Pizza",
            "French fries",
            "Soft drinks",
            "Sugar sweets",
            "Too much oil"
        ]

    return [
         "Bakery Items",
         "Ice cream",
         "salty snacks",
         "Soft drinks",
         "Instant noodles",
         "Chocolate cake"
        ]
    

# ================= 🥗 NUTRITION (FIXED FOR FRONTEND) =================
# ================= 🥗 SMART NUTRITION =================
def get_nutrition(risk, gender, age, pregnant, lang):

    # 🤰 FIRST PRIORITY
    if pregnant:
        calories = 2400
        carbs, protein, fat = 45, 30, 25

    elif age <= 2:
        calories = 1000
        carbs, protein, fat = 45, 20, 35

    elif age <= 12:
        calories = 1600
        carbs, protein, fat = 50, 20, 30

    elif age <= 18:
        calories = 2200
        carbs, protein, fat = 50, 25, 25

    else:
        if risk == 2:
            calories = 1800
            carbs, protein, fat = 35, 35, 30
        elif risk == 1:
            calories = 2000
            carbs, protein, fat = 40, 30, 30
        else:
            calories = 2200
            carbs, protein, fat = 50, 25, 25
    # ==========================================
    # Convert to grams
    # ==========================================
    carbs_g = int((carbs / 100) * calories / 4)
    protein_g = int((protein / 100) * calories / 4)
    fat_g = int((fat / 100) * calories / 9)

    # ==========================================
    # Default minerals
    # ==========================================
    fiber = 25
    calcium = 1000
    iron = 18
    water = 2.5

    # Pregnancy upgrades
    if pregnant:
        fiber = 30
        calcium = 1300
        iron = 27
        water = 3.2

    # Children
    elif age <= 12:
        calcium = 1200
        water = 1.8

    # Babies
    elif age <= 2:
        calcium = 700
        water = 1.0

    # ==========================================
    return {

        "percentages": {
            "Carbs": carbs,
            "Protein": protein,
            "Fat": fat
        },

        "macros": {
            "Carbs %": carbs,
            "Protein %": protein,
            "Fat %": fat,
            "Carbs (g)": carbs_g,
            "Protein (g)": protein_g,
            "Fat (g)": fat_g,
            "Fiber (g)": fiber
        },

        "per_meal": {
            "Carbs (g)": round(carbs_g / 3),
            "Protein (g)": round(protein_g / 3),
            "Fat (g)": round(fat_g / 3)
        },

        "extra": {
            "Calories": calories,
            "Water (L)": water,
            "Calcium (mg)": calcium,
            "Iron (mg)": iron
        },

        "vitamins": {
            "Vitamin A": ["Carrot", "Pumpkin"],
            "Vitamin C": ["Guava", "Orange"],
            "Vitamin D": ["Egg", "Milk"],
            "Vitamin E": ["Nuts"],
            "Vitamin K": ["Gotukola"],
            "Vitamin B": ["Rice", "Kurakkan"]
        },

        "minerals": {
            "Iron": ["Spinach", "Lentils"],
            "Calcium": ["Milk", "Yogurt"],
            "Magnesium": ["Nuts"],
            "Zinc": ["Fish"]
        }
    }
# ================= ⚠ WARNINGS =================
def get_warnings(pregnant, addiction, risk, activity, bmi, lang, age=25):

    warnings = []

    # =================================================
    # 👶 BABIES (0-2)
    # =================================================
    if age <= 2:
        warnings.append("🍼 Breast milk / formula is the main nutrition source")
        warnings.append("⚠ Avoid honey below age 1")
        warnings.append("⚠ Avoid hard foods (nuts, popcorn, candy)")
        warnings.append("💧 Keep baby hydrated")
        warnings.append("👶 Regular pediatric checkups recommended")

        if bmi < 18.5:
            warnings.append("⚠ Low weight may affect healthy growth")

        return warnings

    # =================================================
    # 👦 CHILDREN (3-12)
    # =================================================
    elif age <= 12:
        warnings.append("🍬 Too much sugar may cause tooth decay")
        warnings.append("📱 Too much screen time reduces activity")
        warnings.append("🥗 Growth needs balanced nutrition")

        if activity == 0:
            warnings.append("⚠ Low activity may increase child obesity risk")

        if risk >= 1:
            warnings.append("⚠ Weight should be monitored early")

        if bmi < 18.5:
            warnings.append("⚠ Underweight may affect development")

        return warnings

    # =================================================
    # 🧑 TEENS (13-18)
    # =================================================
    elif age <= 18:
        warnings.append("🍔 Junk food may cause unhealthy weight gain")
        warnings.append("😴 Poor sleep affects learning and hormones")

        if activity == 0:
            warnings.append("⚠ Low activity reduces fitness")

        if risk == 2:
            warnings.append("🚨 Teen obesity needs early action")

        return warnings

    # =================================================
    # 🚬 ADDICTION
    # =================================================
    if addiction in [1, 2, 3]:
        warnings.append("🚬 Smoking / Alcohol increases cancer & organ damage risk")

    if addiction == 1:
        warnings.append("🍺 Alcohol may damage liver health")

    if addiction == 2:
        warnings.append("🚬 Smoking affects lungs and heart")

    if addiction == 3:
        warnings.append("⚠ Combined smoking + alcohol = very high health risk")

    # =================================================
    # 🤰 PREGNANCY
    # =================================================
    if pregnant:
        warnings.append("🤰 Avoid alcohol & smoking completely")
        warnings.append("🥩 Increase protein for baby growth")
        warnings.append("💊 Take prenatal vitamins regularly")
        warnings.append("🧠 Good nutrition supports baby brain development")

        if activity == 0:
            warnings.append("🚶 Light walking recommended during pregnancy")

        if bmi >= 30:
            warnings.append("⚠ High BMI may increase pregnancy complications")

        if bmi < 18.5:
            warnings.append("⚠ Low BMI may need extra nutrition during pregnancy")

    # =================================================
    # 🏃 ACTIVITY
    # =================================================
    if activity == 0:
        warnings.append("⚠ Low activity increases obesity & heart risk")
        warnings.append("💡 Daily walking improves circulation")

        if risk == 2:
            warnings.append("🚨 High risk + no activity = urgent lifestyle change")

    elif activity == 2:
        warnings.append("💧 High activity needs more hydration and recovery")

    # =================================================
    # ❤️ BMI / RISK
    # =================================================
    if bmi >= 30:
        warnings.append("⚠ Obesity increases heart disease & diabetes risk")

    elif bmi >= 25:
        warnings.append("⚠ Overweight may increase future health risks")

    if bmi < 18.5:
        warnings.append("⚠ Underweight may cause nutrient deficiency")

    # =================================================
    # 🔴 RISK SCORE
    # =================================================
    if risk == 2:
        warnings.append("🚨 High risk detected — lifestyle changes needed now")

    elif risk == 1:
        warnings.append("⚠ Moderate risk — improve habits early")

    else:
        warnings.append("✅ Maintain healthy lifestyle habits")

    return warnings
# ================= 💊 SUPPLEMENTS =================
def get_supplements(bmi, gender, age, pregnant, lang):

    # 👶 BABIES
    if age <= 2:
        return [
            "Vitamin D drops",
            "Iron syrup (if doctor recommends)"
        ]

    # 👦 CHILDREN
    elif age <= 12:
        return [
            "Multivitamin syrup",
            "Calcium syrup",
            "Vitamin C chewable"
        ]

    # 🤰 PREGNANT FIRST PRIORITY
    elif pregnant:
        return [
            "Folic Acid",
            "Iron",
            "Calcium",
            "Prenatal Vitamins"
        ]

    # 🧑 TEENS
    elif age <= 18:
        return [
            "Multivitamin chewable",
            "Iron syrup",
            "Vitamin D"
        ]

    # 👨 UNDERWEIGHT ADULT
    elif bmi < 18.5:
        return [
            "Mass Gainer (doctor approved)",
            "Multivitamin",
            "Calcium"
        ]

    # 🔴 OBESE ADULT
    elif bmi >= 30:
        return [
            "Omega 3",
            "Vitamin D3",
            "Magnesium"
        ]

    # 🟢 NORMAL ADULT
    return [
        "Vitamin D3",
        "Calcium",
        "Omega 3"
    ]
    
# ================= 🔔 REMINDERS =================
def get_reminders(risk, activity, lang, pregnant=False, age=25):

    # 👶 Babies
    if age <= 2:
        return [
            "Feed on time 🍼",
            "Give soft healthy foods 🍌",
            "Keep baby hydrated 💧",
            "Ensure enough sleep 😴"
        ]

    # 👦 Children
    elif age <= 12:
        return [
            "Drink water regularly 💧",
            "Eat fruits daily 🍎",
            "Play outside daily ⚽",
            "Sleep 9-10 hours 😴",
            "Limit screen time 📱"
        ]

    # 🧑 Teens
    elif age <= 18:
        return [
            "Exercise daily 🏃",
            "Eat protein foods 🍗",
            "Drink water 💧",
            "Sleep well 😴"
        ]

    # 🤰 Pregnant
    elif pregnant:
        return [
            "Take prenatal vitamins 💊",
            "Drink more water 💧",
            "Light walking 🚶",
            "Eat protein foods 🥚"
        ]

    # 👨 Adults
    reminders = [
        "Drink water every 2 hours 💧",
        "Eat balanced meals 🥗",
        "Stay active daily 🏃",
        "Sleep 7-8 hours 😴"
    ]

    if risk == 2:
        reminders.append("Monitor weight weekly ⚖️")

    if activity == 0:
        reminders.append("Walk daily 🚶")

    return reminders
import random

def get_pregnancy_cravings(pregnant):

    if not pregnant:
        return {"status": "Not Applicable"}

    return [
        {
            "type": "Sweet 🍫",
            "foods": ["Banana", "Dates", "Yogurt", "Dark Chocolate"]
        },
        {
            "type": "Salty 🥒",
            "foods": ["Nuts", "Cheese", "Avocado", "Whole grain crackers"]
        },
        {
            "type": "Carbs 🍞",
            "foods": ["Oats", "Brown rice", "Sweet potato", "Whole wheat bread"]
        },
        {
            "type": "Cold ❄️",
            "foods": ["Fruit smoothie", "Yogurt", "Watermelon", "Cold milk"]
        }
    ]