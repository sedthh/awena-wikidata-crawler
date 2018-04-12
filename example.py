# -*- coding: UTF-8 -*-

import awena

if __name__ == "__main__":
	query		= 'Einstein'
	crawler		= awena.Crawler('en')
	id				= crawler.search(query)
	info			= crawler.load(id)
	print(info)
	
	citizen_of	= crawler.load(info["citizen"])
	print(citizen_of)