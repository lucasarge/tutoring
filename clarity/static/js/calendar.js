// JavaScript file used to display calendars.

document.addEventListener('DOMContentLoaded', function() {
    
    // Gets element from HTML via id.
    var calendarEl = document.getElementById('calendar');
    
    // Initialising calendar through FullCalendar and customising it if element exists.
    if (calendarEl) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        events: '/services/sessions/',
        slotMinTime: '15:30:00',
        slotMaxTime: '20:30:00',
        allDaySlot: false,
        hiddenDays: '0.6',
        expandRows: true,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,listWeek'
        },
        viewDidMount: function(info) {
            if (info.view.type == 'timeGridDay') {
                calendarEl.classList.add('fc-day-view-active')
            } else {
                calendarEl.classList.remove('fc-day-view-active')
            }
        },

        // On click of session present popup with session information.
        eventClick: function(info) {
            if (!info.event.extendedProps.isUser) {
                info.jsEvent.preventDefault();
                return;
            }
            alert('Booking details: ' + info.event.extendedProps.details);
        },
        selectOverlap: function(event) {
            return event.display !== "background";
        }
        });
        calendar.render();
    }

    // Configuration for flatpickr datetime input.
    flatpickr('.flatpickr-datetime', {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: false,

        altInput: true,
        altFormat: "d/m h:i K",
        
        defaultHour:3,
        defaultMinute:30,
        
        minuteIncrement: 15, 

        disable: [
            function(date) {
                return (date.getDay() === 0 || date.getDay() === 6); 
            }
        ],

        minTime: '15:30',
        maxTime: '20:30',

        minDate: "today",
    })
});
