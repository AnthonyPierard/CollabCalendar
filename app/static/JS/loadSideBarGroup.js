function sideBarLoader() {

    //Get data from group api
    $.get( "/getUserGroup", data => {

        //Clear the target division (remove all child)
        $('#groupContainerSideBar').empty()
        let numcol = 0

        //Add group list item
        JSON.parse(data).forEach(element => {

            $('#groupContainerSideBar').append(`
            <li>
            
                <a href="${"#col"+element.idGroup}" 
                    style="text-decoration: none;"
                    data-toggle="collapse"  
                    aria-expanded="false" 
                    aria-controls="${"col"+element.idGroup}"
                >
                    <i class="fas fa-users"></i>
                    <span id="${"na"+element.idGroup}">${element.name}<span>
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
        alert("Error: Server isn't reachable #onGroupLoad")
        location.reload()
    }).done(_ => {

        //For each input of group (wich allow to change group name)
        $(".newName").each((index,element) => {
            
            //On enter verify if name is correct
            $(element).on('keyup', e => {                
                if ((e.key === 'Enter' || e.keyCode === 13) && $(element).val() != "Your calendar" && $(element).val().replace(/ /g,'') != "") {

                    //Send data to server
                    $.post(
                        "/modifyGroup",
                        {
                            id: $(element).attr("id")[2],
                            newName: $(element).val()
                        }
                    ).fail(_ => {
                        alert("Error: Server isn't reachable #groupModif")
                    }).done(_ => {

                        //Clear input value
                        $(`#na${$(element).attr("id")[2]}`).text($(element).val())
                        $(element).val("")
                    })
                }
            })
            
        })
    })

}

//on enter of the input of group creation verify value
$("#name").on('keyup', e => {
    if ((e.key === 'Enter' || e.keyCode === 13) && $("#name").val().replace(/ /g,'') != "") {

        //Send data to sever
        $.post(
            "/addGroup",
            {
                name: $("#name").val()
            }
        ).fail(_ => {
            alert("Error: Server isn't reachable #addGroup")
        }).done(_ => {

            //Reload sidebar and clear input value
            sideBarLoader()
            $("#name").val("")
        })
    }
});

$('#exampleModal').on('show.bs.modal', event => {
    var button = $(event.relatedTarget) // Button that triggered the modal
    var recipient = button.data('whatever') // Extract info from data-* attributes

    $("#idGroup").val(recipient)
})

//Invit user to join group by enter or button clicking
$("#subNewUser").click(_ => submitJoin())
$("#addUser").keydown(event => {
    if(event.keyCode == 13){
        submitJoin()
        return false
    }
});

//Send joinning group notification to a user
function submitJoin() {

    //Send data to server
    $.post(
        "/notifyUserJoinGroup",
        {
            idGroup: $("#idGroup").val(),
            username: $("#addUser").val()
        }
    ).fail(_ => {
        alert("Error: Server isn't reachable #notifyUserJoinGroup")
    }).done(res => {

        //Clear and set up feedback msg
        if(res == "success") $("#usedadded").text($("#addUser").val())
        $("#addUser").val("")

        //Toggle feedback msg
        $("#userAddConfirm").toggle(res == "success")
        $("#userAddFail").toggle(["failed","ErrUsernameInvalid"].includes(res))
    })
}