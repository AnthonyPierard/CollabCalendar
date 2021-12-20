
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