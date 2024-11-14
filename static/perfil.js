const editimageOpen = document.querySelector(".edit-icon"),
      corpoedit = document.querySelector(".corpo"),
      editimageClose = document.querySelector(".img-close");

editimageOpen.addEventListener("click", () => {
    corpoedit.classList.add("editimg");
});

editimageClose.addEventListener("click", () => {
    corpoedit.classList.remove("editimg");
});

// Função para enviar a imagem de perfil via AJAX
function uploadImage() {
    const fileInput = document.getElementById('upload-input');
    const file = fileInput.files[0];
    
    if (file) {
      const formData = new FormData();
      formData.append('profile_image', file);

      // Faz a requisição para o backend para upload da imagem
      fetch('/upload_profile_image', {
        method: 'POST',
        body: formData
      })
      .then(response => response.json())
      .then(data => {
        if (data.success) {
          // Atualiza a imagem de perfil no frontend
          document.getElementById('profile-pic').src = data.image_url;
          alert('Imagem de perfil atualizada com sucesso!');

          // Atualiza a página automaticamente após o upload da imagem
          location.reload(); // Isso vai recarregar a página para refletir as mudanças
        } else {
          alert(data.error || 'Erro ao atualizar a imagem.');
        }
      })
      .catch(error => {
        console.error("Erro ao fazer upload:", error);
        alert('Erro ao tentar fazer upload da imagem.');
      });
    }
}


// Espera o DOM carregar completamente antes de rodar o código
document.addEventListener('DOMContentLoaded', function () {
  // Seleciona o campo de pesquisa
  const pesquisarInput = document.getElementById('pesquisar');

  // Seleciona todas as divs de conteúdo com a classe 'box_content'
  const boxContentDivs = document.querySelectorAll('.box_content');

  // Evento que detecta quando o usuário digita
  pesquisarInput.addEventListener('input', function() {
      // Recupera o valor digitado no campo de pesquisa
      const pesquisaTermo = pesquisarInput.value.toLowerCase(); // Converte para minúsculas para facilitar a comparação

      // Loop por todas as divs de conteúdo
      boxContentDivs.forEach(function(box) {
        // Busca o nome da URL dentro da div, que está em <strong>{{ dado.nome_url }}</strong>
        const nomeUrl = box.querySelector('.name_url').innerText.toLowerCase(); // Também converte para minúsculas

        // Se o nome da URL contém o texto digitado, mostra a div, senão, oculta
        if (nomeUrl.includes(pesquisaTermo)) {
          box.style.display = ''; // Exibe a div
        } 
        else {
          box.style.display = 'none'; // Oculta a div
        }
    });
  });
});

function toggleContent() {
  const content = document.getElementById("content");
  content.classList.toggle("show");
}


function toggleInfoContent(icon) {
  // Seleciona o elemento `.info_content` correspondente ao ícone clicado
  const infoContent = icon.parentElement.nextElementSibling;

  // Alterna a classe `show` na `info_content` e o ícone de seta
  if (icon.classList.contains("uil-angle-up")) {
      infoContent.classList.add("show");
      icon.classList.remove("uil-angle-up");
      icon.classList.add("uil-angle-down");
  } else {
      infoContent.classList.remove("show");
      icon.classList.remove("uil-angle-down");
      icon.classList.add("uil-angle-up");
  }
}

document.querySelectorAll(".trash2").forEach(trashIcon => {
  trashIcon.addEventListener("click", function() {
      const boxContent = this.closest(".box_content"); // Seleciona o item inteiro para remover
      const itemId = boxContent.getAttribute("data-id"); // Obtém o ID do item (que será adicionado no HTML)

      if (itemId) {
          fetch(`/deletar_url/${itemId}`, {
              method: 'POST',
              headers: {
                  'Content-Type': 'application/json'
              }
          })
          .then(response => response.json())
          .then(data => {
              if (data.success) {
                  boxContent.remove(); // Remove o item da página
                  alert(data.message);
              } else {
                  alert(data.message);
              }
          })
          .catch(error => console.error('Erro ao deletar:', error));
      }
  });
});