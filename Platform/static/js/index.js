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
        
        if (!monthlyData[month]) {
            monthlyData[month] = { zone_1: 0, zone_2: 0, zone_3: 0, count: 0 };
        }
        
        monthlyData[month].zone_1 += entry.zone_1_power_consumption;
        monthlyData[month].zone_2 += entry.zone_2_power_consumption;
        monthlyData[month].zone_3 += entry.zone_3_power_consumption;
        monthlyData[month].count += 1;
    });
    
    return Object.entries(monthlyData).map(([month, values]) => ({
        date: month,
        zone_1_power_consumption: values.zone_1 / values.count,
        zone_2_power_consumption: values.zone_2 / values.count,
        zone_3_power_consumption: values.zone_3 / values.count
    }));
}

function createChart(elementId, labels, data) {
    new Chart(document.getElementById(elementId), {
        type: 'line',
        data: {
            labels: labels,
            datasets: [{
                label: 'Power Consumption',
                data: data,
                borderWidth: 1,
                borderColor: 'rgba(75, 192, 192, 1)',
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                tension: 0.1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
}

async function initCharts() {
    const data = await fetchData();
    const monthlyData = aggregateDataByMonth(data);

    const labels = monthlyData.map(entry => entry.date);
    const zone1Data = monthlyData.map(entry => entry.zone_1_power_consumption);
    const zone2Data = monthlyData.map(entry => entry.zone_2_power_consumption);
    const zone3Data = monthlyData.map(entry => entry.zone_3_power_consumption);

    createChart('graph1', labels, zone1Data);
    createChart('graph2', labels, zone2Data);
    createChart('graph3', labels, zone3Data);
}

document.addEventListener('DOMContentLoaded', initCharts);
