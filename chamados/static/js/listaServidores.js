document.addEventListener('DOMContentLoaded', function() {
    const modal = document.querySelector('#modal');
    const buttonYes = document.querySelector('#buttonYes');
    const buttonNo = document.querySelector('#buttonNo');
    const fecharSair = document.querySelector('.fechar-sair');
    const btnsApagar = document.querySelectorAll('.btn-apagar');

    let servidorIdToDelete;

    btnsApagar.forEach(btnApagar => {
        btnApagar.addEventListener('click', function (e) {
            e.preventDefault();
            modal.style.display = 'block';
            servidorIdToDelete = this.getAttribute('data-servidor-id');
        });
    });

    buttonNo.addEventListener('click', function(){
        modal.style.display = 'none';
    });

    buttonYes.addEventListener('click', function(){
        if (servidorIdToDelete) {
                window.location.href = "/apagaServidor/" + servidorIdToDelete
        }
    });

    fecharSair.addEventListener('click', function(){
        modal.style.display = 'none';
    });

});
