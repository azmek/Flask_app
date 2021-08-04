from flask import Flask, redirect, url_for, render_template, request, session
import requests
import json

app = Flask(__name__)
app.secret_key = "hello"
api_list = []
data_dump = []


@app.route('/search_results', methods=['POST'])
def search_results():
    # retrieve the company code from the frontend
    company_code = request.form['company_code']
    # Retrieve data from AlphaVantage's open API
    # Documentation availabe at : https://www.alphavantage.co/documentation
    try:
        r = requests.get('https://www.alphavantage.co/query?function=SYMBOL_SEARCH&keywords=' +
                         company_code+'&apikey='+api_list[0])

        # Creating headings for the table in the frontend
        headings = ("Code", "  ", "Name")
        data = json.loads(r.content)

        data_dump.append(data['bestMatches'])

        return render_template('search_results.html', headings=headings, data=data['bestMatches'])
    except:
        return "You have not entered an API key"


# Make sure user provides their own API and store it locally
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        api_key = request.form["user_key"]
        session["api_key"] = api_key
        api_list.append(api_key)
        return redirect(url_for("welcome"))
    else:
        if "api_key" in session:
            return redirect(url_for("welcome"))
        return render_template('index.html')


# welcome page to enter Company code
@app.route('/welcome')
def welcome():
    if "api_key" in session:
        api_key = session["api_key"]
        return render_template('welcome.html')
    else:
        return redirect(url_for("index"))


# More Details page
@app.route('/additional_details/<string:name>',  methods=['GET', 'POST'])
def additional_details(name):
    fresh_list = data_dump[0]
    for items in fresh_list:
        for k, v in items.items():
            if v == name:
                print(v)

    return render_template('additional_details.html',  name=name, items=items)


# User can clear their API from the browser  and redirect to homepage
@ app.route('/logout')
def logout():
    session.pop("api_key", None)
    del api_list[:]
    return redirect(url_for("index"))


# main
if __name__ == '__main__':
    app.run(debug=True)
