$(document).ready(function(){
    var pubnub = new PubNub({ publishKey : 'pub-c-154a7313-6d0a-4b45-bc9a-4464eb536bc8', subscribeKey : 'sub-c-49c47702-067f-11e7-b34d-02ee2ddab7fe' });

    pubnub.addListener({
          message: function(obj) {
            update();
          }});
    pubnub.subscribe({channels:[channel]});


    function submit() {
        $('form').ajaxForm(function() {
                $('.form-control').val('');
                pubnub.publish({channel: channel, message : 1});
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
    //setInterval(update, 1000);
    submit();
});
