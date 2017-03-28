
// Settings Page
function isBackupsChecked() {
	if ($('#backups').is(':checked')) {
		return 'on';
	} else {
		return 'off';
	}
}

function submitSettings(id, sk, backups, type){
		
	// get the vars		
	data = {'atid': id, 'atsk': sk, 'buf': 'nothing', 'backups': backups, 'type': type};

	$.ajax({
		method: 'POST',
		url: '/api/settings',
		data: data,
		cache: false,
		success: function(response){
			console.log(response);
			$('#finalMsg p').css('color', '#fafafa');
			$('#finalMsg p').text('Successfully updated Settings!');
			$('#finalMsg').show();
		},
		error: function(response){
			console.log(response);
			$('#finalMsg p').css('color', 'rgb(255, 166, 168)');
			$('#finalMsg p').text('Error updating Settings!');
			$('#finalMsg').show();
		}
	});
}

jQuery(document).ready(function($) {
	$('#finalMsg').hide();
	$('#upd').click(function() {
		// get the parsleys
		var v_id = $('#atid').parsley();
		var val_id = v_id.isValid();
		console.log(val_id);
		var v_sk = $('#atsk').parsley();
		var val_sk = v_sk.isValid();
		console.log(val_sk);
		//var v_buf = $('#buf').parsley();
		//var val_buf = v_buf.isValid();
		//console.log(val_buf);
		//$('#atid').parsley().isValid()
		//$('#atid').parsley().on('form:validate', function(formInstance) {
		//	var ok_id = formInstance.isValid({group: 'id', force: true}) || formInstance.isValid({group: 'sk', force: true});
		//	$('#atid').removeClass('invalid').addClass('valid');
		//
		//	if (!ok){
		//		$('#atid').removeClass('valid').addClass('invalid');
		//	}
		//});

		var id = $('#atid').val();
		console.log(id);

		var sk = $('#atsk').val();
		console.log(sk);

		//var buf = $('#buf').val();
		//console.log(buf);

		var backups = isBackupsChecked();
		console.log(backups);

		if (v_id.isValid() && v_sk.isValid()){
			submitSettings(id, sk, backups, 'update');
		} else {
			return false;
		}
	});
});

// Add Page
jQuery(document).ready(function($) {
	$('#msgBox').hide();
	$('#sbm-repo').click(function() {
		var at = $('#at').val();
		var url = $('#repo-url').val();
		var name = $('#name').val();

		var data = {'at':at, 'url':url, 'name':name}

		$.ajax({
			type: 'POST',
			url: '/api/repo',
			data: data,
			cache: false,
			success: function(result){
				console.log(result);
				$('#msgBox').css('color', '#29d1bb');
				$('#msgBox p').text('Successfully added Repo!');
				$('#msgBox').show();
			},
			error: function(error){
				console.log(error);
				$('#msgBox').css('color', 'rgb(255, 166, 168)');
				$('#msgBox').text("Error adding Repo!");
				$('#msgBox').show();
			}
		});
	});
});