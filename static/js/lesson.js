// lesson.js
jQuery(function($) {

	var $container = $('#content_display');

	$container.isotope({
		itemSelector: '.item',
		layoutMode: 'fitRows',
		filter: $('#content_filters').attr('data-default'),
	});

	$('#content_filters').on( 'click', '.button', function() {
		var filterValue = $(this).attr('data-filter');
		$container.isotope({ filter: filterValue });
	});

	var $quiz_container = $('#content_display_quiz');

	$quiz_container.isotope({
		itemSelector: '.item',
		layoutMode: 'fitRows',
		filter: '.item_quiz',
	});

	$('#content_filters').on( 'click', '.button', function() {
		var filterValue = $(this).attr('data-filter');
		$quiz_container.isotope({ filter: filterValue });
	});


    $( ".postform" ).submit(function( event ) {
        event.preventDefault();
        console.log($(this).attr('data-reply_target'));
        var reply_thread = $(this).attr('data-reply_target')
        $.ajax({
            url : "/discussions/post/add/",
            type : "POST",
            data : $("#"+event.target.id).serializeArray(),
            dataType : "json",

            // handle a successful response
            success : function(json) {
				var hdr = '<dt><h4>' + json.subject + '</h4><small>' + json.creator + '</small><small style="float: right"> ' + json.modified + '</small></dt>';
				var body = '<dd>' + json.text + '</dd>';
				var msg = hdr + ' ' + body;

                // $('#posts').append(msg);
                $("#"+reply_thread).append(msg);               
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