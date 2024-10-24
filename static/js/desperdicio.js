document.getElementById('btn-wasteConfirm').addEventListener('click', () => {
    wasteNumber = document.getElementById('inputNumDesperdicio').value;
    date = document.getElementById('date').value;
    
    axios.post('/registrarDesperdicio', {'waste': wasteNumber, 'date': date})
    .then(function(response){
        //console.log(response.data['value']);
        if (response.data['value'] == true) {
            Swal.fire({
                title: "Bom Trabalho!",
                text: "Registro de desperdício feito com sucesso!",
                icon: "success"
              });
        } 
    })
    .catch(function(error){
        console.error(error);
    });
});