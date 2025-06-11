
export const validarMatricula = async (matricula) => {
    
    const ano = new Date().getFullYear();
    // const mesAtual = new Date().getMonth() + 1;
    const mesAtual = 2;


    for (let mes = mesAtual; mes >= 1 ; mes--) {
        mes = mes < 10 ? `0${mes}` : mes;

        const url = `/get-matriculas/${ano}/${mes}`
        const response = await fetch(url)

        if (!response.ok) {
            throw new Error(`Erro ao buscar matricula para fazer validação: ${response.statusText}`);
        }

        const data = await response.json();
        console.log(data);
    }

};
