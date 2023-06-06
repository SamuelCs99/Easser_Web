from django.shortcuts import redirect,render
from django.views import View
from django.http import HttpResponse
from bs4 import BeautifulSoup
import requests
import mechanicalsoup
from django.template.loader import render_to_string


# Create your views here.


def series(request):
    if request.method == 'POST':
        # Obtener la URL proporcionada por el usuario
        url = request.POST.get('url', '')

        # Crear una instancia del navegador MechanicalSoup
        browser = mechanicalsoup.StatefulBrowser()
        
        # Realizar la solicitud HTTP y obtener el contenido de la página
        response = browser.open(url)
        
        # Verificar el código de estado de la respuesta
        if response.status_code == 200:
            # Obtener el contenido HTML de la página
            soup = browser.get_current_page()
            
            # Encontrar todas las líneas que contengan class="episode-title"
            lines = soup.find_all('td', class_='episode-title')
            
            # Crear una lista para almacenar los resultados
            results = []

            # Obtener el título de la página principal
            title = soup.title.string
            
            # Iterar sobre las líneas encontradas
            for line in lines:
                # Encontrar los elementos <a> y <strong> dentro de la línea
                anchors = line.find_all('a')
                strongs = line.find_all('strong')
                
                # Extraer los atributos href de los elementos <a>
                hrefs = [a['href'] for a in anchors]
                
                # Extraer el contenido de los elementos <strong>
                strong_contents = [strong.get_text() for strong in strongs]

                # Obtener info de cada página a partir del href
                page_info = []
                for href in hrefs:
                    response = browser.open(href)
                    if response.status_code == 200:
                        soup = browser.get_current_page()
                        info = []
                        for tr in soup.find_all('tr', class_='po'):
                            episode_server_img = tr.find('td', class_='episode-server-img')
                            server_name = episode_server_img.text.strip()
        
                            if server_name == 'gamovideo.com':
                                episode_server = tr.find('td', class_='episode-server')
                                reproducir_url = episode_server.find('a')['href']
                                episode_lang = tr.find('td', class_='episode-lang')
                                
                                lang_img_src = episode_lang.find('img')['src']
                                if lang_img_src[-6:-4] == "en":
                                    lang_img_src = "Ingles (sub)"
                                elif lang_img_src[-6:-4] == "es":
                                    lang_img_src = "Español"
                                elif lang_img_src[-6:-4] =="la":
                                    lang_img_src = "Latino"
                                else:
                                    lang_img_src = lang_img_src[-6:-4]

                                info.append({'idioma': lang_img_src, 'link': reproducir_url})

                        page_info.append(info)
                    else:
                        page_info.append('Error al obtener informacion del capitulo')
                
                # Agregar los resultados a la lista
                results.append({'hrefs': page_info, 'strong_contents': strong_contents[0]})
            
            '''# Devolver la información obtenida como una respuesta HTTP
            return render(request, 'results.html', {'results': results, 'title': title[0:-16]})'''

            # Renderizar la plantilla de resultados y obtener el contenido como HTML
            results_html = render_to_string('results.html', {'results': results, 'title': title[0:-16]})
        
            # Devolver solo el contenido de resultados en formato HTML
            return HttpResponse(results_html)
        else:
            # Devolver una respuesta de error en caso de que la solicitud falle
            return HttpResponse('Error al obtener la página web')
    
    # Si no es una solicitud POST, renderizar la página del formulario
    return render(request, 'series_form.html')
