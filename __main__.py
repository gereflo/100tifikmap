import time
import json

from colored import fg, bg, attr
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as OptionsF
from selenium.webdriver.edge.options import Options as OptionsE
from selenium.webdriver.chrome.options import Options as OptionsC
from selenium.webdriver.common.keys import Keys
from geopy import geocoders
import os
import codecs


# ----Clases----

class Cita:
    def __init__(self, paperCitado, autoresCitados, linkCitados, paper, autores, link, lugar, latitude, longitude):
        self.paperCitado = paperCitado
        self.autoresCitados = autoresCitados
        self.linkCitados = linkCitados
        self.paper = paper
        self.autores = autores
        self.link = link
        self.lugar = lugar
        self.latitude = latitude
        self.longitude = longitude

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def toHTML(self):
        html = (
                "<h1>" + self.lugar + "</h1><a href='" + self.linkCitados + "'><h4>Cite from:" + self.paperCitado + "</h4></a><a href='" + self.link + "'><h4>Cite: "
                + self.paper + "</h4></a><h5>Authors:" + self.autores + "</h5>")
        html = html.replace('"', "'")
        return html

    def toArrayElement(self):
        html = self.toHTML()
        element = f'["{html}",{self.latitude},{self.longitude},"{self.lugar}"],'
        return element

    # def to_dict(self):
    #     return {"paperCitado": self.paperCitado, "autoresCitados": self.autoresCitados, "linkCitados": self.linkCitados,
    #             "paper": self.paper, "autores": self.autores, "link": self.link, "lugar": self.lugar,
    #             "latitude": self.latitude, "longitude": self.longitude}
    #
    # def toJSON(self):
    #     return json.dumps(self, default=lambda o: o.__dict__,
    #                       sort_keys=True, indent=4)


# ----Functions-----

