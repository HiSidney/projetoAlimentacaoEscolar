function abrirConfirmacaoRefeicao(){
    const confirmacaoRefeicao = document.getElementById('janela-modal-confirmacaoRefeicao');
    confirmacaoRefeicao.classList.add('abrir');

    confirmacaoRefeicao.addEventListener('click', (e) => {
        if(e.target.id == 'cancelarConfirmacao' || e.target.id == 'janela-modal-confirmacaoRefeicao' || e.target.id == 'confirmaRefeicao'){
            confirmacaoRefeicao.classList.remove('abrir')
        }
    });
};

document.getElementById('confirmaRefeicao').addEventListener('click', function () {
    const modalUser = document.getElementById('janela-modal-user');
    modalUser.classList.add('abrir');

    modalUser.addEventListener('click', (e) => {
        if(e.target.id == 'janela-modal-user' || e.target.id == 'sairConta'){
            modalUser.classList.remove('abrir')
        }
    });
});





function confirmacaoDaConfirmacao(){
    Swal.fire({
        title: "Good job!",
        text: "Plano Concluido!",
        icon: "success"
      });
};

function cancelamentoDaConfirmacao(){
    Swal.fire({
        title: "Oh no...",
        text: "Você cancelou o plano!",
        icon: "error"
      });
};

function confirmacaoAtualizacaoCalendario(){
    Swal.fire({
        title: "Good job!",
        text: "Atualização do Cardápio Concluido!",
        icon: "success"
      });
};

function confirmacaoDasAtividadesEventos(){
    Swal.fire({
        title: "Good job!",
        text: "Atividades/Eventos Concluidos!",
        icon: "success"
      });
};

function confirmacaoDoRegistroDesperdicio(){
    Swal.fire({
        title: "Good job!",
        text: "Registro de Desperdício Concluido!",
        icon: "success"
      });
};