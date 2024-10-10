let lastSuggestions = [];
$(document).ready(function() {
    // Inicializar el autocompletado (asumiendo que ya está definido)
  $("#url").autocomplete({
    source: "/autocomplete/",
    response: function(event, ui) {
      const searchTerm = event.target.value;
      lastSuggestions = { [searchTerm]: ui.content };
    },
    select: function(event, ui) {
      // Obtener la URL de la serie seleccionada
      let selectedSerieUrl = ui.item.url;
      // Enviar la solicitud AJAX utilizando la URL seleccionada
      getResults(selectedSerieUrl)
    }
  });

  // Selector para el botón de búsqueda
  $("#submitButton").click(function() {
    // Limpiar el div de resultados
    $('#suggestionsResult').empty();
    
    const searchTerm = $("#url").val();
    const suggestions = lastSuggestions[searchTerm] || []; // Si no hay sugerencias, devuelve un array vacío

    // Crear el div para mostrar las sugerencias
    const resultsDiv = $("<div id='suggestionsResult'></div>");
    suggestions.forEach(suggestion => {
      const suggestionElement = $(`<div class="clickable-div"><ul><li><h5>${suggestion.label}</h5></li></ul></div>`);
      suggestionElement.click(function() {
          const selectedSerieUrl = suggestion.url;
          $('#myModal').css('display', 'none');
          getResults(selectedSerieUrl)
      });
      resultsDiv.append(suggestionElement);
    });

    $("#btn-close").click(function() {
      $('#myModal').css('display', 'none');
    });

    // reemplaza el contenido del cuerpo del modal
    $('#myModal .modall-body').html(resultsDiv);
    // Mostrar el modal
    $('#myModal').css('display', 'block');
  });

  function getResults(selectedSerieUrl) {
     // Mostrar el loader
      showLoader();
    $.ajax({
      type: "GET",
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

  function showLoader() {
      $("#loader").show();
  }

  function hideLoader() {
      $("#loader").hide();
  }
});