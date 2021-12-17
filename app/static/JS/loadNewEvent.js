
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
                date : $('#dateInput').val()
			},
			type : 'POST',
			url : '/new_activity'
		})
		.done(function(data) {

			if (data.error) {
				$('#errorAlert').text(data.error).show();
				$('#successAlert').hide();
			}
			else {
				$('#successAlert').text(data.name).show();
				$('#errorAlert').hide();
			}

		});	

		event.preventDefault();

	});

});