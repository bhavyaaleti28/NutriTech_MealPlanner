    // At the top of script.js or in a <script> tag in index.html
    if (!localStorage.getItem('userEmail')) {
        window.location.href = 'login.html';
    }
let currentStep = 0;
const formSteps = document.querySelectorAll('.form-step');

document.addEventListener('DOMContentLoaded', () => {
    // Show welcome message if user is logged in
    const welcomeDiv = document.getElementById('welcomeMessage');
    const userName = localStorage.getItem('userName');
    if (welcomeDiv) {
        if (userName) {
            welcomeDiv.textContent = `Welcome, ${userName}`;
        } else {
            welcomeDiv.textContent = 'Welcome, User';
        }
    }

    const form = document.getElementById('nutritionForm');
    if (form) {
        form.addEventListener('submit', generateMealPlan);
    }
    showStep(currentStep);
});

function showStep(step) {
    formSteps.forEach((formStep, index) => {
        formStep.classList.toggle('active', index === step);
    });
}

function nextStep() {
    if (currentStep < formSteps.length - 1) {
        currentStep++;
        showStep(currentStep);
    }
}

function prevStep() {
    if (currentStep > 0) {
        currentStep--;
        showStep(currentStep);
    }
}

// Function to handle the form submission
async function generateMealPlan(event) {
    if (event) {
        event.preventDefault(); // Prevent form submission and page refresh
    }

    const formData = new FormData(document.getElementById('nutritionForm'));
    const userData = {};

    formData.forEach((value, key) => {
        userData[key] = value;
    });

    // Add email and name from localStorage if needed for backend
    const userName = localStorage.getItem('userName');
    const userEmail = localStorage.getItem('userEmail');
    if (userName) userData.name = userName;
    if (userEmail) userData.email = userEmail;

    console.log('Submitting user data:', userData);

    try {
        // Save user data
        console.log('Sending data to server...');
        const saveResponse = await fetch('https://nutritech-auth.onrender.com/update_user', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors',
            credentials: 'include',
            body: JSON.stringify(userData)
        });

        console.log('Server response status:', saveResponse.status);
        const responseData = await saveResponse.json();
        console.log('Server response:', responseData);

        if (!saveResponse.ok) {
            throw new Error(responseData.message || 'Failed to save user data');
        }

        // Generate meal plan
        console.log('Generating meal plan...');
        const mealPlanResponse = await fetch('https://nutritech-mealplan.onrender.com/generate_meal_plan', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
            },
            mode: 'cors',
            credentials: 'include',
            body: JSON.stringify(userData)
        });

        console.log('Meal plan response status:', mealPlanResponse.status);
        const mealPlanData = await mealPlanResponse.json();
        console.log('Meal plan response:', mealPlanData);

        if (!mealPlanResponse.ok) {
            throw new Error(mealPlanData.error || 'Failed to generate meal plan');
        }

        if (!mealPlanData.meal_plan) {
            throw new Error('No meal plan received from server');
        }

        displayMealPlan(mealPlanData.meal_plan);

        // Hide form and show meal plan button
        document.getElementById('nutritionForm').style.display = 'none';
        document.getElementById('mealPlanButton').style.display = 'block';
        console.log('Form submitted successfully');
    } catch (error) {
        console.error('Error:', error);
        const errorMessage = error.message || 'Failed to process request. Please try again.';
        alert(errorMessage);
        
        // Show the form again in case of error
        document.getElementById('nutritionForm').style.display = 'block';
        document.getElementById('mealPlanButton').style.display = 'none';
    }
}

// Function to display the meal plan in the HTML page
function displayMealPlan(mealPlan) {
    console.log('Displaying meal plan...');
    let outputDiv = document.getElementById("mealPlanOutput");
    console.log('Output div:', outputDiv);

    if (!outputDiv) {
        console.error("mealPlanOutput div not found!");
        return;
    }

    try {
        // Insert the meal plan directly as HTML
        outputDiv.innerHTML = mealPlan;
        console.log('Meal plan inserted into div');

        // Add download button
        const downloadBtn = document.createElement('button');
        downloadBtn.className = 'download-btn';
        downloadBtn.textContent = 'Download Meal Plan';
        downloadBtn.onclick = () => downloadMealPlan(mealPlan);
        outputDiv.appendChild(downloadBtn);
        console.log('Download button added');

        // Show the meal plan container immediately
        const mealPlanContainer = document.getElementById('mealPlanContainer');
        const backToFormButton = document.getElementById('backToFormButton');
        
        if (mealPlanContainer) {
            mealPlanContainer.style.display = 'block';
            console.log('Meal plan container displayed');
        } else {
            console.error('Meal plan container not found!');
        }
        
        if (backToFormButton) {
            backToFormButton.style.display = 'block';
            console.log('Back to form button displayed');
        } else {
            console.error('Back to form button not found!');
        }
    } catch (error) {
        console.error('Error displaying meal plan:', error);
        console.error('Error stack:', error.stack);
    }
}

// Function to download the meal plan
function downloadMealPlan(mealPlan) {
    const blob = new Blob([mealPlan], { type: 'text/html' });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = 'meal_plan.html';
    
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    
    URL.revokeObjectURL(url);
}

// Function to go back to the form
function goBackToForm() {
    document.getElementById('mealPlanContainer').style.display = 'none';
    document.getElementById('mealPlanButton').style.display = 'none';
    document.getElementById('nutritionForm').style.display = 'block';

    currentStep = 0;
    showStep(currentStep);
}