# Awena is a Python3 Wikidata search library that parses the returned Data type results to a human-readable format

The library uses the Wikidata JSON Rest Api to fetch data instead of querying its Query Service. No knowledge of SPARQL is necessary to use this tool. You can just keep iterating through relevant item ids instead.

Awena lets you search for names, labels, etc. and use their ids to load their information from the knowledge graph:

```python
import awena

query		= 'Einstein'
crawler		= awena.Crawler('en') # set language of results
id		= crawler.search(query)	# will return "Q937"
info		= crawler.load(id)
print(info)
	
>>> {
>>>	'label': 'Albert Einstein', 
>>>	'description': 'German-born physicist and founder of the theory of relativity', 
>>>	'sex': 'male', 
>>>	'citizen': 'Q43287', 
>>>	'father': 'Q88665', 
>>>	'mother': 'Q4357787', 
>>>	'number_of_siblings': 1, 
>>>	'number_of_children': 3, 
>>>	'occupation': 'Q19350898', 
>>>	'date_of_birth': '+1879-03-14T00:00:00Z', 
>>>	'place_of_birth': 'Q3012', 
>>>	'date_of_death': '+1955-04-18T00:00:00Z', 
>>>	'place_of_death': 'Q138518', 
>>>	'cause_of_death': 'Q616003'
>>> }
```

Some values are also valid ids, that you can use the same way to receive information about them:

```python
citizen_of	= crawler.load(info["citizen"])
print(citizen_of)

>>> {
>>>	'label': 'German Empire', 
>>>	'description': 'empire in Central Europe between 1871–1918'
>>> }

```

