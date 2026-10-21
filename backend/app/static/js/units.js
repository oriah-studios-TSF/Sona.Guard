document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const unitTypeFilter = document.getElementById('unitTypeFilter');
    const statusFilter = document.getElementById('statusFilter');
    const occupancyFilter = document.getElementById('occupancyFilter');
    const resetFilters = document.getElementById('resetFilters');
    const propertyFilter = document.getElementById('propertyFilter');
    const unitCards = document.querySelectorAll('.unit-card');
    const totalUnitsView = document.querySelector('.total-units-view')


    function filterUnits() {
        const searchTerm = searchInput?.value.trim().toLowerCase() || '';
        const selectedType = unitTypeFilter?.value || '';
        const selectedStatus = statusFilter?.value || '';
        const selectedOccupancy = occupancyFilter?.value || '';
        const selectedProperty = propertyFilter?.value || '';

        let visibleCount = 0;

        unitCards.forEach((card) => {
            const unitType = card.dataset.unitType || '';
            const status = card.dataset.status || '';
            const occupancy = card.dataset.occupancy || '';
            const unitNumber = card.dataset.unitNumber || '';
            const unitProperty = card.dataset.unitProperty || '';
            const cardText = card.textContent.toLowerCase();

            const matchesSearch = !searchTerm || unitNumber.toLowerCase().includes(searchTerm) || cardText.includes(searchTerm);
            const matchesType = !selectedType || unitType === selectedType;
            const matchesStatus = !selectedStatus || status === selectedStatus;
            const matchesOccupancy = !selectedOccupancy || occupancy === selectedOccupancy;
            const matchesProperty = !selectedProperty || unitProperty === selectedProperty;

            const isVisible = matchesSearch && matchesType && matchesStatus && matchesOccupancy && matchesProperty;

            card.style.display = isVisible ? 'flex' : 'none';

            if (isVisible) {
                visibleCount++;
            }
        });

        if (totalUnitsView) {
            totalUnitsView.textContent = `${visibleCount} Units`;
        }
    }

    searchInput?.addEventListener('input', filterUnits);
    unitTypeFilter?.addEventListener('change', filterUnits);
    statusFilter?.addEventListener('change', filterUnits);
    occupancyFilter?.addEventListener('change', filterUnits);
    propertyFilter?.addEventListener('change', filterUnits);

    resetFilters?.addEventListener('click', () => {
        if (searchInput) searchInput.value = '';
        if (unitTypeFilter) unitTypeFilter.value = '';
        if (statusFilter) statusFilter.value = '';
        if (occupancyFilter) occupancyFilter.value = '';
        if (propertyFilter) propertyFilter.value = '';
        
        filterUnits();
    });

    filterUnits();

});

// Create Unit Model
const createUnitModel = document.getElementById('create-unit-model')
const openCreateUnitButton = document.getElementById('open-create-unit-button')
const closeCreateUnitButton = document.getElementById('close-create-unit-button')
const cancelCreateUnitButton = document.getElementById('cancel-create-unit-button')

function openCreateUnitModel() {
    createUnitModel.classList.add('is-open')
}

function closeCreateUnitModel() {
    createUnitModel.classList.remove('is-open')
}

openCreateUnitButton?.addEventListener('click', openCreateUnitModel)
closeCreateUnitButton?.addEventListener('click', closeCreateUnitModel)
cancelCreateUnitButton?.addEventListener('click', closeCreateUnitModel)


// View Unit Model
const viewUnitModel = document.getElementById('view-unit-model');
const closeViewUnitButton = document.getElementById('close-view-unit-button');
const cancelViewUnitButton = document.getElementById('cancel-view-unit-button');

