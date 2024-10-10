from django.shortcuts import redirect,render
from django.views import View
from django.http import HttpResponse
from django.http import JsonResponse
from bs4 import BeautifulSoup
import requests
import mechanicalsoup
from django.template.loader import render_to_string
from .models import Series
from django.db.utils import IntegrityError
from django.contrib.admin.views.decorators import staff_member_required


# Create your views here.

def home(request):
    return render(request, 'series_form.html')

# Constantes para los nombres de idioma
LANGUAGES = {
    "en": "Ingles (sub)",
    "es": "Español",
    "la": "Latino"
}

def fetch_episode_info(browser, href):
    try:
        response = browser.open(href)
        episode_info = []

        if response.status_code == 200:
            soup = browser.get_current_page()

            for tr in soup.find_all('tr', class_='po'):
                episode_server_img = tr.find('td', class_='episode-server-img')
                server_name = episode_server_img.text.strip()

                if server_name == 'gamovideo.com':
                    episode_server = tr.find('td', class_='episode-server')
                    reproducir_url = episode_server.find('a')['href']
                    episode_lang = tr.find('td', class_='episode-lang')
                    lang_img_src = episode_lang.find('img')['src'][-6:-4]
                    language = LANGUAGES.get(lang_img_src, lang_img_src)
                    episode_info.append({'idioma': language, 'link': reproducir_url})
        else:
            episode_info.append('Error al obtener informacion del capitulo')
        
        return episode_info
    except Exception as e:
        # Manejo de excepciones en caso de error
        print(f"Error al obtener informacion del capitulo: {str(e)}")
        return []

def series(request):
    if request.method == 'GET':

        # Obtener la URL proporcionada por el usuario
        url = request.GET.get('url', '')

        # Crear una instancia del navegador MechanicalSoup
        browser = mechanicalsoup.StatefulBrowser()

        try:
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
                        episode_info = fetch_episode_info(browser, href)
                        page_info.append(episode_info)
                    
                    # Agregar los resultados a la lista
                    results.append({'hrefs': page_info, 'strong_contents': strong_contents[0]})
                
                # Devolver la información obtenida como una respuesta HTTP
                results_html = render_to_string('results.html', {'results': results, 'title': title[0:-16]})
                return HttpResponse(results_html)
            else:
                return HttpResponse('Error al obtener la página web')
        except Exception as e:
            # Manejo de excepciones en caso de error
            print(f"Error al procesar la solicitud: {str(e)}")
            return HttpResponse('Error en la solicitud')
    
    

#____ UPDATE DB ____


def procesar_elemento(href, title):
    try:
        # Verificar si el título ya existe en la tabla Series
        if not Series.objects.filter(serie=title).exists():
            # Si no existe, agrega un nuevo elemento
            nueva_serie = Series(serie=title, url=href)
            nueva_serie.save()
            print(f"Nueva serie agregada: {title}")
    except IntegrityError as e:
        print("Error al agregar serie:", e)

def update(link):
    #link = "URL_DE_LA_PAGINA"  # Reemplaza con la URL de la página web que deseas analizar
    
    # Inicializar el navegador MechanicalSoup
    browser = mechanicalsoup.StatefulBrowser()
    
    try:
        # Abrir la página y obtener el contenido HTML
        browser.open(link)
        page = browser.get_current_page()
        
        # Buscar los elementos <ul> con la clase "dictionary-list"
        ul_elements = page.find_all('ul', class_='dictionary-list')
        
        for ul_element in ul_elements:
            # Buscar los elementos <li> dentro de cada <ul>
            li_elements = ul_element.find_all('li')
            
            for li_element in li_elements:
                # Buscar los elementos <a> dentro de cada <li>
                a_element = li_element.find('a')
                
                if a_element:
                    elementoHref = a_element.get('href')
                    elementoHref = "https://gnula.se" + elementoHref
                    elementoTitle = a_element.get('title')
                    
                    procesar_elemento(elementoHref, elementoTitle)
                    
    except Exception as e:
        print("Error:", e)
    
    # Cerrar el navegador
    browser.close()
    
@staff_member_required
def getUpdate(request):
    if request.method == 'POST':
        
        dic_list = [
            "https://gnula.se/lista-de-series/",
            "https://gnula.se/lista-de-series/A/",
            "https://gnula.se/lista-de-series/B/",
            "https://gnula.se/lista-de-series/C/",
            "https://gnula.se/lista-de-series/D/",
            "https://gnula.se/lista-de-series/E/",
            "https://gnula.se/lista-de-series/F/",
            "https://gnula.se/lista-de-series/G/",
            "https://gnula.se/lista-de-series/H/",
            "https://gnula.se/lista-de-series/I/",
            "https://gnula.se/lista-de-series/J/",
            "https://gnula.se/lista-de-series/K/",
            "https://gnula.se/lista-de-series/L/",
            "https://gnula.se/lista-de-series/M/",
            "https://gnula.se/lista-de-series/N/",
            "https://gnula.se/lista-de-series/O/",
            "https://gnula.se/lista-de-series/P/",
            "https://gnula.se/lista-de-series/Q/",
            "https://gnula.se/lista-de-series/R/",
            "https://gnula.se/lista-de-series/S/",
            "https://gnula.se/lista-de-series/T/",
            "https://gnula.se/lista-de-series/U/",
            "https://gnula.se/lista-de-series/V/",
            "https://gnula.se/lista-de-series/W/",
            "https://gnula.se/lista-de-series/X/",
            "https://gnula.se/lista-de-series/Y/",
            "https://gnula.se/lista-de-series/Z/"
        ]
        for dic in dic_list:
            update(dic)
        return redirect('actualizar')  # Redirige de nuevo a la página de actualización
    else:
        return render(request, 'actualizar.html')



#____AUTOCOMPLETE____

def autocomplete_titulos(request):
    if 'term' in request.GET:
        term = request.GET.get('term')
        series = Series.objects.filter(serie__icontains=term)[:10]  # Usamos el campo 'serie'
        resultados = [{'id': serie.id_serie, 'label': serie.serie, 'url': serie.url} for serie in series]
        return JsonResponse(resultados, safe=False)
    else:
        return JsonResponse({'results': []}, safe=False)
