$(document).ready(function() {
	$("#wrapper").fadeIn(500, function() {
		$("#footer").delay(500).fadeIn(300, function() {
			$("#user-box").show("slide", { direction: "up" }, 400, function() {
				$("#container").fadeIn(400);
			});
		});
	});
	var $tabs = $("#tabs-nohdr").tabs({
		fx: { 
            opacity: 'toggle' 
        },
		load: function(event, ui) {
			$(ui.panel).delegate('.innerlink', 'click', function(event) {
				$(ui.panel).hide();
				$("*").css("cursor", "wait")
				$(ui.panel).load(this.href, function() {
					$(ui.panel).delay(200).fadeIn('fast', function() {
						$("*").css("cursor", "")
					});
				});
				event.preventDefault();
			});
			$(ui.panel).delegate('.dashlink', 'click', function(event) {
				$(ui.panel).hide();
				var pat_id = $(this).attr('patientid');
				$("*").css("cursor", "wait")
				$tabs.tabs('select', 1).bind('tabsshow', function() {
					url = '/referring/patientCase/' + pat_id + '/';
					$("#inner-right").load(url);
					$("*").css("cursor", "");
				});

				event.preventDefault();
			});
			$(ui.panel).delegate('.loadright', 'click', function(event) {
				$("#inner-right").hide();
				$("*").css("cursor", "wait")
				$("#inner-right").load(this.href, function() {
					$("#inner-right").delay(200).fadeIn('fast', function() {
						$("*").css("cursor", "")
					});
				});
				event.preventDefault();
			});
			$(ui.panel).delegate('.msgloadright', 'click', function(event) {
				$("#messages-inner-right").hide();
				$("*").css("cursor", "wait")
				$("#messages-inner-right").load(this.href, function() {
					$("#messages-inner-right").delay(200).fadeIn('fast', function() {
						$("*").css("cursor", "")
					});
				});
				event.preventDefault();
			});
		},
		ajaxOptions: {
			error: function( xhr, status, index, anchor ) {
				$( anchor.hash ).load("error.htm");
			}
		}
	});
});