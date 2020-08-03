

import csv

real_results = [
    {"name": "Cocker Spaniel", "amount": 0.250},
    {"name": "Miniature Poodle", "amount": 0.250},
    {"name": "Miniature Pinscher", "amount": 0.125},
    {"name": "Pomeranian", "amount": 0.125},
    {"name": "English Cocker Spaniel", "amount": 0.125},
    {"name": "Companion", "amount": 0.03125}, # only pomeranian counts
    {"name": "Terrier", "amount": 0.03125},
    {"name": "Sighhound", "amount": 0.03125},
    {"name": "Hound", "amount": 0.03125},
]

def alt_names(breed):
    if breed == "Companion":
        return ['Keeshond', 'Pomeranian', 'Pug', 'Bichon Frise', 'Shih Tzu']
    if breed == 'Terrier':
        return ['Terrier', 'Terrier (any)']

    return [breed]

with open("responses.csv") as responsefile:
    reader = csv.DictReader(responsefile)

    final_tally = []

    for row in reader:
        name = row['Your Name']
        guesses = row['Your Answers (check each breed that you think belongs)']

        guesses = [g.strip() for g in guesses.split(",")]

        score = 0.0
        score_weighted = 0.0
        # scoring
        for g in guesses:
            correct = False
            for r in real_results:
                breeds = alt_names(r["name"])
                ratio = r['amount']

                if g in breeds:
                    correct = True
                    score_weighted += ratio / float(len(guesses))

            if correct:
                score += 1
            else:
                score -= 1

        final_tally.append({
            'Name' : '"' + name + '"',
            'Binary Score' : "%0.0f" % score,
            'Weighted Score' : '%f' % score_weighted,
            'Guesses' : row['Your Answers (check each breed that you think belongs)'],
            })

final_tally = sorted(final_tally, key =lambda x: x['Weighted Score'], reverse=True)

with open('scores.csv', 'w', newline='') as scorefile:
    writer=csv.DictWriter(scorefile, fieldnames = final_tally[0].keys())

    writer.writeheader()

    for r in final_tally:
        writer.writerow(r)