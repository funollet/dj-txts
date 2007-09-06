// Requires jquery.js

function append_to_preview (xml) {
    $("#preview-content").append(xml)
    return false
}

function show_preview () {
    var abstract_markup = $("[@name=abstract_markup]").val()
    var body_markup = $("[@name=body_markup]").val()
    
    $("#preview-content").html('')
    $("#preview").show("slow")
    
    if (abstract_markup.length != 0) {
        $.post("/preview/", {"markup": '``------abstract--------------``'}, append_to_preview)
        $.post("/preview/", {"markup": abstract_markup}, append_to_preview)
        $.post("/preview/", {"markup": '``------end of abstract-------``'}, append_to_preview)
    }
    $.post("/preview/", {"markup": body_markup}, append_to_preview)
    return false
}

function hide_preview () {
    $("#preview").hide("slow")
    return false
}

$(document).ready( function(){
    $("a#button-preview").toggle(show_preview, hide_preview)
})
