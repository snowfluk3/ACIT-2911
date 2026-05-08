const loginBtn = document.getElementById("login-btn")
const loginPopup = document.getElementById("login-popup")
const loginForm = document.getElementById("login-form")
const loginError = document.getElementById("login-error")
const errorText = document.getElementById("error-text")

const closeBtn = document.getElementById("close-btn")
const overlay = document.getElementById("overlay")

const passwordField = document.getElementById("password-field")
const togglePassword = document.getElementById("toggle-password")

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

    loginForm.querySelector('input[name="username"]').addEventListener('input', () => {
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

        this.textContent = type === "password" ? 'Show' : 'Hide'
    })
}
