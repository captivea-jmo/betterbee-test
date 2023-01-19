$(document).ready(function () {
    $(".download_btn").click(function (e) {
        var $btn = $(".sure_btn");
        $btn.hide();

        var $el = $(e.target).parents("tr").find("#category_id").attr("value");
        var category_id = parseInt($el);
        $.ajax({
            url: "/create-request-download",
            data: {
                category_id: category_id,
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $(".alert_message").modal("show");
                if (datas.error) {
                    $(".alert_text").html(datas.error);
                } else if (datas.success_msg) {
                    $(".alert_text").html(datas.success_msg);
                }
            },
        });
    });

    $(".delete_btn").click(function (e) {
        var $btn = $(".sure_btn");
        var $el = $(e.target).parents("tr").find("#category_id").attr("value");
        var category_id = parseInt($el);
        $("#popup_cat_id").val(category_id);
        $.ajax({
            url: "/create-request-delete",
            data: {
                category_id: category_id,
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $(".alert_message").modal("show");
                if (datas.msg) {
                    $(".alert_text").html(datas.msg);
                }

                if (!datas.hide_i_am_sure_btn) {
                    $btn.show();
                } else {
                    $btn.hide();
                }
            },
        });
    });

    $(".sure_btn").click(function (e) {
        var $btn = $(e.currentTarget);
        $.ajax({
            url: "/create-request-delete",
            data: {
                category_id: $("#popup_cat_id").val(),
                do_delete: 1,
            },
            type: "post",
            cache: false,
            success: function (result) {
                var datas = JSON.parse(result);
                $(".alert_message").modal("show");
                if (datas.msg) {
                    $(".alert_text").html(datas.msg);
                }

                if (datas.hide_i_am_sure_btn) {
                    $btn.hide();
                } else {
                    console.log("kishan show button");
                    $btn.show();
                }
            },
        });
    });
    $("#view_btn").click(function (e) {
        $(".alert_message").modal("hide");
        window.open("/my/gdpr_request");
    });
});
