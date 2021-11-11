$(document).ready(function () {

    $("#analyze-btn").click(function (event) {  //analiza gramatyki
        var grm;
        grm = $('#solution-area').val();
        $.get('/gramatyk/check_gramma/', {gramma: grm}, function (data) {
            $('#analyze-area').val('');
            $('#analyze-area').val(data);
            if (data.contains("BŁĄD! ")) {
                $('#analyze-area').css({'color': 'red'});
                $('#chomsky-btn').attr('disabled', true);
                $('#greibach-btn').attr('disabled', true);
                $('#regular-btn').attr('disabled', true);
            }
            else {
                $('#analyze-area').css('color', '#F0C674');
                $('#chomsky-btn').attr('disabled', false);
                $('#greibach-btn').attr('disabled', false);
                $('#regular-btn').attr('disabled', false);
            }
        });
    });

    $("#analyze-area").click(function(event){  //selekt po kliknieciu
       // $('#analyze-area').select()
    });

    $('#likes').click(function () {  //lajki
        var solid;
        solid = $(this).attr("data-solid");
        $.get('/gramatyk/like_solution/', {solution_id: solid}, function (data) {
            $('#like_count').html(data);
            $('#likes').hide();
        });
    });

    $('#save-btn').attr('disabled', true);  //enable/disable buttonów
    $('#analyze-btn').attr('disabled', true);
    $('#chomsky-btn').attr('disabled', true);
    $('#greibach-btn').attr('disabled', true);
    $('#regular-btn').attr('disabled', true);
    $('#solution-area').on('input',function () {
        if ($(this).val().length != 0) {
            $('#save-btn').attr('disabled', false);
            $('#analyze-btn').attr('disabled', false);
        }
        else {
            $('#save-btn').attr('disabled', true);
            $('#analyze-btn').attr('disabled', true);
            $('#chomsky-btn').attr('disabled', true);
            $('#greibach-btn').attr('disabled', true);
            $('#regular-btn').attr('disabled', true);
        }
    });

    var a = $(document).height()-125;
    var b = $(document).height()-225;

    $(window).resize(function () {  //resize okna
        var bodyheight = $(document).height();
        $("#analyze-area").height(bodyheight-125);
        $("#solution-area").height(bodyheight-225);
    }).resize();


    /* taka szukajka jakby
     $('#suggestion').keyup(function () {
     var query;
     query = $(this).val();
     $.get('/gramatyk/suggest_solution/', {suggestion: query}, function (data) {
     $('#sols').html(data);
     });
     });
     */

});
