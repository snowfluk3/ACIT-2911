const loginBtn = document.getElementById("login-btn")
const loginPopup = document.getElementById("login-popup")

const closeBtn = document.getElementById("close-btn")
const overlay = document.getElementById("overlay")

const passwordField = document.getElementById("password-field")
const togglePassword = document.getElementById("toggle-password")

loginBtn.onclick = () => {
    loginPopup.classList.add("show")
    overlay.classList.add("show")
}

[closeBtn, overlay].forEach(element => {
    element.onclick = () => {
        loginPopup.classList.remove("show")
        overlay.classList.remove("show")
    }
})

// Show Password logic
togglePassword.addEventListener("click", function () {
    const type = passwordField.getAttribute("type") === "password" ? "text" : "password"
    passwordField.setAttribute("type", type)

    this.textContent = type === "password" ? 'Show' : 'Hide'
})