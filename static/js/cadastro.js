const inputCpf = document.getElementById('input-cpf');

inputCpf.addEventListener('input', function(e) {
    // Remove tudo que não for dígito
    let cpf = e.target.value.replace(/\D/g, '');

    // Formata o CPF
    if (cpf.length > 11) {
        cpf = cpf.slice(0, 11);
    }
    if (cpf.length > 9) {
        cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    }
    if (cpf.length > 6) {
        cpf = cpf.replace(/(\d{3})(\d)/, '$1.$2');
    }
    if (cpf.length > 3) {
        cpf = cpf.replace(/(\d{3})(\d)/, '$1-$2');
    }

    // Atualiza o valor do input
    e.target.value = cpf;
});

document.getElementById('bnt-cadastro').addEventListener('click', function (){
    const nome = document.getElementById('input-nome').value;
    const rm = document.getElementById('input-rm').value;
    const cpf = document.getElementById('input-cpf').value;
    const email = document.getElementById('input-email').value;
    const telefone = document.getElementById('input-telefone').value;
    const senha = document.getElementById('input-senha').value;
    const senha2 = document.getElementById('input-senha2').value;
    const tipo_acesso = document.getElementById('input-tipo_acesso').value;

    if (senha != senha2 ) {
        alert('Confirmar Senha Incoreta');
    } else if (senha.length < 8) {
        alert('Número de caracteres mínimos é necessário');
    } else {

        Usuario = {
            'nome': nome,
            'rm': rm,
            'cpf': cpf,
            'email': email,
            'telefone': telefone,
            'senha': senha,
            'tipo_acesso': tipo_acesso,
        }

        console.log(Usuario);

        axios.post('/cadastro', Usuario)
        .then(function(response){
            console.log(response.data)
        })
        .catch(function(error){
            console.error(error)
        })
    }

    

})