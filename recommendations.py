# A dictionary of movie critics and their ratings of a small
# set of movies
from math import sqrt
import csv
critics ={'Lisa Rose': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'Superman Returns': 3.5, 'You, Me and Dupree': 2.5, 'The Night Listener': 3.0},
          'Gene Seymour': {'Lady in the Water': 3.0, 'Snakes on a Plane': 3.5, 'Just My Luck': 1.5, 'Superman Returns': 5.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 3.5},
          'Michael Phillips': {'Lady in the Water': 2.5, 'Snakes on a Plane': 3.0, 'Superman Returns': 3.5, 'The Night Listener': 4.0},
          'Claudia Puig': {'Snakes on a Plane': 3.5, 'Just My Luck': 3.0, 'The Night Listener': 4.5, 'Superman Returns': 4.0, 'You, Me and Dupree': 2.5},
          'Mick LaSalle': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'Just My Luck': 2.0, 'Superman Returns': 3.0, 'The Night Listener': 3.0, 'You, Me and Dupree': 2.0},
          'Jack Matthews': {'Lady in the Water': 3.0, 'Snakes on a Plane': 4.0, 'The Night Listener': 3.0, 'Superman Returns': 5.0, 'You, Me and Dupree': 3.5},
          'Toby': {'Snakes on a Plane': 4.5,'You, Me and Dupree': 1.0,'Superman Returns': 4.0}}

# method of Euclidean distance score: measurement of distance

def sim_distance(pref, person1, person2):
    si = list()

    for i in pref[person1]:
        if i in pref[person2]:
            si.append(i)

    if len(si) == 0: return 0

    sum_of_squares = sum([pow(pref[person1][i]-pref[person2][i],2) for i in si])

    return 1 / (1+sum_of_squares)

# Pearson correlation coefficient: measurement of linear fitting
def sim_pearson(pref, person1, person2):
    si = list()

    for i in pref[person1]:
        if i in pref[person2]:
            si.append(i)

    if len(si) == 0: return 0

    sum1 = sum([pref[person1][i] for i in si])
    sum2 = sum([pref[person2][i] for i in si])

    sum1sq = sum([pow(pref[person1][i], 2) for i in si])
    sum2sq = sum([pow(pref[person2][i], 2) for i in si])

    psum = sum([pref[person1][i] * pref[person2][i] for i in si])
    n = len(si)

    num = psum - (sum1 * sum2 / n)
    den = sqrt((sum1sq - pow(sum1, 2) / n) * (sum2sq - pow(sum2, 2) / n))
    if den == 0: return 0
    r = num / den

    return r

# Taminoto correlation coefficient: measurement of binary situation
def sim_taminoto(prefs, person1, person2):
    union = list(set(prefs[person1] | prefs[person2]))
    intersection = list(set(prefs[person1] & prefs[person2]))
    return 1.0 * len(intersection) / len(union)

# Returns the best matches for person from the prefs dictionary.
# Number of results and similarity function are optional params.

def topMatches(pref, person, n = 5, similarity = sim_pearson):
    score = [(similarity(pref, person, other), other) for other in pref if other != person]

    score.sort()
    score.reverse()
    return score[0:n]

# Gets recommendations for a person by using a weighted average
#  of every other user's rankings
def getRecommendations(prefs, person, similarity = sim_pearson):
    totals = {}
    simSums = {}
    for other in prefs:
        if other == person: continue

        sim = similarity(prefs, person, other)
        if sim <= 0: continue

        for item in prefs[other]:
            # only score movies I haven't seen yet
            if item not in prefs[person] or prefs[person][item] == 0:
                # Similarity * Score
                totals.setdefault(item, 0)
                totals[item] += prefs[other][item] * sim
                # Sum of similarities
                simSums.setdefault(item, 0)
                simSums[item] += sim

    # Create the normalized list
    rankings =[(total / simSums[item], item) for item, total in totals.items()]

    # Return the sorted list
    rankings.sort()
    rankings.reverse()
    return rankings

# transformation of the critics to another form

def transformPrefs(prefs):
    result ={}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item,{})
            # Flip item and person
            result[item][person] = prefs[person][item]
    return result

