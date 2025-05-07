import requests

url = "http://127.0.0.1:5000/generate_meal_plan"
data = {
    "diet": "vegetarian",
    "age": 25,
    "gender": "female",
    "height": 165,
    "weight": 60,
    "allergies": "none",
    "healthGoals": "weight loss",
    "activityLevel": "moderate",
    "cuisine": "Indian"
}

response = requests.post(url, json=data)

if response.status_code == 200:
    with open("meal_plan.json", "wb") as f:
        f.write(response.content)
    print("✅ Meal plan downloaded as 'meal_plan.json'")
else:
    print("❌ Error:", response.text)
