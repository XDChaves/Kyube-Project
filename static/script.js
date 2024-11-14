const password = document.querySelectorAll('#password1, #password2, #password3');

const formOpenBtn = document.querySelector("#form-open"),
    corpo = document.querySelector(".corpo"),
    formulariolog = document.querySelector(".formulario"),
    signupBtn = document.querySelector("#form_cad"),
    loginBtn = document.querySelector("#form_log"),
    pw_hide = document.querySelectorAll(".eyes"),
    formCloseBtn = document.querySelector(".form-close");

function resetPasswordFields() {
    // Define todos os inputs de senha para o tipo 'password'
    password.forEach((input) => {
        input.setAttribute('type', 'password');
    });

    // Define todos os ícones para 'uil-eye-slash'
    pw_hide.forEach((icon) => {
        icon.classList.remove('uil-eye');
        icon.classList.add('uil-eye-slash');
    });
}

formOpenBtn.addEventListener("click", () => {
    corpo.classList.add("show");
    resetPasswordFields();
});

formCloseBtn.addEventListener("click", () => {
    corpo.classList.remove("show");
    formulariolog.classList.remove("active");

    // Limpa todos os campos de entrada na seção de formulário
    document.querySelectorAll('.formulario input').forEach((input) => {
        input.value = '';  // Apaga o conteúdo dos inputs
    });

    // Limpa as mensagens de erro, se houver
    const errorMessages = document.getElementById('errorMessages');
    if (errorMessages) {
        errorMessages.textContent = '';
    }

    // Reseta os campos de senha e ícones
    resetPasswordFields();
});

signupBtn.addEventListener("click", (e) => {
    e.preventDefault();
    formulariolog.classList.add("active");
    
    const errorMessages = document.getElementById('errorMessages');
    if (errorMessages) {
        errorMessages.textContent = '';
    }

    resetPasswordFields();
});

loginBtn.addEventListener("click", (e) => {
    e.preventDefault();
    formulariolog.classList.remove("active");
    
    const errorMessages = document.getElementById('errorMessages');
    if (errorMessages) {
        errorMessages.textContent = '';
    }

    resetPasswordFields();
});

pw_hide.forEach((icon) => {
    icon.addEventListener("click", () => {
        let getPwInput = icon.parentElement.querySelector("input");
        if (getPwInput.type === "password") {
            getPwInput.type = "text";
            icon.classList.replace("uil-eye-slash", "uil-eye");
        } else {
            getPwInput.type = "password";
            icon.classList.replace("uil-eye", "uil-eye-slash");
        }
    });
});

document.addEventListener("DOMContentLoaded", function() {
    // Verifica se existe uma mensagem flash de necessidade de login
    const flashMessages = document.querySelectorAll(".flash-message");
    if (flashMessages.length > 0) {
        // Adiciona a classe 'show' para abrir o formulário automaticamente
        document.querySelector(".corpo").classList.add("show");
    }
});
