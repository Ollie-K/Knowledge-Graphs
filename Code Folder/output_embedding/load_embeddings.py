# Load back with memory-mapping = read-only, shared across processes.
from gensim.models import KeyedVectors


wv = KeyedVectors.load("default.embeddings", mmap='r') #loading embeddings


similarity = wv.similarity('hawaiian', 'pineapple') #calculating cosine similarity for these two terms
print('similarity of hawaiian & pineapple') #printing the two terms
print(similarity) #printing the similarity score


similarity = wv.similarity('hawaiian', 'egg') #calculating cosine similarity for these two terms
print('similarity of hawaiian & egg')#printing the two terms
print(similarity)#printing the similarity score

similarity = wv.similarity('meat', 'city') #calculating cosine similarity for these two terms
print('similarity of meat & city')#printing the two terms
print(similarity)#printing the similarity score


similarity = wv.similarity('detroit', 'michigan') #calculating cosine similarity for these two terms
print('similarity of detroit & michigan')#printing the two terms
print(similarity)#printing the similarity score

similarity = wv.similarity('currency', 'country') #calculating cosine similarity for these two terms
print('similarity of currency & country')#printing the two terms
print(similarity)#printing the similarity score

