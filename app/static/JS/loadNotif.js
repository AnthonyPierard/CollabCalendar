
//Get notification and add it to notification menu
function checkNotif() {
    
    //get data from server
    $.get(
        "/checkNotif"
    , data => {
        /* 
        data => keys:
            new: TODO: is datat new (need to load notification ?)
            notif: Array of JSON => keys:
                id: id of the notification
                title: title of the notification
                msg: message of the notification
                type: type of notification (0 -> System message; 1 -> Joinning group)
                data: extra data of the notification
        */

        //Tranform the respond in a readable data-structure 
        JSdata = JSON.parse(data)
        if(JSdata.new){ //TODO
            
            //Check if there are notification
            if(JSdata.notif.length > 0) {

                //Update notification unread count (in a red dote)
                $("#notifCount").show()
                $("#notifCount").text(JSdata.notif.length)

                //Clear notification menu
                $("#notifContainer").empty()

                //Add Notification dom object
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
                
            //Hide red dote if no notification
            } else $("#notifCount").hide()
        }
    })
}

/* 
Allow on click action
---------------------
Parameter:
    el: DOM object of the target notif
    idNotif: id of the target notif
    typeNotif: type of the target notif (0-> System msg, 1-> Group joinning)
    data: additionnal data to procceed the action
*/
function notifAction(el, idNotif, typeNotif, data) {

    //Hide dom element (to avoid refreshing)
    $(el).hide()

    //Set readable data
    dataAJAX = {}
    if(data != "null") {

        let dataSplit = data.split("&")
        let url = dataSplit[0]
        for(let el of dataSplit[1].split(":")) {
            let elSplit = el.split("->")
            dataAJAX[elSplit[0]] = elSplit[1]
        }
    }

    //Switch case of target action
    if(typeNotif == 0) requestDelete(el, idNotif)
    if(typeNotif == 1) {
        requestDelete(el, idNotif)
        joinGroup(dataAJAX)
    } 

}

/* 
Remove notification
---------------------
Parameter:
    el: DOM object of the target notif
    idNotif: id of the target notif
*/
function requestDelete(el, idNotif) {

    //Send data to server
    $.post(
        "/delNotif",
        {
            id: idNotif
        }
    ).done( data => {
        if(data == "success") {
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

/* 
Allow to add current user to a target group
---------------------
Parameter:
    dataAJAX: data to send to the server
*/
function joinGroup(dataAJAX) {

    //Set up username ("" means current user see APY.py file)
    dataAJAX.username = ""
    
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