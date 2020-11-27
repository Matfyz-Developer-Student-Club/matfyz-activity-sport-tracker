/**
 * @version 3
 */

//Create horizontalBar plug-in for ChartJS
let originalLineDraw = Chart.controllers.horizontalBar.prototype.draw;
Chart.helpers.extend(Chart.controllers.horizontalBar.prototype, {
    draw: function () {
        originalLineDraw.apply(this, arguments);

        let chart = this.chart;
        let ctx = chart.chart.ctx;

        _checkpoints_hover = {x: [], y: {top: 0, bottom: 0}};

        let indexList = chart.config.options.linesAtIndex;
        let color_id = 0
        let index_count = 0
        let last_index_pos = 0
        for (let index of indexList) {
            index_count = index_count + 1;

            let xaxis = chart.scales['x-axis-0'];
            let yaxis = chart.scales['y-axis-0'];

            let x1 = xaxis.getPixelForValue(index);
            let y1 = 0;

            let x2 = xaxis.getPixelForValue(index);
            let y2 = yaxis.height + 8;

            let color = _checkpoints_colors[color_id];
            color_id = (color_id + 1) % 2;

            _checkpoints_hover.x.push({x: x1, value: index});
            _checkpoints_hover.y.top = y1;
            _checkpoints_hover.y.bottom = y2;

            ctx.save();
            ctx.beginPath();
            ctx.moveTo(x1, y1);
            ctx.strokeStyle = color;
            ctx.lineWidth = 3
            ctx.lineTo(x2, y2);
            ctx.stroke();

            ctx.font = "20px Arial";
            ctx.fillStyle = "black";
            ctx.textAlign = "right";
            ctx.textBaseline = "alphabetic";
            if (last_index_pos + ctx.measureText(index_count.toString()).width + 10 <= x1) {
                ctx.fillText(index_count.toString(), x1 - 5, 15);
                last_index_pos = x1;
            }

            ctx.restore();
        }
    }
});

function canvasMouseMove(e) {
    let rect = this.getBoundingClientRect();
    let xPos = e.clientX - rect.left;
    let yPos = e.clientY - rect.top;

    // Tooltip Element
    let tooltipEl = document.getElementById('checkpoint_tooltip');

    // Create element on first render
    if (!tooltipEl) {
        tooltipEl = document.createElement('div');
        tooltipEl.id = 'checkpoint_tooltip';
        tooltipEl.innerText = '';
        document.body.appendChild(tooltipEl);
    }

    // Get nearest checkpoint
    let checkPoint = getNearestCheckPoint(xPos);

    // Hide if no tooltip needed
    if (!((yPos >= _checkpoints_hover.y.top) && (yPos <= _checkpoints_hover.y.bottom) && checkPoint.value >= 0)) {
        tooltipEl.style.display = 'none';
        return;
    }

    // Set Text
    tooltipEl.innerText = getCheckPoint(checkPoint.value);

    // Display, position, and set styles for font
    tooltipEl.style.display = 'block';
    tooltipEl.style.position = 'absolute';
    tooltipEl.style.left = (rect.left + window.pageXOffset + checkPoint.x - 100) + 'px';
    tooltipEl.style.top = (rect.top + window.pageYOffset - 10) + 'px';
}

function getNearestCheckPoint(x) {
    let res = {x: -1, value: -1};
    // we do not want any checkpoint farther than 15px
    let min = 15;
    for (let item of _checkpoints_hover.x) {
        if (Math.abs(x - item.x) < min) {
            min = Math.abs(x - item.x);
            res = item;
        }
    }
    return res;
}

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
let _checkpoints_hover;
let _checkpoints_colors = ['rgba(0, 123, 255, 1)', 'rgba(24, 222, 56, 1)'];
let csrftoken = $('meta[name=csrf-token]').attr('content');
let _elem = document.getElementById('myChart');
let _ctx = _elem.getContext('2d')

/* globals Chart:false, feather:false */
jQuery(document).ready(function () {

    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })

    _elem.onmousemove = canvasMouseMove;

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

            let myChart = new Chart(_ctx, {
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
                    },
                    tooltips: {
                        callbacks: {
                            label: function (tooltipItem, data) { return tooltipItem.xLabel + ' km'; }
                        }
                    }
                }
            });
        },
    });
});
