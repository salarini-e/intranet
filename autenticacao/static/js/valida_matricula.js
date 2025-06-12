export const validarMatricula = async (matricula, secretarias) => {
    const mostrarErro = (mensagem) => {
        document.getElementById("error").innerText = mensagem;
    };

    const setEstadoValidacao = (validando) => {
        const btn = document.getElementById("validar");
        const img = document.getElementById("loading_validar");
        const text = document.getElementById("btn_text");
        const cadastrar = document.getElementById("cadastrar");

        btn.classList.remove("btn-success", "btn-secondary", "btnValidar");
        text.classList.remove("text_loading");
        img.classList.remove("loading_image");

        if (validando) {
            mostrarErro("");
            btn.classList.add("btn-secondary", "btnValidar");
            text.classList.add("text_loading");
            img.classList.add("loading_image");
            cadastrar.disabled = false;
        } else {
            cadastrar.disabled = true;
        }
    };

    if (matricula == "000000") {
        mostrarErro("Preencha a matrícula");
        return;
    }

    setEstadoValidacao(true);
    alert("Aguarde enquanto sua matrícula é validada!");

    const ano = new Date().getFullYear();
    const mesAtual = new Date().getMonth() + 1;
    console.log("secretarias: ", secretarias);
    try {
        for (let m = mesAtual; m >= 1; m--) {
            const mes = m < 10 ? `0${m}` : `${m}`;
            const url = `/get-matriculas/${ano}/${mes}`;
            const response = await fetch(url);
            const servidores = await response.json();

            const encontrado = servidores.find(
                (s) => s.matricula === matricula
            );
            if (encontrado) {
                console.log("achei");
                console.log(encontrado);
                setEstadoValidacao(false);
                montarSelect(JSON.stringify(encontrado));
                return;
            }
        }

        // Aqui: matrícula não foi encontrada
        console.log("Matrícula não encontrada");
        setEstadoValidacao(false);
        mostrarErro("Não foi possível encontrar sua matrícula!");
    } catch (err) {
        console.error("Erro ao buscar matrícula:", err);
        setEstadoValidacao(false);
        mostrarErro("Erro na validação. Tente novamente mais tarde.");
    }
};

