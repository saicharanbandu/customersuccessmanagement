$(document).ready(function () {
    $(".prospect-action").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function(data) {
            $("#updateModal .modal-content").html(data);
        });
    });

    $(".status-action").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function(data) {
            $("#updateModal .modal-content").html(data);
            $("#id_status").on("change", function() {
                let url = `${$(this).closest("form").attr("data-url")}?status=${$(this).val()}`;
                $.get(url, function(data) {
                    $("#updateModal .modal-content #statusOptions").html(data);
                });
            });
        });
    });

    
});