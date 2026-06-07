document.addEventListener('DOMContentLoaded', function() {
    
    var calendarEl = document.getElementById('calendar');
    
    var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    events: '/services/sessions/',
    // slotMinTime: '03:30:00',
    // slotMaxTime: '08:30:00',
    headerToolbar: {
        left: 'prev,next today',
        center: 'title',
        right: 'dayGridMonth,timeGridWeek,timeGridDay'
    }
    });
    
    calendar.render();
});