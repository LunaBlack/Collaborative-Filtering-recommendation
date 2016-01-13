#!/usr/bin/python
# -*- coding: utf-8 -*-


import random
import math
import sys


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

    #for i in xrange(numUsers):
    #    rLu.append(dict())
    rLu = [{} for i in xrange(numUsers)]

    #for i in xrange(numItems):
    #    rLm.append(dict())
    rLm = [{} for i in xrange(numItems)]

    for r in ratingTuples:
        rLu[int(r[0]-1)][int(r[1])] = int(r[2])
        rLm[int(r[1]-1)][int(r[0])] = int(r[2])

    for user in rLu:
        try:
            m = sum(user.values())/float(len(user))
            user['mean'] = m
            max_common_movie = 0
            for v in rLu:
                t = len(set(user.keys()) & set(v.keys()))
                if  t > max_common_movie:
                    if v is not user:
                        max_common_movie = t
            user['max_common'] = max_common_movie
        except ZeroDivisionError:
            user['mean'] = 0.
            user['max_common'] = 0
    for movie in rLm:
        try:
            m = sum(movie.values())/float(len(movie))
            movie['mean'] = m
            max_common_user = 0
            for n in rLm:
                t = len(set(movie.keys()) & set(n.keys()))
                if t > max_common_user:
                    if n is not movie:
                        max_common_user = t
            movie['max_common'] = max_common_user
        except ZeroDivisionError:
            movie['mean'] = 0.
            movie['max_common'] = 0

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
        mean_rating = rLu[u-1]['mean']
    else:
        mean_rating = 0.0

    return mean_rating


# Return the mean rating for a movie with given ID m.
def meanMovieRating(m, rLm):
    if len(rLm[m-1])!= 0:
        mean_rating = rLm[m-1]['mean']
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
    common_movie = list(set(userRatings[u-1].keys()) & set(userRatings[v-1].keys()))

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

    if k == -1:
        return sim_user_list

    for i in sim_user_list[:k]:
        user_sim_list.append((i[1], i[0]))

    return user_sim_list


# calculate the KNN using pre-calculated similarity
def kNearestNeighbors2(u, userRatings, k, similarity_m):
    sim_user_list = list() # a list of (similarity, user ID)-pairs
    user_sim_list = list() # a list of (user ID, similarity)-pairs

    for i in xrange(len(userRatings)):
        sim = 0
        if i != u-1:
            sim = similarity_m[u][i+1]
            sim_user_list.append((sim, i+1))

    sim_user_list.sort()
    sim_user_list.reverse()

    if k == -1:
        return sim_user_list

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
    sum_1 = 0.0
    sum_2 = 0.0

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

# return both the return value of CFMMRatingPrediction and CFMMRatingPrediction
def CFMMRatingPrediction2(u, m, userRatings, movieRatings, friends):
    rating = CFRatingPrediction(u, m, userRatings, friends)
    mean_rating_m = meanMovieRating(m, movieRatings)
    average_rating = (rating + mean_rating_m) / 2
    return rating, average_rating

# The function computes the max number of movies that user u and another user have commonly rated.
# First, compute the number of movies that user u and each user in all-users have commonly rated.
# Second, find the max of all the numbers.
def maxCommonMovie(u, userRatings):
    common_movie_list = list()

    #length = len(userRatings)
    for i, v in enumerate(userRatings):
        if i != u-1:
            #common_movie = 0
            #for movie in userRatings[u-1]:
            #    if movie in userRatings[i]:
            #        common_movie += 1
            common_movie = len(set(userRatings[u-1]) & set(v))
            common_movie_list.append(common_movie)

    #common_movie_list.sort()
    #max_common_movie = common_movie_list[-1]
    return max(common_movie_list)


