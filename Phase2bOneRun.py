#!/usr/bin/python
# -*- coding: utf-8 -*-


# This file contains a program that evaluates each prediction algorithm
# by using an 80-20 split of the ratings into training and testing sets.

# The performance of the collaborative filtering algorithm may depend on the number of
# "friends" used. So run the algorithms CFRatingPrediction and CFMMRatingPrediction
# with 0 friends, 25 friends, 300 friends, 500 friends, and the friends consisting of
# the entire population of users.
# So this file evaluates 14 algorithms in total.


from project2Phase2a import *


if __name__ == '__main__':    
    numUsers = 943
    numItems = 1682
    numRatings = 100000
    testPercent = 0.2
    
    ratingList = readRatings()
    [trainingSet, testSet] = partitionRatings(ratingList, testPercent)
    [rLu, rLm] = createRatingsDataStructure(numUsers, numItems, trainingSet)

    actualRatings = list()
    predictedRatings = list()
    for i in xrange(14):
        predictedRatings.append(list())

    for i in testSet:
        u = i[0]
        m = i[1]
        actualRatings.append(i[2])
        
        predictedRatings[0].append(randomPrediction(u, m))
        predictedRatings[1].append(meanUserRatingPrediction(u, m, rLu))
        predictedRatings[2].append(meanMovieRatingPrediction(u, m, rLm))
        predictedRatings[3].append(meanRatingPrediction(u, m, rLu, rLm))

        friends = kNearestNeighbors(u, rLu, k = 0)
        predictedRatings[4].append(CFRatingPrediction(u, m, rLu, friends))
        predictedRatings[5].append(CFMMRatingPrediction(u, m, rLu, rLm, friends))

        friends = kNearestNeighbors(u, rLu, k = 25)
        predictedRatings[6].append(CFRatingPrediction(u, m, rLu, friends))
        predictedRatings[7].append(CFMMRatingPrediction(u, m, rLu, rLm, friends))

        friends = kNearestNeighbors(u, rLu, k = 300)
        predictedRatings[8].append(CFRatingPrediction(u, m, rLu, friends))
        predictedRatings[9].append(CFMMRatingPrediction(u, m, rLu, rLm, friends))

        friends = kNearestNeighbors(u, rLu, k = 500)
        predictedRatings[10].append(CFRatingPrediction(u, m, rLu, friends))
        predictedRatings[11].append(CFMMRatingPrediction(u, m, rLu, rLm, friends))

        friends = kNearestNeighbors(u, rLu, k = numUsers)
        predictedRatings[12].append(CFRatingPrediction(u, m, rLu, friends))
        predictedRatings[13].append(CFMMRatingPrediction(u, m, rLu, rLm, friends))

    value_rmse = list()
    for i in xrange(14):
        value = rmse(actualRatings, predictedRatings[i])
        value_rmse.append(value)

    print "Random prediction RMSE: ", value_rmse[0]
    print "User Mean Rating prediction RMSE: ", value_rmse[1]
    print "Movie Mean Rating prediction RMSE: ", value_rmse[2]
    print "User-Movie Mean Rating prediction RMSE: ", value_rmse[3]
    print "Collaborative Filtering Rating prediction RMSE (friends = 0): ", value_rmse[4]
    print "CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = 0): ", value_rmse[5]
    print "Collaborative Filtering Rating prediction RMSE (friends = 25): ", value_rmse[6]
    print "CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = 25): ", value_rmse[7]
    print "Collaborative Filtering Rating prediction RMSE (friends = 300): ", value_rmse[8]
    print "CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = 300): ", value_rmse[9]
    print "Collaborative Filtering Rating prediction RMSE (friends = 500): ", value_rmse[10]
    print "CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = 500): ", value_rmse[11]
    print "Collaborative Filtering Rating prediction RMSE (friends = numUsers): ", value_rmse[12]
    print "CollaborativeFiltering-Movie Mean Rating prediction RMSE (friends = numUsers): ", value_rmse[13]
