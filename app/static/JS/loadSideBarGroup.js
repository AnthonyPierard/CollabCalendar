function sideBarLoader() {

    //Get data from group api
    $.get( "/getUserGroup", data => {
        
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