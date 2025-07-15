document.addEventListener("DOMContentLoaded", function () {
    const timeDisplay = document.getElementById("time");
    const form = document.querySelector("form");
    let timeLeft = window.quizTimeLimit || 60;

    if (!timeDisplay || !form) {
        console.error("❌ Required DOM elements not found.");
        return;
    }

    console.log("⏱️ Starting timer:", timeLeft);

    function formatTime(seconds) {
        const mins = Math.floor(seconds / 60);
        const secs = seconds % 60;
        return `${String(mins).padStart(2, '0')}:${String(secs).padStart(2, '0')}`;
    }

    function updateTimer() {
        if (timeLeft <= 0) {
            clearInterval(timer);
            alert("⏰ Time's up! Submitting quiz.");
            form.submit();
        } else {
            timeDisplay.textContent = formatTime(timeLeft);
            timeLeft--;
        }
    }

    updateTimer(); 
    const timer = setInterval(updateTimer, 1000);
});
