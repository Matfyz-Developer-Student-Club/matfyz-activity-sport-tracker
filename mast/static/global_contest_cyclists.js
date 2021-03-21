/**
 * @version 1
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

            ctx.font = "18px Montserrat";
            ctx.fillStyle = "black";
            ctx.textAlign = "left";
            ctx.textBaseline = "alphabetic";

            // ctx.fillText(_checkpoints[index], x1 + 5, 15);
            wrapText(ctx, _checkpoints[index], x1 + 5, 15, ctx.lineWidth, 20 )
            last_index_pos = x1;

            ctx.restore();
        }
    }
});

function wrapText(context, text, x, y, maxWidth, lineHeight) {
    var words = text.split(' ');
    var line = '';

    for (var n = 0; n < words.length; n++) {
        var testLine = line + words[n] + ' ';
        var metrics = context.measureText(testLine);
        var testWidth = metrics.width;
        if (testWidth > maxWidth && n > 0) {
            context.fillText(line, x, y);
            line = words[n] + ' ';
            y += lineHeight;
        } else {
            line = testLine;
        }
    }
    context.fillText(line, x, y);
}

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
let _checkpoints_colors = ['rgb(54, 162, 235)', 'rgb(255, 99, 132)'];
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
        url: "/get_global_contest_cyclists",
        type: "GET",
        data: {vals: ''},
        success: function (response) {
            let full_data = JSON.parse(response.payload);
            _data = full_data['data'];
            _label = full_data['label'];
            _checkpoints = full_data['checkpoints'];
            let keys = Object.keys(_checkpoints)
            let max = Math.ceil(parseInt(keys[keys.length - 1]) / 100) * 100;

            let myChart = new Chart(_ctx, {
                type: 'horizontalBar',
                data: {
                    labels: [],
                    datasets: [{
                        data: _data,
                        backgroundColor: [
                            'rgba(255, 159, 64, 0.8)',
                            'rgba(255, 99, 132, 0.2)'
                        ],
                        borderWidth: 1
                    }]
                },
                options: {
                    responsive: true,
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
                                minRotation: 45,
                                maxRotation: 45,
                                callback: function (value) {
                                    return value + ' km';
                                }
                            }
                        }],
                        yAxes: [{
                            display: true,
                            scaleLabel: {
                                display: true,
                                labelString: _label[0],
                                fontStyle: "bold"
                            }
                        }]
                    },
                    tooltips: {
                        callbacks: {
                            label: function (tooltipItem, data) {
                                return tooltipItem.xLabel + ' km';
                            }
                        }
                    }
                }
            });
        },
    });
});
