var defaultChartOptions = {
  type: 'line',
  data: {
    labels: ["1", "2", "3", "4", "5", "6", "7"],
    datasets: [{
      label: 'Statistics',
      data: [460, 458, 330, 502, 430, 610, 488],
      borderWidth: 2,
      backgroundColor: '#6777ef',
      borderColor: '#6777ef',
      borderWidth: 2.5,
      pointBackgroundColor: '#ffffff',
      pointRadius: 4
    }]
  },
  options: {
    legend: {
      display: false
    },
    scales: {
      yAxes: [{
        gridLines: {
          display: false,
        },
        ticks: {
          beginAtZero: true,
          stepSize: 150
        }
      }],
      xAxes: [{
        ticks: {
          display: false
        },
        gridLines: {
          display: false
        }
      }]
    },
  }
};

var ctx = document.getElementById("commands").getContext('2d');
var commandsChart = new Chart(ctx, defaultChartOptions);

var ctx = document.getElementById("memory").getContext('2d');
var memoryChart = new Chart(ctx, defaultChartOptions);

var ctx = document.getElementById("network").getContext('2d');

var networkChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"],
    datasets: [{
      label: 'Statistics',
      data: [640, 387, 530, 302, 430, 270, 488],
      borderWidth: 5,
      borderColor: '#6777ef',
      backgroundColor: 'transparent',
      pointBackgroundColor: '#fff',
      pointBorderColor: '#6777ef',
      pointRadius: 4
    }]
  },
  options: {
    legend: {
      display: false
    },
    scales: {
      yAxes: [{
        gridLines: {
          display: false,
          drawBorder: false,
        },
        ticks: {
          stepSize: 150
        }
      }],
      xAxes: [{
        gridLines: {
          color: '#fbfbfb',
          lineWidth: 2
        }
      }]
    },
  }
});



function addData(chart, label, data) {

  chart.data.datasets.forEach((dataset) => {
    dataset.data.push(data);
    dataset.data.shift();
  });
  chart.update();
};

// $(function() {
//   t = setInterval("addData(chart, '', 100)", 1000);
// })