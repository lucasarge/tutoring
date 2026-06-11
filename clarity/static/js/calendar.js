document.addEventListener('DOMContentLoaded', function() {
    
    var calendarEl = document.getElementById('calendar');
    var calendarMinEl = document.getElementById('calendar-min');
    
    if (calendarEl) {
        var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/services/sessions/',
        // slotMinTime: '03:30:00',
        // slotMaxTime: '08:30:00',
        allDaySlot: false,
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        }
        });
        calendar.render();
    }
    
    if (calendarMinEl) {
        var calendarMin = new FullCalendar.Calendar(calendarMinEl, {
        initialView: 'listDay',
        events: '/services/sessions/',
        // slotMinTime: '03:30:00',
        // slotMaxTime: '08:30:00',
        allDaySlot: false,
        headerToolbar: false
        });
        calendarMin.render();
    }
});
