"""
Created on Mon Mar 22 09:23:57 2021

@author: ollie
"""
from rdflib import Graph

def query1():

   
    g = Graph()
    g.parse("pizza_inference.ttl", format="ttl")

    
        
    print("Query SPARQL.2:")
    
    qres = g.query(
    """SELECT ?name ?address ?city_name WHERE{
   ?entity a ok:Bianca ;
           ok:soldBy ?establishment .
   ?establishment ok:establishmentName ?name ;
               ok:hasAddress ?add ;
               ok:inCity ?city .
    ?add ok:addressName ?address .
    ?city ok:cityName ?city_name .
    }""")

    
    f_out = open('query1.csv',"w+")
    for row in qres:
            #Row is a list of matched RDF terms: URIs, literals or blank nodes
       print(row.name, row.address, row.city_name)
       line_str = '\"%s\","%s\","%s\"\n' % (row.name, row.address, row.city_name)
       f_out.write(line_str)

    f_out.close()

def query2():

   
    g = Graph()
    g.parse("pizza_inference.ttl", format="ttl")

    
        
    print("Query SPARQL.3:")
    
    qres = g.query(
    """SELECT ( ROUND(100*AVG (?x))/100 AS ?average) ?cc
    WHERE{
   ?entity a ok:Margherita ;
        ok:hasPrice ?x .
   ?entity ok:soldBy ?est .
   ?est ok:inCountry ?country .
   ?country ok:hasCurrency ?currency .
   ?currency ok:currencyCode ?cc .
    
    }""")

 
        
    for row in qres:
        #Row is a list of matched RDF terms: URIs, literals or blank nodes
        print("Average price for a Margherita is %s %s" % (str(row.average), str(row.cc)))
   
def query3():

   
    g = Graph()
    g.parse("pizza_inference.ttl", format="ttl")

    
        
    print("Query SPARQL.4:")
    
    qres = g.query(
    """SELECT ?city_name ?state_name (COUNT (?x) AS ?howmany) 
    WHERE{
   ?x a ok:Establishment ;
        ok:inCity ?city ;
        ok:inState ?state .
   ?state ok:stateName ?state_name .
   ?city ok:cityName ?city_name .
    }
    GROUP BY ?city
    ORDER BY ?state_name ?howmany
    """)

 
        
    for row in qres:
        #Row is a list of matched RDF terms: URIs, literals or blank nodes
        print("%s, %s has %s establishments" % (str(row.city_name), str(row.state_name), str(row.howmany)))        
   
    
def query4():

   
    g = Graph()
    g.parse("pizza_inference.ttl", format="ttl")

    
        
    print("Query SPARQL.5:")
    
    qres = g.query(
    """SELECT ?x
    WHERE {
        ?x a ok:Establishment .
        FILTER NOT EXISTS { ?x  ok:inPostcode ?any .}
    } """)
    
    for row in qres:
        #Row is a list of matched RDF terms: URIs, literals or blank nodes
        print(row.x)
    
query1()
query2()
query3()
query4()