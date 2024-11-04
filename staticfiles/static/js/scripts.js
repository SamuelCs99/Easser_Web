//___VARIABLES-CONSTANTES___
let lastSuggestions = [];
let vista = 'forEachEpisode';
const loaderDym = $('<div id="loaderDym" class="pre-loaderDym"><div class="loader"><span class="bar"></span><span class="bar"></span> <span class="bar"></span></div><div class="loader"><p>Cargando...</p></div></div>');

//___FUNCIONES___
function getResults(selectedSerieUrl) {
  // Mostrar el loader
  showLoader();
  $.ajax({
    type: "GET",
    url: vista,
    data: {
      url: selectedSerieUrl,
      csrfmiddlewaretoken: $("input[name='csrfmiddlewaretoken']").val()
    },
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

function vdLink(anchor) {
  const url = anchor.href;

  // Comprobar si ya existe un contenedor de respuesta
  if ($(anchor).next('.respuesta').length === 0) {
    $(anchor).after(loaderDym);
    fetch(`/episode/?href=${encodeURIComponent(url)}`, {
        method: 'GET',
        headers: {
            'Content-Type': 'text/html'
        }
    })
    .then(response => response.text())
    .then(data => {
        const episodeLink = $('<div>', {
          class: 'respuesta',
          html: data
        });
        loaderDym.remove();
        $(anchor).after(episodeLink);
    })
    .catch(error => {
        console.error('Error en la solicitud GET:', error);
    });
  }
}

async function search(term) {
  try {
      const response = await fetch(`/autocomplete/?term=${encodeURIComponent(term)}`, {
          method: 'GET',
          headers: {
              'Content-Type': 'application/json'
          }
      });
      const data = await response.json();
      return data;
  } catch (error) {
      console.error('Error en la solicitud GET:', error);
  }
}

//___EVENTOS___
$(document).ready(function() {
    // Inicializar el autocompletado
  $("#url").autocomplete({
    minLength: 2,
    source: "/autocomplete/",
    response: function(event, ui) {
      const searchTerm = event.target.value;
      //Almacena la ultima sugerencia obtenida
      lastSuggestions = { [searchTerm]: ui.content };
    },
    select: function(event, ui) {
      if (ui.item.label === 'No Hay Coincidencias') {
        return false; // Prevenir acción si es "no results"
      } else {
        // Obtener la URL de la serie seleccionada
        let selectedSerieUrl = ui.item.url;
        // Enviar la solicitud AJAX utilizando la URL seleccionada
        getResults(selectedSerieUrl);
      }
    }
  }).autocomplete("instance")._renderItem = function(ul, item) {
    return $("<li>")
        .append("<div class='" + (item.label === 'No Hay Coincidencias' ? "no-results" : "") + "'>" + item.label + "</div>")
        .appendTo(ul);
};

  //Switch para elegir la vista a usar en la busqueda
  $('#flexSwitchCheckDefault').on('change', function() {
    vista = $(this).is(':checked') ? 'series' : 'forEachEpisode';
  });

  // Selector para el botón de búsqueda
  $("#submitButton").click(async function() {
    // Limpiar el div de resultados
    $('#suggestionsResult').empty();

    // Mostrar el modal con loader
    $('#myModal .modall-body').append(loaderDym);
    $('#myModal').css('display', 'block');
    
    const searchTerm = $("#url").val();
    const suggestions = lastSuggestions[searchTerm] || await search(searchTerm) || [];

// Crear el div para mostrar las sugerencias
    const resultsDiv = $("<div id='suggestionsResult'></div>");
    if (suggestions[0].label === 'No Hay Coincidencias') {
      const noSuggestion = $('<h4 class="text-center fst-italic opacity-50">No Hay Coincidencias</h4>');
      resultsDiv.append(noSuggestion)
    } else {  
      suggestions.forEach(suggestion => {
        const suggestionElement = $(`<div class="clickable-div"><ul><li><h5>${suggestion.label}</h5></li></ul></div>`);
        suggestionElement.click(function() {
          const selectedSerieUrl = suggestion.url;
          $('#myModal').css('display', 'none');
          getResults(selectedSerieUrl)
        });
        resultsDiv.append(suggestionElement);
      });
    }

    $("#btn-close").click(function() {
      $('#myModal').css('display', 'none');
    });

    // reemplaza el contenido del cuerpo del modal
    $('#myModal .modall-body').html(resultsDiv);
  });

  // Tabla expandible
  $('#results-container').on('click', 'strong.season_title', function() {
    // Seleccionamos la tabla dentro del <li> que contiene el <strong> clicado
    const episodesTable = $(this).closest('li.expand').find('table.episodes');
    
     // Usar slideToggle para mostrar u ocultar la tabla con animación
     episodesTable.toggleClass('hidden');
  });

});
