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
        $.get(url, function(data) {
            $("#updateModal .modal-content").html(data);
        });
    });

    $(".view-action").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function(data) {
            $("#viewModal .modal-content").html(data);
        }).done(() =>{
            $(".prospect-action").on("click", function () {
                let url = $(this).attr("data-url");
                $.get(url, function(data) {
                    $("#updateModal .modal-content").html(data);
                });
            });
        });
    });

    
    $(".status-action").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function(data) {
            $("#updateModal .modal-content").html(data);
            $("#id_status").on("change", function() {
                let status = $(this).val();
                let url = `${$(this).closest("form").attr("data-url")}?status=${status}`;
                $.get(url, function(data) {
                    $("#updateModal .modal-content #statusOptions").html(data);
                    if(status === 'trial') {
                        $("#id_date").on("change", function() {
                            let date = $(this).val();
                            let url = `${$(this).closest("div").attr("data-url")}?date=${date}`;
                            $.get(url, function(data) {
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


$(document).ready(function() {
    pervID = null
    count = 1
    // When popover trigger is clicked
    $('.trigger-popover').click(function(event) {
        console.log('trigger me')
        let element_id = $(this).attr('data-id');
        let popoverContent = $(`[data-name="popover-content-${element_id}"]`).html();
        // Destroy old popover
        $(this).popover('dispose');
        // Initialize new popover with updated content
        $(this).popover({
            html: true,
            title: "Meeting Schedule",
            content: popoverContent
        });
        if (!$(event.target).closest('.popover').length && !$(event.target).closest('.trigger-popover').length) {
            $('.trigger-popover').popover('hide');
        }
        $(this).popover('show');
    });
    // Hide popover when clicking outside
    $(document, 'calendar-table').click(function(event) {
        if (!$(event.target).closest('.popover').length && !$(event.target).closest('.trigger-popover').length) {
            $('.trigger-popover').popover('hide');
        }
    });
});
