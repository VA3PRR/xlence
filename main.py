#!/usr/bin/env python3
import json
import xlence_app as xlence
from xlence_flask import *
from xlence_functions import *
from xlence_classes import *
		
#	Mainloop
if __name__ == '__main__':
	xlence.exercise_data = {
		"name":		"testing",
		"author":	"VA3PRR",
		"release":	"2023-03-03",
		"due":		"2023-03-05",
		"has_due_date":		"off",
		"summary":	"Test Exercise"
	}

	xlence.templates = buildTemplates()
	app.run()