// lesson.js
jQuery(function($) {

	var $container = $('#content_display');

	$container.isotope({
		itemSelector: '.item',
		layoutMode: 'fitRows',
		filter: '.item_topic',
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


	$(document).ready(function() {

	});

});