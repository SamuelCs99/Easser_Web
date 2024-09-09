$(document).ready(function() {
    // Inicializar el autocompletado (asumiendo que ya está definido)
    $("#url").autocomplete({
      source: "/autocomplete/",
      select: function(event, ui) {
        // Mostrar el loader
        showLoader();

        // Obtener la URL de la serie seleccionada
        var selectedSerieUrl = ui.item.url;
  
        // Enviar la solicitud AJAX utilizando la URL seleccionada
        $.ajax({
          type: "POST",
          url: $("#series-form").data("url"),
          data: {
            url: selectedSerieUrl,
            csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
          },
          // Resto del código de la solicitud AJAX
          success: function(response) {
            // Ocultar el loader
            hideLoader();

            // Actualizar el contenido de resultados
            $("#results-container").html(response);
        },
        error: function() {
            // Ocultar el loader en caso de error
            hideLoader();

            // Mostrar un mensaje de error o realizar alguna acción adicional
            console.error('Error al obtener los resultados');
        }
        });
      }
    });

    function showLoader() {
        $("#loader").show();
    }

    function hideLoader() {
        $("#loader").hide();
    }
  });