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


# The function computes the similarity in ratings between the two users, using the
# movies that the two users have commonly rated. The similarity between two users
# will always be between -1 and +1.
def similarity(u, v, userRatings):
    sim = 0.0
    sum_1 = sum_2 =sum_3 = 0.0

    # Find the movies that the two users have commonly rated.
    common_movie = list()
    for i in userRatings[u-1]:
        if i in userRatings[v-1]:
           common_movie.append(i)

    if len(common_movie) == 0:
        return sim

    # Compute the mean ratings that user u or user v has given to movies.
    mean_rating_1 = meanUserRating(u, userRatings)
    mean_rating_2 = meanUserRating(v, userRatings)   

    # Compute the similarity in ratings between the two users.
    for i in common_movie:
        sum_1 += (userRatings[u-1][i] - mean_rating_1) * (userRatings[v-1][i] - mean_rating_2)
        sum_2 += (userRatings[u-1][i] - mean_rating_1) ** 2
        sum_3 += (userRatings[v-1][i] - mean_rating_2) ** 2
    if sum_1 == 0 or sum_2 == 0 or sum_3 == 0:
        return sim
    else:
        sim = sum_1 / ( math.sqrt(sum_2) * math.sqrt(sum_3) )
        return sim


# The function returns the list of (user ID, similarity)-pairs for the k users
# who are most similar to user u. The user u herself will be excluded from
# candidates being considered by this function.
def kNearestNeighbors(u, userRatings, k):
    sim_user_list = list() # a list of (similarity, user ID)-pairs
    user_sim_list = list() # a list of (user ID, similarity)-pairs
    
    for i in xrange(len(userRatings)):
        sim = 0
        if i != u-1:
            sim = similarity(u, i+1, userRatings)
            sim_user_list.append((sim, i+1))

    sim_user_list.sort()
    sim_user_list.reverse()

    for i in sim_user_list[:k]:
        user_sim_list.append((i[1], i[0]))

    return user_sim_list
        

# The function predicts a rating by user u for movie m.
# It uses the ratings of the list of friends to come up with a rating by u of m according to formula.
# The argument corresponding to friends is computed by a call to the kNearestNeighbors function.
def CFRatingPrediction(u, m, userRatings, friends):
    
    # Construct a dictionary, whose keys are userID and
    # whose values are (similarity, mean_rating)-pairs.
    user_dict = dict()
    
    for i in friends:
        user_dict.setdefault(i[0], list())
        user_dict[i[0]].append(i[1])
        mean_rating = meanUserRating(i[0], userRatings)
        user_dict[i[0]].append(mean_rating)

    rating = meanUserRating(u, userRatings)
    sum_1 = sum_2 = 0.0

    for i in friends:
        if m in userRatings[i[0]-1]:
            sum_1 += (userRatings[i[0]-1][m] - user_dict[i[0]][1]) * user_dict[i[0]][0]
            sum_2 += abs(user_dict[i[0]][0])

    if sum_2 == 0:
        return rating
    else:
        rating += sum_1 / sum_2
        return rating


# The function computes a number using the formula (which is same to the function CFRatingPrediction),
# and then returns the average of this and mean rating of movie m.
def CFMMRatingPrediction(u, m, userRatings, movieRatings, friends):
    rating = CFRatingPrediction(u, m, userRatings, friends)
    mean_rating_m = meanMovieRating(m, movieRatings)
    average_rating = (rating + mean_rating_m) / 2
    return average_rating
