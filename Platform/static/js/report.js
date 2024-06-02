async function fetchData() {
    const response = await fetch('/data/power_consumption_data/');
    const data = await response.json();
    return data;
}

function aggregateDataByMonth(data) {
    const monthlyData = {};
    
    data.forEach(entry => {
        const date = new Date(entry.date);
        const month = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}`;
        const day = `${date.getFullYear()}-${String(date.getMonth() + 1).padStart(2, '0')}-${String(date.getDate()).padStart(2, '0')}`;
        
        if (!monthlyData[month]) {
            monthlyData[month] = { zone_1: 0, zone_2: 0, zone_3: 0, count: 0, daily: {} };
        }
        
        if (!monthlyData[month].daily[day]) {
            monthlyData[month].daily[day] = { zone_1: 0, zone_2: 0, zone_3: 0, count: 0 };
        }
        
        monthlyData[month].zone_1 += entry.zone_1_power_consumption;
        monthlyData[month].zone_2 += entry.zone_2_power_consumption;
        monthlyData[month].zone_3 += entry.zone_3_power_consumption;
        monthlyData[month].count += 1;
        
        monthlyData[month].daily[day].zone_1 += entry.zone_1_power_consumption;
        monthlyData[month].daily[day].zone_2 += entry.zone_2_power_consumption;
        monthlyData[month].daily[day].zone_3 += entry.zone_3_power_consumption;
        monthlyData[month].daily[day].count += 1;
    });
    
    return Object.entries(monthlyData).map(([month, values]) => ({
        month,
        zone_1_avg: values.zone_1 / values.count,
        zone_2_avg: values.zone_2 / values.count,
        zone_3_avg: values.zone_3 / values.count,
        total_zone_1: values.zone_1,
        total_zone_2: values.zone_2,
        total_zone_3: values.zone_3,
        daily: Object.entries(values.daily).map(([day, dailyValues]) => ({
            day,
            zone_1: dailyValues.zone_1,
            zone_2: dailyValues.zone_2,
            zone_3: dailyValues.zone_3
        }))
    }));
}

function populateDailyTable(data) {
    const tbody = document.querySelector("#daily-table tbody");
    tbody.innerHTML = ''; 

    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.day}</td>
            <td>${row.zone_1.toFixed(2)}</td>
            <td>${row.zone_2.toFixed(2)}</td>
            <td>${row.zone_3.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function populateMonthlyTable(data) {
    const tbody = document.querySelector("#demo-table tbody");
    tbody.innerHTML = ''; 

    data.forEach(row => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${row.month}</td>
            <td>${row.total_zone_1.toFixed(2)}</td>
            <td>${row.total_zone_2.toFixed(2)}</td>
            <td>${row.total_zone_3.toFixed(2)}</td>
        `;
        tbody.appendChild(tr);
    });
}

function handleMonthSelection(aggregatedData) {
    const monthSelect = document.querySelector("#month-select");
    monthSelect.addEventListener('change', () => {
        const selectedMonth = monthSelect.value;
        const selectedData = aggregatedData.find(data => data.month === selectedMonth);

        if (selectedData) {
            populateDailyTable(selectedData.daily);
        }
    });
}

document.addEventListener('DOMContentLoaded', async () => {
    const rawData = await fetchData();
    const aggregatedData = aggregateDataByMonth(rawData);
    
    const monthSelect = document.querySelector("#month-select");
    aggregatedData.forEach(row => {
        const option = document.createElement('option');
        option.value = row.month;
        option.text = row.month;
        monthSelect.appendChild(option);
    });

    populateMonthlyTable(aggregatedData);
    handleMonthSelection(aggregatedData);
});
