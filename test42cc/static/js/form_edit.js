$(function () {
    $('#form_id').submit(function () {
        $(this).ajaxSubmit({
            beforeSend: function () {
                $('#progress').html("Progress saving data...");
                $('#progress').show();
                $('input:submit').attr("disabled", "disabled");
                $('#form_id input:text').attr("disabled", "disabled");
                $('#form_id textarea').attr("disabled", "disabled");
                $('#form_id input:file').attr("disabled", "disabled");
            },
            success: function (responce) {
                $('input:submit').removeAttr("disabled");
                $('#form_id input:text').removeAttr("disabled");
                $('#form_id textarea').removeAttr("disabled");
                $('#form_id input:file').removeAttr("disabled");
                data = $.parseJSON(responce);
                if (data['status'] == 1) {
                    $("#progress").hide();
                    err = data['errors'];
                    $.each(err, function (name, error) {
                        $("#errors_list").append(name + ": " + error);
                    });
                }
                else {
                    $('#progress').html("Form data have saved");
                    $('#progress').css({color: "green"});
                    //window.location.href = data['redirect'];
                }
            }
        });
        return false;
    });
});

