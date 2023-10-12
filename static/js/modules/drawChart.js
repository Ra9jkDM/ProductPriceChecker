export function drawChart(input, id){
    const ctx = document.getElementById(id);

    new Chart(ctx, {
        type: 'line',
        data: {
        labels: input.labels,
        datasets: input.datasets
        },
        options: {
        /*scales: {
            y: {
            beginAtZero: true
            }
        }*/
        }
    });
}
