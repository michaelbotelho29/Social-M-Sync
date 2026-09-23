document.querySelector('form').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
    }
});

function toggleSenha() {
    const inputSenha = document.getElementById('password');
    const btnOlho = document.querySelector('#btn-toggle-senha-img');

    if (inputSenha.type === 'password') {
        inputSenha.type = 'text';
        btnOlho.src = "/static/imgs/eye-opened.png"
    } else {
        inputSenha.type = 'password';
        btnOlho.src = "/static/imgs/eye-closed.png"
    }
}

function EnterAccount() {
    const username = document.querySelector("#username").value.trim(), password = document.querySelector("#password").value.trim()
    document.querySelector("#entrar").style.display="none"
    document.querySelector("#loadingIndicator").style.display="flex"
    fetch(`/check-loginUsername?logUsername=${encodeURIComponent(username)}`)
    .then(response => response.json())
    .then(data => {
        if(data.existe){
            fetch(`/check-loginPassword?logPassword=${encodeURIComponent(password)}`)
            .then(response => response.json())
            .then(data => {
                if(data.verify){
                    document.querySelector("#pag1").style.display="none"
                    document.querySelector("#pag2").style.display="flex"
                    document.querySelector("#emailWarnDisplay").textContent=data.email
                }else{
                    document.querySelector("#loginWarning").textContent="Senha incorreta"
                    document.querySelector("#entrar").style.display="flex"
                    document.querySelector("#loadingIndicator").style.display="none"
                }
            })
        }else{
            document.querySelector("#loginWarning").textContent="Nome de usuário não encontrado"
            document.querySelector("#entrar").style.display="flex"
            document.querySelector("#loadingIndicator").style.display="none"
        }
    })
}