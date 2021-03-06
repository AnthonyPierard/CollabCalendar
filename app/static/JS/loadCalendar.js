
//Script executed after page loading
document.addEventListener('DOMContentLoaded', () => {

    sideBarLoader()

    //Load calendar, see: https://fullcalendar.io/docs/initialize-globals
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar( calendarEl, {
      
      //Set up viewButton
      views: {
        dayGridMonth: { buttonText: 'month' },
        timeGridWeek: { buttonText: 'week' },
        timeGridDay : { buttonText: 'day' },
      },

      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
      },

      //Set current date
      initialDate: new Date().toISOString(),

      //config
      defaultView: 'dayGridMonth',
      eventLimit: true,
      navLinks: true,
      editable: true,
      selectable: true,
      firstDay: 1,

      //Onhover show tooltip (info => data structure) [see: https://fullcalendar.io/docs/eventMouseEnter]
      eventMouseEnter: (info) => {

        //Show in tooltip summary of event
        $(info.el).tooltip({title: info.event.extendedProps.summary});             

      //Change event data onDrop (info => data structure) [see: https://fullcalendar.io/docs/eventDrop]
      }, eventDrop: info => {
        console.log("drop")
        console.log(info)
        //Post data
        $.post(
          `/pullData`,
          {
            id: info.event.id,
            newDate: info.event.start.toISOString()
          
          //On failed, alert and replace activity
          }).fail(_ => {
          info.revert()
          alert("Error: Server isn't reachable")
        })
      
      //Set time format of printed event's hour (hh:mm) [see: https://fullcalendar.io/docs/eventTimeFormat]
      }, eventTimeFormat: { 
        hour: 'numeric',
        minute: '2-digit',
        meridiem: false,
        hour12: false
      
      //Get request to get JSON with event [see: https://fullcalendar.io/docs/events-json-feed]
      }, events: {
				url: 'getDataEvent',
				error: _ => {
					$('#script-warning').show();
				}
			}, loading: bool => {
				$('#loading').toggle(bool);

      //Show modify modale on event click [see: https://fullcalendar.io/docs/eventClick]
			}, eventClick: info => {


        // get data on event to show
        $('#ShowTaskModal').modal({ show: false})
        $('#ShowTaskModal').modal('show')

        $.get('/showDataEvent/'+info.event.id).done( data => {

          // ??viter les doublons dans les valeurs des modals
          $("#ShowTaskModalHeader").empty()
          $("#ShowTaskModalDescription").empty()
          $("#ShowTaskModalDate").empty()
          $("#ShowTaskModalInterval").empty()

          $("#ModifyTaskModalDescription").empty()
          $("#newNameInput").empty()
          $("#newDateInput").empty()
          $("#newIntervalInput").empty()


          JSON.parse(data).forEach( el => {
            if( el.id == info.event.id){

              // affichage des infos sur la tache
              $("#ShowTaskModalHeader").append(el.title)
              $("#ShowTaskModalDescription").append(el.summary)
              $("#ShowTaskModalDate").append(el.start)
              $("#ShowTaskModalInterval").append(el.end)

              


              $('#taskid').empty()
              $('#newNameInput').empty()
              $('#newDescriptionInput').empty()
              $('#newDateInput').empty()
              $('#newIntervalInput').empty()

              $("#newNameInput").append(`<input type="text" id="hiddenNewName"class="form-control" value="${el.title}">`) 


              $("#newDescriptionInput").append(`<textarea class="form-control" id="hiddenNewDescription" rows="3"> ${el.summary}</textarea>`)
              $("#newDateInput").append(`<input class="form-control" id="hiddenNewDate" type="datetime-local" name="dateBeginInput" value="${el.start}" >`)
              $("#newIntervalInput").append(`<input class="form-control" id="hiddenNewInterval" type="number"  name="intervalInput" min="1" max="24" value="${el.end}" style="padding-left: 0.5cm;">`)
              
              // ajout des hidden id pour les fonctions de modifications et suppression de tache
              $("#taskid").append(`<input type="hidden" name="idhidden" id="idhidden" value="${el.id}">`)



            }
          })

        }).fail(_ => {
          alert("Error: Server isn't reachable ")
        })

        // PrepareremoveActivity(info.event.id)

        
      //Filter which event to show [see: https://fullcalendar.io/docs/event-render-hooks]
      }, eventDidMount: info => {
        console.log("didMount")
        console.log(info)
        groupId = info.el.classList[info.el.classList.length-1].split("eventGroup")[1]
        $(info.el).toggle($(`#sw${groupId}`).is(":checked"))
        info.el.style.backgroundColor = toColor(groupId) //Set group color
      }
    });

    calendar.render();
    sideBarLoader()
});


function closeShowModal() {
  $('#ShowTaskModal').modal('hide');
}

//Toggle display of an group of event
function toggleEvent(groupId) {
  $(`.eventGroup${groupId}`).each((index, element) => {
    $(element).toggle()
  })
}

//Get color from Interger
function toColor(num) {
  num *= 14254
  num >>>= 0;
  var b = num & 0xFF,
      g = (num & 0xFF00) >>> 8,
      r = (num & 0xFF0000) >>> 16 /*,
      a = ( (num & 0xFF000000) >>> 24 ) / 255*/ ;
  return "rgb(" + [r, g, b].join(",") + ")";
}
