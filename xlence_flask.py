from flask import Flask
from flask import request
from flask import redirect, url_for, render_template
import xlence_app as xlence
from xlence_functions import *
import json
import re
app = Flask(__name__)

@app.route("/")
def main_page():
	return render_template("index.html")	

@app.route("/import_digest/",methods=["GET","POST"])
def import_digest():
	data = request.files["digest"]
	data.save(data.filename)
	fh = open(data.filename,"r")
	imported_digest = fh.read()
	fh.close()
	xlence.digest_data = bs(imported_digest,"lxml")
	parse_digest()
	html_string = "Imported "+data.filename
	return html_string

@app.route("/exercise/")
def exercise_details():
	return xlence.exercise_data

@app.route("/import_exercise/",methods=["POST"])
def import_exercise():
	data = request.files["imported_exercise"]
	data.save(data.filename)
	fh = open(data.filename,"r")
	imported_exercise = fh.read()
	fh.close()
	xlence.exercise_data = json.loads(imported_exercise)
	print(xlence.exercise_data)
	print(imported_exercise)
	return xlence.exercise_data

@app.route("/static/exercise_edit.html",methods=["GET","POST"])
def edit_exercise():
	if request.method == "GET":
		html_string = render_template("exercise_new.html").replace("{NAME}",xlence.exercise_data["name"]).replace("{RELEASE}",xlence.exercise_data["release"]).replace("{DUE}",xlence.exercise_data["due"]).replace("{HASDUE}",xlence.exercise_data["has_due_date"]).replace("{AUTHOR}",xlence.exercise_data["author"]).replace("{SUMMARY}",xlence.exercise_data["summary"])
	else:
		form = request.form
		xlence.exercise_data["name"] = form.get("exercise_name")
		xlence.exercise_data["release"] = form.get("exercise_release_date")
		xlence.exercise_data["due"] = form.get("exercise_due_date")
		xlence.exercise_data["has_due_date"] = form.get("exercise_has_due_date")
		xlence.exercise_data["author"] = form.get("exercise_author")
		xlence.exercise_data["summary"] = form.get("exercise_summary")
		html_string = xlence.exercise_data
	return html_string
	
@app.route("/static/criteria_new.html",methods=["GET","POST"])
def create_criteria():
	if request.method == "GET":
		html_string = """
			<form method="POST" id="select_template">
			<select name="template">
			<option default disabled>Standard Forms Templates</option>
			
		"""
		parent = ""
		for template in xlence.templates:
			if  xlence.templates[template][0] != parent:
				parent = xlence.templates[template][0]
				pre_strg = "<option disabled>"+parent+" xlence.templates</option>"
			else:
				pre_strg = ""
			strg = "<option value='"+xlence.templates[template][1].name+"'>"+xlence.templates[template][1].name+"</option>"
			html_string+=pre_strg+strg

		html_string += """
			</select><br>
			<input type="button" value="Select Template" onclick="selectTemplate();">
		</form>
		"""
	else:
		template_name = request.form.get("template")
		current_template = xlence.templates[template_name][1]
		html_string = current_template.selectCriteria("/save_criteria/")
	return html_string

@app.route("/select_template/",methods=["POST"])
def select_template():
	template_name = request.form.get("template")
	xlence.current_template = xlence.templates[template_name][1]
	html_string = "<h4>Variables for "+xlence.current_template.name+"</h4><br>"
	html_string += xlence.current_template.selectCriteria()
	return html_string
	
@app.route("/save_criteria/",methods=["POST"])
def save_criteria():
	global criteria_data
	criteria_data = request.form
	return redirect(url_for("main_page"))
	
@app.route("/edit_template/")
def edit_template():
	global criteria_data
	display = []
	for field in criteria_data:
		data = criteria_data[field]
		if data != "ignore":
			arr = [field,data]
			display.append(arr)
	return display

