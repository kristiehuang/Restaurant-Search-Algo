def search(query, ranking=lambda r: -r.stars):
    results = [r for r in Restaurant.all if query in r.name]
    return sorted(results, key=ranking)
def reviewed_both(r, s):
    #return len([x for x in r.reviewers if x in s.reviewers]) #slow version
    return fast_overlap(r.reviewers, s.reviewers)

def fast_overlap(s, t):
    i, j, count = 0, 0, 0
    while i < len(s) and j < len(t):
        if s[i] == t[j]:
            count += 1
            i += 1
            j += 1
        elif s[i] < t[j]:
            i += 1
        else:
            j+=1
    return count


class Restaurant:
    all = []
    def __init__(self, name, stars, reviewers):
        self.name, self.stars = name, stars
        self.reviewers = reviewers
        Restaurant.all.append(self)

    def similar(self, k, similarity=reviewed_both):
        #return k most similar rests to SELF
        ...
        rests = list(Restaurant.all)
        rests.remove(self)
        return sorted(rests, key=lambda r: -similarity(self, r))[:k]

    def __repr__(self):
        return self.name

import json
reviewers_for_rest = {}
for line in open('reviews.json'):
    r = json.loads(line)
    biz = r['business_id']
    if biz not in reviewers_for_rest:
        reviewers_for_rest[biz] = [r['user_id']]
    else:
        reviewers_for_rest[biz].append(r['user_id'])

for line in open('restaurants.json'):
    r = json.loads(line)
    reviewers = reviewers_for_rest[r['business_id']]
    Restaurant(r['name'], r['stars'], sorted(reviewers))

while True:
    print('> ', end='')
    results = search(input().strip())
    for r in results:
        print(r, 'shares reviewers with', r.similar(3))