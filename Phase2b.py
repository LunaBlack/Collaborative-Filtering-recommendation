#!/usr/bin/python
# -*- coding: utf-8 -*-


# This file contains a program that evaluates each prediction algorithm
# by using an 80-20 split of the ratings into training and testing sets.

# To make sure that the reported rmse values are reliable, the process will be
# performed 10 repetitions. The average rmse value of each prediction algorithm
# (averaged over the 10 repetitions) will be written into a file "output.txt".

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
    
    value_rmse = list()
    for i in xrange(14):
        value_rmse.append(list())

    for time in xrange(10): # repeat ten times
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

        for i in xrange(14):
            value = rmse(actualRatings, predictedRatings[i])
            value_rmse[i].append(value)

    # compute the average rmse value of each prediction algorithm
    # (averaged over the 10 repetitions)
    average_rmse = list()
    for i in xrange(14):
        summation = 0.0
        for j in value_rmse[i]:
            summation += j
        average = summation/10
        average_rmse.append(average)

    with open('output.txt', 'w') as f:
        f.write("Random prediction Average RMSE: " + str(average_rmse[0]) + "\n")
        f.write("User Mean Rating prediction Average RMSE: " + str(average_rmse[1]) + "\n")
        f.write("Movie Mean Rating prediction Average RMSE: " + str(average_rmse[2]) + "\n")
        f.write("User-Movie Mean Rating prediction Average RMSE: " + str(average_rmse[3]) + "\n")
        f.write("Collaborative Filtering Rating prediction Average RMSE (friends = 0): " + str(average_rmse[4]) + "\n")
        f.write("CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = 0): " + str(average_rmse[5]) + "\n")
        f.write("Collaborative Filtering Rating prediction Average RMSE (friends = 25): " + str(average_rmse[6]) + "\n")
        f.write("CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = 25): " + str(average_rmse[7]) + "\n")
        f.write("Collaborative Filtering Rating prediction Average RMSE (friends = 300): " + str(average_rmse[8]) + "\n")
        f.write("CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = 300): " + str(average_rmse[9]) + "\n")
        f.write("Collaborative Filtering Rating prediction Average RMSE (friends = 500): " + str(average_rmse[10]) + "\n")
        f.write("CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = 500): " + str(average_rmse[11]) + "\n")
        f.write("Collaborative Filtering Rating prediction Average RMSE (friends = numUsers): " + str(average_rmse[12]) + "\n")
        f.write("CollaborativeFiltering-Movie Mean Rating prediction Average RMSE (friends = numUsers): " + str(average_rmse[13]) + "\n")
