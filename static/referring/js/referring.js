$(document).ready(function() {
	$("#wrapper").fadeIn(500, function() {
		$("#footer").delay(500).fadeIn(300, function() {
			$("#user-box").show("slide", { direction: "up" }, 400, function() {
				$("#container").fadeIn(400);
			});
		});
	});
	$("#container").delegate(".loadright", "click", function(event) {
		$("#inner-right").css('opacity','0.001');
		$("#change-password-modal").show();
		$("#inner-right").empty();
		$("*").css("cursor", "wait");
		$("#inner-right").load(this.href, function() {
			$("#inner-right").fadeTo('slow','1');
			$("*").css("cursor", "");
			$("#change-password-modal").hide();
		});
		event.preventDefault();
		return false;
	});
	$("#container").delegate('.innerlink', 'click', function(event) {
		$('.ui-tabs-panel:not(.ui-tabs-hide)').hide();
		$("#change-password-modal").show();
		$('.ui-tabs-panel:not(.ui-tabs-hide)').empty();
		$("*").css("cursor", "wait");
		$('.ui-tabs-panel:not(.ui-tabs-hide)').load(this.href, function() {
			$('.ui-tabs-panel:not(.ui-tabs-hide)').delay(200).fadeIn('fast', function() {
				$("*").css("cursor", "");
				$("#change-password-modal").hide();
			});
		});
		event.preventDefault();
		return false;
	});
	$("#container").delegate('.dashlink', 'click', function(event) {
		$('.ui-tabs-panel:not(.ui-tabs-hide)').hide();
		$('.ui-tabs-panel:not(.ui-tabs-hide)').empty();
		$("#change-password-modal").show();
		var pat_id = $(this).attr('patientid');
		$("*").css("cursor", "wait");
		$tabs.tabs('select', 1).bind('tabsshow', function() {
			url = '/referring/patientCase/' + pat_id + '/';
			$("#inner-right").hide();
			$("#inner-right").empty();
			$("#inner-right").load(url, function() {
				$("#inner-right").delay(200).fadeIn('fast', function() {
					$("*").css("cursor", "");
					$("#change-password-modal").hide();
				});
			});
		});
		event.preventDefault();
		return false;
	});
	$("#container").delegate('.msglink', 'click', function(event) {
		$('.ui-tabs-panel:not(.ui-tabs-hide)').hide();
		$('.ui-tabs-panel:not(.ui-tabs-hide)').empty();
		$("#change-password-modal").show();
		var pat_id = $(this).attr('patientid');
		$("*").css("cursor", "wait");
		var url = this.href;
		$tabs.tabs('select', 2).bind('tabsshow', function() {
			$("#messages-inner-right").css('opacity','0.001');
			$("#messages-inner-right").empty();
			$("#messages-inner-right").load(url, function() {
				$("#messages-inner-right").fadeTo('fast','1');
				$("*").css("cursor", "");
				$("#change-password-modal").hide();
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