function readImage() {
    if (this.files && this.files[0]) {
        var file = new FileReader();
        file.onload = function(e) {
            document.getElementById("cinza").src = e.target.result;
        };       
        file.readAsDataURL(this.files[0]);
    }
}

document.getElementById("imgChooser").addEventListener("change", readImage, false);

function confirmacaoAtualizacaoCalendario() {
    const imgCardapio = document.getElementById('imgChooser');
    const data1 = document.getElementById('date1').value;
    const data2 = document.getElementById('date2').value;
    
    // Verifica se algum arquivo foi selecionado
    if (imgCardapio.files.length > 0) {
        const arquivo = imgCardapio.files[0]; // Pega o primeiro arquivo
        
        // Cria um FormData para enviar o arquivo
        const formData = new FormData();
        formData.append('file', arquivo);
        formData.append('date1', data1);
        formData.append('date2', data2);

        console.log(formData);

        // Envia o arquivo com Axios
        axios.post('/uploudImgCardapio', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        })
        .then(response => {
            console.log('Arquivo enviado com sucesso:', response.data);
        })
        .catch(error => {
            console.error('Erro ao enviar arquivo:', error);
        });
        
    } else {
        console.log('Nenhum arquivo selecionado.');
    }
}

document.getElementById('confirmacaoDasAtividadesEventos').addEventListener('click', () => {
    
    data = document.getElementById('dateT').value;

    checkboxesRefeicoes = document.querySelectorAll('input[name="refeicao"]:checked');
    refeicoes = [];
    Array.from(checkboxesRefeicoes).map(i => refeicoes.push(i.id));

    valores = {
        "date": data,
        "manha": 0,
        "almoco": 0,
        "tarde": 0,
    }

    if (refeicoes.includes('manha')) {
        valores.manha = 1;
    }
    if (refeicoes.includes('almoco')) {
        valores.almoco = 1;
    }
    if (refeicoes.includes('tarde')) {
        valores.tarde = 1;
    }

    console.log(data);
    console.log(refeicoes);
    console.log(valores);

    axios.post('/atualizacaoCardapio', valores)
        .then(function(response){
            //console.log(response.data);
            alert(response.data," adicionado com sucesso!")
        })
        .catch(function (error) {
            // manipula erros da requisição
            console.error(error);
        })

})
    

document.getElementById('btn-enviar-notificacao').addEventListener('click', () => {
    const notificaco = document.getElementById('informacoes').value;

    axios.post('/salvar-notificacao', Notificacao = {'text':notificaco})
    .then(function(response){
        console.log(response.data);
        alert('sucess');
    })
    .catch(function(error){
        console.error(error);
    })
})