document.querySelectorAll('.view-button').forEach(button => {
    button.addEventListener('click', () => {
        const card = button.closest('.unit-card');

        

        document.getElementById('view-unit-number').textContent = card.querySelector('.unit-card-header h1').textContent.trim();
        document.getElementById('view-unit-type').textContent = card.querySelector('.unit-type').textContent.trim();
        document.getElementById('view-unit-status').textContent = card.querySelector('.unit-status').textContent.trim();
        
        const statusBadge = document.getElementById('view-unit-status');
        const statusElement = card.querySelector('.unit-status');
        const status = card.dataset.status;
        statusBadge.textContent = statusElement.textContent.trim();
        statusBadge.classList.remove('active', 'inactive');
        statusBadge.classList.add(status);
        
        const occupancyBadge = document.getElementById('view-unit-occupancy');
        const occupancyElement = card.querySelector('.occupation-status');
        const occupancyStatus = card.dataset.occupancy

        occupancyBadge.textContent = occupancyElement.textContent.trim();
        occupancyBadge.classList.remove('occupied', 'vacant');
        occupancyBadge.classList.add(occupancyStatus);

        
        document.getElementById('view-unit-property').textContent = card.querySelector('.unit-estate').textContent.trim();

        viewUnitModel.classList.add('is-open');
    });
});

function closeViewUnitModel() {
    viewUnitModel.classList.remove('is-open');
}

closeViewUnitButton?.addEventListener('click', closeViewUnitModel);
cancelViewUnitButton?.addEventListener('click', closeViewUnitModel);

// Edit Unit Model
const editUnitModel = document.getElementById('edit-unit-model');
const editUnitForm = document.getElementById('edit-unit-form');
const closeEditUnitButton = document.getElementById('edit-unit-close-button');
const cancelEditUnitButton = document.getElementById('cancel-edit-unit');

document.querySelectorAll('.edit-button').forEach(button => {
    button.addEventListener('click', () => {
        const card = button.closest('.unit-card');

        document.getElementById('edit-unit-number').value = card.dataset.unitNumber;
        document.getElementById('edit-unit-type').value = card.dataset.unitType;
        document.getElementById('edit-unit-status').value = card.dataset.status === 'active' ? 'true' : 'false'

        editUnitForm.action = `/units/${card.dataset.unitId}/edit`;
        editUnitModel.classList.add('is-open');
    });
});

function closeEditUnitModel() {
    editUnitModel.classList.remove('is-open');
}

closeEditUnitButton?.addEventListener('click', closeEditUnitModel);
cancelEditUnitButton?.addEventListener('click', closeEditUnitModel);

// More options container
// Find every element with the class "unit-more-container" on the page.
// Each unit card has its own container for the More button and its dropdown menu.
document.querySelectorAll('.unit-more-container').forEach(container => {

    // Find the More button that belongs to this particular container.
    // Using container.querySelector() ensures we get the button for this unit,
    // rather than accidentally selecting a button from another unit card.
    const moreButton = container.querySelector('.more');

    // Listen for a click on this unit's More button.
    // The function inside addEventListener() runs whenever the button is clicked.
    moreButton.addEventListener('click', event => {

        // Stop this click from travelling up through the HTML element hierarchy.
        // This is called event bubbling.
        // It is useful when another click listener on a parent or the document
        // should not treat this button click as a click somewhere outside the menu.
        event.stopPropagation();

        // Check whether this unit's menu is already open.
        // classList.contains() returns true if the container currently has
        // the CSS class "is-open", or false if it does not.
        // We save the result because we need to know whether to open or close it.
        const isAlreadyOpen = container.classList.contains('is-open');

        // Find every unit menu that is currently open.
        // The selector ".unit-more-container.is-open" means an element must have
        // BOTH classes: "unit-more-container" and "is-open".
        document.querySelectorAll('.unit-more-container.is-open').forEach(openContainer => {

            // Remove the "is-open" class from each open menu.
            // Your CSS uses this class to control whether the dropdown is visible.
            // Removing it closes the menu.
            openContainer.classList.remove('is-open');

            // Find the More button inside this menu and update its accessibility state.
            // aria-expanded="false" communicates that the menu is now collapsed.
            // The optional chaining operator (?.) means setAttribute() is called
            // only if a More button was found. If there is no button, JavaScript
            // skips this call instead of throwing an error.
            openContainer.querySelector('.more')?.setAttribute('aria-expanded', 'false');
        });

        // Now decide whether to reopen this menu.
        // We saved isAlreadyOpen BEFORE closing all the menus.
        // If it was already open, we leave it closed.
        // If it was closed, we open it.
        if (!isAlreadyOpen) {

            // Add the "is-open" class to this unit's container.
            // Your CSS detects this class and displays its dropdown menu.
            container.classList.add('is-open');

            // Tell assistive technology that this button's menu is expanded.
            // The value is a string because HTML attribute values are text.
            moreButton.setAttribute('aria-expanded', 'true');
        }
    });
});

