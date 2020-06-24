# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 15:41:06 2020

@author: rajkothari634
"""

import numpy as np
import matplotlib as plt
import pandas as pd

datasetPost = pd.read_csv('posts.csv')
datasetViews = pd.read_csv('views.csv')
datasetPost["category"].fillna("No category", inplace = True)

X = datasetPost.iloc[:,2:4]

from sklearn.preprocessing import LabelEncoder , OneHotEncoder
labelencoder_X = LabelEncoder()
X.iloc[:,0] = labelencoder_X.fit_transform(X.iloc[:,0])
X.iloc[:,1] = labelencoder_X.fit_transform(X.iloc[:,1])
onehotencoder = OneHotEncoder(categorical_features = [0])
X = onehotencoder.fit_transform(X).toarray()
from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity(X, X)
ans = 'y'
while ans == 'y' :
    print("give user_id")
    user_id = input()
    sample_sim = cosine_sim
    post_index = []
    similarity_value = []
    for view in datasetViews.values :
        if view[0] == user_id :
            index = datasetPost[datasetPost['_id'] == view[1]].index[0]
            if index not in post_index :
                post_index.append(index)
                sample_sim[index,index] = 0
                similarity_value.append(sample_sim[index,:])
    ans='n'
    arr2D = np.array(similarity_value)
    for index in post_index :
        arr2D[:,index] = 0
    recommended_post_index_byuser = []
    while len(recommended_post_index_byuser) != 10 :
        result = np.where(arr2D == np.amax(arr2D))
        listOfCordinates = list(zip(result[0], result[1]))
        columnindex = 0
        for cord in listOfCordinates:
            columnindex = cord
        recommended_post_index_byuser.append(columnindex[1])
        arr2D[:,columnindex[1]] = 0
    for index in recommended_post_index_byuser :
        print((np.array(datasetPost))[index,0])
ans = 'y'
while ans == 'y' :
    print("give post_id")
    post_id = input()
    post_index_bypost = datasetPost.index[datasetPost['_id'] == post_id][0]
    sim_arr = cosine_sim[post_index_bypost,:]
    simarr = np.array(sim_arr)
    simarr[post_index_bypost] = 0
    recommended_post_index_bypost = []
    while len(recommended_post_index_bypost)!=10:
        result = np.where(simarr == np.amax(simarr))
        for i in result[0] :
            if len(recommended_post_index_bypost)==10 :
                break
            recommended_post_index_bypost.append(i)
            simarr[i] = 0
    for index in recommended_post_index_bypost :
        print((np.array(datasetPost))[index,0])
    ans = 'n'
    
    
    
    