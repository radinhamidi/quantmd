$(document).ready(function() {
	$("#wrapper").fadeIn(500, function() {
		$("#footer").delay(500).fadeIn(300, function() {
			$("#user-box").show("slide", { direction: "up" }, 400, function() {
				$("#container").fadeIn(400);
			});
		});
	});
	$("#container").delegate('.innerlink', 'click', function(event) {
		$('.ui-tabs-panel:not(.ui-tabs-hide)').hide();
		$('.ui-tabs-panel:not(.ui-tabs-hide)').empty();
		$("*").css("cursor", "wait");
		$('.ui-tabs-panel:not(.ui-tabs-hide)').load(this.href, function() {
			$('.ui-tabs-panel:not(.ui-tabs-hide)').delay(200).fadeIn('fast', function() {
				$("*").css("cursor", "");
			});
		});
		event.preventDefault();
		return false;
	});
	$("#container").delegate('.msgloadright', 'click', function(event) {
		$("#messages-inner-right").css('opacity','0.001');
		$("#messages-inner-right").empty();
		$("#change-password-modal").show();
		$("*").css("cursor", "wait");
		$("#messages-inner-right").load(this.href, function() {
		$("#messages-inner-right").fadeTo('fast','1');
			$("*").css("cursor", "");
			$("#change-password-modal").hide();
		});
		event.preventDefault();
		return false;
	});
	var $tabs = $("#tabs-nohdr").tabs({
		fx: { 
            opacity: 'toggle' 
        },
		ajaxOptions: {
			error: function( xhr, status, index, anchor ) {
				$( anchor.hash ).load("error.htm");
			},
			cache: false
		},
		show: function(event, ui) {
			$(".ui-tabs-hide").empty();
		},
		cache: false
	});
});