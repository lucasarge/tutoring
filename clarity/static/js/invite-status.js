// JavaScript file used to auto update page for invites.

const inviteId = document.getElementById("invite-data").dataset.inviteId

const pollInterval = setInterval(async () => {
    const response = await fetch(
        `/services/invite-status/${inviteId}`
    )

    const data = await response.json()

    // If invite is used or expired give respective response. Check for this every 3 seconds.
    if (data.used) {
        clearInterval(pollInterval)
        window.location.href = `/services/${data.service_id}/survey/`
    }
    if (data.expired) {
        clearInterval(pollInterval)
        document.getElementById("invite").innerText = "Invite Expired"
    }
}, 3000)