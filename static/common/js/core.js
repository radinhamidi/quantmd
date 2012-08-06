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
		height: 160,
		width: 350,
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
function confirmBooking(id1,id2) {

	$("#timeslot-confirm").dialog({
		resizable: false,
		height: 160,
		width: 350,
		modal: true,
		buttons: {
			"Confirm": function() {
				//Confirm Logout
				//Process Booking
				$("#inner-right").load('/referring/makeAppointment/'+id1+'/'+id2+'/');
				$(this).dialog("close");
			},
			Cancel: function() {
				$(this).dialog("close");
			}
		}
	});
}

function confirmBookingForReschedule(id1,id2,id3) {

	$("#timeslot-confirm").dialog({
		resizable: false,
		height: 160,
		width: 350,
		modal: true,
		buttons: {
			"Confirm": function() {
				//Confirm Logout
				//Process Booking
				$("#inner-right").load('/referring/remakeAppointment/'+id1+'/'+id2+'/'+id3+'/');
				$(this).dialog("close");
			},
			Cancel: function() {
				$(this).dialog("close");
			}
		}
	});
}

function confirmBookingForReschedule2(id1,id2) {

	$("#timeslot-confirm").dialog({
		resizable: false,
		height: 160,
		width: 350,
		modal: true,
		buttons: {
			"Confirm": function() {
				//Confirm Logout
				//Process Booking
				$("#inner-right").load('/receptionist/rescheduleAction2/'+id1+'/'+id2+'/');
				$(this).dialog("close");
			},
			Cancel: function() {
				$(this).dialog("close");
			}
		}
	});
}