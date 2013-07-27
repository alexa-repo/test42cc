$(function(){
    $('#form_id').submit(function(){
        $(this).ajaxSubmit({
            beforeSend: function(){
                $('#progress').show();
                $('input:submit').attr("disabled","disabled");
            },
            success : function(responce) {
                $("#progress").hide();
                $('input:submit').removeAttr("disabled");
                data = $.parseJSON(responce);
                if (data['status'] == 1){
                    err = data['errors'];
                    $.each(err, function(name, error) {
                        $("#errors_list").append(name + ": " + error);
                    });
                                       }
                else{
                    window.location.href = data['redirect'];
                }
            }
        });
    return false;
    });
});

