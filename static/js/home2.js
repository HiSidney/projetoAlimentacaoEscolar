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
  