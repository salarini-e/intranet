function inserirRamalNoTopoTabela(ramal) {
    var tabela = document.querySelector('.table tbody'); // seleciona o corpo da tabela

    var novaLinha = document.createElement('tr'); // cria uma nova linha

    // Adiciona as células com os dados do ramal
    novaLinha.innerHTML = `
        <td class="cell"><span class="truncate">${ramal.secretaria}</span></td>
        <td class="cell">${ramal.setor}</td>
        <td class="cell">${ramal.referencia}</td>
        <td class="cell">${ramal.numero}</td>
        <td class="cell"><a class="btn-sm app-btn-secondary rounded py-1 px-4" href="${ramal.webex}">View</a></td>
    `;

    // Insere a nova linha no topo da tabela
    tabela.insertBefore(novaLinha, tabela.firstChild);
}

function cadastrarRamal(csrf_token){
    
    const formData = new FormData();

    // Adicionar os dados ao objeto FormData
    formData.append('secretaria', document.getElementById('setting-input-1').value);
    formData.append('setor', document.getElementById('setting-input-2').value);
    formData.append('referencia', document.getElementById('setting-input-3').value);
    formData.append('numero', document.getElementById('setting-input-4').value);
    formData.append('webex', document.getElementById('setting-input-5').value);

    formData.append('csrfmiddlewaretoken', csrf_token);

    postRequest('/telefonia/api/criar-ramal/', formData)
    .then(data => {
        if (data.status == 400){
            alert(data.message);
        }else if(data.status==200){
            modal.style.display = 'none';            
            inserirRamalNoTopoTabela(data.ramal);						
            document.getElementById('response-message').innerText = data.message;
        }
         
    });
}	