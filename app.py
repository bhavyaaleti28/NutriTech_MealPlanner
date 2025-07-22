from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import markdown
import traceback
import time
import os

app = Flask(__name__)

# Simple CORS configuration
CORS(app, supports_credentials=True)
FRONTEND_URL = 'https://nutritech-frontend.onrender.com'
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', FRONTEND_URL)
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Accept,Origin')
    response.headers.add('Access-Control-Allow-Methods', 'GET,POST,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Configure Gemini API
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))# Replace with your actual API key

# Create Gemini model instance
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to generate a meal plan
def generate_meal_plan(data):
    try:
        print("Generating meal plan with data:", data)
        start_time = time.time()
        
        prompt = (
            f"Create a personalized 7-day meal plan for a {data.get('diet', 'balanced')} diet. "
            f"User details: Age {data.get('age', 'N/A')}, Gender {data.get('gender', 'N/A')}, "
            f"Height {data.get('height', 'N/A')} cm, Weight {data.get('weight', 'N/A')} kg. "
            f"Consider allergies: {data.get('allergies', 'None')}. "
            f"Health goal: {data.get('healthGoals', 'General Health')}. "
            f"Activity level: {data.get('activityLevel', 'Moderate')}. "
            f"Preferred cuisine: {data.get('cuisine', 'No Preference')}. "
            f"Include breakfast, lunch, and dinner for each day."
            f"Include number of calories provided by each meal."
        )

        response = model.generate_content(prompt)
        end_time = time.time()
        print(f"Meal plan generation took {end_time - start_time:.2f} seconds")
        
        if not response:
            print("No response from AI model")
            return "Error: No response from AI model"
            
        return response.text
    
    except Exception as e:
        print(f"Error generating meal plan: {str(e)}")
        print("Full traceback:")
        print(traceback.format_exc())
        return f"Error: {str(e)}"

# Define API route
@app.route('/generate_meal_plan', methods=['POST', 'OPTIONS'])
def generate_meal():
    if request.method == "OPTIONS":
        print("Received OPTIONS request")
        return '', 200

    try:
        print("Received meal plan request")
        data = request.get_json()
        print("Request data:", data)

        # Validate required fields
        required_fields = ["diet", "healthGoals", "activityLevel"]
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            print(f"Missing required fields: {missing_fields}")
            return jsonify({"error": f"Missing required fields: {', '.join(missing_fields)}"}), 400

        # Generate meal plan
        meal_plan = generate_meal_plan(data)
        if meal_plan.startswith("Error:"):
            return jsonify({"error": meal_plan}), 500
            
        formatted_plan = markdown.markdown(meal_plan)
        
        response = jsonify({
            "meal_plan": formatted_plan,
            "message": "Meal plan generated successfully"
        })
        
        print("Meal plan generated successfully")
        return response

    except Exception as e:
        print(f"Error in generate_meal: {str(e)}")
        print("Full traceback:")
        print(traceback.format_exc())
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("Starting meal plan generation server...")
    app.run(port=5000, debug=True)
