document.addEventListener('DOMContentLoaded', () => {

    sideBarLoader()

    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      
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

      //Onhover show tooltip
      eventMouseEnter: (info) => {
        $(info.el).tooltip({title: info.event.extendedProps.summary});             

      //Change event data onDrop
      },
      
      eventDrop: info => {

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
      
      //Set time format of printed event's hour (hh:mm)
      },
      
      eventTimeFormat: { 
        hour: 'numeric',
        minute: '2-digit',
        meridiem: false,
        hour12: false
      
        //Get request to get JSON with event
      }, events: {
				url: 'getDataEvent',
				error: _ => {
					$('#script-warning').show();
				}
			}, loading: bool => {
				$('#loading').toggle(bool);

			}, eventClick: info => {


        // get data on event to show

        $('#ShowTaskModal').modal({ show: false})
        $('#ShowTaskModal').modal('show')

        $.get('/showDataEvent/'+info.event.id).done( data => {

          // éviter les doublons dans les valeurs des modals
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

              //
              $("#ShowTaskModalHeader").append(el.title)
              $("#ShowTaskModalDescription").append(el.summary)
              $("#ShowTaskModalDate").append(el.start)
              $("#ShowTaskModalInterval").append(el.end)

              
              $("#newNameInput").append(`<input type="text" class="form-control" value="${el.title}">`)
              $("#ModifyTaskModalDescription").append(el.summary)
              $("#newDateInput").append(`<input class="form-control"  type="datetime-local" name="dateBeginInput" value="${el.start}" >`)
              $("#newIntervalInput").append(`<input class="form-control" type="number"  name="intervalInput" min="1" max="24" value="${el.end}" style="padding-left: 0.5cm;">`)
              
              // ajout des hidden id pour les fonctions de modifications et suppression de tache
              $("#taskid").append(`<input type="hidden" name="idhidden" id="idhidden" value="${el.id}">`)



            }
          })

        }).fail(_ => {
          alert("Error: Server isn't reachable ")
        })

        // PrepareremoveActivity(info.event.id)

        
      }, 
      
      eventDidMount: info => {
        groupId = info.el.className.split(" ")[8].split("eventGroup")[1]
        $(info.el).toggle($(`#sw${groupId}`).is(":checked"))
        info.el.style.backgroundColor = toColor(groupId)
      }


    });

    calendar.render();
    sideBarLoader()
  });


  function closeShowModal() {
    $('#ShowTaskModal').modal('hide');
  }

//à finir début -----------------------------------------------------------------
// à terminer : trouver un moyen de donner l'id


  function modifyActivity(id) {

    // get data on event to show

    // $('#ShowTaskModal').modal({ show: false})
    // $('#ShowTaskModal').modal('show')

    $.get('/showDataEvent/'+ id).done( data => {

      // $("#ModifyTaskModalHeader").empty()
      // $("#ModifyTaskModalDescription").empty()
      // $("#ModifyTaskModalDate").empty()
      // $("#ModifyTaskModalInterval").empty()


      JSON.parse(data).forEach( el => {
        if( el.id == id){

          $("#ModifyTaskModalHeader").append(el.title)
          $("#ModifyTaskModalDescription").append(el.summary)
          $("#ModifyTaskModalDate").append(el.start)
          $("#ModifyTaskModalInterval").append(el.end)

        }
      })
  
    }).fail(_ => {
      alert("Error: Server isn't reachable ")
    })

  }

//à finir fin-----------------------------------------------------------------

  
  
function toggleEvent(groupId) {
  //console.log($(`.eventGroup${groupId}`))
  $(`.eventGroup${groupId}`).each((index, element) => {
    $(element).toggle()
  })
}

function toColor(num) {
  num *= 14254
  num >>>= 0;
  var b = num & 0xFF,
      g = (num & 0xFF00) >>> 8,
      r = (num & 0xFF0000) >>> 16 /*,
      a = ( (num & 0xFF000000) >>> 24 ) / 255*/ ;
  return "rgb(" + [r, g, b].join(",") + ")";
}
