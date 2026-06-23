document.addEventListener('DOMContentLoaded', function() {
    
    var calendarEl = document.getElementById('calendar');
    
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
        }
        });
        calendar.render();
    }

    flatpickr('.flatpickr-datetime', {
        enableTime: true,
        dateFormat: "Y-m-d H:i",
        time_24hr: true,
        
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
