
nom = "None"
description = ""
date = "20/12/2021"
duration = "2"

$('#NewTaskModal').on('show.bs.modal', function (event) {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var date = button.data('whatever') // Extract info from data-* attributes
    // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
    // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
    var modal = $(this)

    nom = modal.find('#Task-name')
    description= modal.find('#description')
    date = modal.find('#taskDate')
    duration= modal.find('#duration')

    modal.find('.modal-title').text("Add a new task : " )//+ date)
    modal.find('.modal-body input#taskDate').val(date)
})

var data = {
    name: nom,
    description: description,
    date: date,
    duration: duration}
 
getdata = () => {
    $.ajax({
        type: 'POST',
        url: '/',
        data: data
    })
    .done(function(res) {})
    .fail(function(error) {alert('Oops... ' + JSON.stringify(error.responseJSON));})
}