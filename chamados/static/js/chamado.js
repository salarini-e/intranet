const prioridadeChamado = document.getElementById('prioridade-chamado')
const statusChamado = document.querySelector('#status-chamado')
const atendenteResponsavel = document.querySelector('#atendente-responsavel')

if(prioridadeChamado.textContent == "Prioridade: Média"){
    prioridadeChamado.style.border = '1px solid orange'
}

if(prioridadeChamado.textContent == "Prioridade: Alta"){
    prioridadeChamado.style.border = '1px solid red'
}

if(prioridadeChamado.textContent == "Prioridade: Baixa"){
    prioridadeChamado.style.border = '1px solid blue'
}

if(statusChamado.textContent == "Status: Aberto"){
    statusChamado.style.border = '1px solid green'
}

if(statusChamado.textContent == "Status: Pendente"){
    statusChamado.style.border = '1px solid orange'
}

if(statusChamado.textContent == "Status: Finalizado"){
    statusChamado.style.border = '1px solid red'
}

if (atendenteResponsavel.textContent != 'Atendente responsável: None'){
    atendenteResponsavel.style.border = '1px solid blue'
}

if(atendenteResponsavel.textContent == 'Atendente responsável: None'){
    atendenteResponsavel.textContent = 'Atendente responsável: Nenhum'
}

const submitChamado = document.querySelector('#submit-chamado');

submitChamado.addEventListener('click', e =>{
    submitChamado.setAttribute("disabled", "disabled");
    submitChamado.textContent = "Enviando Comentário...";
    submitChamado.style.background = "rgb(4,177,53)"
    submitChamado.style.transition = "ease 3s"
    submitChamado.classList.add('btn-success')
    document.getElementById('formComentario').submit();
});