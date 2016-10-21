/**
 * Created by Aditya on 21-10-2016.
 */

function showFlashMessage(message, type){
    var template = "<div class='container container-alert-flash'>" +
        "<div class='col-sm-3 col-sm-offset-8'>" +
        "<div class='alert alert-"+ type +" alert-dismissible' role='alert'>" +
        "<button type='button' class='close' data-dismiss='alert' aria-label='Close'>" +
        "<span aria-hidden='true'>&times;</span></button>" +
        message + "</div></div></div>";
    $("body").append(template);
    $(".container-alert-flash").fadeIn();
    setTimeout(function(){
        $(".container-alert-flash").fadeOut();
    }, 2000);
}