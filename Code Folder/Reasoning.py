from rdflib import Graph

import owlrl


def OWLRLInference():
    
    g = Graph()
    #import old triples
    g.parse("new_pizza_triples.ttl", format="ttl")    
    
    print("Loaded '" + str(len(g)) + "' triples.")
    #import ontology
    g.load("ollie_keers.owl",  format="xml")
    
   
    
    #Performs RDFS reasoning adapted from Ernesto Jimenez-Ruiz
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(g)
    
    
    print("After inference rules: '" + str(len(g)) + "' triples.")
    

    print("\nSaving extended graph")
    #exporting to xml format as this can be read by protege, but ttl cannot
    g.serialize(destination='pizza_inference.rdf', format='xml')
    #exporting to ttl format as per marking requirements
    g.serialize(destination='pizza_inference.ttl', format='ttl')

    



OWLRLInference()

