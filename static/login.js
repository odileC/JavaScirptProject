$(function () {
    $(document).ready(function () { 
        $(".welcome").fadeIn();
        $(".nhsNumber").fadeIn(3000);
        $(".nhsInput").fadeIn(3000);
        $(".submit").fadeIn(3000);
        $(".nhsInput").keyup(function () {

            var strongRegex = /\d{10}$/;
            if ($(this).val().length > 10) {
                $('#notification').text('The NHS number should be a 10-digit number');
                $('#showResult').removeClass('.glyphicon glyphicon-ok-sign justify2');
            }
            else if (strongRegex.test($(this).val())) {
                $('#showResult').removeClass('.glyphicon glyphicon-ok-sign justify');
                $('#showResult').addClass('.glyphicon glyphicon-ok-sign justify2');
                $('#notification').text('');

            }
            else {

                $('#notification').text('The NHS number should be a 10-digit number');

            }

        });

    });

    $('.centerContent .submit').on('click', function () {
        Loading();;
    });
    function Loading() {
        $('#originPage').css({ 'display': 'none' });
        　 $('#overlay').css({ 'display': 'block' });
        }
});


