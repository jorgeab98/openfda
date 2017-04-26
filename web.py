import http.client
import json
import http.server
import socketserver

# Copyright [2017] [Jorge Arroyo Blanco]

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and limitations under the License.

# Author : Jorge Arroyo Blanco

class OpenFDAClient():
	
	OPENFDA_API_URL="api.fda.gov"
	OPENFDA_API_EVENT="/drug/event.json"
	OPENFDA_API_LYRICA="/drug/event.json?search=patient.drug.medicinalproduct:"
	OPENFDA_API_COMPANY="/drug/event.json?search=companynumb:"

	def get_event(self,LIMIT):
		conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)	
		conn.request("GET",self.OPENFDA_API_EVENT + "?limit=" + LIMIT)
		r1 = conn.getresponse()
		data = r1.read()
		data1=data.decode("utf8")
		data2=json.loads(data1)
		return data2
		
	def get_event_lyrica(self,LIMIT):
		conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)	
		conn.request("GET",self.OPENFDA_API_LYRICA + LIMIT + "&limit=10")
		r1 = conn.getresponse()
		data = r1.read()
		data1=data.decode("utf8")
		data2=json.loads(data1)
		return data2
		
	def get_event_company(self,LIMIT):
		conn=http.client.HTTPSConnection(self.OPENFDA_API_URL)	
		conn.request("GET",self.OPENFDA_API_COMPANY + LIMIT + "&limit=10")
		r1 = conn.getresponse()
		data = r1.read()
		data1=data.decode("utf8")
		data2=json.loads(data1)
		return data2
			
class OpenFDAParser():
	
	def look_drugs(self,event):
		lista_medicamentos=[]
		event1=event['results']
		for event in event1:
			event2=event["patient"]["drug"][0]['medicinalproduct']
			event3=json.dumps(event2)
			lista_medicamentos+=[event3]
		return lista_medicamentos
		
	def look_for_drug(self,busqueda):
		lista_lyrica=[]
		for event in busqueda['results']:
			a=event["companynumb"]
			lista_lyrica+=[a]
		return lista_lyrica
		
	def look_companies(self,company):
		lista_empresas=[]
		company1=company['results']
		for company in company1:
			company2=company['companynumb']
			company3=json.dumps(company2)
			lista_empresas+=[company3]
		return lista_empresas
		
	def look_for_companies(self,busqueda_empresas):
		lista_companies=[]
		empresa1=busqueda_empresas['results']
		for busqueda_empresas in empresa1:
			empresa2=busqueda_empresas["patient"]["drug"][0]['medicinalproduct']
			lista_companies+=[empresa2]
		return lista_companies
	
	def look_gender(self,sex):
		lista_sex=[]
		sex1=sex['results']
		for sex in sex1:
			sex2=sex["patient"]["patientsex"]
			sex3=json.dumps(sex2)
			lista_sex+=[sex3]
		return lista_sex
		
	def look_age(self,age):
		lista_age=[]
		age1=age['results']
		for age in age1:
			if "patientonsetage" in age["patient"]:
				age2=age["patient"]["patientonsetage"]
			else:
				age2="-"
			age3=json.dumps(age2)
			lista_age+=[age3]
		return lista_age
	
class OpenFDAHTML():
	
	def get_main_page(self):
		html='''
        <html> 
			<head>
				<title>OpenFDA Cool App</title>
			</head>
			<body>
				<h1>OpenFDA Client</h1>
				<form method="get" action="listDrugs">
					<input type="submit" value="Medicamentos">
					</input>
					Limite:
					<input name="drug_limit" type="text" >
					</input>
				</form>
				<form method="get" action="searchDrug">
					<input name="drug" type="text" >
					</input>
					<input type="submit" value="Buscar medicamento">
					</input>
				</form>
				
				<form method="get" action="listCompanies">
					<input type="submit" value="Empresas">
					</input>
					Limite:
					<input name="companies_limit" type="text" >
					</input>
				</form>
				<form method="get" action="searchCompany">
					<input name="company" type="text" >
					</input>
					<input type="submit" value="Buscar empresa">
					</input>
				</form>
				
				<form method="get" action="listGender">
					<input type="submit" value="Sexos">
					</input>
					Limite:
					<input name="sex_limit" type="text" >
					</input>
				</form>
			</body>
        </html> 
		'''
		return html
		
	def get_main_page2(self):
		html2='''
        <html> 
			<head>
				<title>OpenFDA Cool App</title>
			</head>
			<body>
				<form method="get" action="listAge">
					<input type="submit" value="Edades">
					</input>
					Limite:
					<input name="age_limit" type="text" >
					</input>
				</form>
			</body>
        </html> 
		'''
		return html2
	
	def get_html_event_drug(self,lista_medicamentos):
		html_event_drug='''
		<html>
			<head>
				<title>Medicamentos</title>
			</head>
			<body>
				<h1>Medicamentos</h1>
				<ol>
		'''
		for i in lista_medicamentos:
			html_event_drug+='<li>'+i+'</li>'
		html_event_drug+='''
				</ol>
			</body>
		</html>
		'''
		return html_event_drug
		
	def get_html_event_company(self,lista_empresas):
		html_event_company='''
		<html>
			<head>
				<title>Empresas</title>
			</head>
			<body>
				<h1>Empresas</h1>
				<ol>
		'''
		for i in lista_empresas:
			html_event_company+='<li>'+i+'</li>'
		html_event_company+='''
				</ol>
			</body>
		</html>
		'''
		return html_event_company
		
	def get_html_lyrica(self,lista_lyrica):
		html_lyrica='''
		<html>
			<head>
				<title>Empresas</title>
			</head>
			<body>
				<h1>Empresas</h1>
				<ol>
		'''
		for i in lista_lyrica:
			html_lyrica+='<li>'+i+'</li>'
		html_lyrica+='''
				</ol>
			</body>
		</html>
		'''
		return html_lyrica
		
	def get_html_companies(self,lista_companies):
		html_companies='''
		<html>
			<head>
				<title>Medicamentos</title>
			</head>
			<body>
				<h1>Medicamentos</h1>
				<ol>
		'''
		for i in lista_companies:
			html_companies+='<li>'+i+'</li>'
		html_companies+='''
				</ol>
			</body>
		</html>
		'''
		return html_companies
		
	def get_html_event_sex(self,lista_sex):
		html_event_sex='''
		<html>
			<head>
				<title>Sexos</title>
			</head>
			<body>
				<h1>Sexos</h1>
				<ol>
		'''
		for i in lista_sex:
			html_event_sex+='<li>'+i+'</li>'
		html_event_sex+='''
				</ol>
			</body>
		</html>
		'''
		return html_event_sex
		
	def get_html_event_age(self,lista_age):
		html_event_age='''
		<html>
			<head>
				<title>Edades</title>
			</head>
			<body>
				<h1>Edades</h1>
				<ol>
		'''
		for i in lista_age:
			html_event_age+='<li>'+i+'</li>'
		html_event_age+='''
				</ol>
			</body>
		</html>
		'''
		return html_event_age
		
	def get_html_error(self):
		html_event_error='''
		<html>
			<head>
				<title>ERROR 404</title>
			</head>
			<body>
			<h1>ERROR 404
			NOT FOUND
			</h1>
			</body>
		</html>
		'''
		return html_event_error

