function checkNotif() {
    
    $.get(
        "/checkNotif"
    , data => {
        JSdata = JSON.parse(data)
        if(JSdata.new){
            
            if(JSdata.notif.length > 0) {
                $("#notifCount").show()
                $("#notifCount").text(JSdata.notif.length)

                $("#notifContainer").empty()

                for(let el of JSdata.notif) {
                    $("#notifContainer").append(`
                    <li onclick="notifAction(this, ${el.id}, ${el.type}, '${el.data}')"">
                        <a class="dropdown-item">
                            ${el.title}
                            <br>
                            <small>${el.msg}</small>
                        </a>
                    </li>
                    `)
                }
                

            } else $("#notifCount").hide()
        }
    })
}

function notifAction(el, idNotif, typeNotif, data) {
    $(el).hide()
    dataAJAX = {}
    if(data != "null") {

        let dataSplit = data.split("&")
        let url = dataSplit[0]
        for(let el of dataSplit[1].split(":")) {
            let elSplit = el.split("->")
            dataAJAX[elSplit[0]] = elSplit[1]
        }
    }
    if(typeNotif == 0) requestDelete(el, idNotif)
    if(typeNotif == 1) {
        requestDelete(el, idNotif)
        joinGroup(dataAJAX)
    } 

}

function requestDelete(el, idNotif) {

    $.post(
        "/delNotif",
        {
            id: idNotif
        }
    ).done( data => {
        if(data == "success") {
            console.log("Delete request")
            $(el).hide()
            if(parseInt($("#notifCount").text()) > 0){
                $("#notifCount").text(parseInt($("#notifCount").text())-1)
                if(parseInt($("#notifCount").text()) == 0) $("#notifCount").hide()
            }
        } else {
            alert("Error: Unable to achive the notification")
        }
    }).fail( _ => {
        alert("Error: server isn't reachable")
    })

}

function joinGroup(dataAJAX) {
    dataAJAX.username = ""
    console.log(dataAJAX)
    
    $.post(
        "/addUserToGroup",
        dataAJAX
    ).done( data => {
        if(data == "success") {
            sideBarLoader()

        } else {
            alert("Error: can't add to group")
        }
    }).fail( _ => {
        alert("Error: server isn't reachable")
    })
}


checkNotif()
var myInterval = setInterval(checkNotif, 10000); //Loop of 10sec