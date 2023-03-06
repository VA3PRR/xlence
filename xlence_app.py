default_exercise_name = "WinlinkTraining.ca Exercise"
default_exercise_author = "VA3XLC"
default_exercise_summary = "Sample training exercise"
default_exercise_has_due_date = "off"

"""
Globals
"""

#	Holds data about the exercise
exercise_data = {
	"name":	default_exercise_name,
	"author":	default_exercise_author,
	"summary":	default_exercise_summary,
	"has_due_date":	default_exercise_has_due_date
}

#	Holds data about scoring criteria
criteria_data = {}

#	Holds scoring data
score_data = {}

#	Holds information parsed from the message digest
digest = {}

#	Holds the parsed digest
digest_data = None

#	Holds the standard form templates
templates = {}

templates_directory = "static/templates/"
current_template = None
