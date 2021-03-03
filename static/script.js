$(document).ready(function() {
    $('input[type="radio"]').click(function() {
        $('#dailyDates').show();
        if($(this).attr('id') == 'daily') {
            $('#dailyDates').show();
        }
        else {
            $('#dailyDates').hide();
        }
    });
});