$(document).ready(function() {
    $('.dailyDates').show();
    $('input[type="radio"]').click(function() {
      if($(this).attr('value') == 'daily') {
          $('.dailyDates').show();
      }
      else {
          $('.dailyDates').hide();
      }
    });
  });

  var mychart = document.getElementById("chart_{{month}}{{day}}").getContext("2d");
    var LineChartDemo = new Chart(mychart, {
        type: 'line',
        data: dailyChartData,
        options: {
            responsive: false,
            scales: {
                xAxes: [{
                    scaleLabel: {
                        display: true,
                        labelString: 'Time'
                    }
                }],
            }
        }
    });