const loginBtn = document.getElementById("login-btn")
const loginPopup = document.getElementById("login-popup")
const loginForm = document.getElementById("login-form")
const loginError = document.getElementById("login-error")
const errorText = document.getElementById("error-text")

const registerPopup = document.getElementById("register-popup")
const registerForm = document.getElementById("register-form")
const toggleLink = document.getElementById("register-toggle")
const closeRegButton = document.getElementById("close-reg-button")


const closeBtn = document.getElementById("close-btn")
const overlay = document.getElementById("overlay")

const passwordField = document.getElementById("password-field")
const togglePassword = document.getElementById("toggle-password")

const registerPasswordField = document.getElementById("register-password-field")
const registerTogglePassword = document.getElementById("register-toggle-password")

// Overlay and Popup Logic
if (loginBtn && loginPopup && overlay) {
    loginBtn.onclick = () => {
        loginPopup.classList.add("show")
        overlay.classList.add("show")
    }

    ;[closeBtn, overlay].forEach(element => {
        element.onclick = () => {
            loginPopup.classList.remove("show")
            overlay.classList.remove("show")
        }
    })
}

if (toggleLink && registerForm && registerPopup) {
    toggleLink.onclick = (e) => {
        e.preventDefault()
        loginPopup.classList.remove("show")
        registerPopup.classList.add("show")
    }
}

if (closeRegButton && registerPopup && overlay) {
    [closeRegButton, overlay].forEach(element => {
        element.addEventListener("click", () => {
            loginPopup.classList.remove("show")
            registerPopup.classList.remove("show")
            overlay.classList.remove("show")
            if (registerForm) registerForm.reset()
        })
    })
}

// Error Logic
if (loginForm) {
    loginForm.addEventListener("submit", async (event) => {
        event.preventDefault()

        const formData = new FormData(event.target)

        const response = await fetch(event.target.action, {
            method: 'POST',
            body: formData
        })

        const result = await response.json()

        if (response.ok && result.success) {
            window.location.href = result.redirect
        } else {
            errorText.innerText = result.error
            loginError.style.display = "block"
        }
    })

    loginForm.querySelector('input[name="login_input"]').addEventListener('input', () => {
        loginError.style.display = "none"
    })

    closeBtn.addEventListener("click", () => {
        loginError.style.display = "none"
        loginForm.reset()
    })

    // Show Password logic
    togglePassword.addEventListener("click", function () {
        const type = passwordField.getAttribute("type") === "password" ? "text" : "password"
        passwordField.setAttribute("type", type)

        this.innerText = type === "password" ? 'Show' : 'Hide'
    })
}

if (registerForm) {
    registerForm.addEventListener("submit", async (event) => {
        event.preventDefault()

        const formData = new FormData(event.target)

        const response = await fetch(event.target.action, {
            method: 'POST',
            body: formData
        })

        const result = await response.json()

        if (result.success) {
            window.location.href = result.redirect
        } else {
            alert(result.error)
        }
    })

    registerTogglePassword.addEventListener("click", function () {
        const type = registerPasswordField.getAttribute("type") === "password" ? "text" : "password"
        registerPasswordField.setAttribute("type", type)

        this.innerText = type === "password" ? 'Show' : 'Hide'
    })
}