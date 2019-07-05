function create_default_chart_option() {
  var options = {
    type: 'line',
    data: {
      labels: ["", "", "", "", "", "", ""],
      datasets: [{
        label: '',
        data: ["", "", "", "", "", "", ""],
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
            stepSize: 1
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
  return options
}


var ctx1 = document.getElementById("commands").getContext('2d');
var commandsChart = new Chart(ctx1, create_default_chart_option());

var ctx2 = document.getElementById("memory").getContext('2d');
var memoryChart = new Chart(ctx2, create_default_chart_option());

var ctx = document.getElementById("network").getContext('2d');
var networkChart = new Chart(ctx, {
  type: 'line',
  data: {
    labels: ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
    datasets: [{
      label: 'Input',
      data: ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
      borderWidth: 3,
      borderColor: '#6777ef',
      backgroundColor: 'transparent',
      pointBackgroundColor: '#fff',
      pointBorderColor: '#6777ef',
      pointRadius: 2.5
    }, {
      label: 'Output',
      data: ["", "", "", "", "", "", "", "", "", "", "", "", "", ""],
      borderWidth: 3,
      borderColor: 'rgba(254,86,83,.7)',
      backgroundColor: 'transparent',
      pointBackgroundColor: '#fff',
      pointBorderColor: 'rgba(254,86,83,.7)',
      pointRadius: 2.5
    }]
  },
  options: {
    scales: {
      yAxes: [{
        gridLines: {
          display: false,
          drawBorder: false,
        },
        scaleLabel: {
          display: true,
          labelString: 'Network I/O(kbps)'
        },
        ticks: {
          beginAtZero: true
        }
      }],
      xAxes: [{
        gridLines: {
          color: '#fbfbfb',
          lineWidth: 2
        }
      }]
    },
    legend: {
      position: "top",
    }
  }
});



function addData(chart, data) {
  chart.data.datasets.forEach((dataset) => {
    dataset.data.push(data);
    if (dataset.data.length >= 8) {
      dataset.data.shift();
    }
  });
  chart.update();
};

function addNetworkData(data) {
  var input_dataset = networkChart.data.datasets[0].data;
  var output_dataset = networkChart.data.datasets[1].data;
  networkChart.data.labels.push(data.time)
  networkChart.data.labels.shift()
  input_dataset.push(data.network_input)
  output_dataset.push(data.network_output)
  if (input_dataset.length >= 15) {
    input_dataset.shift();
  }
  if (output_dataset.length >= 15) {
    output_dataset.shift();
  }
  networkChart.update();
}

function getData() {
  $.ajax({
    method: "get",
    url: '/redisboard/dashboard_api/',
    success: function(data) {
      if (data.code == 0) {
        addData(commandsChart, data.data.cmd_per_sec)
        addData(memoryChart, data.data.memory)
        addNetworkData(data.data)
      } else {
        iziToast.error({
          title: 'Error!',
          message: data.error,
          position: 'topRight'
        });
      }
    }
  })
};
$(function() {
  t = setInterval("getData()", 5000);
})