function PlotFirst() {
    let host = window.location.host
    fetch(`http://${host}/ipl/api/first`)
        .then(response => response.json())
        .then((result) => {
            seasons = result['seasons'];
            matches = result['matches'];
            var chart = Highcharts.chart("container", {
                title: {
                    text: "Matches per Season"
                },
                subtitle: {
                    text: "IPL Data"
                },
                xAxis: {
                    title: {
                        text: "Seasons"
                    },
                    categories: seasons
                },
                yAxis: {
                    title: {
                        text: "Match played"
                    }
                },
                series: [
                    {
                        type: "column",
                        name: "Matches",
                        colorByPoint: true,
                        data: matches,
                        showInLegend: false
                    }
                ]
            });
        })
}

function PlotSecond() {
    let host = window.location.host
    fetch(`http://${host}/ipl/api/second`)
    .then(response => response.json())
    .then((result) => {
        seasons = result['season'];
        match_data = result['team_data'];
        var chart = Highcharts.chart('container', {
            chart: {
                type: 'bar'
            },
            title: {
                text: 'Stacked bar chart'
            },
            xAxis: {
                categories: seasons
            },
            yAxis: {
                min: 0,
                title: {
                    text: 'Matches won'
                }
            },
            legend: {
                reversed: true
            },
            plotOptions: {
                series: {
                    stacking: 'normal'
                }
            },
            series: match_data
        });
    })
}

function PlotThird() {
    let host = window.location.host
    fetch(`http://${host}/ipl/api/third`)
        .then(response => response.json())
        .then((result) => {
            teams = result['teams'];
            extra_runs = result['extra_runs'];
            var chart = Highcharts.chart("container", {
                title: {
                    text: "Extra runs conceded by teams in 2016"
                },
                subtitle: {
                    text: "IPL Data"
                },
                xAxis: {
                    title: {
                        text: "Teams"
                    },
                    categories: teams
                },
                yAxis: {
                    title: {
                        text: "Extra Runs Conceded"
                    }
                },
                series: [
                    {
                        type: "column",
                        name: "Extra Runs",
                        colorByPoint: true,
                        data: extra_runs,
                        showInLegend: false
                    }
                ]
            });
        })
}

function PlotFourth() {
    let host = window.location.host
    fetch(`http://${host}/ipl/api/fourth`)
        .then(response => response.json())
        .then((result) => {
            bowlers = result['bowlers'];
            economies = result['economies'];
            var chart = Highcharts.chart("container", {
                title: {
                    text: "Most Economical Bowlers in 2015"
                },
                subtitle: {
                    text: "IPL Data"
                },
                xAxis: {
                    title: {
                        text: "Bowler"
                    },
                    categories: bowlers
                },
                yAxis: {
                    title: {
                        text: "Economy Rate"
                    }
                },
                series: [
                    {
                        type: "column",
                        name: "Economy Rate",
                        colorByPoint: true,
                        data: economies,
                        showInLegend: false
                    }
                ]
            });
        })
}


function PlotFifth() {
    let host = window.location.host
    fetch(`http://${host}/ipl/api/fifth`)
        .then(response => response.json())
        .then((result) => {
            bowlers = result['bowlers'];
            economies = result['economies'];
            var chart = Highcharts.chart("container", {
                title: {
                    text: "Most Economical Bowlers at death overs"
                },
                subtitle: {
                    text: "IPL Data"
                },
                xAxis: {
                    title: {
                        text: "Bowler"
                    },
                    categories: bowlers
                },
                yAxis: {
                    title: {
                        text: "Economy Rate"
                    }
                },
                series: [
                    {
                        type: "column",
                        name: "Economy Rate",
                        colorByPoint: true,
                        data: economies,
                        showInLegend: false
                    }
                ]
            });
        })

        fetch(`http://${host}/ipl/api/fifth/1`)
        .then(response => response.json())
        .then((result) => {
            teams = result['teams'];
            economies = result['economies'];
            var chart = Highcharts.chart("container-1", {
                title: {
                    text: "Most Economical Teams at death overs"
                },
                subtitle: {
                    text: "IPL Data"
                },
                xAxis: {
                    title: {
                        text: "Team"
                    },
                    categories: teams
                },
                yAxis: {
                    title: {
                        text: "Economy Rate"
                    }
                },
                series: [
                    {
                        type: "column",
                        name: "Economy Rate",
                        colorByPoint: true,
                        data: economies,
                        showInLegend: false
                    }
                ]
            });
        })
}