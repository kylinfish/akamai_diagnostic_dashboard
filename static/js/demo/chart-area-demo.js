// Set new default font family and font color to mimic Bootstrap's default styling
Chart.defaults.global.defaultFontFamily = '-apple-system,system-ui,BlinkMacSystemFont,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif';
Chart.defaults.global.defaultFontColor = '#292b2c';

// Area Chart Example
var ctx = document.getElementById("myAreaChart");
var myLineChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["June 1", "June 2", "June 3", "June 4", "June 5", "June 6", "June 7", "June 8", "June 9", "June 10", "June 11", "June 12", "June 13"],
    datasets: [{
      label: "2XX",
      lineTension: 0.3,
      backgroundColor: "rgba(0, 230,216,0.2)",
      borderColor: "rgba(0, 230, 64, 1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(0, 230, 64, 1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(0, 230, 64, 1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [1950, 1700, 1850, 1400, 1528, 1785, 2015, 2300, 1488, 1250, 1813, 2109, 1289],
    },
    {
      label: "3XX",
      lineTension: 0.3,
      backgroundColor: "rgba(2,117,216,0.2)",
      borderColor: "rgba(2,117,216,1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(2,117,216,1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(2,117,216,1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [585, 510, 555, 420, 458, 535, 604, 690, 446, 375, 543, 632, 386],
    },
    {
      label: "4XX",
      lineTension: 0.3,
      backgroundColor: "rgba(238, 238,0,0.2)",
      borderColor: "rgba(238, 238, 0, 1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(238, 238, 0, 1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(238, 238, 0, 1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [97, 85,  92,  70,  76,  89, 100,  115, 74,  62,  90, 105,  64],
    },
    {
      label: "5XX",
      lineTension: 0.3,
      backgroundColor: "rgba(241, 169, 160, 02)",
      borderColor: "rgba(242, 38, 19, 1)",
      pointRadius: 5,
      pointBackgroundColor: "rgba(242, 38, 19, 1)",
      pointBorderColor: "rgba(255,255,255,0.8)",
      pointHoverRadius: 5,
      pointHoverBackgroundColor: "rgba(242, 38, 19, 1)",
      pointHitRadius: 50,
      pointBorderWidth: 2,
      data: [78, 68,  74,  56,  61, 71,  1500,  92,  59, 50,  72, 84, 51],
    }],
  },
  options: {
    scales: {
      xAxes: [{
        time: {
          unit: 'date'
        },
        gridLines: {
          display: false
        },
        ticks: {
          maxTicksLimit: 7
        }
      }],
      yAxes: [{
        ticks: {
          min: 0,
          max: 3000,
          maxTicksLimit: 5
        },
        gridLines: {
          color: "rgba(0, 0, 0, .125)",
        }
      }],
    },
    legend: {
      display: true
    }
  }
});
