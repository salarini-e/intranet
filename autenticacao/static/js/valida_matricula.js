
export const validarMatricula = async (matricula) => {
    
    if (matricula == "000000"){
        document.getElementById('error').innerText = 'Preencha a matrícula';
        return

    } else {
        let btnValidar = document.getElementById('validar');  
        let imageValidar = document.getElementById('loading_validar');   
        let textValidar = document.getElementById('btn_text');      
        btnValidar.classList.remove('btn-success');
        btnValidar.classList.add('btn-secondary');
        btnValidar.classList.add('btnValidar');
        textValidar.classList.add('text_loading');
        imageValidar.classList.add('loading_image');
        document.getElementById('cadastrar').disabled = false;
        alert('Aguarde enquanto sua matrícula é validada!')    
    }


    const ano = new Date().getFullYear();
    // const mesAtual = new Date().getMonth() + 1;
    const mesAtual = 1;

    for (let mes = mesAtual; mes >= 1 ; mes--) {
        mes = mes < 10 ? `0${mes}` : mes;

        const url = `/get-matriculas/${ano}/${mes}`
        const response = await fetch(url)

        if (!response.ok) {
            throw new Error(`Erro ao buscar matricula para fazer validação: ${response.statusText}`);
        }

        let servidores = await response.json();
    
        try{
            for(let servidor of servidores) {
                if (servidor.matricula == matricula){
                    console.log("achei");
                    btnValidar.classList.add('btn-success');
                    btnValidar.classList.remove('btn-secondary');
                    btnValidar.classList.remove('btnValidar');
                    textValidar.classList.remove('text_loading');
                    imageValidar.classList.remove('loading_image');
                    document.getElementById('cadastrar').disabled = true;
                    break
                }  
            }
        } catch {
            console.log("Nao foi possivel encontrar sua matricula!")
        }
        
    }

};

// function callMetaServidor(){
//     // document.getElementById('error').innerHTML = '';
//     // podeCadastrar = true;
//     // if (buttonCadastrar.classList.contains('disabled')) {
//     //     buttonCadastrar.classList.remove('disabled');
//     // }
//     // // document.getElementById('response-message').display = 'none';
//     // var matricula = document.getElementById('matricula').value; 
//     // var url = "{% url 'ins:getServidor' %}" + "?matricula=" + matricula; 
    
//     if(matricula== "000000"){
//         document.getElementById('error').innerText = 'Preencha a matrícula';
//     }
//     else{
//         getRequest(url, montarSelect);       
//         btnValidar = document.getElementById('validar');  
//         imageValidar = document.getElementById('loading_validar');   
//         textValidar = document.getElementById('btn_text');      
//         btnValidar.classList.remove('btn-success');
//         btnValidar.classList.add('btn-secondary');
//         btnValidar.classList.add('btnValidar');
//         textValidar.classList.add('text_loading');
//     imageValidar.classList.add('loading_image');
//         document.getElementById('cadastrar').disabled = false;
//         alert('Aguarde enquanto sua matrícula é validada!')
//     }
// }
    
            