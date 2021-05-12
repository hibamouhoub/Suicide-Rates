from flask import Flask,render_template, request, redirect, url_for
from elasticsearch import Elasticsearch
from sharts import *
es = Elasticsearch()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'



@app.route('/by_gender/<year>/<total>', methods=['GET'])
def by_gender(year,total):
    active = {'gender':'active',
              'gen':'', 
              'age':'',
              'gdp':''
            }
    plotsrc = gender[str(year)]
    return render_template('index.html', plot=plotsrc , active= active , year = year,total = total)


@app.route('/by_generation/<year>/<total>', methods=['GET'])
def by_generation(year,total):
    active = {'gender':'',
              'generation':'active', 
              'age':'',
              'gdp':''
            }
    plotsrc = gen[str(year)]
    return render_template('index.html', plot=plotsrc , active= active , year = year,total = total)


@app.route('/by_age/<year>/<total>', methods=['GET'])
def by_age(year,total):
    active = {'gender':'',
              'generation':'', 
              'age':'active',
              'gdp':''
            }
    plotsrc = age[str(year)]
    return render_template('index.html', plot=plotsrc , active= active , year = year ,total = total)


@app.route('/by_gdp_capital/<year>/<total>', methods=['GET'])
def by_gdp_capital(year,total):
    active = {'gender':'',
              'generation':'', 
              'age':'',
              'gdp':'active'
            }
    plotsrc = gdp[str(year)]
    return render_template('index.html', plot=plotsrc , active= active , year = year ,total = total)


@app.route('/')
def select():
    return render_template('select.html')


@app.route('/go', methods=['POST'])
def go():
    year = request.form['year']
    print(year)
    res = es.search(index='suicide_rates', body={
            "query": {
                "constant_score": {
                "filter": {
                    "match": { "year":year }
                }
                }
            },
            "aggs": {
                "Total_suicide": { "sum": { "field": "suicides_no" } }
            }
    }
    )
    total = int(res['aggregations']['Total_suicide']['value'])
    return redirect(url_for('by_gender', year=year, total=total))

if __name__ == "__main__":
    DEBUG = True
    HOST = '0.0.0.0'
    app.run(debug=DEBUG, host=HOST)