def placesDisplay(place, abuscar, pais=False, retZero=False):
    contries = ["Afghanistan", "Albania", "Algeria", "American Samoa", "Andorra", "Angola", "Anguilla", "Antarctica",
                "Antigua and Barbuda", "Argentina", "Armenia", "Aruba", "Australia", "Austria", "Azerbaijan", "Bahamas",
                "Bahrain", "Bangladesh", "Barbados", "Belarus", "Belgium", "Belize", "Benin", "Bermuda", "Bhutan",
                "Bolivia", "Bosnia and Herzegowina", "Botswana", "Bouvet Island", "Brazil",
                "British Indian Ocean Territory", "Brunei Darussalam", "Bulgaria", "Burkina Faso", "Burundi",
                "Cambodia", "Cameroon", "Canada", "Cape Verde", "Cayman Islands", "Central African Republic", "Chad",
                "Chile", "China", "Christmas Island", "Cocos (Keeling) Islands", "Colombia", "Comoros", "Congo",
                "Congo, the Democratic Republic of the", "Cook Islands", "Costa Rica", "Cote d'Ivoire",
                "Croatia (Hrvatska)", "Cuba", "Cyprus", "Czech Republic", "Denmark", "Djibouti", "Dominica",
                "Dominican Republic", "East Timor", "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea",
                "Estonia", "Ethiopia", "Falkland Islands (Malvinas)", "Faroe Islands", "Fiji", "Finland", "France",
                "France Metropolitan", "French Guiana", "French Polynesia", "French Southern Territories", "Gabon",
                "Gambia", "Georgia", "Germany", "Ghana", "Gibraltar", "Greece", "Greenland", "Grenada", "Guadeloupe",
                "Guam", "Guatemala", "Guinea", "Guinea-Bissau", "Guyana", "Haiti", "Heard and Mc Donald Islands",
                "Holy See (Vatican City State)", "Honduras", "Hong Kong", "Hungary", "Iceland", "India", "Indonesia",
                "Iran (Islamic Republic of)", "Iraq", "Ireland", "Israel", "Italy", "Jamaica", "Japan", "Jordan",
                "Kazakhstan", "Kenya", "Kiribati", "Korea, Democratic People's Republic of", "Korea, Republic of",
                "Kuwait", "Kyrgyzstan", "Lao, People's Democratic Republic", "Latvia", "Lebanon", "Lesotho", "Liberia",
                "Libyan Arab Jamahiriya", "Liechtenstein", "Lithuania", "Luxembourg", "Macau",
                "Macedonia, The Former Yugoslav Republic of", "Madagascar", "Malawi", "Malaysia", "Maldives", "Mali",
                "Malta", "Marshall Islands", "Martinique", "Mauritania", "Mauritius", "Mayotte", "Mexico",
                "Micronesia, Federated States of", "Moldova, Republic of", "Monaco", "Mongolia", "Montserrat",
                "Morocco", "Mozambique", "Myanmar", "Namibia", "Nauru", "Nepal", "Netherlands", "Netherlands Antilles",
                "New Caledonia", "New Zealand", "Nicaragua", "Niger", "Nigeria", "Niue", "Norfolk Island",
                "Northern Mariana Islands", "Norway", "Oman", "Pakistan", "Palau", "Panama", "Papua New Guinea",
                "Paraguay", "Peru", "Philippines", "Pitcairn", "Poland", "Portugal", "Puerto Rico", "Qatar", "Reunion",
                "Romania", "Russian Federation", "Rwanda", "Saint Kitts and Nevis", "Saint Lucia",
                "Saint Vincent and the Grenadines", "Samoa", "San Marino", "Sao Tome and Principe", "Saudi Arabia",
                "Senegal", "Seychelles", "Sierra Leone", "Singapore", "Slovakia (Slovak Republic)", "Slovenia",
                "Solomon Islands", "Somalia", "South Africa", "South Georgia and the South Sandwich Islands", "Spain",
                "Sri Lanka", "St. Helena", "St. Pierre and Miquelon", "Sudan", "Suriname",
                "Svalbard and Jan Mayen Islands", "Swaziland", "Sweden", "Switzerland", "Syrian Arab Republic",
                "Taiwan, Province of China", "Tajikistan", "Tanzania, United Republic of", "Thailand", "Togo",
                "Tokelau", "Tonga", "Trinidad and Tobago", "Tunisia", "Turkey", "Turkmenistan",
                "Turks and Caicos Islands", "Tuvalu", "Uganda", "Ukraine", "United Arab Emirates", "United Kingdom",
                "Uk", "Usa",
                "United States", "United States Minor Outlying Islands", "Uruguay", "Uzbekistan", "Vanuatu",
                "Venezuela", "Vietnam", "Virgin Islands (British)", "Virgin Islands (U.S.)",
                "Wallis and Futuna Islands", "Western Sahara", "Yemen", "Yugoslavia", "Zambia", "Zimbabwe"]

    # abuscar.extend(contries)

    respuesta = 0
    flag = True

    for palabra in abuscar:
        for element in place:
            e = element.lower().replace('.', '')
            p = palabra.lower()
            if e.find(p) != -1 and flag:
                element = ''.join([i for i in element if not i.isdigit()])
                element = element.strip()
                respuesta = element.replace('.', '')
                flag = False
            if e.capitalize() in contries and flag == False and pais == True:
                respuesta = respuesta + ', ' + e.capitalize()
                flag = 2

    if respuesta == 0:
        for palabra in contries:
            for element in place:
                e = element.lower().replace('.', '')
                p = palabra.lower()
                if e.find(p) != -1 and flag:
                    element = ''.join([i for i in element if not i.isdigit()])
                    # element = element.strip()
                    respuesta = palabra

    if respuesta == 0:
        return place

    return respuesta


# ------------------------

def placePoints(serchQuery):
    # Se debe de obtener una clave de Bing para este paso
    geolocator = geocoders.Bing("Ag7ceErbHJORhQmZYkcqitAhObbQo42dg_ucM65A7O0GBi6JTaKWVLMIgtP6mqV2")

    # address, (latitude, longitude) = geolocator.geocode("Weizmann Institute of Science")
    location = geolocator.geocode(serchQuery, timeout=10)
    # print(location.address)
    # print(location.latitude)
    # print(location.longitude)
    # print(location.raw)

    return [location.address, [location.latitude, location.longitude]]
    # return [serchQuery, [10, 20]]


# -------------------------
def waiting(wait, mensaje=""):
    for i in range(wait + 1):
        idx = "Espere " + str(wait - i) + "mensaje"
        # print('\r', idx, end='')
        print("'\r{0}".format(idx), end='')
        time.sleep(1)
    print("", "\r", end='')


# ---Variables----

