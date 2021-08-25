$(function () {
    $(document).ready(function (){
        $.get('/predict'
    , function(data) {
        console.l
        if (data.w1change<=0){
            $("#w1").css({ 'display': 'none'});

        }else{
            $('#w1').text(data.w1change)
            $("#w1").css({ 'display': 'block'}); 
        }           
  });
    });


});