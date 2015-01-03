// discussions.js
jQuery(function($) {

	var $container = $('#thread_display');

	$container.isotope({
		itemSelector: '.thread_content',
		layoutMode: 'vertical',
		filter: $('#thread_display').attr('data-selected'),
	});

	$('#thread_filters').on( 'click', '.button', function() {
		var filterValue = $(this).attr('data-filter');
		$container.isotope({ filter: filterValue });
	});

	
    $( ".postform" ).submit(function( event ) {
        event.preventDefault();
        var reply_thread = $(this).attr('data-reply_target');
        console.log($("#"+event.target.id).serializeArray());
        $.ajax({
            url : $(this).attr('action'),
            type : "POST",
            data : $("#"+event.target.id).serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {
            	var hdr = '<div class="well" style="margin-left: 30px"><dt>' + json.subject + ' <small> ' + json.creator + '</small><small style="float: right"> ' + json.modified + '</small></dt>';
				var body = '<dd>' + json.text + '</dd></div>';
				var msg = hdr + ' ' + body;

                // $('#posts').append(msg);
                $("#"+reply_thread).prepend(msg);
                $("#"+event.target.id).trigger("reset");
            },

            // handle a non-successful response
            error : function(xhr, errmsg, err) {
                console.log(xhr.status + ": " + errmsg ); // provide a bit more info about the error to the console
            }
        });
    });


	$(document).ready(function() {

	});

});