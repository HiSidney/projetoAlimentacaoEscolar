const todasAsDivs = document.querySelectorAll('.cafeManha, .almoco, .cafeTarde');

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

    console.log(idsSelecionados);

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
    
    console.log(valores);

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

    console.log(organizados);

    axios.post('/', organizados)
        .then(function(response){
            //console.log(response.data);
            console.log(response.data," adicionado com sucesso!")
        })
        .catch(function (error) {
            // manipula erros da requisição
            console.error(error);
        })

})

