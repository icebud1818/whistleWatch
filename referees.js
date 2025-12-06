let refereeData = [];
let charts = [];

// Load referee stats JSON
fetch("refStats.json")
  .then(r => r.json())
  .then(data => {
    // Only refs with >=10 games
    refereeData = data.filter(r => r.games >= 10);

    // Trim whitespace and sort alphabetically
    refereeData.forEach(r => r.referee = r.referee.trim());
    refereeData.sort((a, b) => a.referee.localeCompare(b.referee));

    populateMenu();
    renderCharts(); // render charts for first referee
  });

function populateMenu() {
    const menu = document.getElementById("refSelect");
    menu.innerHTML = ""; // clear any existing options

    refereeData.forEach(ref => {
        const option = document.createElement("option");
        option.value = ref.referee;
        option.textContent = ref.referee;
        menu.appendChild(option);
    });

    // Auto-render charts when selection changes
    menu.addEventListener("change", renderCharts);
}

function renderCharts() {
    const selectedName = document.getElementById("refSelect").value;
    const selected = refereeData.find(r => r.referee === selectedName);

    const chartsDiv = document.getElementById("charts");
    chartsDiv.innerHTML = "";

    charts.forEach(c => c.destroy());
    charts = [];

    const stats = [
        { label: "Average Red Cards per Game", fn: r => r.totalRedCard / r.games },
        { label: "Average Yellow Cards per Game", fn: r => r.totalYellowCards / r.games },
        { label: "Average Fouls per Game", fn: r => r.totalFouls / r.games },
        { label: "Home Red Cards per Game", fn: r => r.homeRedCard / r.games },
        { label: "Home Yellow Cards per Game", fn: r => r.homeYellowCard / r.games },
        { label: "Home Fouls per Game", fn: r => r.homeFouls / r.games },
        { label: "Away Red Cards per Game", fn: r => r.awayRedCard / r.games },
        { label: "Away Yellow Cards per Game", fn: r => r.awayYellowCard / r.games },
        { label: "Away Fouls per Game", fn: r => r.awayFouls / r.games },
        { label: "Home-Away Red Diff", fn: r => (r.homeRedCard - r.awayRedCard) / r.games },
        { label: "Home-Away Yellow Diff", fn: r => (r.homeYellowCard - r.awayYellowCard) / r.games },
        { label: "Home-Away Foul Diff", fn: r => (r.homeFouls - r.awayFouls) / r.games },
        { label: "Foul-to-Yellow Ratio", fn: r => r.totalFouls / r.totalYellowCards }
    ];

    stats.forEach(stat => {
        const container = document.createElement("div");
        container.className = "chart-container";

        const canvas = document.createElement("canvas");
        container.appendChild(canvas);

        const valueDiv = document.createElement("div");
        valueDiv.className = "ref-value";
        valueDiv.textContent = `${stat.label}: ${stat.fn(selected).toFixed(2)}`;
        container.appendChild(valueDiv);

        chartsDiv.appendChild(container);

        const allValues = refereeData.map(r => stat.fn(r));
        const colors = refereeData.map(r =>
            r.referee === selected.referee ? "pink" : "rgba(54, 162, 235, 0.7)"
        );

        const chart = new Chart(canvas.getContext("2d"), {
            type: "bar",
            data: {
                labels: refereeData.map(r => r.referee),
                datasets: [{
                    label: stat.label,
                    data: allValues,
                    backgroundColor: colors
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                scales: {
                    x: { ticks: { autoSkip: false, maxRotation: 90, minRotation: 90 } },
                    y: { beginAtZero: true }
                },
                plugins: { legend: { display: true } }
            }
        });

        charts.push(chart);
    });
}
