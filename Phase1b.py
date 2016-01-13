#!/usr/bin/python
# -*- coding: utf-8 -*-


# This file contains a program that evaluates each of the 4 simple prediction algorithms
# by using an 80-20 split of the ratings into training and testing sets.


from project2Phase1a import *


if __name__ == '__main__':    
    numUsers = 943
    numItems = 1682
    numRatings = 100000
    testPercent = 0.2
    
    ratingList = readRatings()
    [trainingSet, testSet] = partitionRatings(ratingList, testPercent)
    [rLu, rLm] = createRatingsDataStructure(numUsers, numItems, trainingSet)

    actualRatings = list()
    predictedRatings_1 = list()
    predictedRatings_2 = list()
    predictedRatings_3 = list()
    predictedRatings_4 = list()

    for i in testSet:
        u = i[0]
        m = i[1]
        actualRatings.append(i[2])
        
        predictedRatings_1.append(randomPrediction(u, m))
        predictedRatings_2.append(meanUserRatingPrediction(u, m, rLu))
        predictedRatings_3.append(meanMovieRatingPrediction(u, m, rLm))
        predictedRatings_4.append(meanRatingPrediction(u, m, rLu, rLm))   

    rmse_1 = rmse(actualRatings, predictedRatings_1)
    rmse_2 = rmse(actualRatings, predictedRatings_2)
    rmse_3 = rmse(actualRatings, predictedRatings_3)
    rmse_4 = rmse(actualRatings, predictedRatings_4)

    print "Random prediction RMSE: ", rmse_1
    print "User Mean Rating prediction RMSE: ", rmse_2
    print "Movie Mean Rating prediction RMSE: ", rmse_3
    print "User-Movie Mean Rating prediction RMSE: ", rmse_4
    
