from bs4 import BeautifulSoup as bs
import lxml
import xlence_app as xlence
import re

class Template:
	def __init__(self, name, text_file):
		self.name = name
		self.text_file = text_file
		self.location = "/".join(text_file.split("/")[:-1:])
		self.text_data = self.getText()
		self.form_file = self.location+"/"+self.getForms()
		self.form_data = self.getFormData()
		self.fields = self.getVars()
		
	def getForms(self):
		fh = open(self.text_file,"rb")
		form_name = fh.readlines(1)[0].decode()
		fh.close()
		form_name = form_name.replace(": ",":").replace("Form:","").replace("\r","").replace("\n","").split(",")[0]
		return form_name
		
	def getFormData(self):
		fh = open(self.form_file,"rb")
		form_data = fh.read().decode()
		fh.close()
		self.html = bs(form_data)
		self.inputs = self.html.find_all("input")
		return form_data
		
	def getText(self):
		fh = open(self.text_file,"rb")
		text_data = fh.read().decode()
		fh.close()
		return text_data
	
	def getVars(self):
		search_string = "<var (.+?)>"
		variables_used = re.findall(search_string, self.text_data)
		variables_used = list(dict.fromkeys(variables_used))
		return variables_used
		
	def prepareHTML(self):
		thwart_strg = "{MsgSender}"
		onsubmit_strg = "return confirm('To complete your form submission, click OK and close the open browser window. You will return to the new message window so you can post your message to the outbox');"
		processor_strg = "http://{FormServer}:{FormPort}"
		this_html = self.form_data.replace(thwart_strg,"").replace(onsubmit_strg,"").replace(processor_strg,"/save_criteria/")
		return this_html
	
	def selectCriteria(self):
		html_string = """
		<form method="POST" id="select_criteria">
		<table>
		<tr>
			<th>Variable</th>
			<td></td>
			<th>Ignore</th>
			<th>Set?</th>
			<th>Equal to?</th>
			<th>Contains?</th>
			<td></td>
		</tr>
		"""
		for var in self.fields:
			strg = """
				<tr>
					<th><VAR></th>
					<td></td>
					<td>
						<input type="radio" name="<VAR>" value="ignore" checked="true">
					</td>
					<td>
						<input type="radio" name="<VAR>" value="set">
					</td>
					<td>
						<input type="radio" name="<VAR>" value="equals">
					</td>
					<td>
						<input type="radio" name="<VAR>" value="contains">
					</td>
					<td>
						<input type="text" name="<VAR>-comparison">
					</td>
				</tr>
			""".replace("<VAR>",var)
			html_string += strg
		
		html_string+="""
			<tr>
				<td></td>
				<td></td>
				<td></td>
				<td></td>
				<td><input type="button" value="Reset" onclick="document.getElementById().reset();"></td>
				<td><input type="button" value ="Submit" onclick="selectCriteria();"></td>
				<td></td>
			</tr>
			</table>
		</form>
		"""
		return html_string