@app.route("/view_digest/")
def view_digest():
	global digest
	html_string = """
	<link rel="stylesheet" href="/static/core.css">
	<table>
		<tr>
			<th>Callsign</th>
			<th>Date</th>
			<th>Entry #</th>
		</tr>
	"""
	for callsign in digest:
		data = digest[callsign]
		entries = 1
		for entry in data:
			strg = "<tr><td>"+callsign+"</td><td>"+entry["date"]+"</td><td>"+str(entries)+"</td></tr>"
			entries+=1
			html_string += strg
	html_string += "</table>"
	return html_string

@app.route("/create_exercise/",methods=["POST"])
def create_exercise():
	data = request.form
	xlence.exercise_data["name"] = data.get("exercise_name")
	xlence.exercise_data["release"] = data.get("exercise_release_date")
	xlence.exercise_data["due"] = data.get("exercise_due_date")
	xlence.exercise_data["author"] = data.get("exercise_author")
	xlence.exercise_data["summary"] = data.get("exercise_summary")
	return xlence.exercise_data
	
@app.route("/select_criteria/",methods=["POST"])
def select_criteria():
	criteria = request.form
	html_data = """
		<table>
			<tr>
				<th>Variable</th>
				<th>Action/Value</th>
			</tr>
	"""
	for element in criteria:
		value = criteria[element]
		if value == "ignore" or value == "":
			continue
		else:
			xlence.criteria_data[element]=value
			html_data += "<tr><td>"+element+"</td><td>"+criteria[element]+"</td></tr>"
	html_data += "</table>"
	return html_data
	
@app.route("/process_scores/",methods=["POST"])
def process_scores():
	digest = xlence.digest
	criteria = xlence.criteria_data
	template = xlence.current_template
	template_text = template.text_data.replace("\r","").split("\n")
	lines = []
	scores = {}
	max_score = 0
	for line in template_text:
		for key in criteria:
			if "-comparison" in key:
				continue
			elif str(key) in line:
				lines.append(line.replace(">","").split("<var "))
			max_score += 1
	xlence.exercise_data["points"] = max_score			
	for callsign in digest:
		data = digest[callsign]
		points = 0
		for message in data:
			message_date = message["date"]
			message_subject = message["subject"]
			message_text = message["message"].split("\n")
			matched_criteria = []
			for line in message_text:
				for cr_line in lines:
					if cr_line[0] in line and cr_line[1] not in matched_criteria:
						line = line.replace(cr_line[0],"")
						criterion = criteria[cr_line[1]]
						if criterion == "set" and len(line)>0:
							matched_criteria.append(cr_line[1])
							points += 1
						elif criterion in "equals contains".split(" "):
							comparison = criteria[str(cr_line[1]+"-comparison")]
							if criterion == "equals":
								if re.match(comparison.lower(),line.lower()):
									matched_criteria.append(cr_line[1])
									points+=1
							elif criterion == "contains":
								if re.search(comparison.lower(),line.lower()):
									matched_criteria.append(cr_line[1])
									points+=1
			
			scores[callsign] = {
				"score":			points,
				"criteria_met":	matched_criteria,
				"message_date":	message_date
				}
	xlence.score_data = scores		
	return xlence.score_data

@app.route("/export_scores/",methods=["POST"])
def export_scores():
	score_data = xlence.score_data
	num_entrants = len(score_data)
	exercise_data = xlence.exercise_data
	html_string = """
	<html>
		<head>
		<title>Scores for Exercise: <EXNAME></title>
		</head>
		<h3><EXNAME></h3><br>
		<p>Exercise summary: <EXSUMMARY></p><br>
		<p>A total of <ENTRANTS> callsigns have participated in this exercise.</p>
		<br>
		<table>
			<tr>
				<th>Callsign</th>
				<th>Score</th>
				<th>Date</th>
			</tr>
	""".replace("<EXNAME>",exercise_data["name"]).replace("<EXSUMMARY>",exercise_data["summary"]).replace("<ENTRANTS>",str(num_entrants))
	for callsign in score_data:
		entry = score_data[callsign]
		strg = "<tr><td>"+callsign+"</td><td>"+str(entry["score"])+"/"+str(exercise_data["points"])+"</td><td>"+entry["message_date"]+"</td></tr>"
		html_string += strg
	html_string += "</table></html>"
	return html_string