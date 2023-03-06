function bootSequence()	{
	document.getElementById("button_criteria").disabled = true;
	document.getElementById("button_digest").disabled = true;
	document.getElementById("button_scores").disabled = true;
}


//	Handles selections from HELP menu
function toolHelp(href)	{
	href = "/static/help/"+href.toLowerCase()+".html";
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById("tool").innerHTML = this.responseText;
		}
	};
	xhttp.open("GET",href,true);
	xhttp.setRequestHeader("Content-type","text/html");
	xhttp.send()
}

//	Handles global navigation
function doNavigate(href,target,method)	{
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById(target).innerHTML = this.responseText;
		}
	};
	xhttp.open(method,href,true);
	xhttp.setRequestHeader("Content-type","text/html");
	xhttp.send()
}
//	Populates the "tool" (or "tool_horizontal") panel
function toolNavigate(href,horizontal=0)	{
	href = href.toLowerCase();
	if(horizontal!=0)	{
		tool = "tool_horizontal";
	}
	else	{
		tool = "tool"
	}
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById(tool).innerHTML = this.responseText;
		}
	};
	href = "/static/"+href+".html";
	xhttp.open("GET",href,true);
	xhttp.setRequestHeader("Content-type","text/html");
	xhttp.send()
}



//	Vestigial?
function navigate(href)	{
	href = href.toLowerCase();
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById("content").innerHTML = this.responseText;
		}
	};
	href = "/static/"+href+".html";
	xhttp.open("GET",href,true);
	xhttp.setRequestHeader("Content-type","text/html");
	xhttp.send()
}



//	Displays output from current exercise form
function exerciseOutput(caller)	{
	var FD;
	if(caller == 'button_import_exercise')	{
		FD = new FormData(document.getElementById("import_exercise"));		
	}
	else	{
		FD = new FormData(document.getElementById("create_exercise"));
	}
	output = document.getElementById("tool_output");
	name = FD.get("exercise_name");
	release = FD.get("exercise_release_date");
	due = FD.get("exercise_due_date");
	has_due = FD.get("exercise_has_due_date");
	if(has_due == "off")	{
		has_due = "on";
	}
	else	{
		has_due = "off";
	}
	author = FD.get("exercise_author");
	summary = FD.get("exercise_summary");
	var html_string = "<table><tr><th>Exercise Name</th><td>"+name+"</td></tr>";
	html_string += "<tr><th>Release</th><td>"+release+"</td></tr>";
	html_string += "<th>Due</th><td>"+due+" ("+has_due+")</td></tr>";
	html_string += "<th>Author</th><td>"+author+"</td></tr>";
	html_string += "<th>Summary</th><td>"+summary+"</td></tr></table>";
	output.innerHTML = html_string;
}


//	Submits the current exercise and returns details via "tool_output" div
function submitExercise()	{
	const FD = new FormData(document.getElementById("create_exercise"));
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById("tool_output").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST","/create_exercise/");
	xhttp.send(FD);
	document.getElementById("button_criteria").disabled = false;
}
function importExercise()	{
	const FD = new FormData(document.getElementById("import_exercise"));
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			//document.getElementById("tool_output").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST","/import_exercise/");
	xhttp.send(FD);
	document.getElementById("button_criteria").disabled = false;
	exerciseOutput('button_import_exercise');
}

function selectCriteria()	{
	const FD = new FormData(document.getElementById("select_criteria"));
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById("tool_output_horizontal").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST","/select_criteria/");
	xhttp.send(FD);
	document.getElementById("button_digest").disabled = false;
}

function selectTemplate()	{
	const FD = new FormData(document.getElementById("select_template"));
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById("tool_output_horizontal").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST","/select_template/");
	xhttp.send(FD);
}

function importDigest()	{
	const FD = new FormData(document.getElementById("digest_upload"));
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById("tool_output").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST","/import_digest/");
	xhttp.send(FD);
	document.getElementById("button_scores").disabled = false;
}
function doScores()	{
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById("tool_output_horizontal").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST","/process_scores/");
	xhttp.send();
}

function exportScores()	{
	var xhttp	= new XMLHttpRequest();
	xhttp.onreadystatechange  = function()	{
		if(this.readyState == 4 && this.status == 200)	{
			document.getElementById("tool_output_horizontal").innerHTML = this.responseText;
		}
	};
	xhttp.open("POST","/export_scores/");
	xhttp.send();	
}
