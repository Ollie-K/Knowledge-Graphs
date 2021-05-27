from rdflib import Graph

import owlrl


def OWLRLInference():
    
    g = Graph()
    #import old triples
    g.parse("new_pizza_triples.ttl", format="ttl")    
    print("Loaded '" + str(len(g)) + "' triples.")
    #import ontology
    g.load("ollie_keers.owl",  format="xml")
    g.load("pizza.owl",  format="xml")
    g.load("equivalences.ttl", format="ttl")
   
    
    #Performs RDFS reasoning adapted from Ernesto Jimenez-Ruiz
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, axiomatic_triples=False, datatype_axioms=False).expand(g)
    
    
    print("After inference rules: '" + str(len(g)) + "' triples.")

    print("\nSaving extended graph")
    #exporting to xml format as this can be read by protege, but ttl cannot
    g.serialize(destination='reasoned_data_alignments.rdf', format='xml')
    #exporting to ttl format as per marking requirements
    g.serialize(destination='reasoned_data_alignments.ttl', format='ttl')

    qres = g.query(
    """ASK {?any a pizza:MeatyPizza . }""")

    #Single row with one boolean vale
    for row in qres:
        print("Are there any members of pizza:MeatyPizza? " + str(row))
        
        
    qres = g.query(
    """ASK {?any a ok:Meaty_Item . }""")

    #Single row with one boolean vale
    for row in qres:
        print("Are there any members of ok:Meaty_Item? " + str(row))

    qres = g.query(
    """ASK {?any a ok:Margherita . }""")

    #Single row with one boolean vale
    for row in qres:
        print("Are there any members of ok:Margherita? " + str(row))

OWLRLInference()