abuscar = ['University', 'Université', 'Institute', 'Research', 'Laboratory', 'Academy', 'Facility', 'Hospital']
error = bg(1) + fg('white')
highlight = fg(198)
ok = fg(34)
reset = attr('reset')
# print(color + 'Hello World !!!' + reset)
# print ('%sHello World !!! %s' % (error, reset))

html = "<h1>%s</h1><a href='%s'><h4>Cite from: %s</h4></a><a href='%s'><h4>Cite: %s</h4></a><h5>Authors: $s</h5>"

globalPlaces = []
papersQueCitan = []

# -----Main------

try:
    os.remove("array.txt")
except FileNotFoundError:
    print("No se ha encontrado archivo de Array")
try:
    os.remove("errors.txt")
except FileNotFoundError:
    print("No se ha encontrado archivo de errores")
try:
    os.remove("places.json")
except FileNotFoundError:
    print("No se ha encontrado archivo de places")

try:
    os.remove("papersJson.json")
except FileNotFoundError:
    print("No se ha encontrado archivo de papersJson")

chrome_options = OptionsC()
firefox_options = OptionsF()
edge_options = OptionsE()
edge_options.use_chromium = True

# chrome_options.add_argument("--headless")

term = 'Garcia-Campos+MA'
address = 'https://pubmed.ncbi.nlm.nih.gov/?term=' + term

# firefox = webdriver.Firefox(executable_path=r"E:\Proyects\100tifikmap\webdrivers\geckodriver.exe",
#                             options=firefox_options)
# chrome = webdriver.Chrome(executable_path=r"E:\Proyects\100tifikmap\webdrivers\chromedriver.exe",
#                           options=chrome_options)
edge = webdriver.Edge(executable_path=r"E:\Proyects\100tifikmap\webdrivers\msedgedriver.exe")

# firefox.get(address)
# chrome.get(address)
edge.get(address)
edge.implicitly_wait(10)
edge.maximize_window()

print(edge.title)
table = edge.find_elements_by_class_name('docsum-content')
# print(len(table))
for tr in table:
    print('------------------------------------------------------------------')
    # print(tr.get_attribute('innerHTML'))
    paper = tr.find_element_by_class_name("docsum-title")
    title = paper.get_attribute("textContent").strip()
    # title = paper.get_attribute("outerHTML")
    linkPaper = paper.get_attribute('href')
    # print(paper)
    print(title)
    print(linkPaper)
    edge2 = webdriver.Edge(executable_path=r"E:\Proyects\100tifikmap\webdrivers\msedgedriver.exe")
    edge2.get(linkPaper)
    usaButton = edge2.find_elements_by_class_name('usa-button')
    for button in usaButton:
        try:
            citedBy = button.get_attribute("data-ga-category")
            citedByStr = str(citedBy)
            if citedByStr == 'cited_by':
                link = button.get_attribute('data-href')
                edge2.get('https://pubmed.ncbi.nlm.nih.gov' + link)
                break
        except StaleElementReferenceException:
            print('Paper sin citas 1')
            edge2.quit()
            break
    try:
        loadButton = edge2.find_element_by_class_name('load-button')
        pages = loadButton.get_attribute('data-last-page')
        # print('paginas: ' + pages)

    except NoSuchElementException:
        print('Paper sin citas 2')
        edge2.quit()
        continue

    pages = range(1, int(pages) + 1)
    currentlink = edge2.current_url
    # print(currentlink)
    citedIn = []
    for p in pages:
        cidtedInpage = currentlink + '&page=' + str(p)
        # print(cidtedInpage)
        edge2.get(cidtedInpage)
        citedList = edge2.find_elements_by_class_name('docsum-title')
        for cited in citedList:
            name = cited.get_attribute("textContent").strip()
            paperlink = cited.get_attribute("href")
            paperElement = [name, paperlink]
            citedIn = [*citedIn, paperElement]
        # print('Paper citados en pagina' + str(p) + ': ' + str(len(cited)))
        # citedIn = [*citedIn, *cited]

    print('Citas totales: ' + str(len(citedIn)))
    if len(citedIn):
        num = 1;
        for cite in citedIn:
            if num == 1:
                num += 1
                continue
            print('---------Cita No.', num, '----------')
            print('Paper: ', cite[0] + cite[1])
            edge2.get(cite[1])
            authorsList = edge2.find_element_by_class_name('authors-list')
            authors = authorsList.find_elements_by_class_name('full-name')
            authorsString = ""
            for author in authors:
                authorsString = authorsString + author.get_attribute('textContent') + ", "
            print("Authors: ", authorsString)
            expandedAuthors = edge2.find_element_by_id('expanded-authors')
            # itemList = authors.find_element_by_class_name('item-list')
            # print(itemList.get_attribute('innerHTML'))
            itemList = expandedAuthors.find_elements_by_css_selector('li')
            places = []
            for li in itemList:
                text = li.get_attribute('textContent').split(', ')
                place = placesDisplay(text, abuscar, False)
                if isinstance(place, str):
                    globalPlaces.append(place)
                    paperQueCita = Cita(title, 'Autores Citados', linkPaper, cite[0], authorsString, cite[1], place, 0,
                                        0)
                    papersQueCitan.append(paperQueCita)
                places.append(place)
                # print('-----: ', place)
            try:
                places = list(set(places))
            except:
                print(error, '#########Error aqui###########', places, reset)

            print(len(globalPlaces), " Global places: ", globalPlaces)

            # # print("-----: ", places)
            # for place in places:
            #     if isinstance(place, list):
            #         print(error, '####', place, reset)
            #         f = codecs.open("errors.txt", "a+", "utf-8")
            #         f.write(str(place) + "\r")
            #         # print(paperQueCita.toArrayElement())
            #         f.close()
            #     else:
            #         try:
            #             points = placePoints(place)
            #         except:
            #             print("Something went wrong")
            #             continue
            #         html = '<h1>' + title + '</h1>' + cite[0] + authorsString + place
            #         reference = [html, points[1][0], points[1][1], place]
            #         # print(reference)
            #         paperQueCita = Cita(title, 'Autores Citados', linkPaper, cite[0], authorsString, cite[1], place,
            #                             points[1][0], points[1][1])
            #         # print(ok, paperQueCita, reset)
            #         print(ok, '-------', place, points, reset)
            #         f = codecs.open("Array.txt", "a+", "utf-8")
            #         f.write(paperQueCita.toArrayElement() + "\r")
            #         # print(paperQueCita.toArrayElement())
            #         f.close()
            num += 1
        edge2.quit()

