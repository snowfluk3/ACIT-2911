const generateBtn = document.getElementById("generate-btn")
const recipesGrid = document.getElementById("recipes-grid")
const recipesLoading = document.getElementById("recipes-loading")
const recipesError = document.getElementById("recipes-error")

let pollInterval = null

function setLoading(isLoading) {
    recipesLoading.style.display = isLoading ? "block" : "none"
    if (generateBtn) generateBtn.disabled = isLoading
}

function showError(message) {
    recipesError.querySelector("p").textContent = message
    recipesError.style.display = "block"
}

async function loadRecipesFromDB() {
    try {
        const response = await fetch("/recipes/rendered")
        if (response.ok) {
            recipesGrid.innerHTML = await response.text()
        }
    } catch {}
}

function stopPolling() {
    if (pollInterval) {
        clearInterval(pollInterval)
        pollInterval = null
    }
}

function startPolling() {
    pollInterval = setInterval(async () => {
        try {
            const response = await fetch("/recipes/status")
            const data = await response.json()

            if (data.state === "done") {
                stopPolling()
                await loadRecipesFromDB()
                setLoading(false)
            } else if (data.state === "error") {
                stopPolling()
                showError(`Could not generate recipes: ${data.error}`)
                setLoading(false)
            }
        } catch (err) {
            stopPolling()
            showError(`Could not check generation status: ${err.message}`)
            setLoading(false)
        }
    }, 2000)
}

if (generateBtn) {
    generateBtn.addEventListener("click", async () => {
        recipesError.style.display = "none"
        setLoading(true)

        try {
            const response = await fetch("/recipes/generate", { method: "POST" })
            if (response.status === 409) {
                // Already generating — just start polling
                startPolling()
                return
            }
            if (!response.ok) throw new Error(await response.text())
            startPolling()
        } catch (err) {
            showError(`Could not start recipe generation: ${err.message}`)
            setLoading(false)
        }
    })
}

// On page load: show any existing recipes and resume polling if generation is in progress
async function init() {
    await loadRecipesFromDB()
    try {
        const response = await fetch("/recipes/status")
        const data = await response.json()
        if (data.state === "generating") {
            setLoading(true)
            startPolling()
        }
    } catch {}
}

init()
