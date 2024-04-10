
$(document).ready(function () {
    $(".customer-action").on("click", function () {
        let url = $(this).attr("data-url");
        $.get(url, function (data) {
            $("#updateModal .modal-content").html(data);
        });
    });

    $(".view-action").on('click', function () {
        let url = $(this).attr("data-url");
        $.get(url, function (data) {
            $("#viewModal .modal-content").html(data);
        });
    });


    select_plan_handler();

    $("#id_is_yearly").on("change", function () {
        let url = $(this).closest("form").attr("data-url");
        let plan_url = $(this).closest("form").attr("plan-url");
        let is_yearly = $('#id_is_yearly').is(':checked');
        let plan_id = $('input[type=radio][name=plan]:checked').val();

        let params = {
            "plan_id": plan_id,
            "is_yearly": is_yearly
        }
        if (plan_id) {
            load_plan_amount(url, params);
        }
        $.get(plan_url, params, function (data) {
            $("#planOptions").html(data);
            select_plan_handler();
        });
    });

    $("#applyDiscount").on("click", function () {
        calculate_total();
    });
});


const calculate_total = () => {
    let subtotalAmount = $("#subtotalAmount").html().replace('₹', '').replace(',', '');
    let discount = $("#id_discount").val() ? $("#id_discount").val(): 0;

    $("#discountAmount").html(`- ₹${discount}`);
    let totalAmount = new Intl.NumberFormat('en-IN').format(parseInt(subtotalAmount) - parseInt(discount));
    $("#totalAmount").html(`₹${totalAmount}`);
    
    
}
const select_plan_handler = () => {
    $("input[type=radio][name=plan]").on("change", function () {
        let url = $(this).closest("form").attr("data-url");
        let is_yearly = $('#id_is_yearly').is(':checked');
        let plan_id = $('input[type=radio][name=plan]:checked').val();

        let params = {
            "plan_id": plan_id,
            "is_yearly": is_yearly
        }

        if (plan_id) {
            load_plan_amount(url, params);
            $("#paymentInfo").removeClass('d-none')
        }
    });
}


const load_plan_amount = (url, params) => {
    $.get(url, params, function (data) {
        $("#subtotalAmount").html(`₹${data.payable_amount}`);
        calculate_total();
    });
}
