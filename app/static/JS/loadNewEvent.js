


$(document).ready(function() {
	$('form').on('submit', function(event) {

		//send informations on task from fronted to backend
		$.ajax({
			data : {
				//takes data on task from the html form
				name : $('#nameInput').val(),
				description : $('#descriptionInput').val(),
                dateBegin : $('#dateBeginInput').val(),
                interval : $('#intervalInput').val(),
				idGroup : $("#groupSelect").val(),
			},
			type : 'POST',
			url : '/new_activity'
		})
		.done(function(data) {
			if (data.error) {
				alert("Error: problem occured while adding new task ")	
			}
			else {
            	calendar.render();
            	sideBarLoader()
			}
		});	
	});
});





function modifyActivity() {

	$('#formModifyTask').on('submit', function(event) {
		$.ajax({
			data : {
				taskid : $('#idhidden').val(),
				name : $('#hiddenNewName').val(),
				description : $('#hiddenNewDescription').val(),
                dateBegin : $('#hiddenNewDate').val(),
                interval : $('#hiddenNewInterval').val(),
			},
			type : 'POST',
			url : '/modify_activity'
		})
		.done(function(data) {
			$('#taskid').empty()
			$('#newNameInput').empty()
			$('#newDescriptionInput').empty()
			$('#newDateInput').empty()
			$('#newIntervalInput').empty()

			if (data.error) {		
				alert("Error: problem occured while modifying task ")	
			}
			else {
                calendar.render();
            	sideBarLoader()
			}
		});	
	});
}




function removeActivity() {
	$.post(
		"/remove_activity",
		{
			id: $('#idhidden').val()
		}
	).done( data => {
		if (data = "succes"){
			$('#ShowTaskModal').modal('hide');
			location.reload();
		  }else{
			  alert("Error: problem occured while deleting task ")
			}

	}).fail( _ => {
		alert("Error: server isn't reachable")
	})
}



























$("#NewTaskModal").on('shown.bs.modal', _ => {

	
	$.get(
		"/getUserGroup"
	).done( data => {

		$("#groupSelect").empty()

		/*data => ARRAY of JSON => keys: idGroup, nameGroup*/
		JSON.parse(data).forEach(el => {
			$("#groupSelect").append(`<option value="${el.idGroup}">${el.name}</option>`)
		})

	}).fail(_ => {
		alert("Error: Server isn't reachable")
	})

  })
