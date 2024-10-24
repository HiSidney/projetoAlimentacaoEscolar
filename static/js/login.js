document.getElementById('btn-login').addEventListener('click', function (){
    const status = document.querySelector('input[name="status"]:checked').id;

    if(status == 'aluno'){
        window.location.href = '/';
    } else {
        window.location.href = '/relatorio';
    }
})