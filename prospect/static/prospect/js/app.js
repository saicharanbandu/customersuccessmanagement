$(document).ready(function () {
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