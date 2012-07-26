var patient_dt;

$(document).ready(function() {
	make_dt();		
	
    $("#popup-schedule-date").datepicker({
		
	});
	
	  /* attach a submit handler to the form */
	$("#select-center").submit(function(event) {

    /* stop form from submitting normally */
		event.preventDefault(); 
        
    /* get some values from elements on the page: */
		var $form = $( this ),
			url = $form.attr( 'action' );

    /* Send the data using post and put the results in a div */
		$.post( url, $("#select-center").serialize(),
		function( data ) {
			$( "#schedule-content" ).empty().append($(data));
		}
		);
     });
  

    $('#textfield-clear').show();
	$('#textfield-textfield').hide();

	$('#textfield-clear').focus(function() {
		$('#textfield-clear').hide();
		$('#textfield-textfield').show();
		$('#textfield-textfield').focus();
	});
	$('#textfield-textfield').blur(function() {
		if($('#textfield-textfield').val() == '') {
			$('#textfield-clear').show();
			$('#textfield-textfield').hide();
		}
	}); 
	
	$("#create-patient").submit(function(event) {

    /* stop form from submitting normally */
		event.preventDefault(); 
        
    /* get some values from elements on the page: */
		var $form = $( this ),
			url = $form.attr( 'action' );

    /* Send the data using post and put the results in a div */
		$.post( url, $("#create-patient").serialize(),
		function( data ) {
			$( "#patients-content" ).empty().append($(data));
		}
		);
     });
	 
	 $("#makeAppointment").submit(function(event) {

    /* stop form from submitting normally */
		event.preventDefault(); 
        
    /* get some values from elements on the page: */
		var $form = $( this ),
			url = $form.attr( 'action' );

    /* Send the data using post and put the results in a div */
		$.post( url, $("#makeAppointment").serialize(),
		function( data ) {
			$( "#schedule-content" ).empty().append($(data));
		}
		);
     });
     
     $("#ssn-form").submit(function(event) {

    /* stop form from submitting normally */
		event.preventDefault(); 
        
    /* get some values from elements on the page: */
		var $form = $( this ),
			url = $form.attr( 'action' );

    /* Send the data using post and put the results in a div */
		$.post( url, $("#ssn-form").serialize(),
		function( data ) {
			$( "#patients-content" ).empty().append($(data));
		}
		);
     });
     
     
     $("#create-link").submit(function(event) {

    /* stop form from submitting normally */
		event.preventDefault(); 
        
    /* get some values from elements on the page: */
		var $form = $( this ),
			url = $form.attr( 'action' );

    /* Send the data using post and put the results in a div */
		$.post( url, $("#create-link").serialize(),
		function( data ) {
			$( "#patients-content" ).empty().append($(data));
		}
		);
     });
     
	
});

function reset_dt_view() {
  localStorage.removeItem('DataTables_PatientTable');
  patient_dt.fnDestroy();
  make_dt();
}

function make_dt() {
	patient_dt = $('#patient-table').dataTable({
		"bPaginate": true,
		"bLengthChange": false,
		"bFilter": true,
		"bSort": true,
		"bInfo": false,
		"bStateSave": true,
		"fnStateSave": function (oSettings, oData) {
			localStorage.setItem( 'DataTables_PatientTable', JSON.stringify(oData) );
		},
		"fnStateLoad": function (oSettings) {
			return JSON.parse( localStorage.getItem('DataTables_PatientTable') );
		},
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 7,
		"sPaginationType": "full_numbers"
	});
	schedule_dt = $('#schedule-table').dataTable({
		"bPaginate": false,
		"bLengthChange": false,
		"bFilter": false,
		"bSort": false,
		"bInfo": false,
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 10,
		"sPaginationType": "full_numbers",
	    "sScrollY": "300px"
	});
	patient_dt = $('#schedule-timeslot-table').dataTable({
		"bPaginate": false,
		"bLengthChange": false,
		"bFilter": false,
		"bSort": true,
		"bInfo": false,
		"bStateSave": true,
		"fnStateSave": function (oSettings, oData) {
			localStorage.setItem( 'DataTables_PatientTable', JSON.stringify(oData) );
		},
		"fnStateLoad": function (oSettings) {
			return JSON.parse( localStorage.getItem('DataTables_PatientTable') );
		},
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 10,
		"sPaginationType": "full_numbers"
	});
	schedule_dt = $('#create-patient-table').dataTable({
		"bPaginate": false,
		"bLengthChange": false,
		"bFilter": false,
		"bSort": false,
		"bInfo": false,
		"bStateSave": true,
		"fnStateSave": function (oSettings, oData) {
			localStorage.setItem( 'DataTables_PatientTable', JSON.stringify(oData) );
		},
		"fnStateLoad": function (oSettings) {
			return JSON.parse( localStorage.getItem('DataTables_PatientTable') );
		},
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 10,
		"sPaginationType": "full_numbers"
	});
	schedule_dt = $('#patient-info-table').dataTable({
		"bPaginate": false,
		"bLengthChange": false,
		"bFilter": false,
		"bSort": false,
		"bInfo": false,
		"bStateSave": true,
		"fnStateSave": function (oSettings, oData) {
			localStorage.setItem( 'DataTables_PatientTable', JSON.stringify(oData) );
		},
		"fnStateLoad": function (oSettings) {
			return JSON.parse( localStorage.getItem('DataTables_PatientTable') );
		},
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 10,
		"sPaginationType": "full_numbers",
		"sScrollY": "330px"
	});
	schedule_dt = $('#diagnosis-table').dataTable({
		"bPaginate": true,
		"bLengthChange": false,
		"bFilter": true,
		"bSort": true,
		"bInfo": false,
		"bStateSave": true,
		"fnStateSave": function (oSettings, oData) {
			localStorage.setItem( 'DataTables_PatientTable', JSON.stringify(oData) );
		},
		"fnStateLoad": function (oSettings) {
			return JSON.parse( localStorage.getItem('DataTables_PatientTable') );
		},
		"bAutoWidth": false,
		"bRetrieve": true,
		"bJQueryUI": false,
		"iDisplayLength": 10,
		"sPaginationType": "full_numbers"
	});
}