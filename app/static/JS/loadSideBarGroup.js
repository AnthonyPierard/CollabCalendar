function sideBarLoader() {

    //Get data from group api
    $.get( "/getUserGroup", data => {

        //Clear the target division (remove all child)
        $('#groupContainerSideBar').empty()
        let numcol = 0
        let inputModal = `
            `

        //Add group list item
        JSON.parse(data).forEach(element => {

            $('#groupContainerSideBar').append(`<li>
            
                <a href="${"#col"+element.idGroup}" 
                    data-toggle="collapse"  
                    aria-expanded="false" 
                    aria-controls="${"col"+element.idGroup}"
                >
                    <i class="fas fa-users"></i>${element.name}
                </a>
            </li>
            <div id="${"col"+element.idGroup}" class="collapse" style="background-color: #A8A8A8;">
                <div class="card-body">
                    ${(numcol == 0)?"":`
                    <input id="${"nn"+element.idGroup}" name="newName" class="h-75 form-control form-control-sm newName" type="text" placeholder="New name"></br>
                    <button type="button" class="w-100 btn-xs btn-primary" data-toggle="modal" data-target="#exampleModal" data-whatever="${element.idGroup}">
                        Add user
                    </button><br><br>`}
                    <div class="custom-control custom-switch">
                        <input type="checkbox" class="custom-control-input" id="${"sw"+element.idGroup}" ${(numcol == 0)?"checked":""}>
                        <label class="sw custom-control-label" for="${"sw"+element.idGroup}" onclick='toggleEvent(${element.idGroup})'>Show group</label>
                    </div>
                </div>
            </div>
            `) //${(numcol == 0)?"checked":""}

            numcol++
        });

    //In case of failed
    }).fail(_ => {

        //print alert and reload page
        alert("Error: Server isn't reachable")
        location.reload()
    }).done(_ => {
        $(".newName").each((index,element) => {
            //console.log($(element).attr("id")[2])
            
            $(element).on('keyup', e => {
                if ((e.key === 'Enter' || e.keyCode === 13) && $(element).val().replace(/ /g,'') != "") {
                    
                    $.post(
                        "/modifyGroup",
                        {
                            id: $(element).attr("id")[2],
                            newName: $(element).val()
                        }
                    ).fail(_ => {
                        alert("Error: Server isn't reachable")
                    }).done(_ => {
                        sideBarLoader()
                        $(element).val("")
                    })
                }
            })
            
        })
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

$('#exampleModal').on('show.bs.modal', event => {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var recipient = button.data('whatever') // Extract info from data-* attributes
    console.log(recipient)

    $("#idGroup").val(recipient)
})

$("#subNewUser").click(_ => {

    $.post(
        "/addUserToGroup",
        {
            idGroup: $("#idGroup").val(),
            username: $("#addUser").val()
        }
    ).fail(_ => {
        alert("Error: Server isn't reachable")
    }).done(res => {
        if(res == "success"){
            $("#exampleModal").modal('hide');
            $("#addUser").val("")
        }
        else{
            $("#addUser")
        }
    })

    console.log(`Envoye de : idGroup = ${$("#idGroup").val()}; msg = ${$("#addUser").val()}`)
})