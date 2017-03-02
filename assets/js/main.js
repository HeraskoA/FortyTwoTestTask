var in_current_window = false;
var new_requests = 0

function del_elem(index) {
    if ($('.request').length >= 10) {
        $('.request')[index].remove();
    };
}

function paste_request(row) {
    var i = 0;
    const_priority =  row.find("input[name='priority']").val();
        while (1) {
            current_priority = $('.request').eq(i).find("input[name='priority']").val();
            if (sort==0) {
                if (const_priority < current_priority) {
                    $('.request').eq(i).before(row);
                    break;
                };
            }else{
                if (const_priority > current_priority) {
                    $('.request').eq(i).before(row);
                    break;
                }
            };
                if (const_priority == current_priority) {
                    if (i == ($('.request').length - 1)) {
                        $('tbody').append(row);
                        break;
                    } else {
                        i++;
                        continue;
                    };
                };
                i++;
        };
}

function get_index_of_min_element() {
    min_id = Number.MAX_VALUE;
    index_min_elem = 0;
    for (var i = 0; i < 10; i++) {
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
                        data.fields.priority + "<form id='priority_form' action='/requests/' method='post'>" + 
                        token + "<input id='id_priority' min='0' name='priority' type='number' value="+
                        data.fields.priority +" /><button type='submit' name='req_id' value=" + 
                        data.pk + " class='btn'>Submit</button></form></td>")
    return $(request)
}

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
                        del_elem(get_index_of_min_element());
                        if (sort != false) {
                            paste_request(get_request(this));
                        } else{
                            $('tbody').append(get_request(this));
                        } 
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