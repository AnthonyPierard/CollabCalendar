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

      // eventClick pas fini 
      eventClick: function(info) {

        // $("#NewTaskModal").show();
        // alert('Event: ' + info.event.title);
        // alert('Coordinates: ' + info.jsEvent.pageX + ',' + info.jsEvent.pageY);
        // alert('View: ' + info.view.type);
    
        // // change the border color just for fun
        info.el.style.borderColor = 'red';
      }

      


    });

    calendar.render();

    sideBarLoader()
  });

  