
function submitContactForm(){
        var reg = /^[A-Z0-9._%+-]+@([A-Z0-9-]+\.)+[A-Z]{2,4}$/i;
        var name = $('#taskname').val();
        var date = $('#datename').val();
       
        if(name.trim() == '' ){
            alert('Please enter your name.');
            $('#taskname').focus();
            return false;
        }else if(date.trim() == '' ){
            alert('Please enter a date.');
            $('#inputMessage').focus();
            return false;
        }else{
            $.ajax({
                type:'POST',
                url:'addtask',
                data:'contactFrmSubmit=1&name='+name+'date'+date,
                beforeSend: function () {
                    $('.submitBtn').attr("disabled","disabled");
                    $('.modal-body').css('opacity', '.5');
                },
                success:function(msg){
                    if(msg == 'ok'){
                        $('#taskname').val('');
                        $('#datename').val('');
                        $('.statusMsg').html('<span style="color:green;">task added</p>');
                    }else{
                        $('.statusMsg').html('<span style="color:red;">task not added</span>');
                    }
                    $('.submitBtn').removeAttr("disabled");
                    $('.modal-body').css('opacity', '');
                }
            });
        }
    }

