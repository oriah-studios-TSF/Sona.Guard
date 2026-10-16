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
