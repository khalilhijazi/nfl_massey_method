import requests
from bs4 import BeautifulSoup

base_url = 'http://www.nfl.com/schedules/'
f = open('result.csv', 'w')


def main():
    max_week_count = 18

    # gets data on regular season games

    for year in range(1970, 2019):
        print("Regular Season: {}".format(year))
        year_url = base_url + str(year) + "/REG"
        if year == 2018:
            max_week_count = 15
        for week in range(1, max_week_count):
            source_code = requests.get(year_url + str(week))
            plain_text = source_code.text
            soup = BeautifulSoup(plain_text, "html.parser")
            get_games(soup)

    # gets data on playoff games

    for year in range(1970, 2018):
        print("Playoffs: {}".format(year))
        year_url = base_url + str(year) + "/POST"
        source_code = requests.get(year_url + str(week))
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, "html.parser")
        get_games(soup)

    # closing file

    f.close()


# loops through all the games on a page and writes the data to a csv result file


def get_games(soup):

    # gets all divs for match ups

    divs = soup.find_all('div', {'class': 'list-matchup-row-team'})

    # looping through each match up on that page

    for div in divs:
        spans = div.find_all('span')

        team_away = spans[0].text
        away_score = spans[3].text
        team_home = spans[7].text
        home_score = spans[4].text
        f.write("{},{},{},{}\n".format(team_away, away_score, team_home, home_score))


main()