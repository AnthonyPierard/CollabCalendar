function sideBarLoader() {

    //Get data from group api
    $.get( "/getUserGroup", data => {

        //Clear the target division (remove all child)
        $('#groupContainerSideBar').empty()

        //Add group list item
        JSON.parse(data).forEach(element => {
            $('#groupContainerSideBar').append(`<li><a href="${"#"}"><i class="fas fa-users"></i>${element.name}</a></li>`)
        });

    //In case of failed
    }).fail(_ => {

        //print alert and reload page
        alert("Error: Server isn't reachable")
        location.reload()
    })

}

$("#name").on('keyup', e => {
    if ((e.key === 'Enter' || e.keyCode === 13) && $("#name").val().replace(/ /g,'') != "") {

        $.post(
            "/addGroup",
            {
                name: $("#name").val()
            }
        ).fail(_ => {
            alert("Error: Server isn't reachable")
        }).done(_ => {
            sideBarLoader()
            $("#name").val("")
        })
    }
});