class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler): 
		
	def get_any_drug(self):
		drug1=self.path.split("=")[1]
		return drug1
		
	def do_GET(self):
		
		html=OpenFDAHTML()
		client=OpenFDAClient()
		parser=OpenFDAParser()
		
		main_page = False
		is_event_drug = False
		is_searchDrug = False
		is_event_company = False
		is_searchCompany = False
		is_event_sex = False
		is_error = False
		is_found = False
		is_secret = False
		is_redirect = False
		is_event_age = False
		main_page2 = False
		
		if self.path == '/':
			main_page=True
			is_found=True
		elif "/listDrugs" in self.path:
			is_event_drug=True
			is_found=True
		elif "searchDrug" in self.path:
			is_searchDrug=True
			is_found=True
		elif "/listCompanies" in self.path:
			is_event_company=True
			is_found=True
		elif "searchCompany" in self.path:
			is_searchCompany=True
			is_found=True
		elif "/listGender" in self.path:
			is_event_sex=True
			is_found=True
		elif "/secret" in self.path:
			is_secret=True
			is_found=True
		elif "/redirect" in self.path:
			is_redirect=True
			is_found=True
		elif "/listAge" in self.path:
			is_event_age=True
			is_found=True
		elif "/age" in self.path:
			main_page2=True
			is_found=True
		else:
			is_error=True
			
		if is_secret:
			self.send_response(401)
			self.send_header('WWW-Authenticate','Basic realm="Login required"')
		elif is_redirect:
			self.send_response(302)
			self.send_header('Location','/')
		elif is_found:
			self.send_response(200)
			self.send_header('Content-type','text/html')
		else:
			self.send_response(404)
			self.send_header('Content-type','text/html')
			
		self.end_headers()
		html_page = html.get_main_page()
		
		if main_page:
			self.wfile.write(bytes(html_page, "utf8"))
		elif main_page2:
			self.wfile.write(bytes(html.get_main_page2(), "utf8"))
		elif is_event_drug:
			LIMIT=self.get_any_drug()
			event=client.get_event(LIMIT)
			medicamentos=parser.look_drugs(event)
			html_medicine=html.get_html_event_drug(medicamentos) 
			self.wfile.write(bytes(html_medicine, "utf8"))	
		elif is_searchDrug:
			LIMIT=self.get_any_drug()
			busqueda=client.get_event_lyrica(LIMIT)
			drug_searched=parser.look_for_drug(busqueda)
			html_lyrica=html.get_html_lyrica(drug_searched) 
			self.wfile.write(bytes(html_lyrica, "utf8"))	
	
		elif is_event_company:
			LIMIT=self.get_any_drug()
			company=client.get_event(LIMIT)
			empresas=parser.look_companies(company)
			html_company=html.get_html_event_company(empresas)
			self.wfile.write(bytes(html_company, "utf8"))
		elif is_searchCompany:
			LIMIT=self.get_any_drug()
			busqueda_empresas=client.get_event_company(LIMIT)
			company_searched=parser.look_for_companies(busqueda_empresas)
			html_companies=html.get_html_companies(company_searched) 
			self.wfile.write(bytes(html_companies, "utf8"))
		
		elif is_event_sex:
			LIMIT=self.get_any_drug()
			sex=client.get_event(LIMIT)
			generos=parser.look_gender(sex)
			html_sex=html.get_html_event_sex(generos) 
			self.wfile.write(bytes(html_sex, "utf8"))	
			
		elif is_event_age:
			LIMIT=self.get_any_drug()
			age=client.get_event(LIMIT)
			edades=parser.look_age(age)
			html_age=html.get_html_event_age(edades) 
			self.wfile.write(bytes(html_age, "utf8"))
			
		else:
			html_error=html.get_html_error() 
			self.wfile.write(bytes(html_error, "utf8"))
		return
