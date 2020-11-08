/* globals Chart:false, feather:false */
jQuery(document).ready(function () {

    function getCheckPoint(value) {
        
    }

    let _data;
    let _labels;
    let _checkpoints;

    $.ajax({
        url: "/get_global_contest",
        type: "GET",
        data: {vals: ''},
        success: function (response) {
            full_data = JSON.parse(response.payload);
            _data = full_data['data'];
            _labels = full_data['labels'];
            _checkpoints = full_data['checkpoints'];

            var myChart_foot = new Chart(document.getElementById('myChart').getContext('2d'), {
                type: 'horizontalBar',
                data: {
                    labels: _labels,
                    datasets: [{
                        label: 'Distance in Km',
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
                    scales: {
                        xAxes: [{
                            ticks: {
                                beginAtZero: true,
                                 callback: function (value, index, values) {
                                    return '$' + value;
                                }
                            }
                        }],
                        yAxes: [
                        ]
                    }
                }
            });
        },
    });
});