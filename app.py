from flask import Flask, render_template, request, jsonify
import google.generativeai as genai

app = Flask(__name__)

# Configure Google Gemini AI
GENAI_API_KEY = "AIzaSyAQYLivLfx7FwNmi5U9zZQAfQjBpltO6K0"  # Replace with a valid key
genai.configure(api_key=GENAI_API_KEY)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/generate', methods=['POST'])
def generate_plan():
    try:
        data = request.get_json()
        name = data.get("name")
        gender = data.get("gender")
        age = data.get("age")
        weight = data.get("weight")
        goal = data.get("goal")
        preference = data.get("preference")
        avoided = data.get("avoided", "None")
        calories = data.get("calories")
        duration = data.get("duration")

        if duration == "1_day":
            time_frame = "for 1 day"
        elif duration == "1_week":
            time_frame = "for 1 week"
        else:
            time_frame = "for an appropriate duration"

        # AI Prompt with Calories
        prompt = f"""
        Provide a personalized nutrition plan {time_frame} for {name}, a {gender} aged {age} years, weighing {weight}kg.
        Goal: {goal}
        Dietary Preference: {preference}
        Avoided Items: {avoided}
        Required Daily Caloric Intake: {calories} kcal

        The plan should include:
        - Recommended meals for {time_frame}
        - Macronutrient breakdown
        - Caloric intake per meal
        - Substitutions based on avoided items or dietary preferences
        """

        # Call Google Gemini AI
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content([prompt])
        plan = response.text if hasattr(response, "text") else "No recommendation available."

        # Convert AI's markdown-style bold (**text**) into proper HTML <strong> tags
        plan = plan.replace("**", "").replace("##", "")

        return jsonify({"plan": plan})

    except Exception as e:
        return jsonify({"plan": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(debug=True)
