const todasAsDivs = document.querySelectorAll('.cafeManha, .almoco, .cafeTarde');

axios.get('/pega-notificacao')
.then(function(response){
    // console.log(response.data);
    document.getElementById('campo-notificacao').innerHTML = `<strong>Olá ${response.data['nomeUser']}! </strong>${response.data['notificacao'][2]}`;
    getrotaSelectGerarRefeicaoJsFunction() 
    // tem q mudar. primeiro, verivicar de o usuario já respondeu na rotaSelectGerarRefeicao
})
.catch(function(error){
    console.error(error);
});

function getrotaSelectGerarRefeicaoJsFunction() {
axios.get('/rotaSelectGerarRefeicao')
.then(function(response){
    const resposta = response.data;
    // console.log(resposta);

    const classesParaRemover = [
        'cafeBloqueado',
        'cafeMarcado',
        'cafeDesmarcado',
        'almocoBloqueado',
        'almocoMarcado',
        'almocoDesmarcado'
    ];

    // Remove as classes de cada div
    todasAsDivs.forEach(div => {
        classesParaRemover.forEach(classe => {
            div.classList.remove(classe);
        });
    });

    // Verificando se a resposta é vazia
    if (resposta.length === 0) {
        // Ação se a resposta for uma tupla vazia
        console.log("A resposta está vazia.");

        // Iterar sobre as divs e adicionar as classes bloqueadas
        todasAsDivs.forEach(div => {
            if (div.classList.contains('cafeManha')) {
                div.classList.add('cafeBloqueado');
            } else if (div.classList.contains('almoco')) {
                div.classList.add('almocoBloqueado');
            } else if (div.classList.contains('cafeTarde')) {
                div.classList.add('cafeBloqueado');
            }
        });
    } else {
        // Ação se a resposta não for vazia
        // console.log("A resposta contém dados:");
        // Dias da semana em ordem para associar com os IDs das divs
        const diasSemana = ['segunda', 'terca', 'quarta', 'quinta', 'sexta'];

        // Itera sobre cada dia da resposta e aplica as classes necessárias
        resposta.forEach((dia, index) => {
            const [data, cafeManhaStatus, almocoStatus, cafeTardeStatus] = dia;
            const diaSemana = diasSemana[index]; // Dia da semana atual no HTML

            // Seleciona os elementos pelo ID do dia da semana
            const cafeManhaDiv = document.getElementById(`${diaSemana}-manha`);
            const almocoDiv = document.getElementById(`${diaSemana}-almoco`);
            const cafeTardeDiv = document.getElementById(`${diaSemana}-tarde`);

            // Verifica e aplica as classes para o café da manhã
            if (cafeManhaStatus) {
                cafeManhaDiv.classList.add('cafeMarcado');
            } else {
                cafeManhaDiv.classList.add('cafeBloqueado');
            }

            // Verifica e aplica as classes para o almoço
            if (almocoStatus) {
                almocoDiv.classList.add('almocoMarcado');
            } else {
                almocoDiv.classList.add('almocoBloqueado');
            }

            // Verifica e aplica as classes para o café da tarde
            if (cafeTardeStatus) {
                cafeTardeDiv.classList.add('cafeMarcado');
            } else {
                cafeTardeDiv.classList.add('cafeBloqueado');
            }
        });

    }


})
.catch(function(error){
    console.error(error);
})
}

todasAsDivs.forEach(div => {
    div.addEventListener('click', (event) => {
        // `event.currentTarget` refere-se ao elemento que foi 

        const elementoClicado = event.currentTarget;
        if(elementoClicado.className[0] == 'c') {
            elementoClicado.classList.toggle("cafeDesmarcado");
        } else {
            elementoClicado.classList.toggle("almocoDesmarcado");
        };
    });
});


document.getElementById('abrirConfirmacaoRefeicao').addEventListener('click', () => {

    const segunda = document.querySelectorAll('div[name="segunda"],div[name="terca"],div[name="quarta"],div[name="quinta"],div[name="sexta"]');

    const segundaList = Array.from(segunda).filter(i => 
        i.classList.contains('cafeMarcado') || 
        i.classList.contains('almocoMarcado')
    );

    const idsSelecionados = segundaList.map(i => i.id); // Pega os IDs

    // console.log(idsSelecionados);

    valores = {
        "segunda-manha": 0,
        "segunda-almoco": 0,
        "segunda-tarde": 0,
        "terca-manha": 0,
        "terca-almoco": 0,
        "terca-tarde": 0,
        "quarta-manha": 0,
        "quarta-almoco": 0,
        "quarta-tarde": 0,
        "quinta-manha": 0,
        "quinta-almoco": 0,
        "quinta-tarde": 0,
        "sexta-manha": 0,
        "sexta-almoco": 0,
        "sexta-tarde": 0,
    }

    
    // Loop para atualizar os valores com base nos itens selecionados
    idsSelecionados.forEach(id => {
        if (valores.hasOwnProperty(id)) {
            valores[id] = 1; // Atualiza o valor para 1 se o id estiver nos selecionados
        }
    });
    
    // console.log(valores);

    // Objeto para armazenar os valores organizados
    const organizados = {
        "segunda": [],
        "terca": [],
        "quarta": [],
        "quinta": [],
        "sexta": []
    };

    // Mapeia os períodos
    const periodos = ["manha", "almoco", "tarde"];

    // Preenche o objeto organizado
    for (const dia of Object.keys(organizados)) {
        for (const periodo of periodos) {
            const chave = `${dia}-${periodo}`;
            organizados[dia].push(valores[chave] || 0); // Adiciona 0 se a chave não existir
        }
    }

    console.log('organizados',organizados);

    axios.post('/', organizados)
        .then(function(response){
            //console.log(response.data);
            console.log(response.data," adicionado com sucesso!");
            alert('Refeição Confirmada');
        })
        .catch(function (error) {
            // manipula erros da requisição
            console.error(error);
        })

})

