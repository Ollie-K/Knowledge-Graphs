from rdflib import Graph
from rdflib import URIRef, BNode, Literal
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS, XSD
import pandas as pd
from stringcmp import isub #created by Ernesto Jimenez-Ruiz
from lookup import DBpediaLookup #breated by Ernesto Jimenez-Ruiz
import owlrl

def createTriples():
    
    #Empty graph
    g = Graph()
    #read in the pizza csv
    pizza = pd.read_csv('pizza.csv')

    #Creating Namespaces 
    ok = Namespace("http://www.city.ac.uk/ds/inm713/ollie_keers/")
    rdf = Namespace("http://www.w3.org/1999/02/22-rdf-syntax-ns#")
    rdfs = Namespace("http://www.w3.org/2000/01/rdf-schema#")
    owl = Namespace("http://www.w3.org/2002/07/owl#")
    dbo = Namespace("https://dbpedia.org/ontology/")
    dbp = Namespace("https://dbpedia.org/resource/")
       
    #Prefixes
    g.bind("ok", ok) 
    g.bind("rdf", rdf) 
    g.bind("rdfs", rdf)
    g.bind("owl", owl)
    g.bind("dbo", dbo)
    g.bind("dbp", dbp)
    nm = g.namespace_manager

    dbpedia = DBpediaLookup()    #lookup function from Ernesto Jimenez-Ruiz

    c_dict = {} #empty dictionary for cities to cut down on endpoint queries
    s_dict = {} #empty dictionary for states to cut down on endpoint queries
    last_country = 'temp' # variable to save on endpoint queries
    #general triples for classes
    g.add((ok.Menu_Item, rdf.type, owl.Class))
    g.add((ok.Menu_Item, rdfs.subClassOf, ok.Food))
    g.add((ok.Establishment, rdf.type, owl.Class))
    g.add((ok.Place, rdf.type, owl.Class))
    #looping through pizza dataset to establish triples
    for index, row in pizza.iterrows():
        
        ###General URI Creation###
        #creating a URI for each row in the table, corresponding to an individual item for sale in an establishment
         node = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/product_{}".format(index))
         #creating a URI for each establishment
         estab = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format(row['name']).lower().replace(" ", "_").replace("|", "").replace(",", "").replace("\\", "").replace("’", "").replace("(", "").replace(")", ""))
         #creating a URI for each item
         item = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format((row['menu item']).lower().replace(" ", "_").replace("|", "").replace(",", "").replace("’", "").replace("(", "").replace(")", "")))
         #creating a URI for each address
         address = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format((row['address']).lower().replace(" ", "_").replace("|", "").replace("’", "").replace("(", "").replace(")", "")))

###line below can be uncommented if you want to use local city URIs rather than querying endpoints
         #city = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format((row['city']).lower().replace(" ", "_").replace("|", "").replace("’", "").replace("(", "").replace(")", "")))
         
         #if the city has already been queried, don't query it again, but use locally held information instead
         if row['city'] in c_dict:
             city = c_dict[row['city']]
        #otherwise query dbpedia to find most similar entry 
        #code below from Ernesto Jimenez-Ruiz
         else:
             entities = dbpedia.getKGEntities(row['city'], 5)
             current_sim = -1
             current_uri=''
             for ent in entities:           
                 isub_score = isub(row['city'], ent.label) 
                 if current_sim < isub_score:
                     current_uri = ent.ident
                     current_sim = isub_score
             #set city to the best URI, and also update the dictionary to contain this URI to speed up future querying
             city = URIRef(current_uri)
             c_dict[row['city']] = city
 
