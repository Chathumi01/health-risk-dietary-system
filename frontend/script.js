// ================= GLOBAL =================
let currentLang = "en";
let reminderInterval = null;

function getReminderIcon(text){
    text = text.toLowerCase();

    if(text.includes("water")) return "💧";
    if(text.includes("sleep")) return "😴";
    if(text.includes("active")) return "🏃";
    if(text.includes("fruit")) return "🍎";
    if(text.includes("meal")) return "🥗";

    return "💡";
}

// ================= CHAT TOGGLE =================
window.toggleChat = function(){

    const chat = document.getElementById("chatbox");
    const body = document.getElementById("chatBody");

    if(chat){

        // open / close chatbot
        chat.classList.toggle("hidden");

        // first welcome message only once
        if(body && body.innerHTML.trim() === ""){

            const isSinhala = currentLang === "si";

            body.innerHTML = `
                <div class="chat-msg bot">
                    ${
                        isSinhala
                        ? "👋 ආයුබෝවන්! මම ඔබගේ සෞඛ්‍ය සහායකයා.<br> BMI, ආහාර, වතුර, ව්‍යායාම, PCOS ගැන අහන්න."
                        : "👋 Hi! I'm your Health Assistant.<br> Ask me about BMI, diet, water, exercise, or PCOS."
                    }
                </div>
            `;
        }
    }
}
// ================= SAFE DOM =================
function get(id){
    return document.getElementById(id);
}

