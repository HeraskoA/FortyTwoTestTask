$(document).ready(function(){
    function submit() {
        $('form').ajaxForm(function() {
                $('.form-control').val('');
            })
    }

    function update() {
        $.ajax({
            'type': 'get',
            'data': {   
                'count': count
            },
            'success': function(data, status, xhr) {
                if (data != []) {
                    var dialogWindow = $('.message')
                    $.each(data, function() {
                        count++;
                        dialogWindow.append('<p><address>' +
                                            this.sender +'</address><span>' +
                                            this.text + '</span><div id="date">' + 
                                            this.time + '</div>');
                        scroll();
                    });
                }
            }
        });
    }

    function scroll() {
        var div = $("#chat-messages");
        div.scrollTop(div.prop('scrollHeight'));
    }
    scroll();
    setInterval(update, 1000);
    submit();
});
