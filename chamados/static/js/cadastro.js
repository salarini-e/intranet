const userField = document.querySelector('#id_username');
userField.setAttribute('placeholder', 'Insira o seu nome de usuário de identificação do sistema. Não pode conter espaços, letras maiúsculas ou números. Exemplo: joao_silva')

const passwordField = document.querySelector('#id_password1');
passwordField.setAttribute('placeholder', 'Insira uma senha com, no mínimo, 8 caracteres contendo pelo menos um número. Lembre-se: sua senha não pode ser parecida com o seu usuário.')

const confirmField = document.querySelector('#id_password2');
confirmField.setAttribute('placeholder', 'Confirme a sua senha.')

const nameField = document.querySelector('#id_nome');
nameField.setAttribute('placeholder', 'Insira nome e sobrenome. Exemplo: João Silva')

const phoneField = document.querySelector('#id_contato');
phoneField.setAttribute('placeholder', 'Exemplo: +5522999994444')

const emailField = document.querySelector('#id_email');
emailField.setAttribute('placeholder', 'joao@example.com')