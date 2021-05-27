"""
Created on Thu Apr  1 10:19:26 2021

@author: ollie
"""
Scripts within this file are intended to be viewed/run in the following order:

1. readme.md - this file. Provides an overview of the other scripts, files & folders.
2. pizza.csv - the raw csv file of data that was the basis for this work.
3. ollie_keers.owl - the created ontology, to be viewed in protege if possible. 
    Upon loading the ontology, it is recommended to open the CoModIDE tab to get a schematic overview of the ontology.
4. csv2rdf.py - a script for generating triples from the csv. 
    This is currently configured to query dbpedia for places, but you can comment this out & uncomment relevant lines for faster runtimes. 
    Because the results of past queries are stored, querying still only takes a few minutes.
    Generates file 5:
5. new_pizza_triples.ttl - file of triples generated by csv2rdf.py
6. Reasoning.py - a script to perform programmatic OWL2RL reasoning using new_pizza_triples.ttl and ollie_keers.owl
    This file outputs both a ttl file and an rdf file.
7. pizza_inference.ttl - output from Reasoning.py, cannot be opened in Protege.
8. pizza_inference.rdf - output from Reasoning.py, can be opened in Protege
9. SPARQL.py - sparql query file. 
10. query1.csv - output of first sparql query.
11. Alignment.py - script to provide equivalence triples for pizza.owl and ollie_keers.owl .
    N.B. This file requires pizza.owl to run, which is available at http://owl.cs.manchester.ac.uk/publications/talks-and-tutorials/protg-owl-tutorial/ .
    Outputs equivalences.ttl
12. equivalences.ttl - output from Alignment.py. 
    To be opened in Protege with pizza.owl & ollie_keers.owl for alignment, HermiT reasoner to be used.
    To be opened in Protege with new_pizza_triples.rdf, pizza.owl & ollie_keers.owl for alignment with data, HermiT reasoner to be used. 
    Reasoning with data is not recommended as it will take several hours to complete, and the ontology is inconsistent as outlined in report.
13. AlignmentDataReasoning.py - file to perform programmatic OWL2RL reasoning with ollie_keers.owl, equivalences.ttl, pizza.owl and new_pizza_triples.ttl
    Runs 3 SPARQL queries to check for membership of 3 classes.
    Outputs reasoned_data_alignments.rdf (for protege) and reasoned_data_alignments.ttl
14. default.cfg - default configuration file for use with OWL2Vec*. Results in output_embedding folder
15. elk.cfg - elk configuration file for use with OWL2Vec*. Results in output_embedding_elk folder
16. hermit.cfg - hermit configuration file for use with OWL2Vec*. Results in output_embedding_elk folder
17. output_embedding: folder, containing results from OWL2Vec* with default configuration.
    17a. output_embedding_hermit/load_embeddings.py - script for comparing similarity of terms for these embeddings.
    17b. VecClust.py - script for plotting and inspecting clusters of terms.

18. output_embedding_elk: folder, containing results from OWL2Vec* with elk configuration.
    18a. output_embedding_hermit/load_embeddings.py - script for comparing similarity of terms for these embeddings.
    18b. VecClust.py - script for plotting and inspecting clusters of terms.

19. output_embedding_hermit: folder, containing results from OWL2Vec* with hermit configuration. 
    19a. output_embedding_hermit/load_embeddings.py - script for comparing similarity of terms for these embeddings.
    19b. VecClust.py - script for plotting and inspecting clusters of terms.

20 - entity.py, lookup.py, and stringcmp.py - support scripts by Ernesto Jimenez Ruiz
