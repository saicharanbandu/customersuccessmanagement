let tooltipTriggerList = [].slice.call(document.querySelectorAll("[data-bs-toggle='tooltip']"))
let tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
})

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
