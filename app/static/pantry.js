const addItemBtn = document.getElementById("add-item-btn")
const pantryItemsContainer = document.getElementById("pantry-items")
const itemFormContainer = document.getElementById("item-form-container")
const itemForm = document.getElementById("item-form")
const itemFormTitle = document.getElementById("item-form-title")
const itemIdField = document.getElementById("item-id")
const itemNameField = document.getElementById("item-name")
const itemQuantityField = document.getElementById("item-quantity")
const itemUnitField = document.getElementById("item-unit")
const itemCategoryField = document.getElementById("item-category")
const itemExpiryField = document.getElementById("item-expiry-date")
const itemNotesField = document.getElementById("item-notes")
const cancelItemBtn = document.getElementById("cancel-item-btn")
const submitItemBtn = document.getElementById("submit-item-btn")

// Pantry item management
const API_BASE = "/ingredients"

function formatDate(dateString) {
    if (!dateString) return ""
    const date = new Date(dateString)
    return date.toLocaleDateString(undefined, { year: 'numeric', month: 'short', day: 'numeric' })
}

function resetItemForm() {
    itemIdField.value = ""
    itemNameField.value = ""
    itemQuantityField.value = ""
    itemUnitField.value = ""
    itemCategoryField.value = ""
    itemExpiryField.value = ""
    itemNotesField.value = ""
}

function showItemForm(editing = false) {
    itemFormContainer.classList.remove("hidden")
    itemFormTitle.innerText = editing ? "Edit Pantry Item" : "Add Pantry Item"
    submitItemBtn.innerText = editing ? "Update Item" : "Add Item"
}

function hideItemForm() {
    itemFormContainer.classList.add("hidden")
    resetItemForm()
}

async function fetchIngredients() {
    try {
        const response = await fetch(API_BASE)
        const items = await response.json()
        renderPantryItems(items)
    } catch (error) {
        pantryItemsContainer.innerHTML = `<p class="error-message">Unable to load pantry items. Please refresh.</p>`
    }
}

function renderPantryItems(items) {
    if (!items.length) {
        pantryItemsContainer.innerHTML = `
            <div class="empty-state quicksand-regular">
                <p>No pantry items yet.</p>
                <p>Click "Add Item" to create your first entry.</p>
            </div>
        `
        return
    }

    pantryItemsContainer.innerHTML = items.map(item => `
        <article class="pantry-card">
            <div class="card-header">
                <div>
                    <h3 class="elms-sans-regular">${item.name}</h3>
                    <p class="quicksand-regular">${item.category || "Uncategorized"}</p>
                </div>
                <div class="card-actions">
                    <button class="card-edit quicksand-regular" data-id="${item.id}">Edit</button>
                    <button class="card-delete quicksand-regular" data-id="${item.id}">Delete</button>
                </div>
            </div>
            <p class="quicksand-regular">Quantity: ${item.quantity} ${item.unit || ""}</p>
            <p class="quicksand-regular">Expiry: ${item.expiry_date ? formatDate(item.expiry_date) : "None"}</p>
            ${item.notes ? `<p class="quicksand-regular notes">Notes: ${item.notes}</p>` : ""}
        </article>
    `).join("")

    document.querySelectorAll('.card-edit').forEach(button => {
        button.addEventListener('click', () => handleEditItem(button.dataset.id))
    })

    document.querySelectorAll('.card-delete').forEach(button => {
        button.addEventListener('click', () => handleDeleteItem(button.dataset.id))
    })
}

async function handleEditItem(id) {
    try {
        const response = await fetch(`${API_BASE}/${id}`)
        const item = await response.json()

        itemIdField.value = item.id
        itemNameField.value = item.name
        itemQuantityField.value = item.quantity
        itemUnitField.value = item.unit || ""
        itemCategoryField.value = item.category || ""
        itemExpiryField.value = item.expiry_date || ""
        itemNotesField.value = item.notes || ""

        showItemForm(true)
    } catch (error) {
        alert('Unable to load item for editing.')
    }
}

async function handleDeleteItem(id) {
    const confirmed = confirm('Delete this pantry item?')
    if (!confirmed) return

    await fetch(`${API_BASE}/${id}`, { method: 'DELETE' })
    fetchIngredients()
}

if (itemForm && addItemBtn && pantryItemsContainer) {
    itemForm.addEventListener('submit', async (event) => {
        event.preventDefault()

        const payload = {
            name: itemNameField.value.trim(),
            quantity: Number(itemQuantityField.value) || 0,
            unit: itemUnitField.value.trim(),
            category: itemCategoryField.value.trim(),
            expiry_date: itemExpiryField.value || null,
            notes: itemNotesField.value.trim() || null,
        }

        if (!payload.name) {
            alert('Please enter a pantry item name.')
            return
        }

        const id = itemIdField.value
        const method = id ? 'PUT' : 'POST'
        const endpoint = id ? `${API_BASE}/${id}` : API_BASE

        await fetch(endpoint, {
            method,
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload),
        })

        hideItemForm()
        fetchIngredients()
    })

    addItemBtn.addEventListener('click', () => {
        resetItemForm()
        showItemForm(false)
    })

    cancelItemBtn.addEventListener('click', hideItemForm)

    document.addEventListener('DOMContentLoaded', fetchIngredients)

}