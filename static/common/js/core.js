var mouse_is_inside = false;

$(document).ready(function() {
		
	$("#user-box").click(function() {
		$('#user-box-options').fadeToggle("fast");
	});
	
	//User Options Box - Controller
	$('#user-box').hover(function(){ 
        mouse_is_inside=true; 
    }, function(){ 
        mouse_is_inside=false; 
    });

    $("*").mouseup(function(){ 
        if(!mouse_is_inside) $('#user-box-options').fadeOut("fast");
    });
	$('.ui-tabs-panel').jScrollPane();
});
//Logout Confirmation Dialog
function logout(e) {
	$("#logout-confirm").dialog({
		resizable: false,
		height: 145,
		width: 250,
		modal: true,
		buttons: {
			"Logout": function() {
				//Confirm Logout
				window.location="/logout/";
				$(this).dialog("close")
			},
			Cancel: function() {
				$(this).dialog("close");
			}
		}
	});
}
function changepass() {
	$("#change-password").fadeIn(100);
	$("#change-password").load('/changePasswordView/');
	$("#change-password-modal").fadeIn(100);
}
function closeChangepass() {
	$("#change-password-modal").fadeOut(100);
	$("#change-password").fadeOut(100);
}
function confirmBooking() {

	$("#timeslot-confirm").dialog({
		resizable: false,
		height: 160,
		width: 350,
		modal: true,
		buttons: {
			"Confirm": function() {
				//Confirm Logout
				//Process Booking
				$("#inner-right").load('case-create-scans.htm')
				$(this).dialog("close");
			},
			Cancel: function() {
				$(this).dialog("close");
			}
		}
	});
}