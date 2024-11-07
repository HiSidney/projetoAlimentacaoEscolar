const inputcpf = document.getElementById('input-cpf');

inputcpf.addEventListener('input', function(e) {
    // Remove tudo que não for dígito
    let valor = e.target.value.replace(/\D/g, '');

    // Formata o CPF
    if (valor.length > 11) {
        valor = valor.slice(0, 11); // Limita a 11 dígitos
    }
    if (valor.length > 9) {
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona o primeiro ponto
    }
    if (valor.length > 6) {
        valor = valor.replace(/(\d{3})(\d)/, '$1.$2'); // Adiciona o segundo ponto
    }
    if (valor.length > 3) {
        valor = valor.replace(/(\d{3})(\d)/, '$1-$2'); // Adiciona o traço
    }

    // Atualiza o valor do input
    e.target.value = valor;
});

document.getElementById('btn-login').addEventListener('click', function (){
    const cpf = document.getElementById('input-cpf').value;
    const senha = document.getElementById('input-senha').value;

    Login = {
        'cpf': cpf,
        'senha': senha,
    }
    console.log(Login);

    axios.post('/login', Login)
    .then(function(response){
        console.log(response.data)
        if (!response.data['value']) {
            alert('acesso negado');

        } else {
            if (response.data['tipoAcesso'] == 'ADMIN') {
                window.location.href = '/relatorio';
            } else if (response.data['tipoAcesso'] == 'USER') {
                window.location.href = '/';
            } else {
                window.location.href = '/login';
            }
        }
    })
    .catch(function(error){
        console.error(error)
    })
    
})