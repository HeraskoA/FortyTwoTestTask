$(document).ready(function(){
    var in_current_window = false;
    var new_requests = 0

    function form(){
        $('form').ajaxForm({
            'success': function(data, status, xhr, form) {
                var id = form.find("button[name='req_id']").val();
                var new_priority = form.find("input[name='priority']").val();
                $("div[id="+ id +"]").html(new_priority);
                if (sort != null) {
                    var request = $("div[id="+ id +"]").parent().parent();
                    paste_request(request);
                }
                if (data == '1'){
                    $('#alert').find('div').text('Saved');
                }else{
                    $('#alert').find('div').text('Enter a valid priority');
                }
                $('#alert').show();
                setTimeout(function(){$('#alert').hide()}, 3000);
            }
        });
    }

    function del_elem(index) {
        if ($('.request').length >= 10) {
            $('.request')[index].remove();
        };
    }

    function paste_request(request) {
        var index = 0;
        fixed_priority = parseInt(request.find("input[name='priority']").val());
        while (1) {
            current_priority = parseInt($('.request').eq(index).find("input[name='priority']").val());
            if (sort == 0) {
                if (fixed_priority < current_priority) {
                    $('.request').eq(index).before(request);
                    break;
                };
            }else{
                if (fixed_priority > current_priority) {
                    $('.request').eq(index).before(request);
                    break;
                }
            };
                if (fixed_priority == current_priority) {
                    if (index == ($('.request').length - 1)) {
                        $('tbody').append(request);
                        break;
                    } else {
                        index++;
                        continue;
                    };
                };
            index++;
        };
    }

    function get_index_of_min_element() {
        min_id = Number.MAX_VALUE;
        index_min_elem = 0;
        for (var i = 0; i < $('.request').length; i++) {
            if ($('button[name="req_id"]').eq(i).val() < min_id) {
                min_id = $('button[name="req_id"]').eq(i).val();
                index_min_elem = i;
            };
        };
        return index_min_elem;
    }

    function get_request(data){
        var request = document.createElement('tr');
        request.setAttribute('class', "request");
        $(request).html("<td>" +
                data.fields.path + "</td><td>" +
                data.fields.method + "</td><td>" +
                data.fields.time + "</td><td>" +
                "<div class='priority' id="+ data.pk +">"+ data.fields.priority+"</div>"+
                "&nbsp;<form id='priority_form' action='/requests/' method='post'>" + 
                token + "<input id='id_priority' min='1' name='priority' type='number' value="+
                data.fields.priority +" />&nbsp;<button type='submit' name='req_id' value=" + 
                data.pk + " class='btn" + " btn-default'>Submit</button></form></td>")
        return $(request)
    }

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
            new_requests = 0;
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
            'data': {'frontend_requests': count},
            'success': function(data, status, xhr) {
                if (data != "[]") {
                    data = JSON.parse(data);
                    title(data.length);
                    count = count + data.length;
                    data.reverse();
                    $.each(data, function() {
                        del_elem(get_index_of_min_element());
                        if (sort == null) {
                            $('tbody').append(get_request(this));
                        }else{
                            paste_request(get_request(this));
                        }
                        form();
                    });
                }}
            })
        }, 1000);
    form();
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