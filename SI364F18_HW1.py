## HW 1
## SI 364 F18
## 1000 points

#################################

## List below here, in a comment/comments, the people you worked with on this assignment AND any resources you used to find code (50 point deduction for not doing so). If none, write "None".

# Lauren Sigurdson

## [PROBLEM 1] - 150 points
## Below is code for one of the simplest possible Flask applications. Edit the code so that once you run this application locally and go to the URL 'http://localhost:5000/class', you see a page that says "Welcome to SI 364!"

from flask import Flask, request
from flask import render_template 
import requests
import json
app = Flask(__name__)
app.debug = True

@app.route('/')
def hello_to_you():
    return 'Hello!'

@app.route('/class')
def welcome_class():
    return "Welcome to SI 364!"


## [PROBLEM 2] - 250 points
## Edit the code chunk above again so that if you go to the URL 'http://localhost:5000/movie/<name-of-movie-here-one-word>' 
# you see a big dictionary of data on the page. For example, if you go to the URL 'http://localhost:5000/movie/ratatouille', 
# you should see something like the data shown in the included file sample_ratatouille_data.txt, which contains data about the animated movie Ratatouille. 
# However, if you go to the url http://localhost:5000/movie/titanic, you should get different data, 
# and if you go to the url 'http://localhost:5000/movie/dsagdsgskfsl' for example, you should see data on the page that looks like this:

@app.route('/movie/<movie_name>')
def movie_data(movie_name):
	base_url = "https://itunes.apple.com/search"
	params_diction = {}
	params_diction["term"] = movie_name
	params_diction["country"] = 'US'
	resp = requests.get(base_url, params = params_diction)
	text = resp.text
	python_obj = json.loads(text)
	return str(python_obj)

# {
#  "resultCount":0,
#  "results": []
# }


## You should use the iTunes Search API to get that data.
## Docs for that API are here: https://affiliate.itunes.apple.com/resources/documentation/itunes-store-web-service-search-api/
## Of course, you'll also need the requests library and knowledge of how to make a request to a REST API for data.

## Run the app locally (repeatedly) and try these URLs out!

## [PROBLEM 3] - 250 points

## Edit the above Flask application code so that if you run the application locally and got to the URL http://localhost:5000/question, 
# you see a form that asks you to enter your favorite number.
## Once you enter a number and submit it to the form, you should then see a web page that says "Double your favorite number is <number>". 
# For example, if you enter 2 into the form, you should then see a page that says "Double your favorite number is 4". Careful about types in your Python code!
## You can assume a user will always enter a number only.

@app.route('/question', methods=['GET', 'POST'])
def submit_q():
	return """ <br><br>
	<form action= "/result" method="POST">
	  Enter your favorite number<br>
	  <input type="text" name="fave_num" value = "" <br>
	  <input type="submit" value="Submit">
	</form>
	""" 


@app.route('/result',methods=['GET', 'POST'])
def result_q():
	if request.method == "POST":
		double_num = int(request.form["fave_num"]) * 2
		return 'Double your favorite number is {}'.format(double_num)

	else:
		return "Nothing was selected this time!" 




## [PROBLEM 4] - 350 points

## Come up with your own interactive data exchange that you want to see happen dynamically in the Flask application, and build it into the above code for a Flask 
# application, following a few requirements.

## You should create a form that appears at the route: http://localhost:5000/problem4form

## Submitting the form should result in your seeing the results of the form on the same page.

## What you do for this problem should:
# - not be an exact repeat of something you did in class
# - must include an HTML form with checkboxes and text entry
# - should, on submission of data to the HTML form, show new data that depends upon the data entered into the submission form and is readable by humans 
# (more readable than e.g. the data you got in Problem 2 of this HW). The new data should be gathered via API request or BeautifulSoup.

# You should feel free to be creative and do something fun for you --
# And use this opportunity to make sure you understand these steps: if you think going slowly and carefully writing out steps for a simpler data transaction, 
# like Problem 1, will help build your understanding, you should definitely try that!

# You can assume that a user will give you the type of input/response you expect in your form; you do not need to handle errors or user confusion. 
#(e.g. if your form asks for a name, you can assume a user will type a reasonable name; if your form asks for a number, you can assume a user will type a 
# reasonable number; if your form asks the user to select a checkbox, you can assume they will do that.)

# Points will be assigned for each specification in the problem.

@app.route('/problem4form', methods=['GET', 'POST'])
def prob4():

	html_form = """<br> <br>
	<form action="http://localhost:5000/problem4form" method='GET'>
	Enter your name and select a city: <br> <input type="text" name = "name" value = ''> <br>
  	<input type="checkbox" name="city1" value="AnnArbor"> Ann Arbor, MI <br>
  	<input type="checkbox" name="city2" value="Chicago"> Chicago, IL <br>
  	<input type="checkbox" name="city3" value="Seattle"> Seattle, WA <br>
  	<input type="submit" value="Submit">
	</form>"""
	# print (html_form)
	# print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
	# print(request.method)

	if request.method == 'GET':
		print(request.args)
		result_str = ""
		city_ids = {"AnnArbor":4984247, "Chicago":4887398, "Seattle":5809844}
		city_list = ["AnnArbor", "Chicago", "Seattle"]
		for k in request.args:
			print(request.args.get(k))
			if request.args.get(k) in city_list:
				print(request.args.get(k))
				city_id = city_ids[request.args.get(k)]
				print(city_id)

				base_url = "https://api.openweathermap.org/data/2.5/weather?"
				params_diction = {}
				params_diction["id"] = city_id
				params_diction["APPID"] = '366e9ab271a2967f2012be6f179a537e'
				params_diction["units"] = 'imperial'
				resp = requests.get(base_url, params = params_diction)
				text = resp.text
				python_obj = json.loads(text)

				# print(python_obj)
				# print(python_obj["main"])
				current_temp = python_obj["main"]["temp"]
				result_str += "The current temperature is {} degrees.<br><br>".format(current_temp)
	# 	print(city_id)
		return html_form + result_str
	else:
		return html_form

#{'coord': {'lon': -83.74, 'lat': 42.28}, 'weather': [{'id': 741, 'main': 'Fog', 'description': 'fog', 'icon': '50n'}, {'id': 701, 'main': 'Mist', 'description': 'mist', 'icon': '50n'}], 'base': 'stations', 'main': {'temp': 69.19, 'pressure': 1013, 'humidity': 100, 'temp_min': 64.04, 'temp_max': 74.3}, 'visibility': 402, 'wind': {'speed': 3.06, 'deg': 160.504}, 'clouds': {'all': 1}, 'dt': 1537242180, 'sys': {'type': 1, 'id': 1382, 'message': 0.0045, 'country': 'US', 'sunrise': 1537269498, 'sunset': 1537313936}, 'id': 4984247, 'name': 'Ann Arbor', 'cod': 200}


if __name__ == '__main__':
    app.run()
