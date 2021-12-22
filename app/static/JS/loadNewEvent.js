
// TODO : fix le url, sauvegarder les données


// function submitContactForm(){
//         var reg = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
//         var name = $('#taskname').val();
//         var date = $('#datename').val();
       
//         if(name.trim() == '' ){
//             $('.statusMsg').html('<span style="color:red;">Please enter your name.</p>');
//             // alert('Please enter your name.');
//             $('#taskname').focus();
//             return false;
//         }else if(date.trim() == '' ){
//             $('.statusMsg').html('<span style="color:red;">Please enter a date.</p>');
//             $('#inputMessage').focus();
//             return false;
//         }else{

            
            
//             $.ajax({
//                 type:'POST',
//                 url:'/new_activity',
//                 data:{nameoftask : $('#taskname').val(),
//                       dateoftask : $('#datename').val()},
//                 // //useless
//                 // beforeSend: function () {
//                 //     $('.submitBtn').attr("disabled","disabled");
//                 //     $('.modal-body').css('opacity', '.5');
//                 // },
   
//                 success:function(msg){
//                     // // test
//                     alert(
//                         $('#datename').val()
//                     )
//             $('.statusMsg').html('<span style="color:red;">.....Need to add new in database....</p>');
//             $('#taskname').val('');
//             $('#datename').val('');
//             $('.submitBtn').removeAttr("disabled");
//             $('.modal-body').css('opacity', '');

//                     if(msg == 'ok'){
//                         $('#taskname').val('');
//                         $('#datename').val('');
//                         $('.statusMsg').html('<span style="color:green;">task added</p>');
//                     }else{
//                         $('.statusMsg').html('<span style="color:red;">task not added</span>');
//                     }
//                     $('.submitBtn').removeAttr("disabled");
//                     $('.modal-body').css('opacity', '');
//                 }
//             });
//         }
//     }


// function submitContactForm(){

//         $('form').on('submit', function(event) {
    
//             $.ajax({
//                 data : {
//                     name : $('#nameInput').val(),
//                     email : $('#emailInput').val()
//                 },
//                 type : 'POST',
//                 url : '/new_activity'
//             })
//             .done(function(data) {
    
//                 if (data.error) {
//                     $('#errorAlert').text(data.error).show();
//                     $('#successAlert').hide();
//                 }
//                 else {
//                     $('#successAlert').text(data.name).show();
//                     $('#errorAlert').hide();
//                 }
    
//             });	
    
//             event.preventDefault();
    
//         });
    
//     };


$(document).ready(function() {

	$('form').on('submit', function(event) {

		$.ajax({
			data : {
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

			// alert('in ajax function')

            // event.preventDefault();

			if (data.error) {
				// $('#errorAlert').text(data.error).show();
				// $('#successAlert').hide();
			}
			else {
                $('#inputName').val('');
                $('#inputEmail').val('');
                $('#inputMessage').val('');
                $('.statusMsg').html('<span style="color:green;"> Task added !</p>');
				// $('#successAlert').text(data.name).show();
				// $('#errorAlert').hide();

	


                calendar.render();

               sideBarLoader()
			}
		});	
	});
});






$(document).ready(function() {

	$('#formModifyTask').on('submit', function(event) {

		$.ajax({
			data : {
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

			// alert('in ajax function')

            // event.preventDefault();

			if (data.error) {
				// $('#errorAlert').text(data.error).show();
				// $('#successAlert').hide();
			}
			else {
                $('#inputName').val('');
                $('#inputEmail').val('');
                $('#inputMessage').val('');
                $('.statusMsg').html('<span style="color:green;"> Task added !</p>');
				// $('#successAlert').text(data.name).show();
				// $('#errorAlert').hide();

	


                calendar.render();

               sideBarLoader()
			}
		});	
	});
});












function removeActivity() {


	$.post(
		"/remove_activity",
		{
			id: $('#idhidden').val()
		}
	).done( data => {
		if (data = "succes"){
  
			// $("#deleteTaskMessage").append(`<p style="color: green;"> Task was successfully deleted </p>`)
			
			$('#ShowTaskModal').modal('hide');
			location.reload();

	  
		  }else{alert("Error: problem occured while deleting task ")}

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
			console.log(el)
			$("#groupSelect").append(`<option value="${el.idGroup}">${el.name}</option>`)
		})

	}).fail(_ => {
		alert("Error: Server isn't reachable")
	})

  })
