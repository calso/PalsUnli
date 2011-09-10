/* Author: Emanuel Calso
 * 
 */

$(document).ready(function () {
	$('a.ui-state-default').hover(
		function(){ 
			$(this).addClass("ui-state-hover"); 
		},
		function(){ 
			$(this).removeClass("ui-state-hover"); 
		}
	);
	$('#clear-all-messages a').click(function () {
		$('#messages').fadeOut();
		return false;
	});
	$('li.message a').click(function () {
		var parent_li = $(this).parent();
		var parent_ul = parent_li.parent();
		parent_li.fadeOut();
		var siblings_li = parent_li.siblings('li');
		if (siblings_li.length == 0) {
			$('#messages').fadeOut();
		}
		return false;
	});
});

