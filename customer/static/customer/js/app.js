
$(document).ready(function () {
    $(".customer-action").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function(data) {
            $("#updateModal .modal-content").html(data);
        });
    });

    $(".view-action").on('click', function () {
        let url = $(this).attr("data-url");
        $.ajax({
            url: url,
            success: function (data) {
                $("#viewModal .modal-content").html(data);
            }
        });
    });
});