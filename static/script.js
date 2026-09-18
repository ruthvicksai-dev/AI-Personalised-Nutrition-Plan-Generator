document.getElementById("nutritionForm").addEventListener("submit", function (event) {
    event.preventDefault();
    generateNutrition();
});

function generateNutrition() {
    const name = document.getElementById("name").value;
    const gender = document.getElementById("gender").value;
    const age = document.getElementById("age").value;
    const weight = document.getElementById("weight").value;
    const goal = document.getElementById("goal").value;
    const preference = document.getElementById("preference").value;
    const avoided = document.getElementById("avoided").value;
    const calories = document.getElementById("calories").value;
    const duration = document.getElementById("duration").value;

    // Disable button to prevent multiple requests
    const button = document.querySelector("button");
    button.disabled = true;
    button.innerText = "Generating...";

    fetch("/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            name, gender, age, weight, goal, preference, avoided, calories, duration
        })
    })
    .then(response => response.json())
    .then(data => {
        let formattedPlan = data.plan
            .replace(/\n/g, "<br>")  // Convert new lines to HTML line breaks
            .replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>")  // Convert **bold** to <strong>
            .replace(/##\s*(.*?)(?=\n|$)/g, "<strong>$1</strong>");  // Convert ## Headings to <strong>

        document.getElementById("result").innerHTML = `<p><strong>➡ Nutrition Plan:</strong></p><p>${formattedPlan}</p>`;
        button.disabled = false;
        button.innerText = "Generate Plan";
    })
    .catch(error => {
        document.getElementById("result").innerHTML = `<p style="color: red;"><strong>Error:</strong> ${error.message}</p>`;
        button.disabled = false;
        button.innerText = "Generate Plan";
    });
}
