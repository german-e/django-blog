/*!
* Start Bootstrap - Blog Post v5.0.9 (https://startbootstrap.com/template/blog-post)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-blog-post/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project

document.addEventListener("DOMContentLoaded", function () {
  const loginForm = document.getElementById("loginForm");
  const errorDiv = document.getElementById("loginError");
  

// Cuando se hace clic en el enlace que abre el modal
const loginLinks = document.querySelectorAll('[data-bs-target="#loginModal"]');
const nextInput = document.getElementById("nextInput");

 
  loginLinks.forEach(link => {
    link.addEventListener("click", function () {
      const next = this.getAttribute("data-next");
      if (nextInput) {
        nextInput.value = next;
      }
    });
  });



  loginForm.addEventListener("submit", async function (e) {
    e.preventDefault(); // ✅ Evita envío normal

    const formData = new FormData(loginForm);
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    console.log('Mi formData tiene estos valores: '+ formData);
    try {
      const response = await fetch(loginForm.action, {
        method: "POST",
        headers: {
          "X-CSRFToken": csrfToken,
          "X-Requested-With": "XMLHttpRequest"
        },
        body: formData
      });

      const data = await response.json();


      
      if (data.success) {
        // ✅ Redirige a la URL indicada (o recarga)
        window.location.href = data.redirect_url || "/";
      } else {
        // ❌ Mostrar error
        errorDiv.textContent = data.error || "Error al iniciar sesión";
        errorDiv.classList.remove("d-none");
      }
    } catch (error) {
      errorDiv.textContent = "Error de conexión con el servidor.";
      errorDiv.classList.remove("d-none");
    }
  });
});



//Funcion javascript para darle al boton like sin recargar la página

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.btn-like').forEach(btn => {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const postId = this.dataset.id;
      
      const url = this.dataset.url;
      console.log('Se hizo clic en el boton con url: ', url);

      //anterior: fetch(`blog/posts/${postId}/like/`

      fetch(url, {
        method: 'POST',
        headers: {
          'X-CSRFToken': getCookie('csrftoken'),
          'X-Requested-With': 'XMLHttpRequest',
        }
      })
      .then(response => response.json())
      .then(data => {
        const container = document.getElementById(`like-container-${postId}`);
        const icon = container.querySelector('i');
        const count = container.querySelector('.like-count');

        if (data.dio_like) {
          icon.className = 'bi bi-heart-fill text-danger';
        } else {
          icon.className = 'bi bi-heart';
        }
        count.textContent = data.likes;
      });
    });
  });
});

// Función para obtener CSRF token de la cookie
function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
      cookie = cookie.trim();
      if (cookie.startsWith(name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}

