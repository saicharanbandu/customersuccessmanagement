$(document).ready(function () {
    $(".update-remarks, .update-crm").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function(data) {
            $("#updateModal .modal-content").html(data);
        });
    });
});