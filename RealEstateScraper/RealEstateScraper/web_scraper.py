from RealEstateScraper.property_class import Property
from flask import Response, stream_with_context
from bs4 import BeautifulSoup
import requests


def property_scraper(properties, n_pages=1):
    yield "<p>Searching property.com.au\n</p>"
    for current_page in range(1, n_pages+1):
        yield f"<p>Searching Page {current_page}\n</p>"

        # access url using requests and create soup
        url = f"https://www.property.com.au/buy/list-{current_page}/"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # get all types of properties
        homes = soup.find('div', {"id": "searchResultsTbl"})
        for index, home in enumerate(homes):
            # one extra element in the first line of each page
            # one empty element between each property
            if index != 0 and home != " ":
                # get image
                image = home.find('div', class_='photoviewer').a.img['src']
                # get name of properties
                title = home.find('h3', class_="title").text
                # get price
                price = home.find('span', class_="hidden").text
                # get address
                address = home.find('div', class_="vcard").a.text
                postcode = address.split(', ')[-1]
                # get website address
                property_url = home.find('div', class_="vcard").a['href']

                # enter data into a new property object, add it to list
                new_property = Property(title, address, postcode, price, property_url, image)
                properties.append(new_property)

    yield "<p>Search Completed, Data saved in list\n\n\n</p>"


def realtor_scraper(properties, n_pages=1):
    yield "<p>Searching realtor.com\n</p>"
    for current_page in range(1, n_pages+1):
        yield f"<p>Searching Page {current_page}\n</p>"

        # access url using requests and create soup
        url = f"https://www.realtor.com/international/au/p{current_page}/"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # get a list of all properties on the page
        homes = soup.findAll('li', class_="listing project")
        for index, home in enumerate(homes):
            if index > 0:
                # get image of property
                image = home.a.img['data-src']
                # get title of the property
                title = home.find('div', {"class": "basic-info"}).h3['title']
                # get the price of the property
                price = home.find('div', {"class": "basic-info"}).find('p', {"class": "custom-price"})['title']
                # get the address of the property (strip new line and spaces at the start)
                address = home.find('div', {"class": "basic-info"}).address.a.text.lstrip('\n').lstrip(' ')
                # get the address of the property
                postcode = address.split(', ')[-1]
                # get the href of the property
                property_url = "https://www.realtor.com/" + home.find('div', {"class": "basic-info"}).address.a['href']

                # enter data into a new property object, add it to list
                new_property = Property(title, address, postcode, price, property_url, image)
                properties.append(new_property)

    yield "<p>Search Completed, Data saved in list\n\n\n</p>"


def century21_scraper(properties, n_pages=1):
    yield "<p>Searching century21.com.au\n</p>"
    for current_page in range(1, n_pages + 1):
        yield f"<p>Searching Page {current_page}\n</p>"

        # access url using requests and create soup
        url = f"https://www.century21.com.au/properties-for-sale?page={current_page}&searchtype=sale"
        html_text = requests.get(url).text
        soup = BeautifulSoup(html_text, 'lxml')

        # print(soup)
        # get a list of all properties on the page
        homes = soup.find('ul', {"class": "searchResults grid-1 grid-med-2 grid-lrg-3 grid-print-3 center tight"})\
            .findAll('li')
        for index, home in enumerate(homes):
            # get image source
            image = home.find('div', {"class": "image"}).div['style'].lstrip("background-image: url(").rstrip(')')

            # get title
            title = home.find('div', {"class": "caption"}).address.span.text

            # get price, combine with type of sale
            price = home.find('span', {"class": "contracttext"}).text
            price = price + " " + home.find('span', {"class": "pricetext"}).text.lstrip("\n").lstrip(" ")

            # get address (part of address is in the title)
            address = title + home.find('span', {"class": "streetaddress oneline"}).text

            # website does not provide postcodes
            postcode = "Not Listed"

            # get url
            property_url = home.div.a['href']

            # enter data into a new property object, add it to list
            new_property = Property(title, address, postcode, price, property_url, image)
            properties.append(new_property)

    yield "<p>Search Completed, Data saved in list\n</p>"
    yield "<p>\n</p>"


def properties_to_file(properties, filename_):
    # access / create file
    yield "<p>Entering data into file\n</p>"
    with open(filename_, 'w') as f:
        for prop in properties:
            # enter data into file
            f.write(f"Title: {prop.title}\n")
            f.write(f"Image: {prop.image}\n")
            f.write(f"Address: {prop.address}\n")
            f.write(f"Postcode: {prop.postcode}\n")
            f.write(f"Price: {prop.price}\n")
            f.write(f"More info: {prop.url}\n\n")

    f.close()
    yield f"<p>Data saved in file: {filename_}\n</p>"
    yield "<p>\n</p>"
