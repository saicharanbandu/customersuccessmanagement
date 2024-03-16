var tooltipTriggerList = [].slice.call(document.querySelectorAll("[data-bs-toggle='tooltip']"))
var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

$(document).ready(function () {
    $("#id_prospect-country").change(function () {
        var url = $(this).closest("form").attr("data-url");
        var countryId = $(this).val();

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
