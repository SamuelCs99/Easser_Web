$(document).ready(function() {
    // Manejar el evento de envío del formulario
    $("#series-form").submit(function(event) {
        event.preventDefault();  // Evitar el envío del formulario normal

        // Mostrar el loader
        showLoader();

        // Obtener la URL proporcionada por el usuario
        var url = $("#url").val();
        
        var seriesUrl = $("#series-form").data("url");
        // Obtener el valor del token CSRF desde el formulario
        var csrfToken = $("input[name='csrfmiddlewaretoken']").val();

        // Realizar la solicitud AJAX
        $.ajax({
            type: "POST",
            url: seriesUrl,
            data: {
                url: url,
                csrfmiddlewaretoken: csrfToken
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
    });

    function showLoader() {
        $("#loader").show();
    }

    function hideLoader() {
        $("#loader").hide();
    }
});