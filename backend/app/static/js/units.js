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
