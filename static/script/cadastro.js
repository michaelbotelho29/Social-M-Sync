document.querySelector('form').addEventListener('keydown', function(e) {
    if (e.key === 'Enter') {
      e.preventDefault();
    }
});

/* funções que fazem o sistema de mostrar ou não a senha funcionar */
// Início
function toggleSenha1() {
    const inputSenha = document.getElementById('senha1');
    const btnOlho = document.querySelector('#btn-toggle-senha-img1');

    if (inputSenha.type === 'password') {
        inputSenha.type = 'text';
        btnOlho.src = "/static/imgs/eye-opened.png"
    } else {
        inputSenha.type = 'password';
        btnOlho.src = "/static/imgs/eye-closed.png"
    }
}

function toggleSenha2() {
    const inputSenha = document.getElementById('senha2');
    const btnOlho = document.querySelector('#btn-toggle-senha-img2');

    if (inputSenha.type === 'password') {
        inputSenha.type = 'text';
        btnOlho.src = "/static/imgs/eye-opened.png"
    } else {
        inputSenha.type = 'password';
        btnOlho.src = "/static/imgs/eye-closed.png"
    }
}
// Fim

/* funções para "trocar de página" */
// Início
function lastPage1() {
    document.querySelector("#pag2").style.display="none"
    document.querySelector("#pag1").style.display="flex"
}

function lastPage2() {
    document.querySelector("#confirmTab").style.display="none"
    document.querySelector("#pag2").style.display="flex"
}


function nextPage1() {
    /* sistemas de checagem de informações enviadas pelo usuário na primeira página */
    /* verifica se algum campo do formulário está vazio */
    // Início
    let freio = false
    let inputs = document.querySelectorAll(".inputFirstPage")
    for(let i=0; i<inputs.length; i++){
        if(inputs[i].value.length<1){
            freio = true
        }
    }
    // Fim

    /* verifica se o CPF ou CNPJ são válidos */
    // Início
    let freioCPF = true
    if(document.querySelector("#userCPF").value.length == 11 || document.querySelector("#userCPF").value.length == 14){
        freioCPF = false
    }
    // Fim

    /* verifica se o email contém @ */
    // Início
    let freioEmail = document.querySelector("#userEmail").value.includes('@')
    // Fim

    /* verifica se o telefone é válido */
    // Início
    let freioTelefone = false
    if(document.querySelector("#userNumber").value.length != 11){
        freioTelefone = true
    }
    // Fim

    /* verifica se algum freio foi ativo e mostra próxima página */
    // Início
    if(freio){
        document.querySelector("#pag1-warning").style.display="flex"
        document.querySelector("#pag1-warning").textContent="Todos os campos devem ser preenchidos"
    }else if(freioCPF){
        document.querySelector("#pag1-warning").style.display="flex"
        document.querySelector("#pag1-warning").textContent="Insira um CPF ou CNPJ válido"
    }else if(!freioEmail){
        document.querySelector("#pag1-warning").style.display="flex"
        document.querySelector("#pag1-warning").textContent="Insira um email válido"
    }else if(freioTelefone){
        document.querySelector("#pag1-warning").style.display="flex"
        document.querySelector("#pag1-warning").textContent="Insira um telefone válido"
    }else{
        document.querySelector("#pag2").style.display="flex"
        document.querySelector("#pag1").style.display="none"
        document.querySelector("#pag1-warning").textContent=""
    }
    // Fim
}

function nextPage2(){
    const usernameInput = document.querySelector("#username")
    const username = usernameInput.value.trim()

    if(username.length < 1){
        document.querySelector("#usernameWarning").textContent = "Insira um nome de usuário"
        return
    }

    fetch(`/check-username?username=${encodeURIComponent(username)}`)
        .then(response => response.json())
        .then(data => {
            if(data.exists){
                document.querySelector("#usernameWarning").style.display = "flex"
                document.querySelector("#usernameWarning").textContent = "Esse nome de usuário já está em uso"
            } else {
                document.querySelector("#usernameWarning").style.display = "none"
                if(document.querySelector("#senha1").value == document.querySelector("#senha2").value){
                    const userEmail = document.querySelector("#userEmail").value.trim()
                    document.querySelector("#passwordWarning").textContent=""
                    document.querySelector("#pag2").style.display="none"
                    document.querySelector("#confirmTab").style.display="flex"
                    document.querySelector("#emailWarnDisplay").textContent = userEmail
                    fetch(`/check-email?userEmail=${encodeURIComponent(userEmail)}`)
                }else{
                    document.querySelector("#passwordWarning").textContent="As senhas não batem"
                }
            }
        })
        .catch(error => {
            console.error("Erro ao verificar username:", error)
        })
}

function verificar(){
    const confirmation = document.querySelector("#emailConfirmation").value.trim()
    fetch(`/check-emailConfirmation?confirmation=${encodeURIComponent(confirmation)}`)
    .then(response => response.json())
    .then(data => {
        if(data.verify){
            document.querySelector("#btn-verify").style.display="none"
            document.querySelector("#btn-signUp").style.display="flex"
        } else{
            document.querySelector("#emailWarn2").textContent="código de validação incorreto"
            document.querySelector("#emailWarn2").style.color="#ff6b6b;"
        }
    })
}