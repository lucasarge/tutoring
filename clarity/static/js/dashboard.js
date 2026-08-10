// JavaScript file used to display FullCalendar events and poll the next_meeting_info.

document.addEventListener('DOMContentLoaded', function () {

    // Gets elements from HTML via id.
    var calendarMinEl = document.getElementById('calendar-min');
    var meetingInfo = document.getElementById('meeting-info');

    // If there is the FullCalendar element configure to display in list form.
    if (calendarMinEl) {
        var calendarMin = new FullCalendar.Calendar(calendarMinEl, {
            initialView: 'listMonth',
            events: '/services/sessions/',
            allDaySlot: false,
            headerToolbar: false
        });
        calendarMin.render();
    }

    // If there is meetingInfo get pk from HTML.
    if (meetingInfo) {
        const pk = meetingInfo.dataset.pk;

        // Used to reload meetingInfo at a regular interval.
        function fetchMeetingInfo() {
            fetch(`/services/${pk}/dashboard/`)
                .then(response => response.text())
                .then(html => {

                    // Used to get just the specific div I want reloaded.
                    const parser = new DOMParser();
                    const doc = parser.parseFromString(html, 'text/html')
                    const refreshedDiv = doc.getElementById('meeting-info')

                    // If div exists set innerHTML to refreshed innerHTML. Set refreshed-time.
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

        // Run function every 10 seconds.
        fetchMeetingInfo();
        setInterval(fetchMeetingInfo, 10000)
    }
})