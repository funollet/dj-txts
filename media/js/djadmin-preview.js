function get_form_fields () {
    var form_fields = $("form #txt_form").formToArray();
    $.post("/txt-preview/", form_fields, function(xml) {
        $("#preview").html(xml) ;
    });
//    $("#preview").html('<em>patam!</em>');
}

$(document).ready( function () {
    $("a #button-preview").click(get_form_fields) ;
});
