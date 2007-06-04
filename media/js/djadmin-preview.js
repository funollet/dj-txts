// Don't forget loading jquery.js and form.js (jQuery Form plugin).
function show_preview () {
    var form_fields = $("form #txt_form").formToArray();
    $.post("/preview/", form_fields, function(xml) {
        $("#preview-content").html(xml) ;
        $("#preview").show() ;
    });
    
    return(false) ;
}

function hide_preview () {
    $("#preview").hide();
    return (false);
}

$(document).ready( function () {
    $("a #button-preview").toggle(show_preview, hide_preview) ;
});
