$(document).ready(function() {

	//Call All Buttons to Buttons
	$(".button").button();
	
	// Pane Redirect Command
	$(".panebutton").click(function() {
		$("*").css("cursor", "progress")
		var loadId = $(this).attr("load");
		if(loadId && loadId !== "none") {
			$(this).parents(".content").load(loadId, function() {
				$("*").css("cursor", "")
			});
		}
	});	
});
