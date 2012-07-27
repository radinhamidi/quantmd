$(document).ready(function() {

	//Call All Buttons to Buttons
	$(".button").button();

	//Master Show Pane Command
	$(".showbutton").click(function() {
		var showId = $(this).attr("show");
		var loadId = $(this).attr("load");
		var forceReload = $(this).attr("force");
		
		$("*").css("cursor", "progress")
		
		//Perform CSS Focus z-Index
		var largestZ = 1;
		$(".windows").each(function(i) { 
			var currentZ = parseFloat($(this).css("zIndex")); 
			largestZ = currentZ > largestZ ? currentZ : largestZ; 
		}); 
		$("#"+showId).css("z-index", largestZ + 1); 	
				
		// Check Force Reload Condition
		if(forceReload && forceReload === "no") {
			if($("#"+showId+"-content").is(':empty')) {
				if(loadId && loadId !== "none") {
					$("#"+showId+"-content").load(loadId, function() {
						$("*").css("cursor", "")
					});
				} else {
					//Showing Empty DIV
					alert('showing empty');
				}
			} else {
				//Stop - Do not reload
			}
		} else {
			// Always Force Reload
			if(loadId && loadId !== "none") {
				$("#"+showId+"-content").load(loadId, function() {
					$("*").css("cursor", "")
				});
			}
		}
		
		//Check DIV Already Displayed / Display DIV
		if( !$("#"+showId).is(':visible') ) {
			$("#"+showId).fadeIn('fast');
		}
		
	});
	
	//Master Pane Redirect Command
	$(".panebutton").click(function() {
		$("*").css("cursor", "progress")
		$(this).parents(".content").fadeOut('fast');
		var loadId = $(this).attr("load");
		if(loadId && loadId !== "none") {
			$(this).parents(".content").load(loadId, function() {
				$(this).parents(".content").fadeIn('fast');
				$("*").css("cursor", "")
			});
		}
	});
	
	//Master Pane Focus Command
	$(".windows").click(function() {
		var focusId = $(this).attr("id");
		var largestZ = 1;
		$(".windows").each(function(i) { 
			var currentZ = parseFloat($(this).css("zIndex")); 
			largestZ = currentZ > largestZ ? currentZ : largestZ; 
		}); 
		$("#"+focusId).css("z-index", largestZ + 1);	
	});
	
	//Master Hide Pane Command
	$(".hidebutton").click(function() {
		$(this).parent(".windows").fadeOut('fast');
	});
	
	//Master Hide Pane w/Designate Command
	$(".hidetrigger").click(function() {
		var hideId = $(this).attr("hide");
		$("#"+hideId).fadeOut('fast');
	});
	
	//User Options Box - Controller
	$("#user-box").click(function() {
		$('#user-box-options').fadeToggle("fast");
	});
	
});

//***********************
// Draggable Controllers
//***********************

$(function() {
	$(".windows").draggable({ stack: ".windows", containment: "#drag-container" });
});

//************************
// Special Function Calls
//************************

//Shows a full screen Modal
function showModal(divName) {
	$(divName).fadeIn('fast');
}

//Hides full screen modal
function hideModal(divName) {
	$(divName).fadeOut('fast');
}

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
