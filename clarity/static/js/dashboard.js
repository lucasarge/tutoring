document.addEventListener('DOMContentLoaded', function () {

    var calendarMinEl = document.getElementById('calendar-min');
    var meetingInfo = document.getElementById('meeting-info');

    if (calendarMinEl) {
        var calendarMin = new FullCalendar.Calendar(calendarMinEl, {
            initialView: 'listMonth',
            events: '/services/sessions/',
            allDaySlot: false,
            headerToolbar: false
        });
        calendarMin.render();
    }

    if (meetingInfo) {

        const pk = meetingInfo.dataset.pk;

        function fetchMeetingInfo() {
            fetch(`/services/${pk}/dashboard/`)
                .then(response => response.text())
                .then(html => {

                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html')
                    const refreshedDiv = doc.getElementById('meeting-info')

                    if (refreshedDiv) {
                        meetingInfo.innerHTML = refreshedDiv.innerHTML;

                        const localTime = new Date().toLocaleTimeString();
                        const refreshedTime = document.getElementById('refreshed-time')

                        if (refreshedTime) {
                            refreshedTime.innerHTML = localTime
                        }
                    }
                })
                .catch(error => console.error('Error fetching meeting data:', error));
        }

        fetchMeetingInfo();

        setInterval(fetchMeetingInfo, 10000)

    }
})