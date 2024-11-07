function imprimir() {
    let table = document.getElementById('table-day');
    print(table);
}

axios.get('/getRelatorio')
.then(function(response){
    console.log(response.data);
})
.catch(function(error){
    console.error(error);
})