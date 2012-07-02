$(function(){
	
	//User Name input field	
	
	//onfocus
	$('.nameTxt').focus(function(){
		var getName = $('.nameTxt').val();		
		if(getName=='Email Prefix'){
			$(this).val('');
		}	
	});
	
	//onblur
	$('.nameTxt').blur(function(){
		var getName = $('.nameTxt').val();
			if(getName==''){
				$(this).val('Email Prefix');
			}
			else{
				$('.nameTxt').val(getName);
			}	
	});
	
	
//Password input field 
	
	// onfocus
	$('.passTxt').focus(function(e){
		var getPass = $('.passTxt').val();		
		if(getPass=='Password (more than 8 letters)'){
			$(this).val('');
			this.type = 'password';
		}	
	});
	
	//onblur
	$('.passTxt').blur(function(){
		var getPass = $('.passTxt').val();
		if(getPass==''){
			this.type = 'text';
			$(this).val('Password (more than 8 letters)');
		}
		else{
			$('.passTxt').val(getPass);
		}	
	});
	

//Password input field 
	
	// onfocus
	$('.passTxt2').focus(function(e){
		var getPass = $('.passTxt2').val();		
		if(getPass=='Retype password to sign up'){
			$(this).val('');
			this.type = 'password';
		}	
	});
	
	//onblur
	$('.passTxt2').blur(function(){
		var getPass = $('.passTxt2').val();
		if(getPass==''){
			this.type = 'text';
			$(this).val('Retype password to sign up');
		}
		else{
			$('.passTxt2').val(getPass);
		}	
	});
	
});