let matches = [];
let charts = [];

// Mapping team IDs to names
const teamMapping = {
    3: "Arsenal",
    7: "Aston Villa",
    91: "Bournemouth",
    94: "Brentford",
    36: "Brighton and Hove Albion",
    90: "Burnley",
    8: "Chelsea",
    31: "Crystal Palace",
    11: "Everton",
    54: "Fulham",
    2: "Leeds United",
    14: "Liverpool",
    43: "Manchester City",
    1: "Manchester United",
    4: "Newcastle United",
    17: "Nottingham Forest",
    56: "Sunderland",
    6: "Tottenham Hotspur",
    21: "West Ham United",
    39: "Wolverhampton Wanderers",
    13: "Leicester City",
    35: "West Bromwich Albion",
    49: "Sheffield United",
    45: "Norwich City",
    57: "Watford",
    20: "Southampton",
    102: "Luton Town",
    40: "Ipswich Town"
};

// Load all matches JSON
fetch("./allMatches.json")
  .then(r => r.json())
  .then(data => {
    matches = data;
    populateClubMenu();
  });

function populateClubMenu() {
    const clubSelect = document.getElementById("clubSelect");

    // Sort clubs alphabetically
    const sortedClubs = Object.values(teamMapping).sort();

    sortedClubs.forEach(name => {
        let option = document.createElement("option");
        option.value = name;
        option.textContent = name;
        clubSelect.appendChild(option);
    });

    if (clubSelect.options.length > 0) {
        clubSelect.selectedIndex = 0;
        renderCharts();
    }

    clubSelect.addEventListener("change", renderCharts);
}

function renderCharts() {
    const selectedClub = document.getElementById("clubSelect").value;
    const chartsDiv = document.getElementById("charts");
    chartsDiv.innerHTML = "";

    charts.forEach(c => c.destroy());
    charts = [];

    // Collect stats per referee for this club
    const refereeStats = {};
    matches.forEach(match => {
        if (!match.referee) return;

        const teams = [
            { team: match.homeTeam, side: "home" },
            { team: match.awayTeam, side: "away" }
        ];

        teams.forEach(t => {
            if (t.team.teamName === selectedClub) {
                if (!refereeStats[match.referee]) {
                    refereeStats[match.referee] = { yellow: 0, red: 0, fouls: 0, points: 0, games: 0 };
                }

                const stats = refereeStats[match.referee];
                stats.yellow += t.team.totalYellowCards;
                stats.red += t.team.totalRedCard;
                stats.fouls += t.team.fkFoulLost;

                if (t.team.result === "win") stats.points += 3;
                else if (t.team.result === "draw") stats.points += 1;

                stats.games += 1;
            }
        });
    });

    const statsToShow = [
        { label: "Average Yellow Cards", fn: r => r.yellow / r.games },
        { label: "Average Red Cards", fn: r => r.red / r.games },
        { label: "Average Fouls", fn: r => r.fouls / r.games },
        { label: "Yellow to Foul Rate", fn: r => r.yellow / r.fouls },
        { label: "Points Rate", fn: r => r.points / (r.games * 3) }
    ];

    // Filter out refs with less than 3 games for this club
    const refNames = Object.keys(refereeStats).filter(r => refereeStats[r].games >= 3);

    statsToShow.forEach(stat => {
        const container = document.createElement("div");
        container.className = "chart-container";

        const canvas = document.createElement("canvas");
        container.appendChild(canvas);

        // Club average for this stat
        const values = refNames.map(name => stat.fn(refereeStats[name]));
        const clubAverage = values.reduce((a, b) => a + b, 0) / values.length;

        // Display club average next to chart
        const clubValueDiv = document.createElement("div");
        clubValueDiv.className = "club-value";
        clubValueDiv.textContent = `${stat.label}: ${clubAverage.toFixed(2)}`;
        container.appendChild(clubValueDiv);

        chartsDiv.appendChild(container);

        const chart = new Chart(canvas, {
            type: "bar",
            data: {
                labels: refNames,
                datasets: [{
                    label: stat.label,
                    data: values,
                    backgroundColor: "rgba(54, 162, 235, 0.7)"
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } },
                plugins: {
                    legend: { display: true },
                    annotation: {
                        annotations: {
                            avgLine: {
                                type: 'line',
                                yMin: clubAverage,
                                yMax: clubAverage,
                                borderColor: 'red',
                                borderWidth: 2,
                                label: {
                                    content: 'Average',
                                    enabled: true,
                                    position: 'end'
                                }
                            }
                        }
                    }
                }
            },
            plugins: [Chart.registry.getPlugin('annotation')]
        });

        charts.push(chart);
    });
}
