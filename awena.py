# -*- coding: UTF-8 -*-

# Awena - Alternative Wikidata Enquiry Application

import requests

class Crawler:

	VERSION					= "0.1"
	USER_AGENT			= "Mozilla/5.0 (compatible; Awena/"+VERSION+"; +https://github.com/sedthh/awena-wikidata-crawler/)"

	##### CONSTRUCTOR #####
	def __init__(self,	lang='en'):
		self.lang				= lang
		self.cache				= {}
		
	##### DATA MODEL #####
	def __repr__(self):
		return "<Awena Search instance at {0}>".format(hex(id(self)))
		
	def __str__(self):
		return self.query

	def __len__(self):
		return len(self.cache)
		
	def __eq__(self, other):
		if isinstance(other, bool):
			return bool(self.cache)==other
		return False
	
	def __ne__(self, other):
		return not self.__eq__(other)
	
	##### CLASS FUNCTIONS #####
	
	def search(self, query):
		return self._request(query,False)
		
	def load(self,id):
		if id not in self.cache:
			data		= self._request(False,id)
			self.cache[id]= self._parse(data,id)
		return self.cache[id]
	
	def _request(self,query=False,id=False):
		headers	= {
			"User-Agent"	: Crawler.USER_AGENT
		}
		if id:
			params	= {
				"action"			: "wbgetentities",
				"ids"				: id,
				"language"	: self.lang,
				"format"		: "json"
			}
		else:
			params	= {
				"action"			: "wbsearchentities",
				"search"		: query,
				"language"	: self.lang,
				"format"		: "json"
			}
		data		= requests.get("https://www.wikidata.org/w/api.php",headers=headers,params=params)
		result	= data.json()
		if 'error' in result:	
			raise Exception(result['error']['code'],result['error']['info'])
		elif query and "search" in result and result["search"]:
			if "id" in result["search"][0]:
				return result["search"][0]["id"]
		elif id and "entities" in result and result["entities"]:
			if id in result["entities"] and result["entities"][id]:
				return result["entities"][id]
		return {}
		
	def _parse(self,data,id):
		result	= {"id":id}
		if data:
			if "labels" in data:
				if self.lang in data["labels"]:
					 result["label"]			= data["labels"][self.lang]["value"]
			if "descriptions" in data:
				if self.lang in data["descriptions"]:
					result["description"]	= data["descriptions"][self.lang]["value"]
			if "claims" in data:
				# results to human readable format
				for key	in data["claims"]:
					# humans
					if key=="P21":		# sex
						if data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"] in ("Q6581097","Q44148"):
							result["sex"]					= "male"
						elif data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"] in ("Q6581072","Q43445"):
							result["sex"]					= "female"
						else:
							result["sex"]					= "other"
					elif key=="P27":	# country of citizenship
						result["country"]			= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"]
					elif key=="P106":	# occupation
						result["occupation"]		= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"]
					elif key=="P22":	# father
						result["father"]				= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"]
					elif key=="P25":	# mother
						result["mother"]			= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"]
					elif key=="P40":	#children
						result["number_of_children"]= len(data["claims"][key])
					elif key=="P3373":# siblings
						result["number_of_siblings"]= len(data["claims"][key])
					elif key=="P569": # date of birth
						result["date_of_birth"]	= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["time"]
					elif key=="P19": 	# place of birth
						result["place_of_birth"]	= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"]
					elif key=="P570": 	# date of death
						result["date_of_death"]	= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["time"]
					elif key=="P20": 	# place of death
						result["place_of_death"]= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"]
					elif key=="P509":	# cause of death
						result["cause_of_death"]= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"]
					#locations
					elif key=="P30":	# continent
						result["continent"]			= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"]
					elif key=="P17":	# country
						result["country"]			= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["id"]
					elif key=='P625':	# coordinate location
						result['coordinates']		= str(data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["latitude"])+" "+str(data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["longitude"])
					elif key=='P1082':#population
						result["population"]		= float(data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["amount"][1:])
					elif key=='P2046':#area
						if "Q712226" in data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["unit"]: #km2
							result["population"]		= data["claims"][key][0]["mainsnak"]["datavalue"]["value"]["amount"][1:]+" km2"
		return result		
					