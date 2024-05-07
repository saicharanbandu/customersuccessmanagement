$(document).ready(function () {
    $("#id_prospect-country").change(function () {
        let url = $(this).closest("form").attr("data-url");
        let countryId = $(this).val();

        $.ajax({
            url: url,
            data: {
                "country_id": countryId
            },
            success: function (data) {
                $("#id_prospect-state").html(data);
            }
        });
    });

    $(".prospect-action").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function (data) {
            $("#updateModal .modal-content").html(data);
        });
    });

    $(".view-action").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function (data) {
            $("#viewModal .modal-content").html(data);
        }).done(() => {
            $(".prospect-action").on("click", function () {
                let url = $(this).attr("data-url");
                $.get(url, function (data) {
                    $("#updateModal .modal-content").html(data);
                });
            });
        });
    });


    $(".status-action").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function (data) {
            $("#updateModal .modal-content").html(data);
            $("#id_status").on("change", function () {
                let status = $(this).val();
                let url = `${$(this).closest("form").attr("data-url")}?status=${status}`;
                $.get(url, function (data) {
                    $("#updateModal .modal-content #statusOptions").html(data);
                    if (status === 'trial') {
                        $("#id_date").on("change", function () {
                            let date = $(this).val();
                            let url = `${$(this).closest("div").attr("data-url")}?date=${date}`;
                            $.get(url, function (data) {
                                $("#trialEndDate").html(data);
                            });
                        });
                    }
                });
            });
        });
    });


});


// bootstrap popovers
const popoverTriggerList = document.querySelectorAll('[data-bs-toggle="popover"]')
const popoverList = [...popoverTriggerList].map(popoverTriggerEl => new bootstrap.Popover(popoverTriggerEl))