def calculateSimilarItems(prefs, n = 10):
    # Create a dictionary of items showing which other items they are most similar to.
    result ={}

    # Invert the preference matrix to be item-centric
    itemPrefs = transformPrefs(prefs)

    c = 0

    for item in itemPrefs:
        # Status updates for large datasets
        c += 1
        if c%100 == 0: print("%d / %d" % (c, len(itemPrefs)))
        # Find the most similar items to this one
        scores = topMatches(itemPrefs, item, n = n, similarity = sim_distance)
        result[item] = scores
    return result

def getRecommentedItems(prefs, itemMatch, user):
    userRating = prefs[user]
    score = {}
    totalSim = {}

    # Loop over items rated by this user
    for (item,rating) in userRating.items():

        # Loop over items similar to this one
        for (similarity,item2) in itemMatch[item]:

            # Ignore if this user has already rated this item
            if item2 in userRating: continue

            # Weighted sum of rating times similarity
            score.setdefault(item2, 0)
            score[item2] += similarity * rating

            # Sum of all the similarities
            totalSim.setdefault(item2, 0)
            totalSim[item2] += similarity

    # Divide each total score by total weighting to get an average
    ranking = [(rating / totalSim[item], item) for item,rating in score.items()]

    # Return the rankings from highest to lowest
    ranking.sort(reverse=True)
    return ranking

def calculateSimilarUsers(userPrefs, n = 10):
    # Create a dictionary of items showing which other items they are most similar to.
    result ={}

    c = 0

    for item in userPrefs:
        # Status updates for large datasets
        c += 1
        if c%100 == 0: print("%d / %d" % (c, len(userPrefs)))
        # Find the most similar items to this one
        scores = topMatches(userPrefs, item, similarity = sim_distance)
        result[item] = scores
    return result

def getRecommentedUsers(prefs, userMatch, user):
    userSim = userMatch[user]
    scores = {}
    totalSim = {}

    for similarity,aUser in userSim:
        for movieName, rating in prefs[aUser].items():
            if movieName in userSim: continue
            totalSim.setdefault(movieName, 0)
            totalSim[movieName] += similarity * rating
            scores.setdefault(movieName, 0)
            scores[movieName] += similarity

    ranking = [(similarity / scores[movieName],movieName) for movieName, similarity in totalSim.items()]
    ranking.sort(reverse=True)

    return ranking

def loadMoviesData(fileName1, fileName2):
    # loading of the data csv files
    ratings = open(fileName1)
    nameOfMivies = open(fileName2)
    ID = csv.reader(nameOfMivies)
    movies = csv.reader(ratings)

    # create new dictionary
    rators = {}
    names = {}

    # assign ID to names
    for line in ID:
        id,name = line[0:2]
        names[id] = name

    # create to data set for item recommendation
    for line in movies:
        userId, movieId, rating, timestamp = line
        rators.setdefault(userId,{})
        rators[userId][names[movieId]] = float(rating)

    return rators

if __name__ == "__main__":
    similarity1 = sim_distance(critics, 'Lisa Rose', 'Gene Seymour')
    similarity2 = sim_pearson(critics, 'Lisa Rose', 'Gene Seymour')
    matchToby = topMatches(critics, 'Toby', n=3)
    recommendation1 = getRecommendations(critics, 'Toby')
    recommendation2 = getRecommendations(critics, "Toby", similarity=sim_distance)
    movies = transformPrefs(critics)
    matchSR = topMatches(movies, "Superman Returns")
    recommendation3 = getRecommendations(movies, "Just My Luck")
    itemSim = calculateSimilarItems(critics)
    similarityItemToby = getRecommentedItems(critics, itemSim, "Toby")
    newData = loadMoviesData("ratings.csv", "movies.csv")
    itemSim2 = calculateSimilarItems(newData)
    recommendation4 = getRecommentedItems(newData, itemSim2, "87")[0:5]
    userSim = calculateSimilarUsers(newData)
    recommendation5 = getRecommentedUsers(newData, userSim, "87")[0:5]