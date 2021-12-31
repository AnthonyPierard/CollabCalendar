
/*
    modify the information of the account.
    if action==1 we change the firstname,
    elif action==2 we change the lastname,
    elif action==4 we change the username
    and elif action==5 we change the email.

    we go to a python function to change the DB and we provide it all the information
    to do it (new value and attributs to change).
*/

function modify (action, idUser)
{   

    if (action==1)
    {
        var newValue = document.getElementById("firstname").value
    }
    if (action==2)
    {
        var newValue = document.getElementById("lastname").value
    }
    if (action==4)
    {
        var newValue = document.getElementById("username").value
    }
    if (action==5)
    {
        var newValue = document.getElementById("email").value
    }
    
    $.post(
        "/modifyAccount",
        {
            action : action,
            value : newValue,
            id : idUser
        }
    ).done (data => {
        console.log(data)
        document.location.reload(true)
    })
    .fail (_ => {
        alert("Error server is not reachable #modifyAccount.js")
    })
}