import 'styles/popup.css';

document.addEventListener("DOMContentLoaded", function () {
    const loginButton = document.getElementById("loginButton");

    loginButton.addEventListener("click", function () {
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        if (username && password) {
            alert("Logging in...");
        } else {
            alert("Please enter your username and password.");
        }
    });
});

