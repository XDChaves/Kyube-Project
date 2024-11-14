const textarea = document.getElementById('myTextarea');
const maxHeight = textarea.style.maxHeight;
const maxChars = 1000;

textarea.addEventListener('input', () => {
  // Se o número de caracteres ultrapassar o limite, corta o valor
  if (textarea.value.length > maxChars) {
    textarea.value = textarea.value.slice(0, maxChars);
  }

  // Ajusta a altura automaticamente
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';

  // Limita o texto ao tamanho máximo
  if (textarea.scrollHeight > parseInt(maxHeight)) {
    textarea.value = textarea.value.slice(0, -1);
  }
});

const TEXT = document.getElementById('nome_url');
const maxCharsNOME = 80;

TEXT.addEventListener('input', () => {
  // Se o número de caracteres ultrapassar o limite, corta o valor
  if (TEXT.value.length > maxCharsNOME) {
    TEXT.value = TEXT.value.slice(0, maxCharsNOME);
  }
});

const trashIcon = document.querySelector(".trash1");
const forme = document.getElementById("bloco");

trashIcon.addEventListener("click", () => {
    // Seleciona todos os campos de input e textarea dentro do formulário
    const inputs = forme.querySelectorAll("input, textarea");
    
    // Limpa o valor de cada campo
    inputs.forEach(input => input.value = "");
});

const send_url = document.getElementById('bloco'),
  nome_url = document.getElementById('nome_url'),
  url = document.getElementById('url'),
  errorMessage = document.getElementById('errorMessage');

send_url.addEventListener('submit', (event) => {
    event.preventDefault();

    // Verifica se todos os campos estão preenchidos
    if (!nome_url.value || !url.value){
        errorMessage.textContent = '';
        errorMessage.textContent = 'Os campos NOME e URL são obrigatórios.';
        return;  // Interrompe a execução se esse erro for encontrado
    }

    // Se todas as verificações passarem, permite o envio do formulário
    send_url.submit();
});