# The function computes the new similarity in ratings between the two users, using the
# movies that the two users have commonly rated.
# The new similarity between two users will always be between 0.36788 and 1.
def userSimilarity(u, v, userRatings):
    #common_movie = 0.0
    max_common = maxCommonMovie(u, userRatings)

    # Find the movies that the two users have commonly rated.
    #for i in userRatings[u-1]:
    #    if i in userRatings[v-1]:
    #       common_movie += 1
    common_movie = float(len(set(userRatings[u-1]) & set(userRatings[v-1])))

    sim = similarity(u, v, userRatings)
    user_sim = math.exp(common_movie/max_common - 1) * sim
    return user_sim

# calculate the userSimilarity using pre-calculated similarity and maxCommonUser
def userSimilarity2(u, v, userRatings, similarity_m):
    max_common = userRatings[u-1]['max_common']

    common_movie = float(len(set(userRatings[u-1].keys()) & set(userRatings[v-1].keys())))

    sim = similarity_m[u][v]
    user_sim = sim > 0 and math.exp(common_movie/max_common - 1) * sim or 0
    return user_sim


# The function returns the list of (user ID, similarity)-pairs for the k users
# who are most similar to user u. The user u herself will be excluded from
# candidates being considered by this function.
# The new similarity between users is computed by a call to the userSimilarity function.
def userKNearestNeighbors(u, userRatings, k):
    sim_user_list = list() # a list of (similarity, user ID)-pairs
    user_sim_list = list() # a list of (user ID, similarity)-pairs

    for i in xrange(len(userRatings)):
        sim = 0
        if i != u-1:
            sim = userSimilarity(u, i+1, userRatings)
            sim_user_list.append((sim, i+1))

    sim_user_list.sort()
    sim_user_list.reverse()

    for i in sim_user_list[:k]:
        user_sim_list.append((i[1], i[0]))

    return user_sim_list

# calculate the userKNN using pre-calculated similarity
def userKNearestNeighbors2(u, userRatings, similarity_m):
    sim_user_list = list() # a list of (similarity, user ID)-pairs
    user_sim_list = list() # a list of (user ID, similarity)-pairs

    for i in xrange(len(userRatings)):
        sim = 0
        if i != u-1:
            sim = userSimilarity2(u, i+1, userRatings, similarity_m)
            sim_user_list.append((sim, i+1))

    sim_user_list.sort()
    sim_user_list.reverse()

    return sim_user_list

# The function predicts a rating by user u for movie m.
# It uses the ratings of the list of friends to come up with a rating by u of m according to formula.
# The argument corresponding to friends is computed by a call to the userKNearestNeighbors function.
def userCFRatingPrediction(u, m, userRatings, friends):
    rating = CFRatingPrediction(u, m, userRatings, friends)
    return rating


# This function computes the maximum value of the numbers of users who have both
# rated movie i and another movie which is in movie set.
# First, compute the number of users that movie m and each movie in all-movies have been commonly rated by.
# Second, find the max of all the numbers.
def maxCommonUser(m, movieRatings):
    common_user_list = list()

    for i, n in enumerate(movieRatings):
        if i != m-1:
            common_user = len(set(movieRatings[m-1]) & set(n))
            common_user_list.append(common_user)

    #common_user_list.sort()
    #max_common_user = common_user_list[-1]
    return max(common_user_list)


# The function computes the similarity in ratings between the two movies, using the
# users who have commonly rated the two movies. The similarity between two movies
# will always be between -1 and +1.
def similarity_2(m, n, movieRatings):
    sim = 0.0
    sum_1 = sum_2 =sum_3 = 0.0

    # Find the users that have commonly rated the same two movies.
    common_user = list(set(movieRatings[m-1].keys()) & set(movieRatings[n-1].keys()))

    if len(common_user) == 0:
        return sim

    # Compute the mean ratings that movie m or movie n has been given to.
    mean_rating_1 = meanMovieRating(m, movieRatings)
    mean_rating_2 = meanMovieRating(n, movieRatings)

    # Compute the similarity in ratings between the two movies.
    for i in common_user:
        sum_1 += (movieRatings[m-1][i] - mean_rating_1) * (movieRatings[n-1][i] - mean_rating_2)
        sum_2 += (movieRatings[m-1][i] - mean_rating_1) ** 2
        sum_3 += (movieRatings[n-1][i] - mean_rating_2) ** 2
    if sum_1 == 0 or sum_2 == 0 or sum_3 == 0:
        return sim
    else:
        sim = sum_1 / ( math.sqrt(sum_2) * math.sqrt(sum_3) )
        return sim