function montarSelect(response) {
    console.log();
    var form = document.getElementById("novos-inputs");
    document.getElementById("error").innerHTML = "";

    // Create input for name
    var nameInput = document.createElement("input");
    nameInput.type = "text";
    nameInput.className = "form-control bg-readonly mb-3";
    nameInput.id = "nome";
    nameInput.name = "nome";
    nameInput.required = true;
    nameInput.readOnly = true;

    var nameLabel = document.createElement("label");
    nameLabel.for = "nome";
    nameLabel.className = "form-label";
    nameLabel.innerHTML = "Nome";

    // Create input for CPF Oculto
    var cpfOcultoInput = document.createElement("input");
    cpfOcultoInput.type = "text";
    cpfOcultoInput.className = "form-control bg-readonly mb-3";
    cpfOcultoInput.id = "cpf_oculto";
    cpfOcultoInput.name = "cpf_oculto";
    cpfOcultoInput.required = true;
    cpfOcultoInput.readOnly = true;

    var cpfOcultoLabel = document.createElement("label");
    cpfOcultoLabel.for = "cpf";
    cpfOcultoLabel.className = "form-label";
    cpfOcultoLabel.innerHTML = "CPF";

    // Create input for CPF
    var cpfInput = document.createElement("input");
    cpfInput.type = "text";
    cpfInput.className = "form-control";
    cpfInput.id = "cpf";
    cpfInput.name = "cpf";
    cpfInput.required = true;

    var cpfLabel = document.createElement("label");
    cpfLabel.for = "cpf";
    cpfLabel.className = "form-label";
    cpfLabel.innerHTML = "Confirme seu CPF";

    var divErrorCpf = document.createElement("div");
    divErrorCpf.className = "row mt-1";

    var cpfSmall = document.createElement("small");
    cpfSmall.id = "errorCPF";
    cpfSmall.className = "text-danger";

    // Create select for Secretaria
    var secretariaSelect = document.createElement("select");
    secretariaSelect.className = "form-control bg-readonly";
    secretariaSelect.id = "secretaria";
    secretariaSelect.required = true;
    secretariaSelect.readOnly = true;
    secretariaSelect.name = "secretaria";

    var secretariaLabel = document.createElement("label");
    secretariaLabel.for = "secretaria";
    secretariaLabel.className = "form-label mt-3";
    secretariaLabel.innerHTML = "Secretaria";

    var option1 = document.createElement("option");
    secretariaSelect.add(option1);
    secretariaSelect.tabIndex = "-1";
    secretariaSelect.setAttribute("aria-disabled", "true");

    // Append to form
    form.appendChild(nameLabel);
    form.appendChild(nameInput);
    form.appendChild(cpfOcultoLabel);
    form.appendChild(cpfOcultoInput);
    form.appendChild(cpfLabel);
    form.appendChild(cpfInput);
    form.appendChild(divErrorCpf);
    divErrorCpf.appendChild(cpfSmall);
    form.appendChild(secretariaLabel);
    form.appendChild(secretariaSelect);

    response = JSON.parse(response);
    option1.value = response.secretaria?.id || "";
    option1.text = response.secretaria || "Secretaria não informada";
    nameInput.value = response.nome;
    cpfOcultoInput.value = response.documento;

    // Setor fixo N/H
    var setorLabel = document.createElement("label");
    setorLabel.for = "setor";
    setorLabel.className = "form-label mt-3";
    setorLabel.innerHTML = "Setor";

    var setorSelect = document.createElement("select");
    setorSelect.className = "form-select";
    setorSelect.id = "setor";
    setorSelect.name = "setor";
    setorSelect.required = true;
    setorSelect.disabled = true; // Desabilitado visualmente

    var optionSetor = document.createElement("option");
    optionSetor.value = "N/H";
    optionSetor.text = "N/H";
    optionSetor.selected = true;
    setorSelect.appendChild(optionSetor);

    // Input hidden para envio do valor
    var setorHiddenInput = document.createElement("input");
    setorHiddenInput.type = "hidden";
    setorHiddenInput.name = "setor";
    setorHiddenInput.value = "N/H";

    form.appendChild(setorLabel);
    form.appendChild(setorSelect);
    form.appendChild(setorHiddenInput);

    // Email
    var emailInput = document.createElement("input");
    emailInput.type = "email";
    emailInput.className = "form-control mb-3";
    emailInput.id = "email";
    emailInput.name = "email";
    emailInput.required = true;

    var emailLabel = document.createElement("label");
    emailLabel.for = "email";
    emailLabel.className = "form-label mt-3";
    emailLabel.innerHTML = "Digite seu email";
    form.appendChild(emailLabel);
    form.appendChild(emailInput);

    // Telefone
    var telefoneInput = document.createElement("input");
    telefoneInput.type = "tel";
    telefoneInput.className = "form-control mb-3";
    telefoneInput.id = "telefone";
    telefoneInput.name = "telefone";
    telefoneInput.required = true;

    var telefoneLabel = document.createElement("label");
    telefoneLabel.for = "telefone";
    telefoneLabel.className = "form-label";
    telefoneLabel.innerHTML = "Digite seu telefone";
    form.appendChild(telefoneLabel);
    form.appendChild(telefoneInput);

    // Data de nascimento
    var dtNascimentoInput = document.createElement("input");
    dtNascimentoInput.type = "date";
    dtNascimentoInput.className = "form-control mb-3";
    dtNascimentoInput.id = "dt_nascimento";
    dtNascimentoInput.name = "dt_nascimento";
    dtNascimentoInput.required = true;

    var dtNascimentoLabel = document.createElement("label");
    dtNascimentoLabel.for = "dt_nascimento";
    dtNascimentoLabel.className = "form-label";
    dtNascimentoLabel.innerHTML = "Digite sua data de nascimento";
    form.appendChild(dtNascimentoLabel);
    form.appendChild(dtNascimentoInput);

    // Máscaras e validações
    cpfInput.addEventListener("keyup", function () {
        mascara(cpfInput, icpf);
        checkInputLength(cpfInput.id);
    });

    telefoneInput.addEventListener("keyup", function () {
        mascara(telefoneInput, itel);
    });

    // Reset de carregamento
    textValidar = document.getElementById("btn_text");
    imageValidar = document.getElementById("loading_validar");
    textValidar.classList.remove("text_loading");
    imageValidar.classList.remove("loading_image");
}
