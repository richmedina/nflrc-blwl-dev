// lesson.js
jQuery(function($) {

	var $container = $('#content_display');

	$container.isotope({
		itemSelector: '.item',
		layoutMode: 'fitRows'
	});

	$('#content_filters').on( 'click', 'button', function() {
		var filterValue = $(this).attr('data-filter');
		$container.isotope({ filter: filterValue });
	});


	$(document).ready(function() {

	});

});