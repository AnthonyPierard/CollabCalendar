document.addEventListener('DOMContentLoaded', () => {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
      headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay,listMonth'
      },
      //Set current date
      initialDate: new Date().toISOString(),

      //config
      navLinks: true,
      editable: true,
      selectable: true,

      //Onhover show tooltip
      eventMouseEnter: (info) => {
        $(info.el).tooltip({title: info.event.extendedProps.summary});             

      //Change event data onDrop
      },eventDrop: info => {

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
      }, eventTimeFormat: { 
        hour: 'numeric',
        minute: '2-digit',
        meridiem: false,
        hour12: false
      
        //Get request to get JSON with event
      }, events: {
				url: 'getDataEvent',
				error: () => {
					$('#script-warning').show();
				}
			},
			loading: (bool) => {
				$('#loading').toggle(bool);
			},









      // eventClick pas fini, click sur l'activité dans le calendrier
      eventClick: function(info) {

        // get data on event to show

        $('#ShowTaskModal').modal({ show: false})
        $('#ShowTaskModal').modal('show')

        // afficage temporaire du nom
        $('#ShowTaskModalHeader').show(info.event.title)

        // alert('/showDataEvent/'+info.event.id)


        //$.get("/showDataEvent", data => {

        $.get('/showDataEvent/'+info.event.id).done( data => {
        // $.get("/showDataEvent/").done( data => {

          $("#ShowTaskModalDescription").empty()
          $("#ShowTaskModalDate").empty()
          $("#ShowTaskModalDescription").empty()
          $("#ShowTaskModalDate").empty()

          


          JSON.parse(data).forEach( el => {

            console.log("================consle====showDataEvent============")
            console.log(el)
            // $("#groupSelect").append(`<option value="${el.idGroup}">${el.name}</option>`)

      

            if( el.id == info.event.id){
            
              $("#ShowTaskModalDescription").append(el.summary)
              $("#ShowTaskModalDate").append(el.start)


              $("#ShowTaskModalDescription").append(el.summary)
              $("#ShowTaskModalDate").append(el.start)
  
            }

            
          
          })
      
        }).fail(_ => {
          $("#ShowTaskModalDescription").append("Error: Server isn't reachable =======>"+'/showDataEvent/'+info.event.id)
          alert("Error: Server isn't reachable ")
        })

        
      } 

    });

    

    calendar.render();

    sideBarLoader()
  });


  function closeShowModal() {
 
    $('#ShowTaskModal').modal('hide');
  }



  function removeActivity() {

  $.post ('/remove_activity/'+info.event.id).done( data => {
    if (data = "succes"){

    }

  })}
  
  