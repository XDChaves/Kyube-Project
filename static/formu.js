const form = document.getElementById('validação_cad');
const emailInput = document.getElementById('email');
const nameInput = document.getElementById('nome');
const password1Input = document.getElementById('password1');
const password2Input = document.getElementById('password2');
const errorMessages = document.getElementById('errorMessages');

form.addEventListener('submit', (event) => {
    event.preventDefault();

    // Verifica se as senhas coincidem
    if (password1Input.value !== password2Input.value) {
        errorMessages.textContent = '';
        errorMessages.textContent = 'As senhas não coincidem.';
        return;  // Interrompe a execução se esse erro for encontrado
    }

    // Verifica se todos os campos estão preenchidos
    if (!emailInput.value || !nameInput.value || !password1Input.value || !password2Input.value){
        errorMessages.textContent = '';
        errorMessages.textContent = 'Todos os campos são obrigatórios.';
        return;  // Interrompe a execução se esse erro for encontrado
    }

    // Se todas as verificações passarem, permite o envio do formulário
    form.submit();
});

// Exibe as mensagens flash e as remove após 3 segundos
window.onload = function() {
    const flashMessage = document.getElementById('flash-message');
    if (flashMessage) {
        flashMessage.style.display = 'block';
        setTimeout(function() {
            flashMessage.style.display = 'none';
        }, 2000);  // Oculta após 3 segundos
    }
};

document.addEventListener("DOMContentLoaded", function () {
    const profilePic = document.getElementById("profile-pic");
  
    // Verifica se a imagem está carregada
    profilePic.onload = function () {
        profilePic.classList.add("loaded");
    };
  
    // Caso a imagem esteja em cache, força o evento onload
    if (profilePic.complete) {
        profilePic.onload();
    }
});