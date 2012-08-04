var register_dt;

$(document).ready(function() {
	make_dt();	
	
	$("#rp-schedule-date").datepicker({
			
	});
	
	$("#rp-reschedule-date").datepicker({
			
	});
	
	$('#reschedule-viewbutton').click(function() {
		$('#rp-reschedule-timeslot-table').fadeIn('fast');
	});

	
	reset_dt_view() ;
     
});

function reset_dt_view() {
  localStorage.removeItem('DataTables_RegisterTable');
  register_dt.fnDestroy();
  make_dt();
}

function make_dt() {
	register_dt = $('#register-table').dataTable({
		"bPaginate": true,
		"bLengthChange": false,
		"bFilter": true,
		"bSort": true,
		"bInfo": false,
		"bStateSave": true,
		"fnStateSave": function (oSettings, oData) {
			localStorage.setItem( 'DataTables_RegisterTable', JSON.stringify(oData) );
		},
		"fnStateLoad": function (oSettings) {
			return JSON.parse( localStorage.getItem('DataTables_RegisterTable') );
		},
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 6,
		"sPaginationType": "full_numbers",
		"aaSorting": [[3, "asc"]]
	});
	schedule_timeslot_dt = $('#rp-schedule-timeslot-table').dataTable({
		"bPaginate": false,
		"bLengthChange": false,
		"bFilter": false,
		"bSort": true,
		"bInfo": false,
		"bStateSave": true,
		"fnStateSave": function (oSettings, oData) {
			localStorage.setItem( 'DataTables_ScheduleTimeslotTable', JSON.stringify(oData) );
		},
		"fnStateLoad": function (oSettings) {
			return JSON.parse( localStorage.getItem('DataTables_ScheduleTimeslotTable') );
		},
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 10,
		"sPaginationType": "full_numbers"
	});
	schedule_timeslot_dt = $('#rp-reschedule-timeslot-table').dataTable({
		"bPaginate": false,
		"bLengthChange": false,
		"bFilter": false,
		"bSort": true,
		"bInfo": false,
		"bStateSave": true,
		"fnStateSave": function (oSettings, oData) {
			localStorage.setItem( 'DataTables_ScheduleTimeslotTable', JSON.stringify(oData) );
		},
		"fnStateLoad": function (oSettings) {
			return JSON.parse( localStorage.getItem('DataTables_ScheduleTimeslotTable') );
		},
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 10,
		"sPaginationType": "full_numbers"
	});
}