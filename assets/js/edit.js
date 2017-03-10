$(document).ready(function(){

    function scroll() {
        $('html, body').animate({scrollTop: 0},500);
        return false;
    }

    function display_errors(errors){
        $('.error').remove();
        for (var k in errors) {
            $('form').find('input[name=' + k + ']').attr("class", "form-control has-error");
            $('form').find('input[name=' + k + ']').after('<div color="red" style="float: right;" class="error" id=' + k + '><font color="red">' + errors[k] + '</font></div>');
        }
    }

    function form(){
        $('form').ajaxForm({
            'beforeSend': function(xhr, settings){
                $('#indicator').show();
                $('.btn-primary').addClass('hidden');
                $('.btn-default').addClass('hidden');
                $("input").attr("disabled", "disabled");
                $("textarea").attr("disabled", "disabled");
                },
            'error': function() {alert('error');},
            'success': function(data, status, xhr) {
                    $('#indicator').hide();
                    $("input").removeAttr("disabled");
                    $("textarea").removeAttr("disabled");
                    $('.btn-primary').removeClass('hidden');
                    $('.btn-default').removeClass('hidden');
                    if (data != 1) {
                        $('#saved').hide();
                        display_errors(data);
                        scroll();
                    }else{
                        $('.error').remove();
                        $('.form-control').removeClass('has-error');
                        $('#saved').show();
                    }
            }
        });
    }

    function ImagePreview(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function (e) {
                $('img').css('max-width', 200);
                $('img').css('max-height', 200);
                $('img').attr('src', e.target.result);
            };
            reader.readAsDataURL(input.files[0]);
        }
    }
    form();
    $('input').keyup(function(){
        $(this).removeClass('has-error');
    });
    $("#id_photo").change(function(){
        ImagePreview(this);
    });
})
