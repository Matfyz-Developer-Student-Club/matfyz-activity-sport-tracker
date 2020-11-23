/* globals Chart:false, feather:false */


jQuery(document).ready(function () {
    let _personal_data;
    let _labels;


    $.ajax({
        url: "/get_cycling",
        type: "GET",
        data: {vals: ''},
        success: function (response) {
            full_data = JSON.parse(response.payload);
            _personal_data = full_data['personal_data'];
            _labels = full_data['labels'];
            var ctx = document.getElementById('run_competition')
            var myCanvas = new Chart(ctx, {
              type: 'line',
              data: {
                labels: _labels,
                datasets: [
                    {
                        label: 'you',
                        data: _personal_data,
                        fill: false,
                        pointRadius: 5,
                        borderColor: '#18de38',
                        pointBackgroundColor: '#18de38',
                    },
                    ]
              },
              options: {
                scales: {
                  yAxes: [{
                    ticks: {
                      beginAtZero: false
                    }
                  }]
                },
                legend: {
                  display: false
                }
              }
            });
        },
    });
});