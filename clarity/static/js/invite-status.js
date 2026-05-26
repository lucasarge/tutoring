const inviteId = document.getElementById("invite-data").dataset.inviteId

const pollInterval = setInterval(async () => {
    const response = await fetch(
        `/services/invite-status/${inviteId}`
    )

    const data = await response.json()
    if (data.used) {
        clearInterval(pollInterval)
        window.location.href = `/services/${data.service_id}/dashboard/`
    }
    if (data.expired) {
        clearInterval(pollInterval)
        document.getElementById("invite").innerText = "Invite Expired"
    }
}, 3000)