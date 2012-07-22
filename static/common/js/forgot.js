$(document).ready(function() {

	$(".button").button();
	
    $('#username-clear').show();
	$('#username-username').hide();

	$('#username-clear').focus(function() {
		$('#username-clear').hide();
		$('#username-username').show();
		$('#username-username').focus();
	});
	$('#username-username').blur(function() {
		if($('#username-username').val() == '') {
			$('#username-clear').show();
			$('#username-username').hide();
		}
	}); 

	$('#email-clear').show();
	$('#email-email').hide();

	$('#email-clear').focus(function() {
		$('#email-clear').hide();
		$('#email-email').show();
		$('#email-email').focus();
	});
	$('#email-email').blur(function() {
		if($('#email-email').val() == '') {
			$('#email-clear').show();
			$('#email-email').hide();
		}
	});
	
	$("#forgotbutton").click(function(e) {
		e.preventDefault();
        $("#forgotbox").fadeOut('fast', function() {
			$("#forgot").submit();
		});
    });
    
	$("#backbutton").click(function(e) {
		$("#forgotbox").fadeOut('fast', function() {
			window.location='login.htm';
		});
    });
	
});

