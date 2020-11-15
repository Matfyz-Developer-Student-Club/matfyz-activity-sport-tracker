/**
 * @version 2
 */

//Create horizontalBar plug-in for ChartJS
let originalLineDraw = Chart.controllers.horizontalBar.prototype.draw;
Chart.helpers.extend(Chart.controllers.horizontalBar.prototype, {

  draw: function () {
      originalLineDraw.apply(this, arguments);

      let chart = this.chart;
      let ctx = chart.chart.ctx;

      let indexList = chart.config.options.linesAtIndex;
      let color_id = 0
      for (let index of indexList) {

          let xaxis = chart.scales['x-axis-0'];
          let yaxis = chart.scales['y-axis-0'];

          let x1 = xaxis.getPixelForValue(index);
          let y1 = 0;

          let x2 = xaxis.getPixelForValue(index);
          let y2 = yaxis.height + 8;

          let color = _checkpoints_colors[color_id];
          color_id = (color_id + 1) % 2;

          ctx.save();
          ctx.beginPath();
          ctx.moveTo(x1, y1);
          ctx.strokeStyle = color;
          ctx.lineWidth = 3
          ctx.lineTo(x2, y2);
          ctx.stroke();

          ctx.restore();
      }
  }
});

function getCheckPoint(value) {
    // check if the property/key is defined in the object itself, not in parent'
    if (_checkpoints.hasOwnProperty(value)) {
        return _checkpoints[value]
    } else {
        return '';
    }
}

let _data;
let _labels;
let _checkpoints;
let _checkpoints_colors = ['rgba(0, 123, 255, 1)', 'rgba(24, 222, 56, 1)']
let csrftoken = $('meta[name=csrf-token]').attr('content')
let _ctx = document.getElementById('myChart').getContext('2d')

/* globals Chart:false, feather:false */
jQuery(document).ready(function () {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })

    $.ajax({
        url: "/get_global_contest",
        type: "GET",
        data: {vals: ''},
        success: function (response) {
            let full_data = JSON.parse(response.payload);
            _data = full_data['data'];
            _labels = full_data['labels'];
            _checkpoints = full_data['checkpoints'];
            let keys = Object.keys(_checkpoints)
            let max = Math.ceil(parseInt(keys[keys.length - 1]) / 100) * 100;

            let myChart_foot = new Chart(_ctx, {
                type: 'horizontalBar',
                data: {
                    labels: _labels,
                    datasets: [{
                        data: _data,
                        backgroundColor: [
                            'rgba(54, 162, 235, 0.2)',
                            'rgba(255, 99, 132, 0.2)'
                        ],
                        borderColor: [
                            'rgba(54, 162, 235, 1)',
                            'rgba(255, 99, 132, 1)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    linesAtIndex: keys,
                    legend: {
                        display: false
                    },
                    scales: {
                        xAxes: [{
                            ticks: {
                                beginAtZero: true,
                                suggestedMin: 0,
                                suggestedMax: max,
                                callback: function (value) { return value + ' km'; }
                            }
                        }],
                        yAxes: []
                    }
                }
            });
        },
    });
});

