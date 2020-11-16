/* Email format validation */
const email = document.getElementById("email");
email.addEventListener("input", function (event) {
    if (email.checkValidity()) {
        email.setCustomValidity("Not valid email address.");
    } else {
        email.setCustomValidity("");
    }
});

/* Password match validation */
const password = document.getElementById("password");
const confirm_password = document.getElementById("confirm_password");
confirm_password.addEventListener("input", function (event) {
    if (password.value !== confirm_password.value) {
        confirm_password.setCustomValidity("Passwords do not match.");
    } else {
        confirm_password.setCustomValidity("");
    }
});
