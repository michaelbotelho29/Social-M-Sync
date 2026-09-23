function logarInstagram() {
    const instagramUsername = document.querySelector("#InstagramUsername").value.trim()
    const instagramPassword = document.querySelector("#InstagramPassword").value.trim()

    if (instagramUsername.length < 1 || instagramPassword.length < 1) {
        console.log("Preencha usuário e senha do Instagram")
        return
    }

    fetch('/logarInstagram', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            InstagramUsername: instagramUsername,
            InstagramPassword: instagramPassword
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        console.log("Facebook Logou")
    })
    .catch(error => {
        console.error("Erro ao logar no Instagram:", error)
    })
}

function logarFacebook() {
    const facebookUsername = document.querySelector("#FacebookUsername").value.trim()
    const facebookPassword = document.querySelector("#FacebookPassword").value.trim()

    if (facebookUsername.length < 1 || facebookPassword.length < 1) {
        console.log("Preencha usuário e senha do Facebook")
        return
    }

    fetch('/logarFacebook', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            facebookUsername: facebookUsername,
            facebookPassword: facebookPassword
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        console.log("Facebook Logou")
    })
    .catch(error => {
        console.error("Erro ao logar no Facebook:", error)
    })
}

function logarLinkedIn() {
    const linkedInUsername = document.querySelector("#LinkedInUsername").value.trim()
    const linkedInPassword = document.querySelector("#LinkedInPassword").value.trim()

    if (linkedInUsername.length < 1 || linkedInPassword.length < 1) {
        console.log("Preencha usuário e senha do LinkedIn")
        return
    }

    fetch('/logarLinkedIn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            linkedInUsername: linkedInUsername,
            linkedInPassword: linkedInPassword
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data)
        console.log("LinkedIn Logou")
    })
    .catch(error => {
        console.error("Erro ao logar no LinkedIn:", error)
    })
}