# The function computes the new similarity in ratings between the two movies, using the
# users who have commonly rated the two movies.
# The new similarity between two movies will always be between 0.36788 and 1.
def movieSimilarity(m, n, movieRatings):
    #common_user = 0.0
    max_common = maxCommonUser(m, movieRatings)

    # Find the users that have commonly rated the same two movies.
    #for i in movieRatings[m-1]:
    #    if i in movieRatings[n-1]:
    #       common_user += 1
    common_user = float(len(set(movieRatings[m-1]) & set(movieRatings[n-1])))

    sim = similarity_2(m, n, movieRatings)
    movie_sim = math.exp(common_user/max_common - 1) * sim
    return movie_sim

# calculate the movieSimilarity using pre-calculated similarity and maxCommonMovie
def movieSimilarity2(m, n, movieRatings, similarity_m_2):
    max_common = movieRatings[m-1]['max_common']

    common_user = float(len(set(movieRatings[m-1]) & set(movieRatings[n-1])))

    sim = similarity_m_2[m][n]
    movie_sim = sim > 0 and math.exp(common_user/max_common - 1) * sim or 0
    return movie_sim

# The function returns the list of (movie ID, similarity)-pairs for the k movies
# which are most similar to movie m. The movie m itself will be excluded from
# candidates being considered by this function.
# The new similarity between movies is computed by a call to the movieSimilarity function.
def movieKNearestNeighbors(m, movieRatings, k):
    sim_movie_list = list() # a list of (similarity, movie ID)-pairs
    movie_sim_list = list() # a list of (movie ID, similarity)-pairs

    for i in xrange(len(movieRatings)):
        sim = 0
        if i != m-1:
            sim = movieSimilarity(m, i+1, movieRatings)
            sim_movie_list.append((sim, i+1))

    sim_movie_list.sort()
    sim_movie_list.reverse()

    for i in sim_movie_list[:k]:
        movie_sim_list.append((i[1], i[0]))

    return movie_sim_list

# calculate the movieKNN using pre-calculated similarity
def movieKNearestNeighbors2(m, movieRatings, similarity_m):
    sim_movie_list = list() # a list of (similarity, movie ID)-pairs
    movie_sim_list = list() # a list of (movie ID, similarity)-pairs

    for i in xrange(len(movieRatings)):
        sim = 0
        if i != m-1:
            sim = movieSimilarity2(m, i+1, movieRatings, similarity_m)
            sim_movie_list.append((sim, i+1))

    sim_movie_list.sort()
    sim_movie_list.reverse()

    return sim_movie_list


# The function predicts a rating by user u for movie m.
# It uses the ratings of the list of friends to come up with a rating of m by u according to formula.
# The argument corresponding to friends is computed by a call to the movieKNearestNeighbors function.
def movieCFRatingPrediction(u, m, movieRatings, friends):

    # Construct a dictionary, whose keys are movieID and
    # whose values are (similarity, mean_rating)-pairs.
    movie_dict = dict()

    for i in friends:
        movie_dict.setdefault(i[0], list())
        movie_dict[i[0]].append(i[1])
        mean_rating = meanMovieRating(i[0], movieRatings)
        movie_dict[i[0]].append(mean_rating)

    rating = meanMovieRating(m, movieRatings)
    sum_1 = sum_2 = 0.0

    for i in friends:
        if u in movieRatings[i[0]-1]:
            sum_1 += (movieRatings[i[0]-1][u] - movie_dict[i[0]][1]) * movie_dict[i[0]][0]
            sum_2 += abs(movie_dict[i[0]][0])

    if sum_2 == 0:
        return rating
    else:
        rating += sum_1 / sum_2
        return rating


