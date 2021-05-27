#Adapted from code from Ernesto Jimenez-Ruiz
from owlready2 import *
from rdflib import Graph, URIRef
from rdflib import Namespace
from rdflib.namespace import OWL, RDF, RDFS
import Levenshtein as lev 


def getClasses(onto):        
    return onto.classes()
    
def getDataProperties(onto):        
    return onto.data_properties()
    
def getObjectProperties(onto):        
    return onto.object_properties()
    
def getIndividuals(onto):    
    return onto.individuals()


def getRDFSLabelsForEntity(entity):
    #if hasattr(entity, "label"):
    return entity.label


def getRDFSLabelsForEntity(entity):
    #if hasattr(entity, "label"):
    return entity.label    


def loadOntology(urionto):
    
    #Method from owlready
    onto = get_ontology(urionto).load()
    
    print("Classes in Ontology: " + str(len(list(getClasses(onto)))))
    for cls in getClasses(onto):
        #Name of entity in URI. But in some cases it may be a 
        #code like in mouse and human anatomy ontologies                
        print(cls.iri)
        print("\t"+cls.name)  
        #Labels from RDFS label
        print("\t"+str(getRDFSLabelsForEntity(cls)))
        

def getEntities(urionto):
    onto = get_ontology(urionto).load()
    
    entity_list = []

    for cls in getClasses(onto):
        entity = cls.name
        entity_list.append(entity)
    return entity_list

def getProperties(urionto):
    onto = get_ontology(urionto).load()
    
    prop_list = []
    for dp in getDataProperties(onto):
        prop = dp.name
        prop_list.append(prop)
    for op in getObjectProperties(onto):
        prop = op.name
        prop_list.append(prop)
    return prop_list

#Load ontology from URI or local file
ok="ollie_keers.owl"
pizza="pizza.owl"

ok_ent = getEntities(ok)
ok_prop = getProperties(ok)
pizza_ent = getEntities(pizza)
pizza_prop = getProperties(pizza)

g = Graph()

g.bind("owl", OWL)

for o in ok_ent:
    for p in pizza_ent:
        d = o.lower().replace("_", "")
        f = p.lower().replace("_", "")
        if len(d) > len(f):
            x = len(d)
        else:
            x = len(f)
        if (lev.distance(d, f) / x) < 0.3:
            node = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format(o))
            node2 = URIRef("http://www.co-ode.org/ontologies/pizza#{}".format(p))
            g.add((node, OWL.equivalentClass, node2))
            g.add((node2, OWL.equivalentClass, node))
            
for o in ok_prop:
    for p in pizza_prop:
        d = o.lower().replace("_", "")
        f = p.lower().replace("_", "")
        if len(d) > len(f):
            x = len(d)
        else:
            x = len(f)
        if (lev.distance(d, f) / x) < 0.3:
            node = URIRef("http://www.city.ac.uk/ds/inm713/ollie_keers/{}".format(o))
            node2 = URIRef("http://www.co-ode.org/ontologies/pizza#{}".format(p))
            g.add((node, OWL.equivalentProperty, node2))
            g.add((node2, OWL.equivalentProperty, node))

print(g.serialize(format="turtle").decode("utf-8"))   
g.serialize(destination='equivalences.ttl', format='ttl')