from flask import Flask, render_template, request
from elasticsearch import Elasticsearch
app = Flask(__name__)
es = Elasticsearch()



@app.route('/index', methods=['GET','POST'])
def index():
    q = request.form.get("q")
    if q is not None:
        response = es.search(index="suicide_rates",body={"query": {"match": {"_id": q}}})
        return render_template('index.html', q=q, response=response)

    return render_template('index.html')



