from numpy import *
from numpy.linalg import inv

GAME_COUNT = 11652
TEAM_COUNT = 32
TEAMS = {"Ravens" : 1, "Bengals" : 2, "Browns" : 3, "Steelers" : 4, "Bills" : 5, "Dolphins" : 6, "Patriots" : 7,
    "Jets" : 8, "Texans" : 9, "Colts" : 10, "Jaguars" : 11, "Titans" : 12, "Oilers" : 12, "Broncos" : 13,
    "Chiefs" : 14, "Chargers" : 15, "Raiders" : 16, "Bears" : 17, "Lions" : 18, "Packers" : 19, "Vikings" : 20,
    "Cowboys" : 21, "Giants" : 22, "Eagles" : 23, "Redskins" : 24, "Falcons" : 25, "Panthers" : 26,
    "Saints" : 27, "Buccaneers" : 28, "Cardinals" : 29, "Rams" : 30, "49ers" : 31, "Seahawks" : 32}

# matrix and result vector both initialized with zero entries

m = zeros((GAME_COUNT, TEAM_COUNT))
b_vector = zeros(GAME_COUNT).transpose()

# csv file that was loaded using the scraper in main.py

f = open("result.csv", "r")
lines = f.readlines()
length = len(lines)

# looping through the lines of the file to extract information
# each line contains the data of one of the games between 1970 and now

for i in range(length):
    game_info = lines[i].replace("\n", "").split(",")

    team_x = int(TEAMS[game_info[0]])
    team_y = int(TEAMS[game_info[2]])
    teamx_score = int(game_info[1])
    teamy_score = int(game_info[3])

    # checking which team comes first in the TEAMS dict

    min_team_index = min(team_x, team_y)

    # assigning 30 of the teams a 0 coefficient term
    # assigning team y and team x a 1 and -1 coefficient term depending on their order in the TEAMS dict
    # assigning the result vector entry a value of the point differential between the two teams

    buckets = [0] * TEAM_COUNT
    buckets[team_y - 1] = 1
    buckets[team_x - 1] = -1

    b_vector[i] = teamy_score - teamx_score

    if min_team_index == team_x:
        buckets[team_x - 1] = 1
        buckets[team_y - 1] = -1
        b_vector[i] = teamx_score - teamy_score

    # adding the row equation to the matrix

    m[i] = buckets

# Since this equation is not solvable naturally, here is a least squares approximation

# ATA represents (A^T) * A
# ATB represents (A^T) * b

ATA = matmul(m.transpose(), m)
ATB = matmul(m.transpose(), b_vector)

# here I set the last row of the new left side matrix to all ones and the last entry of the
# new right side result vector to 0

ATA[TEAM_COUNT - 1] = ones(TEAM_COUNT)
ATB[TEAM_COUNT - 1] = 0

# now we solve for the rankings by inverting the left side matrix and multiplying it to the result vector

r_vector = matmul(inv(ATA), ATB)

# Oilers was a name for the Tennessee Titans back in the day. In case you missed it in the TEAMS dict,
# I mapped Oilers and Titans to the same order value to take that into account. Here I remove it because
# I can just use the common day title Titans to refer to the team in the result

TEAMS.pop("Oilers", None)

# mapping each team to its ranking

score_dict = {}
for key, value in TEAMS.items():
    score_dict[key] = r_vector[value - 1]

# sorting the team ranks in descending order based on rank values.

sorted_ranks = sorted(score_dict.items(), key=lambda x: x[1], reverse=True)

# printing each team and its ranking

for (a, b) in sorted_ranks:
    print("{}: {}".format(a, b))

# closing file

f.close()