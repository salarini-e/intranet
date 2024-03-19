document.addEventListener('DOMContentLoaded', function() {
    const modal = document.querySelector('#modal');
    const buttonYes = document.querySelector('#buttonYes');
    const buttonNo = document.querySelector('#buttonNo');
    const fecharSair = document.querySelector('.fechar-sair');
    const btnsApagar = document.querySelectorAll('.btn-apagar');

    let atendenteIdToDelete;

    btnsApagar.forEach(btnApagar => {
        btnApagar.addEventListener('click', function (e) {
            e.preventDefault();
            modal.style.display = 'block';
            atendenteIdToDelete = this.getAttribute('data-atendente-id');
        });
    });

    buttonNo.addEventListener('click', function(){
        modal.style.display = 'none';
    });

    buttonYes.addEventListener('click', function(){
        if (atendenteIdToDelete) {
                window.location.href = "/transformaParaServidor/" + atendenteIdToDelete
        }
    });

    fecharSair.addEventListener('click', function(){
        modal.style.display = 'none';
    });

});
