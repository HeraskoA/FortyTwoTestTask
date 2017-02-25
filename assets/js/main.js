var in_current_window = false;
var new_requests = 0

var Modul1 = (function() {
	return {
		del_elem: 	function del_elem(number) {
						if ($('.request').length >= 10) {
							$('.request')[number].remove();
						}
					},
		title:	function title(count_of_requests) {
					if (!in_current_window && count_of_requests != 0) {
    					new_requests = new_requests + count_of_requests;
						localStorage.RefreshTitle = false;
    					$('title').text(new_requests + ' Requests');
					}
				}
	}
})();

function update() {
    $.ajax({
        'dataType': 'json',
        'type': 'get',
        'data': {'temp': count},
        'success': function(data, status, xhr) {
            if (data != "[]") {
                data = JSON.parse(data);
                Modul1.title(data.length);
				count = count + data.length;
				data.reverse();
                $.each(data, function() {
                    Modul1.del_elem(0);
                    $('tbody').append("<tr class='request'><td>" +
					this.fields.path + "</td><td>" +
					this.fields.method + "</td><td>" +
 					this.fields.time + "</td></tr>");
                });
            }}
    });
	if (localStorage.RefreshTitle == 'true') {
		new_requests = 0;
        $('title').text("Requests");
	};
}

$(document).ready(function(){
	setTimeout(function() {localStorage.RefreshTitle = true;}, 1000);
    setInterval('update()', 1000);
    $(window).focus(function() {
        in_current_window = true;
        new_requests = 0;
        $('title').text("Requests");
		localStorage.RefreshTitle = true;
    });
    $(window).blur(function() {
        in_current_window = false;
	});
})
