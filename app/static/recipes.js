const generateBtn = document.getElementById("generate-btn")
const recipesGrid = document.getElementById("recipes-grid")
const recipesLoading = document.getElementById("recipes-loading")
const recipesError = document.getElementById("recipes-error")

if (generateBtn) {
    generateBtn.addEventListener("click", async () => {
        generateBtn.disabled = true
        recipesGrid.innerHTML = ""
        recipesError.style.display = "none"
        recipesLoading.style.display = "block"

        try {
            const response = await fetch("/recipes/generate", { method: "POST" })
            if (!response.ok) throw new Error(await response.text())
            recipesGrid.innerHTML = await response.text()
        } catch (err) {
            recipesError.querySelector("p").textContent = `Could not generate recipes: ${err.message}. Make sure LM Studio is running.`
            recipesError.style.display = "block"
        } finally {
            recipesLoading.style.display = "none"
            generateBtn.disabled = false
        }
    })
}
