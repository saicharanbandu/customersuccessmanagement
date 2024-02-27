$(document).ready(function () {
    $("#id_country").change(function () {
        var url = $("#customerForm").attr('data-url');
        var countryId = $(this).val();

        $.ajax({
            url: url,
            data: {
                'country_id': countryId
            },
            success: function (data) {
                $("#id_state").html(data);
            }
        });
    });
    $("#id_plan_type").change(function () {
        var url = $("#selectPlanForm").attr('data-plan-url');;
        var planNameId = $(this).val();
        

        $.ajax({
            url: url,
            data: {
                'plan_type_id': planNameId
            },
            success: function (data) {
                $("#id_member_size").html(data);

            }
        });
    });

    $("#id_member_size").change(function () {
        var url = $("#selectPlanForm").attr('data-amount-url');
        var plan_type_id = $('#id_plan_type').val();
        var member_size_id = $('#id_member_size').val();
        var duration = $('#id_duration').val();
        
        $.ajax({
            url: url,
            data: {
                'plan_type_id': plan_type_id, 
                'member_size_id': member_size_id,
                'duration': duration,

            },
            success: function (data) {
                $("#payableAmount").html(`Rs. ${data.payable_amount}`);

            }
        });
    });
});