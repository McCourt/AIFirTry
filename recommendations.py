# A dictionary of movie critics and their ratings of a small
# set of movies
from math import sqrt
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

if __name__ == "__main__":
    print(sim_distance(critics, 'Lisa Rose', 'Gene Seymour'))
    print(sim_pearson(critics, 'Lisa Rose', 'Gene Seymour'))
    print(topMatches(critics, 'Toby', n=3))
    print(getRecommendations(critics, 'Toby'))
    print(getRecommendations(critics, "Toby", similarity=sim_distance))
    movies = transformPrefs(critics)
    print(movies)