// ================= POPUP =================
function showPopup(msg){

    // Sinhala mode = bilingual
    if(currentLang === "si"){
        msg = translateReminder(msg);
    }

    const div = document.createElement("div");

    div.innerText = msg;

    div.style = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: #2e7d32;
        color: white;
        padding: 14px 18px;
        border-radius: 12px;
        z-index: 9999;
        font-size: 15px;
        font-weight: 600;
        max-width: 320px;
        line-height: 1.4;
        box-shadow: 0 10px 20px rgba(0,0,0,0.18);
        animation: popupFade 0.4s ease;
    `;

    document.body.appendChild(div);

    setTimeout(() => {
        div.remove();
    }, 5000);
}

// 👇 ADD HERE (RIGHT AFTER showPopup)
function startReminderPopups(reminders){
    if(!reminders || reminders.length === 0) return;

    let index = 0;

    if(window.reminderInterval){
        clearInterval(window.reminderInterval);
    }

    // first popup instantly
    showPopup(reminders[index]);

    window.reminderInterval = setInterval(() => {
        index = (index + 1) % reminders.length;
        showPopup(reminders[index]);
    }, 12000);
}
// ================= LANGUAGE =================
const TEXT = {
    en: {
      button: "Predict Health",
      analyzing: "🔄 Analyzing...",
      fill: "⚠ Please fill required fields",
      server: "⚠ Server connection failed",
      riskLow: "🟢 LOW RISK",
      riskMid: "🟠 MEDIUM RISK",
      riskHigh: "🔴 HIGH RISK",
      water: "L / day"
    },
  
    // 👇 ADD THIS
    si: {
      button: "සෞඛ්‍යය පුරෝකථනය කරන්න",
      analyzing: "🔄 විශ්ලේෂණය කරමින්...",
      fill: "⚠ කරුණාකර සියලු විස්තර පුරවන්න",
      server: "⚠ සර්වර් සම්බන්ධතාවය අසාර්ථකයි",
      riskLow: "🟢 අඩු අවදානම",
      riskMid: "🟠 මධ්‍යම අවදානම",
      riskHigh: "🔴 ඉහළ අවදානම",
      water: "ලීටර් / දින"
    }
  };
// ================= LANGUAGE SET =================
// ================= LANGUAGE SET =================
function setLang(lang){
    currentLang = lang;
    localStorage.setItem("lang", lang);

    // ===== BUTTON ACTIVE STYLE =====
    get("enBtn").classList.remove("active");
    get("siBtn").classList.remove("active");

    if(lang === "en"){
        get("enBtn").classList.add("active");
    }else{
        get("siBtn").classList.add("active");
    }

    // ===== LEFT SIDE =====
    get("heroBadge").innerText =
        lang==="si" ? "🌿 AI සෞඛ්‍ය අනාවැකි පද්ධතිය" :
                      "🌿 AI HEALTH PREDICTION SYSTEM";

    get("heroTitle").innerHTML =
        lang==="si" ? "සෞඛ්‍යවත් <em>ජීවිතයක්</em>" :
                      "Live <em>Healthy</em>";

    get("heroSub").innerText =
        lang==="si" ? "පුද්ගලික AI සෞඛ්‍ය විශ්ලේෂණය" :
                      "PERSONALIZED AI HEALTH ANALYSIS";

    get("stat1").innerText =
        lang==="si" ? "සෞඛ්‍ය මිනුම්" : "Health Metrics";

    get("stat2").innerText =
        lang==="si" ? "ආහාර සැලසුම්" : "Meal Plans";

    get("stat3").innerText =
        lang==="si" ? "පුද්ගලික" : "Personalized";

    // ===== RIGHT SIDE =====
    document.querySelector(".form-card h2").innerText =
        lang==="si" ? "සෞඛ්‍ය අවදානම් පුරෝකථකය" :
                      "Health Risk Predictor";

    document.querySelector(".subtitle").innerText =
        lang==="si" ? "ඔබගේ තොරතුරු ඇතුලත් කරන්න" :
                      "Enter your details";

    get("ageLabel").innerText =
        lang==="si" ? "වයස" : "Age";

    get("genderLabel").innerText =
        lang==="si" ? "ස්ත්‍රී / පුරුෂ" : "Gender";

    get("heightLabel").innerText =
        lang==="si" ? "උස (cm)" : "Height (cm)";

    get("weightLabel").innerText =
        lang==="si" ? "බර (kg)" : "Weight (kg)";

    get("mealLabel").innerText =
        lang==="si" ? "ආහාර වර්ගය" : "Diet Type";

    get("activityLabel").innerText =
        lang==="si" ? "ක්‍රියාකාරිත්වය" : "Activity";

    get("addictionLabel").innerText =
        lang==="si" ? "අවබෝධික පුරුදු" : "Addiction";

    get("pregnantLabel").innerText =
        lang==="si" ? "ගර්භණීද?" : "Pregnant";

    get("predictBtn").innerText =
        lang==="si" ? "✦ සෞඛ්‍යය පුරෝකථනය කරන්න" :
                      "✦ Predict Health";
                      
    // ===== RESULT PAGE TITLES =====
get("conditionTitle").innerText =
lang==="si"
? "⚠️ ජීවන රටා අවදානම් සාධක"
: "⚠️ Lifestyle Risk Factors";

get("pcosTitle").innerText =
lang==="si"
? "🧬 PCOS පරීක්ෂාව"
: "🧬 PCOS Screening";

get("bmiTitle").innerText =
lang==="si"
? "📊 BMI ආශ්‍රිත අවදානම්"
: "📊 BMI Related Risks";

get("waterTitle").innerText =
lang==="si"
? "💧 දෛනික ජල සැලැස්ම"
: "💧 Daily Water Plan";

get("exerciseTitle").innerText =
lang==="si"
? "🏃 ව්‍යායාම සැලැස්ම"
: "🏃 Exercise Plan";

get("backBtn").innerText =
lang==="si"
? "← ආපසු"
: "← Back";

get("womenTitle").innerText =
lang === "si"
? "🎗 කාන්තා සෞඛ්‍ය මතක් කිරීම"
: "🎗 Women's Health Reminder";

get("nutritionTitle").innerText =
lang==="si"
? "🥗 පෝෂණ විස්තරය"
: "🥗 Nutrition Breakdown";

    // ===== DROPDOWNS =====
    get("gender").options[0].text = lang==="si" ? "තෝරන්න" : "Select";
    get("gender").options[1].text = lang==="si" ? "පුරුෂ" : "Male";
    get("gender").options[2].text = lang==="si" ? "ස්ත්‍රී" : "Female";

    get("meals").options[0].text = lang==="si" ? "තෝරන්න" : "Select";
    get("meals").options[1].text = lang==="si" ? "ශාකහාර" : "Vegetarian";
    get("meals").options[2].text = lang==="si" ? "මාංශහාර" : "Non-Vegetarian";

    get("activity").options[0].text = lang==="si" ? "අඩු" : "Low";
    get("activity").options[1].text = lang==="si" ? "මධ්‍යම" : "Moderate";
    get("activity").options[2].text = lang==="si" ? "ඉහළ" : "High";

    get("addiction").options[0].text = lang==="si" ? "නැහැ" : "No";
    get("addiction").options[1].text = lang==="si" ? "දුම්පානය" : "Smoking";
    get("addiction").options[2].text = lang==="si" ? "මත්පැන්" : "Alcohol";
    get("addiction").options[3].text = lang==="si" ? "දෙකම" : "Both";

    get("pregnant").options[0].text = lang==="si" ? "නැහැ" : "No";
    get("pregnant").options[1].text = lang==="si" ? "ඔව්" : "Yes";
}

if(get("bmiLabels")){

    get("bmiLabels").innerHTML =
    currentLang === "si"
    ? `
      <span>අඩු බර</span>
      <span>සාමාන්‍ය</span>
      <span>වැඩි බර</span>
      <span>අධික බර</span>
    `
    : `
      <span>Underweight</span>
      <span>Normal</span>
      <span>Overweight</span>
      <span>Obese</span>
    `;
}
// ================= 🆕 STATUS COLOR =================
function colorStatus(status){
    if(status === "Good") return "🟢";
    if(status === "Moderate") return "🟠";
    return "🔴";
}
// ================= 🆕 HOUSEHOLD CONVERSION =================
function convertMealText(mealText){
    if(!mealText) return "-";

    return mealText.split("+").map(item=>{
        item = item.trim();

        const match = item.match(/(\d+)g\s(.+)/);
        if(!match) return item;

        const g = parseInt(match[1]);
        const name = match[2].toLowerCase();

        // 🍚 Rice
        if(name.includes("rice")){
            return `🍚 ${g}g (${(g/150).toFixed(1)} cups)`;
        }

        // 🥚 Eggs
        if(name.includes("egg")){
            return `🥚 ${g}g (${Math.round(g/50)} eggs)`;
        }

        // 🥛 Milk
        if(name.includes("milk")){
            return `🥛 ${g}g (${Math.round(g/200)} glass)`;
        }

        // 🍗 Chicken / Fish
        if(name.includes("chicken") || name.includes("fish")){
            return `🍗 ${g}g (${Math.round(g/100)} palm)`;
        }

        // 🥬 Veg
        if(name.includes("beans") || name.includes("mallung") || name.includes("vegetable")){
            return `🥬 ${g}g (${Math.round(g/60)} handful)`;
        }

        return `👉 ${g}g ${name}`;
    }).join("<br>");
}
function renderNutritionBreakdown(data){

    const box = document.getElementById("nutritionBreakdown");
    if(!box) return;

    // No data
    if(!data){
        box.innerHTML = `
        <div class="card">
            <p>
                ${
                    currentLang==="si"
                    ? "⚠ අදාළ නොවේ"
                    : "⚠ Not Applicable"
                }
            </p>
        </div>
        `;
        return;
    }

    box.innerHTML = `
    <div class="card">

        <h3>
            ${
                currentLang==="si"
                ? "📊 දෛනික පෝෂණ ප්‍රමාණය"
                : "📊 Daily Nutrition Intake"
            }
        </h3>

        <p><b>🔥 ${data.cal} kcal</b></p>

        <p>
            🍚 ${
                currentLang==="si"
                ? "කාබෝහයිඩ්‍රේට්"
                : "Carbs"
            }: ${data.carbs}g
        </p>

        <p>
            🍗 ${
                currentLang==="si"
                ? "ප්‍රෝටීන්"
                : "Protein"
            }: ${data.protein}g
        </p>

        <p>
            🥑 ${
                currentLang==="si"
                ? "මේදය"
                : "Fat"
            }: ${data.fat}g
        </p>

        <p>
            🌾 ${
                currentLang==="si"
                ? "තන්තු"
                : "Fiber"
            }: ${data.fiber}g
        </p>

    </div>
    `;
}
function renderCalorieGraph(data){

    const ctx = document.getElementById("calorieChart");
    if(!ctx) return;

    if(!data || data.length === 0){
        return;
    }

    if(window.calChart) window.calChart.destroy();

    window.calChart = new Chart(ctx,{
        type:"bar",
        data:{
            labels:data.map(x=>x.day),
            datasets:[
                {
                    label:"Intake",
                    data:data.map(x=>x.intake)
                },
                {
                    label:"Burn",
                    data:data.map(x=>x.burn)
                },
                {
                    label:"Target",
                    data:data.map(x=>x.target),
                    type:"line"
                }
            ]
        },
        options:{
            responsive:true,
            maintainAspectRatio:false
        }
    });
}
function getReminderSubtext(text){

    text = text.toLowerCase();

    const si = currentLang === "si";

    if(text.includes("water"))
        return si ? "ශරීරයට ජලය අවශ්‍යයි 💧" : "Keeps your body hydrated 💧";

    if(text.includes("sleep"))
        return si ? "හොඳ නින්ද සෞඛ්‍යයට වැදගත් 😴" : "Improves recovery & hormones 😴";

    if(text.includes("active"))
        return si ? "ව්‍යායාම හදවතට හොඳයි 🏃" : "Boosts metabolism & heart health 🏃";

    if(text.includes("meal"))
        return si ? "සමබර ආහාර අවශ්‍යයි 🥗" : "Maintains balanced nutrition 🥗";

    return si ? "කුඩා පුරුදු → ලොකු ප්‍රතිඵල" : "Small habit → big impact";
}


/* 👇 PASTE HERE (replace old translateReminder) */
function translateReminder(text){

    const map = {
        "Drink water every 2 hours":"පැය 2කට වරක් වතුර බොන්න",
        "Eat balanced meals":"සමබර ආහාර ගන්න",
        "Stay active daily":"දිනපතා ක්‍රියාශීලී වන්න",
        "Sleep 7-8 hours":"පැය 7-8 නිදාගන්න",
        "Monitor weight weekly":"සතිපතා බර පරීක්ෂා කරන්න",
        "Walk daily":"දිනපතා ඇවිදින්න"
    };

    if(currentLang === "si"){
        return map[text] ? `${map[text]} (${text})` : text;
    }

    return text;
}
function renderReminders(arr){
    if(!arr) return;

    const box = document.getElementById("reminders");

    box.innerHTML = arr.map(text => `
        <div class="reminder-card">
            <div class="reminder-icon">${getReminderIcon(text)}</div>
            <div>
                <b>${translateReminder(text)}</b>
                <div style="font-size:12px; color:#666;">
                    ${getReminderSubtext(text)}
                </div>
            </div>
        </div>
    `).join("");
}

// ================= MAIN =================
async function predict(){

    const t = TEXT[currentLang] || TEXT["en"];
    const btn = get("predictBtn");

    if(!get("age").value || !get("height").value || !get("weight").value){
        alert(t.fill);
        return;
    }

    btn.innerText = t.analyzing;
    btn.disabled = true;

    const genderVal = get("gender").value;
let pregVal = get("pregnant").value;

// force male = not pregnant
if(genderVal === "0"){
    pregVal = "0";
}

const data = {
    age: get("age").value,
    gender: genderVal,
    height: get("height").value,
    weight: get("weight").value,
    diet_type: get("meals").value,
    activity: get("activity").value,
    tobacco_alcohol: get("addiction").value,
    pregnant: pregVal,
    lang: currentLang
};
    window.lastUserInput = data;

    try{
        const res = await fetch("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data)
          });
          
        const d = await res.json();
        window.healthData = d;

         
        console.log("FULL RESPONSE:", d);

        btn.innerText = t.button;
        btn.disabled = false;

        if(!d || d.error){
            alert("⚠ Invalid response");
            return;
        }

        get("formPage").classList.add("hidden");
        get("resultPage").classList.remove("hidden");

        // ===== BASIC =====
        get("bmi").innerText = d.bmi ?? "-";
        get("bmiValue").innerText = d.bmi ?? "-";
        let messageText = "";
        let icon = "";

        const isSinhala = currentLang === "si";

        if(d.risk === 2){
            icon = "🔴";
            messageText = isSinhala
            ? "ඉහළ අවදානමක් ඇත. වහාම ක්‍රියා කරන්න!"
            : "High risk detected. Take action immediately!";
        }
        else if(d.risk === 1){
            icon = "🟠";
            messageText = isSinhala
            ? "මධ්‍යම අවදානමක් ඇත. ජීවන රටාව වෙනස් කරන්න."
            : "Moderate risk. Improve your lifestyle.";
        }
        else{
            icon = "🟢";
            messageText = isSinhala
            ? "ඔබගේ සෞඛ්‍ය තත්ත්වය හොඳයි."
            : "Your body is in a healthy condition. Maintain your lifestyle!";
        }
        let shakeClass = d.risk === 2 ? "shake" : "";

        get("message").innerHTML = `
        <div class="health-status ${shakeClass}">
             <div class="status-icon">${icon}</div>
             <div>
                 <h2>${d.message}</h2>
                 <p>${messageText}</p>
             </div>
        </div>
        `;

        setRiskUI(d.risk);
        setBMIGauge(d.bmi);
        function translateFoodItem(item){

            const map = {
            "Leafy greens":"කොළ එළවළු",
            "Fish":"මාළු",
            "Oats":"ඕට්ස්",
            "Papaya":"පැපොල්",
            "Kurakkan":"කුරක්කන්",
            "Burger":"බර්ගර්",
            "Pizza":"පීසා",
            "French fries":"ෆ්‍රෙන්ච් ෆ්‍රයිස්",
            "Soft drinks":"සිසිල් බීම",
            "Sugar sweets":"පැණිරස",
            "Too much oil":"අධික තෙල්",
            "Omega 3":"ඔමේගා 3",
            "Vitamin D3":"විටමින් D3",
            "Magnesium":"මැග්නීසියම්"
            };
            
            if(currentLang==="si"){
               return map[item] ? `${map[item]} (${item})` : item;
            }
            
            return item;
            }
        fillList("conditions", d.conditions || d.health_conditions || []);
        renderBMIRiskDetails(d.bmi);

        fillList("foods", d.foods || []);
        fillList("avoid", d.avoid || []);
        fillList("supplements", d.supplements || []);
        fillList("warnings", d.warnings || []);

        renderReminders(d.reminders);
        startReminderPopups(d.reminders);
        renderPCOS(d.pcos, data);
        renderWomenHealthAlert(data);
        renderWater(d.water);
        renderMealTable(d.weekly_meal_plan, currentLang);
        renderExerciseTable(d.exercise_plan, currentLang);
        renderCalorieCard(d.calorie_target);
        renderCalorieGraph(d.daily_analysis);
        renderNutritionBreakdown(d.nutrition_breakdown);
        renderCravings(d.pregnancy_cravings);
        

        // 🆕 FEATURES
        if(typeof renderFoodRecommendations === "function"){
            renderFoodRecommendations(d.food_recommendations);
        }
         
        if(typeof renderCalorieBalance === "function"){
            renderCalorieBalance(d.calorie_balance);
        }
        

    }catch(e){
        console.error(e);
        alert(t.server);
        btn.disabled = false;
        btn.innerText = t.button;
    }
}

// ================= BMI =================
function renderBMIRiskDetails(bmi){

    const box = get("bmiRisks");
    if(!box) return;
    
    bmi = parseFloat(bmi);
    
    const si = currentLang==="si";
    
    let html="";
    
    if(bmi < 18.5){
    
    html = si ? `
    <li>🔵 අඩු BMI</li>
    <li>⚠ දුර්වල ප්‍රතිශක්තිය</li>
    <li>⚠ ශක්තිය අඩුවීම</li>
    <li>⚠ මස්පිණ්ඩු අඩුවීම</li>
    <li>🥚 ප්‍රෝටීන් වැඩි කරන්න</li>
    ` : `
    <li>🔵 Underweight BMI</li>
    <li>⚠ Weak immunity</li>
    <li>⚠ Low energy</li>
    <li>⚠ Muscle loss risk</li>
    <li>🥚 Increase protein intake</li>
    `;
    }
    
    else if(bmi < 25){
    
    html = si ? `
    <li>🟢 සාමාන්‍ය BMI</li>
    <li>✅ සෞඛ්‍ය සම්පන්න බර</li>
    <li>🥗 සමබර ආහාර</li>
    <li>🏃 ක්‍රියාශීලී වන්න</li>
    ` : `
    <li>🟢 Normal BMI</li>
    <li>✅ Healthy body weight</li>
    <li>🥗 Balanced meals</li>
    <li>🏃 Stay active</li>
    `;
    }
    
    else if(bmi < 30){
    
    html = si ? `
    <li>🟠 වැඩි BMI</li>
    <li>⚠ දියවැඩියා අවදානම</li>
    <li>⚠ BP වැඩි විය හැක</li>
    <li>🍚 සුදු බත් අඩු කරන්න</li>
    <li>🚶 දිනපතා ඇවිදින්න</li>
    ` : `
    <li>🟠 Overweight BMI</li>
    <li>⚠ Diabetes risk rising</li>
    <li>⚠ BP may increase</li>
    <li>🍚 Reduce white rice</li>
    <li>🚶 Walk daily</li>
    `;
    }
    
    else{
    
    html = si ? `
    <li>🔴 අධික BMI</li>
    <li>⚠ හෘද රෝග අවදානම</li>
    <li>⚠ දෙවන වර්ගයේ දියවැඩියාව</li>
    <li>⚠ මේද අක්මා අවදානම</li>
    <li>⚠ රුධිර පීඩනය වැඩි විය හැක</li>
    <li>🥥 පොල් තෙල් නරක කොලෙස්ටරෝල් (LDL) වැඩි කරයි</li>
    <li>👨‍⚕️ වෛද්‍යවරයෙකු හමුවන්න</li>
    ` : `
    <li>🔴 Obese BMI</li>
    <li>⚠ Heart disease risk</li>
    <li>⚠ High blood pressure</li>
    <li>⚠ Type 2 diabetes</li>
    <li>⚠ Fatty liver</li>
    <li>🥥 Coconut oil may raise LDL</li>
    <li>👨‍⚕️ Consult doctor</li>
    `;
    }
    
    box.innerHTML = html;
    }
// ================= BMI GAUGE =================
function setBMIGauge(val){

    if(!val) return;

    val = parseFloat(val);

    // BMI max scale = 40
    let percent = (val / 40) * 100;

    if(percent > 100) percent = 100;
    if(percent < 0) percent = 0;

    const pointer = get("bmiPointer");

    if(pointer){
        pointer.style.left = percent + "%";
    }
}
// ================= RISK =================
function setRiskUI(risk){
    const t = TEXT[currentLang];
    if(get("risk")){
        get("risk").innerText =
            risk===2 ? t.riskHigh :
            risk===1 ? t.riskMid :
                       t.riskLow;
    }
}

// ================= WATER =================
function renderWater(w){
    if(!w || !w.schedule) return;

    let html = "";
    w.schedule.forEach(p=>{
        html += `<li>👉 ${p.time} - ${p.amount} L</li>`;
    });

    if(get("waterTotal")){
        get("waterTotal").innerText = `${w.total} L`;
    }

    if(get("waterPlan")){
        get("waterPlan").innerHTML = html;
    }
}

// ================= FOOD TIPS =================

function renderFoodRecommendations(arr){
    if(!arr) return;

    if(get("foodTips")){
        get("foodTips").innerHTML = arr.map(i => `✅ ${i}`).join("<br>");
    }
}
function translateFood(text){

    if(currentLang !== "si") return text;
    
    return text
    .replace(/Egg/gi,"බිත්තර")
    .replace(/bread/gi,"පාන්")
    .replace(/Red rice/gi,"රතු බත්")
    .replace(/White rice/gi,"සුදු බත්")
    .replace(/fish curry/gi,"මාළු කරි")
    .replace(/chicken/gi,"කුකුල් මස්")
    .replace(/banana/gi,"කෙසෙල්")
    .replace(/papaya/gi,"පැපොල්")
    .replace(/orange/gi,"දොඩම්")
    .replace(/guava/gi,"පේර")
    .replace(/soup/gi,"සුප්")
    .replace(/yogurt/gi,"යෝගට්")
    .replace(/String hoppers/gi,"ඉඳි ආප්ප")
    .replace(/Pittu/gi,"පිට්ටු")
    .replace(/Kurakkan roti/gi,"කුරක්කන් රොටි")
    .replace(/Coconut Rotti/gi,"පොල් රොටි");
    }
// ================= MEAL TABLE =================
function renderMealTable(plan, lang){

    const si = lang === "si";

    let daysEn = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"];
    let daysSi = ["සඳුදා","අඟහරුවාදා","බදාදා","බ්‍රහස්පතින්දා","සිකුරාදා","සෙනසුරාදා","ඉරිදා"];

    let html = "";

    for(let i=0; i<daysEn.length; i++){

        let day = daysEn[i];
        let showDay = si ? daysSi[i] : day;

        let m = plan[day];
        if(!m) continue;

        html += `
        <tr>
            <td>${showDay}</td>
            <td>${translateFood(m.Breakfast?.meal || "-")}</td>
            <td>${translateFood(m.Lunch?.meal || "-")}</td>
            <td>${translateFood(m.Snack?.meal || "-")}</td>
            <td>${translateFood(m.Dinner?.meal || "-")}</td>
        </tr>
        `;
    }

    document.getElementById("mealTable").innerHTML = html;
}
// ================= CALORIE CARD =================
function renderCalorieCard(data){

    if(!data) return;

    const card = document.getElementById("calorieCard");
    if(!card) return;

    const calories = data.daily || 0;

    const carbs = data.macros?.["Carbs %"] || 0;
    const protein = data.macros?.["Protein %"] || 0;
    const fat = data.macros?.["Fat %"] || 0;

    const bmi = window.healthData?.bmi || "-";

    card.innerHTML = `
        <h3>${currentLang==="si" ? "🔥 පුද්ගලික දෛනික පෝෂණ සැලැස්ම" : "🔥 Personalized Daily Nutrition Plan"}</h3>

        <p><b>${calories} kcal</b></p>

        <hr/>

        <p>🍚 ${currentLang==="si" ? "කාබෝහයිඩ්‍රේට්" : "Carbs"}: <span>${carbs}%</span></p>
        <p>🥩 ${currentLang==="si" ? "ප්‍රෝටීන්" : "Protein"}: <span>${protein}%</span></p>
        <p>🥑 ${currentLang==="si" ? "මේදය" : "Fat"}: <span>${fat}%</span></p>

        <hr/>

        <p>📌 BMI: <b>${bmi}</b></p>
    `;
}
function renderCravings(data){

    const box = document.getElementById("cravingsBox");
    if(!box) return;

    if(!data){
        box.innerHTML = "";
        return;
    }

    if(data.status){
        box.innerHTML = `
        <div class="card">
            <h3>${currentLang==="si"
                ? "🤰 ගර්භණී ආහාර මාර්ගෝපදේශය"
                : "🤰 Pregnancy Cravings Guide"}
            </h3>

            <p>⚠ ${data.status}</p>
        </div>`;
        return;
    }

    if(!Array.isArray(data) || data.length === 0){
        box.innerHTML = "";
        return;
    }

    box.innerHTML = `
    <div class="card">

        <h3>
        ${currentLang==="si"
        ? "🤰 ගර්භණී ආහාර ආශා මාර්ගෝපදේශය"
        : "🤰 Pregnancy Cravings Guide"}
        </h3>

        ${data.map(i=>`
            <p><b>${i.type}</b></p>

            <ul>
                ${(i.foods || []).map(f=>`<li>${f}</li>`).join("")}
            </ul>
        `).join("")}

        <p>
        💡 ${currentLang==="si"
        ? "සෞඛ්‍ය සම්පන්න ආහාර තෝරා මධ්‍යස්ථව ආහාර ගන්න."
        : "Choose healthy options and eat in moderation."}
        </p>

    </div>`;
}
function translateDay(day){

    const map = {
        Monday:"සඳුදා",
        Tuesday:"අඟහරුවාදා",
        Wednesday:"බදාදා",
        Thursday:"බ්‍රහස්පතින්දා",
        Friday:"සිකුරාදා",
        Saturday:"සෙනසුරාදා",
        Sunday:"ඉරිදා"
    };

    if(currentLang === "si"){
        return map[day] || day;
    }

    return day;
}

function translateWorkout(workout){

    if(currentLang !== "si") return workout;

    return workout
        .replace(/Walking/gi,"ඇවිදීම")
        .replace(/Jogging/gi,"දුවීම")
        .replace(/Yoga/gi,"යෝගා")
        .replace(/Cycling/gi,"සයිකල් පැදීම")
        .replace(/Stretching/gi,"ව්‍යායාම දිගු කිරීම")
        .replace(/Rest/gi,"විවේකය")
        .replace(/Workout/gi,"ව්‍යායාම");
}
// ================= EXERCISE =================
function renderExerciseTable(plan){

    const table = document.getElementById("exerciseTable");
    if(!table) return;

    if(!plan || !Array.isArray(plan) || plan.length === 0){
        table.innerHTML = `
        <tr>
            <td colspan="3">No Data</td>
        </tr>`;
        return;
    }

    let html = "";

    plan.forEach(p => {
        html += `
        <tr>
            <td>${translateDay(p.day || "-")}</td>
            <td>${translateWorkout(p.workout || "-")}</td>
            <td>${p.time || "-"}</td>
        </tr>`;
    });

    table.innerHTML = html;
}
function renderCalorieBalance(c){
    if(!c) return;

    const box = get("calorieBalance");
    if(!box) return;

    box.innerHTML = `
    🍽️ ${currentLang==="si" ? "ලබාගත් කැලරි" : "Intake"}: ${c.weekly_intake} kcal<br>
    🔥 ${currentLang==="si" ? "දහනය කළ කැලරි" : "Burn"}: ${c.weekly_burn} kcal<br>
    ⚖️ ${currentLang==="si" ? "ශුද්ධ ප්‍රමාණය" : "Net"}: <b>${c.net} kcal</b>
    `;
}
//========cancer===========
function renderWomenHealthAlert(user){

    const box = document.getElementById("womenAlert");
    if(!box) return;

    const age = parseInt(user.age);
    const gender = user.gender;
    const pregnant = user.pregnant;

    const si = currentLang === "si";

    // ================= NOT FEMALE =================
    if(gender !== "1"){
        box.innerHTML = `
        <div class="card">
            <p>${si ? "අදාළ නොවේ" : "Not Applicable"}</p>
        </div>`;
        return;
    }

    let html = "";

    // ================= FEMALE NOT PREGNANT =================
    if(pregnant === "0"){

        if(age >= 45){

            html += `
            <div class="card warning-card">
                <h3>${si ? "🎗 කාන්තා සෞඛ්‍ය මතක් කිරීම" : "🎗 Women's Health Reminder"}</h3>

                <p>
                ${
                    si
                    ? "වයස 45ට වැඩි කාන්තාවන් සඳහා ස්තන පරීක්ෂාව සහ වාර්ෂික වෛද්‍ය පරීක්ෂණ නිර්දේශ කරයි."
                    : "Women above 45 are advised to do breast screening and yearly medical checkups."
                }
                </p>
            </div>
            `;

        }else{

            html += `
            <div class="card success-card">
                <p>
                ${
                    si
                    ? "නිතිපතා සෞඛ්‍ය පරීක්ෂණ පවත්වා ගන්න."
                    : "Maintain regular health checkups."
                }
                </p>
            </div>
            `;
        }
    }

    // ================= FEMALE PREGNANT =================
    else if(pregnant === "1"){

        html += `
        <div class="card warning-card">
            <h3>${si ? "🤰 ගර්භණී අවදානම් දැනුම්දීම" : "🤰 Pregnancy Risk Alert"}</h3>
        `;

        if(age <= 17){

            html += `
            <p>
            ${
                si
                ? "⚠ යෞවන ගර්භණීභාවය මවට සහ බිළිඳාට වැඩි සංකූලතා ඇති කළ හැක."
                : "⚠ Teenage pregnancy may have higher maternal and fetal complications."
            }
            </p>
            `;

        }
        else if(age >= 35 && age < 40){

            html += `
            <p>
            ${
                si
                ? "⚠ වයස 35ට වැඩි ගර්භණීභාවය BP සහ ගර්භණී දියවැඩියා අවදානම වැඩි කළ හැක."
                : "⚠ Age 35+ pregnancy may increase BP and gestational diabetes risk."
            }
            </p>
            `;

        }
        else if(age >= 40 && age < 45){

            html += `
            <p>
            ${
                si
                ? "⚠ වයස 40ට වැඩි ගර්භණීභාවය ගබ්සා වීම සහ chromosome අසාමාන්‍යතා අවදානම වැඩි කළ හැක."
                : "⚠ Age 40+ may increase miscarriage and chromosomal abnormality risk."
            }
            </p>
            `;

        }
        else if(age >= 45){

            html += `
            <p>
            ${
                si
                ? "⚠ වයස 45ට වැඩි ගර්භණීභාවය ඉහළ අවදානම් තත්ත්වයක් වන අතර විශේෂඥ වෛද්‍ය අධීක්ෂණය අවශ්‍ය වේ."
                : "⚠ Age 45+ pregnancy is considered high risk and needs specialist care."
            }
            </p>
            `;

        }
        else{

            html += `
            <p>
            ${
                si
                ? "✅ සාමාන්‍ය ගර්භණී සත්කාර සඳහා antenatal clinic පරීක්ෂණ දිගටම කරගෙන යන්න."
                : "✅ Continue regular antenatal clinic follow-up."
            }
            </p>
            `;
        }

        html += `
        <p>
        ${
            si
            ? "👩‍⚕️ ගර්භණී කාලයේ Mammogram පරීක්ෂාව වෛද්‍ය උපදෙස් මත පමණක් කළ යුතුය."
            : "👩‍⚕️ Mammogram during pregnancy should only be done under doctor guidance."
        }
        </p>
        </div>
        `;
    }

    box.innerHTML = html;
}
// ================= CALORIE BALANCE =================

function renderPCOS(p, user){

    const box = get("pcos");
    if(!box) return;

    if(!user){
        box.innerHTML = "";
        return;
    }

    const age = parseInt(user.age);
    const gender = user.gender;
    const pregnant = user.pregnant;

    // ❌ Not applicable cases
    if(gender !== "1" || age < 12 || age > 49 || pregnant === "1") {
        box.innerHTML = `
            <li>${currentLang==="si" ? "අදාළ නොවේ" : "Not applicable"}</li>
        `;
        return;
    }

    // ✅ GET BMI FROM GLOBAL DATA
    const bmi = parseFloat(window.healthData?.bmi) || 0;

    // ✅ DEFINE HIGH BMI (YOU CAN ADJUST)
    const isHighBMI = bmi >= 25;   // overweight + obese

    // ================= LOW RISK =================
    if(!isHighBMI){

        box.innerHTML = `
    <div class="pcos-card low">
        ${currentLang==="si" ? "✅ අඩු PCOS අවදානම" : "✅ Low PCOS Risk"}
    </div>

    <div class="pcos-safe-msg">
        ${
            currentLang==="si"
            ? "ප්‍රධාන PCOS ලක්ෂණ දැනට නොපෙනේ."
            : "No major PCOS-related symptoms are currently indicated."
        }
    </div>
    `;
        return;
    }

    // ================= HIGH RISK =================
    const symptoms = currentLang==="si" ? `
<ul class="pcos-list">
    <li>අවිධිමත් මාසික</li>
    <li>මුහුණේ පැල්ලම් / තෙල් සහිත සම</li>
    <li>අතිරේක රෝම වර්ධනය</li>
    <li>හිසකෙස් අඩුවීම</li>
    <li>බර වැඩිවීම</li>
    <li>කළු පැල්ලම්</li>
</ul>
` : `
<ul class="pcos-list">
    <li>Irregular periods</li>
    <li>Acne or oily skin</li>
    <li>Excess facial/body hair</li>
    <li>Hair thinning</li>
    <li>Weight gain</li>
    <li>Dark skin patches</li>
</ul>
`;
const advice = `
    <div class="pcos-warning">
        ${
            currentLang === "si"
            ? "⚠ ලක්ෂණ නිරීක්ෂණය කර අවශ්‍ය නම් වෛද්‍යවරයෙකු හමුවන්න."
            : "⚠ Monitor symptoms and consult a doctor if needed."
        }
    </div>
`;

    box.innerHTML = `
    <div id="pcosRisk" class="pcos-card high">
        ${currentLang==="si" ? "🔴 ඉහළ PCOS අවදානම" : "🔴 High PCOS Risk"}
    </div>

    <h4>
        ${currentLang==="si" ? "ප්‍රධාන ලක්ෂණ" : "Key Symptoms"}
    </h4>
        ${symptoms}
        ${advice}
    `;

    setTimeout(() => {
        const el = document.getElementById("pcosRisk");
        if(el) el.classList.add("shake");
    }, 100);
}
// ================= LIST =================
function fillList(id, arr){

    const el = get(id);
    if(!el) return;

    if(!arr || arr.length===0){
        el.innerHTML = currentLang==="si"
        ? "<li>⚠ දත්ත නොමැත</li>"
        : "<li>⚠ No data available</li>";
        return;
    }

    el.innerHTML = arr.map(item=>{

        if(currentLang==="si"){

            item = item
            .replace(/Sedentary lifestyle/gi,"ක්‍රියාකාරී නොවන ජීවන රටාව")
            .replace(/High BMI/gi,"ඉහළ BMI")
            .replace(/Low fiber intake/gi,"අඩු ගුඩිබර ආහාර")
            .replace(/High sugar foods/gi,"අධික සීනි ආහාර")
            .replace(/Low water intake/gi,"අඩු ජලය පානය")
            .replace(/High salt intake/gi,"අධික ලුණු භාවිතය")
            .replace(/Poor nutrition/gi,"අඩු පෝෂණය")
            .replace(/obesity/gi,"අධික බර")
            .replace(/diabetes/gi,"දියවැඩියාව")
            .replace(/heart disease/gi,"හෘද රෝග")
            .replace(/risk/gi,"අවදානම")
            .replace(/poor digestion/gi,"දුර්වල ජීර්ණය")
            .replace(/kidney stress/gi,"වකුගඩු පීඩනය")
            .replace(/blood pressure/gi,"රුධිර පීඩනය")
            .replace(/thyroid health/gi,"තයිරොයිඩ් සෞඛ්‍යය");
            
            }

        return `<li>👉 ${item}</li>`;

    }).join("");
}
function goBack(){

    const form = get("formPage");
    const result = get("resultPage");

    if(form) form.classList.remove("hidden");
    if(result) result.classList.add("hidden");

    if(window.reminderInterval){
        clearInterval(window.reminderInterval);
    }

    window.scrollTo({top:0, behavior:"smooth"});
}
// ================= INIT =================
document.addEventListener("DOMContentLoaded", () => {

    // Default language
    const savedLang = localStorage.getItem("lang") || "en";
    setLang(savedLang);   

    const gender = get("gender");
    const pregRow = get("pregnantRow");
    const preg = get("pregnant");
    const chatInput = get("chatInput");

    // ===== SHOW / HIDE PREGNANT =====
    function togglePregnancy() {

        if (!gender || !pregRow || !preg) return;

        // Male
        if (gender.value === "0") {
            pregRow.style.display = "none";
            preg.value = "0";
        }

        // Female
        else if (gender.value === "1") {
            pregRow.style.display = "block";
        }

        // Not selected
        else {
            pregRow.style.display = "none";
            preg.value = "0";
        }
    }

    // Run first time
    togglePregnancy();

    // Change event
    gender.addEventListener("change", togglePregnancy);

    // Enter key chatbot
    if(chatInput){
        chatInput.addEventListener("keypress", function(e){
            if(e.key === "Enter"){
                sendMessage();
            }
        });
    }

});
// ================= CHATBOT =================
function sendMessage(){

    const input = get("chatInput");
    const body = get("chatBody");

    if(!input || !body) return;

    const msg = input.value.trim();

    if(msg === "") return;

    // user message
    body.innerHTML += `
        <div class="chat-msg user">${msg}</div>
    `;

    input.value = "";

    const reply = getHealthReply(msg);

    // typing bubble
    body.innerHTML += `
        <div class="chat-msg bot" id="typingMsg">
            ${currentLang === "si" ? "ටයිප් කරමින්..." : "Typing..."}
       </div>
       `;

    body.scrollTop = body.scrollHeight;

    setTimeout(() => {

        const typing = document.getElementById("typingMsg");

        if(typing){
            typing.innerHTML = reply;
            typing.removeAttribute("id");
        }

        body.scrollTop = body.scrollHeight;

    }, 700);
}

function getHealthReply(msg){

    msg = msg.toLowerCase();

    const bmi = window.healthData?.bmi || null;
    const risk = window.healthData?.risk || null;

    const isSinhala = currentLang === "si";

    const healthWords = [
        "health","bmi","diet","food","exercise","water",
        "sleep","pcos","pregnant","diabetes","heart",
        "fat","weight","cholesterol","risk",
        "calorie","calories","calory","kcal",
        "nutrition","protein","carbs",
        "සෞඛ්‍ය","වතුර","ව්‍යායාම","බර","කැලරි","අවදානම"
    ];

    const isHealth = healthWords.some(word => msg.includes(word));

    if(!isHealth){
        return isSinhala
        ? "⚠ සමාවන්න, මම සෞඛ්‍ය සම්බන්ධ ප්‍රශ්න වලට පමණක් පිළිතුරු දෙමි."
        : "⚠ Sorry, this is outside my domain. I answer health-related questions only.";
    }

    // BMI
    if(msg.includes("bmi")){
        if(bmi){
            return isSinhala
            ? `📊 ඔබගේ BMI අගය ${bmi} යි.`
            : `📊 Your BMI is ${bmi}.`;
        }

        return isSinhala
        ? "📊 BMI යනු ශරීර බර දර්ශකයයි."
        : "📊 BMI means Body Mass Index.";
    }

    // Risk
    if(msg.includes("risk")){
        if(risk == 0){
            return isSinhala ? "🟢 ඔබගේ අවදානම අඩුය." : "🟢 Your risk level is LOW.";
        }

        if(risk == 1){
            return isSinhala ? "🟠 ඔබගේ අවදානම මධ්‍යමයි." : "🟠 Your risk level is MEDIUM.";
        }

        if(risk == 2){
            return isSinhala ? "🔴 ඔබගේ අවදානම ඉහළයි." : "🔴 Your risk level is HIGH.";
        }
    }

    // Calories
    if(
        msg.includes("calorie") ||
        msg.includes("calories") ||
        msg.includes("calory") ||
        msg.includes("kcal") ||
        msg.includes("කැලරි")
    ){
        const cal = window.healthData?.calorie_target?.daily || null;

        if(cal){
            return isSinhala
            ? `🔥 ඔබට දිනකට අවශ්‍ය කැලරි ප්‍රමාණය ${cal} kcal යි.`
            : `🔥 Your recommended calorie intake is ${cal} kcal per day.`;
        }

        return isSinhala
        ? "🔥 කැලරි අවශ්‍යතාව වයස, බර සහ ක්‍රියාකාරීත්වය අනුව වෙනස් වේ."
        : "🔥 Calorie intake depends on age, weight, height, and activity level.";
    }

    // Water
    if(msg.includes("water") || msg.includes("වතුර")){
        return isSinhala
        ? "💧 දිනකට ලීටර් 2-3 වතුර බොන්න."
        : "💧 Drink 2-3 liters daily.";
    }

    // Exercise
    if(msg.includes("exercise") || msg.includes("ව්‍යායාම")){
        return isSinhala
        ? "🏃 දිනකට විනාඩි 30ක් ව්‍යායාම කරන්න."
        : "🏃 Exercise at least 30 mins daily.";
    }

    // Weight
    if(msg.includes("weight") || msg.includes("බර")){
        return isSinhala
        ? "⚖️ සෞඛ්‍ය සම්පන්න බර පවත්වා ගන්න."
        : "⚖️ Maintain a healthy body weight.";
    }

    return isSinhala
    ? "✅ සෞඛ්‍ය සම්පන්න ජීවන රටාවක් පවත්වා ගන්න."
    : "✅ Maintain a healthy lifestyle.";
}