let tooltipTriggerList = [].slice.call(document.querySelectorAll("[data-bs-toggle='tooltip']"))
let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

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

    $("input[type=radio][name=plan], #id_duration").change(function () {
        let url = $(this).closest("form").attr("data-url");
        let plan_id = $('input[type=radio][name=plan]:checked').val();;
        let duration = $('#id_duration').val();

        if (plan_id !=='' && duration !=='' ) {
            $.ajax({
                url: url,
                data: {
                    "plan_id": plan_id,
                    "duration": duration
    
                },
                success: function (data) {
                    $("#payableAmount").html(`Rs. ${data.payable_amount}`);
                }
            });
        }
    });

    $(".view-customer-info").on('click', function () {
        let url = $(this).attr("data-url");
        $.ajax({
            url: url,
            success: function (data) {
                $("#customerInfo .modal-content").html(data);
            }
        });
    });
});


// Show/hide the viewer/editor select box on select of module
$(".module-permission").on("change", function () {
    let module = $(this).parent().attr("data-module");

    if ($(this).is(":checked")) {
        $(`#roleFor${module}`).removeClass("d-none");
    }
    else {
        $(`#roleFor${module}`).addClass("d-none");

    }
})


/** Notification using bootstrap toast */
document.addEventListener("DOMContentLoaded", function () {
    var toastElements = document.querySelectorAll(".toast");
    var toastList = [].map.call(toastElements, function (element) {
        return new bootstrap.Toast(element, {
            autohide: true
        });
    });

    toastList.forEach(function (toast) {
        toast.show();
    });
});
