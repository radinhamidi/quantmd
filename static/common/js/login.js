$(document).ready(function() {

	$("#loginbutton").button();
	
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

	$('#password-clear').show();
	$('#password-password').hide();

	$('#password-clear').focus(function() {
		$('#password-clear').hide();
		$('#password-password').show();
		$('#password-password').focus();
	});
	$('#password-password').blur(function() {
		if($('#password-password').val() == '') {
			$('#password-clear').show();
			$('#password-password').hide();
		}
	});
	
	$("#loginbutton").click(function(e) {
		e.preventDefault();
        $("#loginbox").fadeOut('fast', function() {
			$("#login").submit();
		});
    });
    
});

