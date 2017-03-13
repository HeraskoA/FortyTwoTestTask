var in_current_window = false;
var new_requests = 0

$(document).ready(function(){

    function title(count_of_requests) {
        if (!in_current_window && count_of_requests != 0) {
            new_requests = new_requests + count_of_requests;
            localStorage.UnreadRequests = new_requests;
            $('title').text('(' + new_requests + ')' + ' Requests');
        }
    }

    function set_current_window() {
            in_current_window = true;
            localStorage.UnreadRequests = 0;
            $('title').text("Requests");
    }

    function read_localstorage(){
        if (localStorage.UnreadRequests == undefined) {
            localStorage.UnreadRequests = 0;
        };
        title(parseInt(localStorage.UnreadRequests)+1);
    }

    read_localstorage();
    window.addEventListener('storage', function(event) {
         if (localStorage.UnreadRequests == '0') {
            new_requests = 0;
            $('title').text("Requests");
        }
    });
    setInterval(function update() {
        $.ajax({
            'dataType': 'json',
            'type': 'get',
            'data': {'temp': count},
            'success': function(data, status, xhr) {
                if (data != "[]") {
                    data = JSON.parse(data);
                    title(data.length);
                    count = count + data.length;
                    data.reverse();
                    $.each(data, function() {
                        if ($('.request').length >= 10) {
                            $('.request')[number].remove();
                        };
                        $('tbody').append("<tr class='request'><td>" +
                        this.fields.path + "</td><td>" +
                        this.fields.method + "</td><td>" +
                        this.fields.time + "</td></tr>");
                    });
                }}
            })
        }, 1000);
    $(window).focus(function() {
        set_current_window();
    });
    $(window).mousemove(function(){
        set_current_window();
    });
    $(window).blur(function() {
        in_current_window = false;
    })
})