###as above for cities but for states
         #state = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format((row['state']).lower().replace(" ", "_").replace("|", "").replace("’", "").replace("(", "").replace(")", "")))
    
         if row['state'] in s_dict:
             state = s_dict[row['state']]
         else:
             entities = dbpedia.getKGEntities(row['state'], 5)
             current_sim = -1
             current_uri=''
             for ent in entities:           
                 isub_score = isub(row['state'], ent.label) 
                 if current_sim < isub_score:
                     current_uri = ent.ident
                     current_sim = isub_score
             state = URIRef(current_uri)
             s_dict[row['state']] = state
             
 ###as above but for countries
         #country = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format((row['country']).lower().replace(" ", "_").replace("|", "").replace("’", "").replace("(", "").replace(")", "")))

         if row['country'] == last_country:
             country = country
         else:
            if row['country']:
                last_country = row['country']
                entities = dbpedia.getKGEntities(row['country'], 5)
                current_sim = -1
                current_uri=''
                for ent in entities:           
                    isub_score = isub(row['country'], ent.label) 
                    if current_sim < isub_score:
                        current_uri = ent.ident
                        current_sim = isub_score
                    country = URIRef(current_uri)
         
         #turning category labels for establishments into a list           
         cat_list = row['categories'].split(",")
         #getting the item price
         price = row['item value']
         #setting the currency
         currency = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format((str(row['currency'])).lower().replace(" ", "_").replace("|", "").replace(",", "").replace("’", "").replace("(", "").replace(")", "")))
         #getting item descriptive data
         description = row['item description']
         #Each row represents an individual item
         g.add((node, rdf.type, owl.NamedIndividual))
         #that is sold by an establishment
         g.add((node, ok.soldBy, estab))
         #that establishment sells that item
         g.add((estab, ok.sells, node))
         #the establishemnt is an Establishment
         g.add((estab, rdf.type, ok.Establishment))
         #the establishment is an individual 
         g.add((estab, rdf.type, owl.NamedIndividual))
         #The name of the establishment is stored as a string
         g.add((estab, ok.establishmentName, Literal(row['name'])))
         #Each node is an example of this type of menu item
         g.add((node, rdf.type, item))
         #this type of menu item is a subclass of menu items
         g.add((item, rdfs.subClassOf, ok.Menu_Item))
         #The name of the menu item is stored as a string
         g.add((node, ok.itemName, Literal(row['menu item'])))
         #if an item contains these terms, assign it to the 'bianca' class
         if ("bianca" or "white" or "bianco") in row['menu item'].lower():
             g.add((node, rdf.type, ok.Bianca))
         #if the item contains 'margherita' assign it to the 'margherita' class
         if ("margherita") in row['menu item'].lower():
             g.add((node, rdf.type, ok.Margherita))
         #if there is a description for the item, keep the description as a string
         if str(description) != "nan":
             g.add((node, ok.itemDescription, Literal(str(description))))
         #if a price is given, store it as a literal
         if price > 0.0:
            if type(price) == int:
                 price = float(price)
            g.add((node, ok.hasPrice, Literal(price)))
         #add the establishment address as a URI
         g.add((estab, ok.hasAddress, address))
         #for each of the categories listed for an establishment
         for cat in cat_list:
            #if it contains the word 'restaurant' assign it to 'DineIn' class
            if 'restaurant' in cat.lower():
                g.add((estab, rdf.type, ok.DineIn))
            #if it contains the word 'take' assign it to the "TakeAway" class
            if 'take' in cat.lower():
                g.add((estab, rdf.type, ok.TakeAway))
            #in any case, create a category URI for that descriptor as a 'hashtag'
            category = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/#{}".format(cat.lstrip().lower().replace(" ", "_").replace("|", "").replace(",", "").replace("\\", "").replace("\’", "").replace("\(", "").replace("\)", "").replace("and_", "")))
            #This establishment has that hashtag
            g.add((estab, rdf.type, category))
            #and that category is a subclass of an establishment
            g.add((category, rdfs.subClassOf, ok.Establishment))
        #the address URI is an address
         g.add((address, rdf.type, ok.Address))
         #and that has the street address stored as a string
         g.add((address, ok.addressName, Literal(row['address'])))
         #if the postcode exists, add it as a URI, and associate other location information with it.
         if str(row['postcode']) != "nan":
             postcode = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format((row['postcode'])))
             g.add((postcode, rdf.type, ok.Postcode))
             g.add((estab, ok.inPostcode, postcode))
             g.add((address, ok.inPostcode, postcode))
             g.add((address, ok.locatedIn, postcode))
         #add location information about the city
         g.add((estab, ok.inCity, city))
         g.add((address, ok.inCity, city))
         g.add((postcode, ok.inCity, city))
         g.add((postcode, ok.locatedIn, city))
         g.add((city, rdf.type, ok.City))
         g.add((city, ok.cityName, Literal(row['city'])))
         #add location information about the state
         g.add((estab, ok.inState, state))
         g.add((address, ok.inState, state))
         g.add((postcode, ok.inState, state))
         g.add((city, ok.inState, state))
         g.add((city, ok.locatedIn, state))
         g.add((state, rdf.type, ok.State))
         g.add((state, ok.stateName, Literal(row['state'])))
         #add location information about the country
         g.add((estab, ok.inCountry, country))
         g.add((address, ok.inCountry, country))
         g.add((postcode, ok.inCountry, country))
         g.add((city, ok.inCountry, country))            
         g.add((state, ok.inCountry, country))
         g.add((state, ok.locatedIn, country))
         g.add((country, rdf.type, ok.Country))
         g.add((country, ok.countryName, Literal(row['country'])))
         #if both the country and the currency exist, assign that currency to the country
         if country and str(row['currency']) != "nan":
           # g.add((URIRef(country), ok.hasCurrency, currency))
            g.add((country, ok.hasCurrency, currency))
            g.add((currency, ok.currencyCode, Literal(row['currency'])))
        #counter to check that endpoint queries are running
         if index % 100 == 0:
            print(index)
    #export triples into file
    g.serialize(destination='new_pizza_triples.ttl', format='ttl')
    
createTriples()

