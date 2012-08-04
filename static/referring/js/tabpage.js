$(document).ready(function() {
	
	$("#btn-new-patient").button({
		icons: {
			primary: "ui-icon-plus"
		}
	});
	$("#btn-patient-refresh").button({
		icons: {
			primary: "ui-icon-plus"
		}
	});
	$('.data-table').dataTable({
		"bPaginate": false,
		"bLengthChange": false,
		"bFilter": true,
		"bSort": true,
		"bInfo": false,
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 20,
		"sPaginationType": "full_numbers"
	});
});