globalPlaces = list(set(globalPlaces))
print(len(globalPlaces), globalPlaces)
# f = codecs.open("places.json", "a+", "utf-8")
# jsonStr = json.dumps(globalPlaces)
# f.write(jsonStr + "\r")
# f.close()
# results = [obj.to_dict() for obj in papersQueCitan]
# jsdata = json.dumps({"results": results})
# f = codecs.open("papersJson.json", "a+", "utf-8")
# f.write(jsdata + "\r")
# f.close()

f = codecs.open("array.js", "a+", "utf-8")
f.write("const locations = [" + "\r")
f.close()
for place in globalPlaces:
    print("------------------------------")
    papersName = []
    arrayString = "\t[\"<h1>" + place + "</h1><br>"
    try:
        points = placePoints(place)
        print("Lugar: ", points)
    except:
        print("Something went wrong")
        continue
    for paper in papersQueCitan:
        if paper.lugar == place:
            # print(highlight, paper, reset)
            if paper.paper not in papersName:
                paper.longitude = points[1][0]
                paper.latitude = points[1][1]
                papersName.append(paper.paper)
                print(ok, paper, reset)
                arrayPaper = "<div style='border: thin solid grey'>"
                arrayPaper = arrayPaper + "<a href='" + paper.linkCitados + "'><h4>Cite from: " + paper.paperCitado \
                             + "</h4><a href='" + paper.link + "'><h4>Cite: " + paper.paper + "</h4></a>"
                arrayPaper = arrayPaper.replace('"', "'")
                arrayString = arrayString + arrayPaper
                arrayPaper = arrayPaper + "</div>"
    arrayString = arrayString + "\", " + str(points[1][0]) + ", " + str(points[1][1]) + ", \"" + place.replace('"', "'")+ "\"],"
    f = codecs.open("array.js", "a+", "utf-8")
    f.write(arrayString + "\r")
    print(arrayString)
    f.close()

f = codecs.open("array.js", "a+", "utf-8")
f.write("]" + "\r")
f.close()
edge.quit()
