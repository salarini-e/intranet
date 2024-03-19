const chatSocket = new WebSocket(`ws://${window.location.host}/ws/`);

async function updateChamados(chamado){
  // Create a new table row
  var newRow = document.createElement("tr");
  newRow.className = "tr-table-chamado";

  // Create and append the cells to the new row
  var fields = chamado;
  var cells = ['numero', 'requisitante', 'prioridade', 'setor', 'status', 'tipo', 'assunto', 'dataAbertura'];
  for (var i = 0; i < cells.length; i++) {
    var cell = document.createElement("td");

    // Handle special cases for styling or content modification
    if (cells[i] === 'prioridade') {
      cell.style.color = fields.prioridade === 'Baixa' ? 'blue' : (fields.prioridade === 'Alta' ? 'red' : '#ffa500');
      cell.textContent = fields.prioridade;
    } else if (cells[i] === 'status') {
      cell.textContent = fields.status;
    } else {  
      cell.textContent = fields[cells[i]];
    }

    newRow.appendChild(cell);
  }

  // Create the last cell with the link and button
  var lastCell = document.createElement("td");
  var link = document.createElement("a");
  link.href = "/chamado/" + chamado.id;

  var button = document.createElement("button");
  button.className = "btn btn-primary button-abrir-chamado";
  button.innerHTML = '<i class="bi bi-box-arrow-up-right"></i>';

  link.appendChild(button);
  lastCell.appendChild(link);
  newRow.appendChild(lastCell);
  newRow.style.backgroundColor = '#BDECD6';

  // Get the table reference and insert the new row at the top
  var table = document.getElementById("tabelaDeChamados");
  table.insertBefore(newRow, table.firstChild);

  return true;
}

console.log(chatSocket);

//Logic to receive messages
chatSocket.addEventListener("message", event => {
    const data = JSON.parse(event.data);
    const chamado = JSON.parse(data.message);

    fetch("/userIsStaff/")
        .then(function(response) {
            return response.json();
        })
        .then(function(dados) {
          if (dados){
            updateChamados(chamado);
          }
        });

    
});

chatSocket.addEventListener("close", event => {
    console.error("The WebSocket socked unexpectedly");
});

chatSocket.addEventListener("error", (event) => {
    console.error("WebSocket error:", event);
});

document.addEventListener('DOMContentLoaded', function() {
    let buttonPesquisaChamado = document.getElementById("button-pesquisa-chamado");
    let formMainPage = document.getElementById("form-pesquisa-chamado");

    buttonPesquisaChamado.addEventListener('click', function(){
        let computedStyle = window.getComputedStyle(formMainPage);
        if (computedStyle.display === 'none') {
            formMainPage.style.display = 'block';
        } else {
            formMainPage.style.display = 'none';
        }
    });

    var modal = document.getElementById('modal');

    document.getElementById('button-chamado').addEventListener('click', function() {
        modal.style.display = 'block';
      });
      
    document.querySelector('.fechar').addEventListener('click', function(){
        modal.style.display = "none";
    })
});
