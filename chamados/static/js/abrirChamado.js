// const chatSocket = new WebSocket(`ws://${window.location.host}/ws/`);

// console.log(chatSocket);

// chatSocket.addEventListener("close", event => {
//     console.error("The WebSocket socked unexpectedly");
// });

// chatSocket.addEventListener("error", (event) => {
//     console.error("WebSocket error:", event);
// });

// const $chamadoForm = document.querySelector("#chamadoForm");

// $chamadoForm.addEventListener("submit", event => {
//     const message = true;
//     console.log("to no submit")
//     chatSocket.send(JSON.stringify({
//         "message": message
//     }));

// });

const saveButton = document.querySelector('#save-button');
const form = document.querySelector('#form-chamado');
const setorInput = document.getElementById('id_setor');

setorInput.style.width = '75%!important';

saveButton.addEventListener('click', e => {
    e.preventDefault();

    const requiredInputs = form.querySelectorAll('[required]');
    let allFieldsFilled = true;

    requiredInputs.forEach(input => {
        if (input.value.trim() === '') {
            allFieldsFilled = false;
            input.style.border = '1px solid red';
        } else {
            input.style.border = ''; 
        }
    });

    if (allFieldsFilled) {
        saveButton.setAttribute("disabled", "disabled");
        saveButton.textContent = "Gerando Chamado...";
        saveButton.style.transition = "ease 3s"
        saveButton.classList.add('btn-success')
        form.submit()
    }
});
