from flask import render_template, url_for, redirect, Response, stream_with_context, request
from RealEstateScraper import app, db
from RealEstateScraper.web_scraper import property_scraper, realtor_scraper, century21_scraper, properties_to_file
from RealEstateScraper.db_functions import setup_database
from RealEstateScraper.models import Property


@app.route('/')
@app.route('/input')
def input_integer():
    return render_template('input.html')


@app.route("/scrape", methods=['GET', 'POST'])
def scrape():
    def generate(n_pages):
        # initialize variables for scraping
        properties = []
        # n_pages = 2
        fname = "scraped_data.txt"

        try:
            # scrape all websites
            # scrape website 1
            yield from property_scraper(properties, n_pages)
            # scrape website 2
            yield from realtor_scraper(properties, n_pages)
            # scrape website 3
            yield from century21_scraper(properties, n_pages)

            # save all properties to file
            # yield from properties_to_file(properties, fname)

            yield "<pre>Uploading data to database\n</pre>"
            setup_database(properties)
            yield "<pre>data upload complete</pre>"
            yield '<form action="' + url_for('database') + '"><input type="submit" value="View Database"></form>'
        except Exception as e:
            yield f"Error: {str(e)}\n"
    if request.method == 'POST':
        n_pages = int(request.form['inputNumber'])  # Get the value of the input field
        return Response(stream_with_context(generate(n_pages)))
    else:
        return "Please enter a value on the first page"


@app.route('/database')
def database():
    properties = Property.query.all()
    return render_template('database.html', properties=properties)


# Create the Flask route for editing the data
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_data(id):
    prop = Property.query.get_or_404(id)
    if request.method == 'POST':
        prop.title = request.form['title']
        prop.address = request.form['address']
        prop.postcode = request.form['postcode']
        prop.price = request.form['price']
        prop.url = request.form['url']
        prop.image_uri = request.form['image_uri']
        db.session.commit()
        return redirect(url_for('database'))
    else:
        return render_template('edit.html', prop=prop)


# Create the Flask route for deleting the data
@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete_data(id):
    data = Property.query.get_or_404(id)
    db.session.delete(data)
    db.session.commit()
    return redirect(url_for('database'))


# Create the Flask route for adding new data
@app.route('/add', methods=['GET', 'POST'])
def add_data():
    if request.method == 'POST':
        new_data = Property(title=request.form['title'], address=request.form['address'],
                            postcode=request.form['postcode'], price=request.form['price'],
                            url=request.form['url'], image_uri=request.form['image_uri'])
        db.session.add(new_data)
        db.session.commit()
        return redirect(url_for('database'))
    else:
        return render_template('add.html')