# This function returns the average of predicted ratings computed by userCFRatingPrediction function
# and movieCFRatingPrediction function.
def averageCFRatingPrediction(u, m, userRatings, movieRatings, friends_user, friends_movie):
    rating_user = userCFRatingPrediction(u, m, userRatings, friends_user)
    rating_movie = movieCFRatingPrediction(u, m, movieRatings, friends_movie)
    average_rating = (rating_user + rating_movie) / 2
    return average_rating


# The function evaluates each prediction algorithm by using an 80-20 split
# of the ratings into training and testing sets.
# To make sure that the reported rmse values are reliable, the process will be
# performed 10 repetitions. The average rmse value of each prediction algorithm
# (averaged over the 10 repetitions) will be written into a file "output_ec.txt".
def averageTenRuns():
    numUsers = 943
    numItems = 1682
    numRatings = 100000
    testPercent = 0.2

    ratingList = readRatings()

    times = 10
    value_rmse = [[0.] * times for i in range(19)]

    for time in xrange(times): # repeat ten times
        [trainingSet, testSet] = partitionRatings(ratingList, testPercent)
        [rLu, rLm] = createRatingsDataStructure(numUsers, numItems, trainingSet)

        actualRatings = list()
        predictedRatings = list()
        for i in xrange(5):
            predictedRatings.append(list())

        users = sorted(set([e[0] for e in testSet]))
        similarity_m = [[0.]*(numUsers+1) for i in range(numUsers+1)]
        movies = sorted(set([e[1] for e in testSet]))
        similarity_m_2 = [[0.]*(numItems+1) for i in range(numItems+1)]

        for n, u in enumerate(users):
            for v in users[n+1:]:
                s = similarity(u, v, rLu)
                similarity_m[u][v] = s
                similarity_m[v][u] = s

        for i, m in enumerate(movies):
            for n in movies[i+1:]:
                s = similarity_2(m, n, rLm)
                similarity_m_2[m][n] = s
                similarity_m_2[n][m] = s
                #sys.stdout.write("\r{}_{}".format(m, n))
                #sys.stdout.flush()

        for n, i in enumerate(testSet):
            u, m, r = i
            actualRatings.append(r)

            k_values = [(0, 0), (25, 25), (300, 300), (500, 500), (numUsers, numItems)]
            friends_user = userKNearestNeighbors2(u, rLu, similarity_m)
            friends_movie = movieKNearestNeighbors2(m, rLm, similarity_m_2)

            for nk, k in enumerate(k_values):

                friends_user_k = [(e[1], e[0]) for e in friends_user[:k[0]]]
                friends_movie_k = [(e[1], e[0]) for e in friends_movie[:k[1]]]

                predictedRatings[nk].append(averageCFRatingPrediction(u, m, rLu, rLm, friends_user_k, friends_movie_k))
            #sys.stdout.write("\r{}_{}".format(time, n))
            #sys.stdout.flush()

        for i in xrange(5):
            value_rmse[i][time] = rmse(actualRatings, predictedRatings[i])

    # compute the average rmse value of each prediction algorithm
    # (averaged over the 10 repetitions)
    average_rmse = [sum(v)/times for v in value_rmse]

    with open('output_ec.txt', 'w') as f:
        f.write("New Collaborative Filtering Rating prediction Average RMSE (friends = 0): " + str(average_rmse[0]) + "\n")
        f.write("New Collaborative Filtering Rating prediction Average RMSE (friends = 25): " + str(average_rmse[1]) + "\n")
        f.write("New Collaborative Filtering Rating prediction Average RMSE (friends = 300): " + str(average_rmse[2]) + "\n")
        f.write("New Collaborative Filtering Rating prediction Average RMSE (friends = 500): " + str(average_rmse[3]) + "\n")
        f.write("New Collaborative Filtering Rating prediction Average RMSE (friends = all): " + str(average_rmse[4]) + "\n")



# Main program
if __name__ == '__main__':
    averageTenRuns()