// Resident Assignemnt Model
const residentAssignmentModal = document.getElementById('resident-assignments-model');
const residentAssignmentModalCloseButton = document.getElementById('resident-assignments-close-button');
const closeResidentAssignmentButton = document.getElementById('close-resident-assignments');

// Open Resident Assignemtns from the More menu
document.querySelectorAll('.view-residents-button').forEach(button => {
    button.addEventListener('click', async () => {
        // Identify the unit card containing the clicked button
        const card = button.closest('.unit-card');
        
        // Find the container where the resident cards appear.
        const residentList = document.getElementById('resident-assignments-list');
        
        // Request the residents assigned to this unit
        try {
            const response = await fetch(`/units/${card.dataset.unitId}/residents`);

            // Stop if flask reports an unsuccessful respononse
            if (!response.ok) {
                throw new Error('Could not load residents for this unit.');
            }

            // Convert the JSON response into a JS object
            const data = await response.json();

            const emptyState = document.getElementById('resident-assignment-empty');


            // Check whether this unit has any residents asssigned to it
            if (data.residents.length === 0) {
                emptyState.style.display = 'block';
                residentList.style.display = 'none';
                
                
            } else {
                // Hide the empty state when residents exist.
                emptyState.style.display = 'none';
            }

    
            // Create a card for each resident returned
            // Use the existing HTML elements to display the resident details.
            data.residents.forEach(resident => {
                document.getElementById('resident-assignment-list-full-name').textContent =
                    resident.full_name;
            
                document.getElementById('resident-assignment-list-resident-code').textContent =
                    resident.resident_code;
            
                document.getElementById('resident-assignment-list-phone').textContent =
                    resident.phone_number;
            
                document.getElementById('resident-assignment-list-email').textContent =
                    resident.email || 'Not provided';
            
                document.getElementById('resident-assignment-list-status').textContent =
                    `${resident.is_active ? 'Active' : 'Inactive'}`;

                
                document.getElementById('resident-assignment-list-status').classList.add(
                    resident.is_active ? 'active' : 'inactive'
                );
            });

            
        } catch (error) {
            residentList.textContent = error.message;
        }

        // Display the selected unit's details in the model
        document.getElementById('assignments-unit-number').textContent = card.querySelector('.unit-card-header h1').textContent.trim();
        document.getElementById('assignments-unit-estate').textContent = card.querySelector('.unit-estate').textContent.trim();

        // Open the modal
        residentAssignmentModal.classList.add('is-open');

        const menuContainer = button.closest('.unit-more-container');

        // Close the More menu after selectiong an action

        if (menuContainer) {
            menuContainer.classList.remove('is-open');
            menuContainer.querySelector('.more')?.setAttribute('aria-expanded', 'false');
        }
        
    });
});

// Close the Resident Assignments Modal
function closeResidentAssignmentModal() {
    residentAssignmentModal.classList.remove('is-open');
}



// 
residentAssignmentModalCloseButton?.addEventListener('click', closeResidentAssignmentModal);
closeResidentAssignmentButton?.addEventListener('click', closeResidentAssignmentModal);


