function adicionaTemaClaro() {
    document.body.classList.remove('black');
}

function adicionaTemaEscuro() {
    document.body.classList.add('black');
}

axios.get('/getInfoAboutUser')
.then(function(response){
    console.log(response.data[0]);
    const responses = response.data[0];
    inputName = document.getElementById('input-name').setAttribute('placeholder',responses[1]);
    inputCpf = document.getElementById('input-cpf').setAttribute('placeholder',responses[2]);
    inputCodigo = document.getElementById('input-codigo').setAttribute('placeholder',responses[5]);
    inputTelefone = document.getElementById('input-telefone').setAttribute('placeholder',responses[4]);
    inputId = document.getElementById('input-id').setAttribute('placeholder',responses[0]);
    inputEmail = document.getElementById('input-email').setAttribute('placeholder',responses[3]);
    inputSenha = document.getElementById('input-senha');
    inputSenha2 = document.getElementById('input-senha2');
})
.catch(function(error){
    console.error(error);
})