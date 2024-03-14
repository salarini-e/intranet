function inserirRamalNoTopoTabela(ramal) {
    var tabela = document.querySelector('.table tbody'); // seleciona o corpo da tabela

    var novaLinha = document.createElement('tr'); // cria uma nova linha

    // Adiciona as células com os dados do ramal
    novaLinha.innerHTML = `
        <td class="cell bg-gray"><i class="fa-solid fa-pen-to-square"></i></td>
        <td class="cell bg-gray"><span class="truncate">${ramal.secretaria}</span></td>
        <td class="cell bg-gray">${ramal.setor}</td>
        <td class="cell bg-gray">${ramal.referencia}</td>
        <td class="cell bg-gray">${ramal.responsavel}</td>
        <td class="cell bg-gray">${ramal.numero}</td>        
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
    formData.append('responsavel', document.getElementById('setting-input-4').value);
    formData.append('numero', document.getElementById('setting-input-5').value);    

    formData.append('csrfmiddlewaretoken', csrf_token);

    postRequest('/telefonia/api/criar-ramal/', formData)
    .then(data => {
        if (data.status == 400){
            alert(data.message);
        }else if(data.status==200){
            modal.style.display = 'none';            
            inserirRamalNoTopoTabela(data.ramal);						
            document.getElementById('response-message').innerText = data.message;
            document.getElementById('message').style.display = 'block';
        }
         
    });
}	

function montarSelect(dados) {						
						
    if (typeof dados === 'string') {
        dados = JSON.parse(dados);
    }
    
    var select = document.getElementById("setting-input-2");
    select.innerHTML = '<option value="none">Selecione um setor</option>';

    if (dados && Array.isArray(dados.setores)) {
        dados.setores.forEach(function(setor) {
            var option = document.createElement("option"); 
            option.value = setor.id;
            option.textContent = setor.nome; 
            select.appendChild(option); 
        });
    } else {
        console.error("A propriedade 'setores' não está presente ou não é um array nos dados recebidos.");
    }
}