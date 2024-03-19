const cep = document.getElementById('id_cep');

cep.addEventListener('change', event => {
    console.log("peguei o cep");
    buscaEnderecoPorCEP(cep.value)
});

function buscaEnderecoPorCEP(cep) {
    // Limpa os campos de endereço
    document.getElementById('id_bairro').value = '';
    document.getElementById('id_logradouro').value = '';
  
    // Verifica se o CEP possui o formato correto
    if (cep.length !== 8 || isNaN(cep)) {
      alert('CEP inválido');
      return;
    }
  
    // Faz a requisição à API ViaCEP
    fetch(`https://viacep.com.br/ws/${cep}/json/`)
      .then(response => response.json())
      .then(data => preencheCamposEndereco(data))
      .catch(error => console.error('Erro ao buscar endereço:', error));
  }
  
  function preencheCamposEndereco(data) {
    if (data.erro) {
      alert('CEP não encontrado');
      return;
    }
  
    // Preenche os campos do endereço
    document.getElementById('id_logradouro').value = data.logradouro;
    document.getElementById('id_bairro').value = data.bairro;
  }
  