#!/usr/bin/python
# -*- coding: utf-8 -*-


import random
import math


# Read from the file u.user and return a list containing all of the
# demographic information pertaining to the users.
# The userList contains as many elements as there are users and information
# pertaining to the user with ID i should appear in slot i-1 in userList.
# The userList is a list with 943 dictionaries, each dictionary containing 4 keys.
def createUserList():
    userList = list()

    filename = 'u.user'
    with open(filename, 'r') as f:
        records = f.readlines()
        
    for i in xrange(len(records)):
        userList.append(dict())

    for r in records:
        record = (r.strip()).split('|')
        userList[int(record[0])-1]['age'] = int(record[1])
        userList[int(record[0])-1]['gender'] = record[2]
        userList[int(record[0])-1]['occupation'] = record[3]
        userList[int(record[0])-1]['zip'] = record[4]

    return userList


# Read from the file u.item and return a list containing all of the
# information pertaining to movies given in the file.
# Then movieList contains as many elements as there are movies and information
# pertaining to the movie with ID i should appear in slot i-1 in movieList.
def createMovieList():
    movieList = list()
    
    filename = 'u.item'
    with open(filename, 'r') as f:
        records = f.readlines()
        
    for i in xrange(len(records)):
        movieList.append(dict())

    for r in records:
        record = (r.strip()).split('|')
        movieList[int(record[0])-1]['title'] = record[1]
        movieList[int(record[0])-1]['release date'] = record[2]
        movieList[int(record[0])-1]['"video release date'] = record[3]
        movieList[int(record[0])-1]['IMDB url'] = record[4]
        movieList[int(record[0])-1]['genre'] = list()
        for n in range(5, 24):
            movieList[int(record[0])-1]['genre'].append(int(record[n]))

    return movieList
    

# Read ratings from the file u.data and return a list of 100,000 length-3
# tuples of the form (user, movie, rating).
def readRatings():
    ratingList = list()
    
    filename = 'u.data'
    with open(filename, 'r') as f:
        records = f.readlines()

    for r in records:
        record = (r.strip()).split('\t')
        ratingList.append((int(record[0]), int(record[1]), int(record[2])))

    return ratingList


# The function takes the rating tuple list constructed by readRatings and
# organizes the tuples in this list into two data structures: rLu and rLm.
# The list rLu is a list, with one element per user, of all the ratings provided by each user.
# The list rLm is a list, with one element per movie, of all the ratings received by each movie.
# The ratings provided by user with ID i should appear in slot i-1 in rLu, as a dictionary
# whose keys are IDs of movies that this user has rated and whose values are corresponding ratings.
# The list rLm is quite similar.
def createRatingsDataStructure(numUsers, numItems, ratingTuples):
    rLu = list()
    rLm = list()

    for i in xrange(numUsers):
        rLu.append(dict())

    for i in xrange(numItems):
        rLm.append(dict())

    for r in ratingTuples:
        rLu[int(r[0]-1)][int(r[1])] = int(r[2])
        rLm[int(r[1]-1)][int(r[0])] = int(r[2])

    return [rLu, rLm]


# Read from the file u.genre and returns the list of movie genres listed in the file.
# The genres appears in the order in which they are listed in the file.
def createGenreList():
    genreList = list()
    
    filename = 'u.genre'
    with open(filename, 'r') as f:
        records = f.readlines()

    for r in records:
        record = (r.strip()).split('|')
        if record[0]:
            genreList.append(record[0])

    return genreList


# Return the mean rating provided by user with given ID u.
def meanUserRating(u, rLu):
    if len(rLu[u-1])!= 0:
        sum_rating = 0.0
        for i in rLu[u-1]:
            sum_rating += rLu[u-1][i]
        mean_rating = sum_rating/len(rLu[u-1])
    else:
        mean_rating = 0.0

    return mean_rating


# Return the mean rating for a movie with given ID m.
def meanMovieRating(m, rLm):
    if len(rLm[m-1])!= 0:
        sum_rating = 0.0
        for i in rLm[m-1]:
            sum_rating += rLm[m-1][i]
        mean_rating = sum_rating/len(rLm[m-1])
    else:
        mean_rating = 0.0

    return mean_rating    


# Given a user u and a movie m, simply return a random integer rating in the range [1, 5].
def randomPrediction(u, m):
    rating = random.randint(1,5)
    return rating


# Given a user u and a movie m, simply return the mean rating that user u has given to movies.
# Here userRatings is a list with one element per user, each element being a dictionary
# containing all movie-rating pairs associated with that user.
def meanUserRatingPrediction(u, m, userRatings):
    rating = meanUserRating(u, userRatings)
    return rating


# Given a user u and a movie m, simply return the mean rating that movie m has received.
# Here movieRatings is a list with one element per movie, each element being a dictionary
# containing all user-rating pairs associated with that user.
def meanMovieRatingPrediction(u, m, movieRatings):
    rating = meanMovieRating(m, movieRatings)
    return rating


# Given a user u and a movie m, simply return the average of the mean rating
# that u gives and mean rating that m receives.
def meanRatingPrediction(u, m, userRatings, movieRatings):
    rating_1 = meanUserRating(u, userRatings)
    rating_2 = meanMovieRating(m, movieRatings)
    rating = (rating_1 + rating_2)/2
    return rating


# The function partitions ratings into a training set and a testing set.
# The testing set is obtained by randomly selecting the given percent of the raw ratings. 
# The remaining unselected ratings are returned as the training set.
def partitionRatings(rawRatings, testPercent):
    trainingSet = list(rawRatings)
    testSet = list()

    test_size = int(len(rawRatings) * testPercent)
    
    while len(testSet) < test_size:
        index = random.randrange(len(trainingSet))
        testSet.append(trainingSet.pop(index))

    return [trainingSet, testSet]


# The function computes the RMSE given lists of actual and predicted ratings.
# RMSE is computed by first taking the mean of the squares of differences between actual
# and predicted ratings and then taking the square root of this quantity.
def rmse(actualRatings, predictedRatings):
    summation = 0.0
    length = len(actualRatings)

    for i in xrange(length):
        summation += (actualRatings[i] - predictedRatings[i]) ** 2

    rmse_value = math.sqrt(summation/length)
    return rmse_value
