#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 25 09:50:12 2021

@author: ollie
"""
# Load back with memory-mapping = read-only, shared across processes.
from gensim.models import KeyedVectors
import matplotlib.pyplot as plt
import seaborn as sns; sns.set()  # for plot styling
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


wv = KeyedVectors.load("elk.embeddings", mmap='r') #loading vectors

vec_dict = {} #initialising an empty dictionary
for key in wv.wv.vocab:  # loop through vocabulary
   vec_dict[key] = wv[key] #fill add the corresponding vector to the dictionary of vocab keys

vec_df = pd.DataFrame(vec_dict) #transform dictionary into dataframe
vec_df = vec_df.transpose() #use vocab as index rather than columns
print(vec_df.head()) #preview of dataframe

for i in range(1,10): #looping through number of clusters

    kmeans = KMeans(n_clusters=i) #setting the number of clusters to i
    x = vec_df #setting x for kmeans
    kmeans.fit(x) #fitting to the vectors
    
    pca = PCA(n_components=2) #tranforming data into 2 components
    principalComponents = pca.fit_transform(x) #transforming the data
    principalDf = pd.DataFrame(data = principalComponents , columns = ['principal component 1', 'principal component 2']) #principal components dataframe
    
    principalDf['y_kmeans'] = kmeans.predict(x) #adding a column of labels    
    plt.scatter(x=principalDf['principal component 1'], y=principalDf['principal component 2'], 
                c=principalDf['y_kmeans'], cmap='turbo', s=0.1) #plotting transformed & clustered data
    plt.show() #showing the plot
    
    

kmeans = KMeans(n_clusters=5) #the best number of clusters
x = vec_df #setting x
kmeans.fit(x) #fitting to the data

pca = PCA(n_components=2) #2 components for pca
principalComponents = pca.fit_transform(x) #transforming into 2 components
principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2']) #creating dataframe

principalDf['y_kmeans'] = kmeans.predict(x) #labelling data

plt.scatter(x=principalDf['principal component 1'], y=principalDf['principal component 2'], 
            c=principalDf['y_kmeans'], cmap='turbo', s=0.1) #plotting labelled data
plt.show() #showing it

vec_df['label'] = kmeans.predict(x) #adding labels to original dataframe for inspection

for i in range(5): #for each of the 4 clusters
    sub = vec_df[vec_df['label'] == i] #select a subset of the data with that cluster label
    pca = PCA(n_components=2) #2 components for pca
    principalComponents = pca.fit_transform(sub.iloc[:,:-1]) #fit the pca
    principalDf = pd.DataFrame(data = principalComponents
             , columns = ['principal component 1', 'principal component 2']) #putting it into a dataframe

    plt.scatter(x=principalDf['principal component 1'], y=principalDf['principal component 2'], cmap='turbo', s=0.1) #plotting
    plt.show() #showing the plot
    print(sub.head(10)) #printing 10 items from the cluster to inspect membership
