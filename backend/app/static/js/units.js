document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.getElementById('searchInput');
    const unitTypeFilter = document.getElementById('unitTypeFilter');
    const statusFilter = document.getElementById('statusFilter');
    const occupancyFilter = document.getElementById('occupancyFilter');
    const resetFilters = document.getElementById('resetFilters');
    const unitCards = document.querySelectorAll('.unit-card');
    const totalUnitsView = document.querySelector('.total-units-view')


    function filterUnits() {
        const searchTerm = searchInput?.value.trim().toLowerCase() || '';
        const selectedType = unitTypeFilter?.value || '';
        const selectedStatus = statusFilter?.value || '';
        const selectedOccupancy = occupancyFilter?.value || '';

        let visibleCount = 0;

        unitCards.forEach((card) => {
            const unitType = card.dataset.unitType || '';
            const status = card.dataset.status || '';
            const occupancy = card.dataset.occupancy || '';
            const unitNumber = card.dataset.unitNumber || '';
            const cardText = card.textContent.toLowerCase();

            const matchesSearch = !searchTerm || unitNumber.toLowerCase().includes(searchTerm) || cardText.includes(searchTerm);
            const matchesType = !selectedType || unitType === selectedType;
            const matchesStatus = !selectedStatus || status === selectedStatus;
            const matchesOccupancy = !selectedOccupancy || occupancy === selectedOccupancy;

            const isVisible = matchesSearch && matchesType && matchesStatus && matchesOccupancy;

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

    resetFilters?.addEventListener('click', () => {
        if (searchInput) searchInput.value = '';
        if (unitTypeFilter) unitTypeFilter.value = '';
        if (statusFilter) statusFilter.value = '';
        if (occupancyFilter) occupancyFilter.value = '';
        
        filterUnits();
    });

    filterUnits();

});