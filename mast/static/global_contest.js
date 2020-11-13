/* globals Chart:false, feather:false */
jQuery(document).ready(function () {

    function getCheckPoint(value) {
        // check if the property/key is defined in the object itself, not in parent'
        if (_checkpoints.hasOwnProperty(value)) {
            return _checkpoints[value] + ' - '
        } else {
            return '';
        }
    }


    let _data;
    let _labels;
    let _checkpoints;
    let csrftoken = $('meta[name=csrf-token]').attr('content')

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
                                suggestedMin: 0,
                                suggestedMax: 500,
                                callback: function (value, index, values) {
                                    return getCheckPoint(value) + value;
                                }
                            }
                        }],
                        yAxes: []
                    }
                }
            });
        },
    });
});
