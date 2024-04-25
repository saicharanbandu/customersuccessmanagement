
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
        $("#subtotalAmount").closest(".amount-group").find("label").html(`${data.tariff_selected}`);
        $('#selectedPlanAmount').html(`₹ ${data.monthly_amount}`);
        $("#subtotalAmount").html(`₹ ${data.payable_amount}`);
        if (data.tariff_selected.toUpperCase().indexOf('MONTHLY') !== -1) {
            $('#selectedPlanAmount').closest(".amount-group").addClass('d-none');
        } else {
            $('#selectedPlanAmount').closest(".amount-group").removeClass('d-none');
        }
        calculate_total();
    });
}

// set value to hidden field when payment status changes on the form
// swap btn to modal trigger when payment status is not checked
const checkPaymentStatus = () => {
    if (!$('#paymentStatus').is(':checked')) {
        $('#btnSubmit').addClass('d-none')
        $('#btnModal').removeClass('d-none')
        $('input[name="payment_status"]').val('paid')
    } else {
        $('#btnSubmit').removeClass('d-none')
        $('#btnModal').addClass('d-none')
        $('input[name="payment_status"]').val('pending')
    }
}
$('#paymentStatus').on('click', function () {
    checkPaymentStatus();
})
checkPaymentStatus();

// set value to hidden field when payment mode changes on the form
const setPaymentMode = (element) => {
    if ($(element).is(':checked')) {
        $('input[name="payment_mode"]').val($(element).val())
    } 
}
$('.set-payment-mode').on('click', function () {
    setPaymentMode($(this));
})
setPaymentMode();

// submit actual form on submit from modal
$('#proxySubmit').on("click", function () {
    $('#btnSubmit').click()
})