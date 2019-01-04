import requests
import os
from configparser import ConfigParser


def format_elimination_bracket_teams(bracket_template, alliances):
    bracket_sheet = bracket_template

    d = {1: {"red": 1, "blue": 4}, 2: {"red": 2, "blue": 3}}

    for sf in range(1, 3):
        bracket_sheet = bracket_sheet.replace("#{SF_" + str(sf) + "_Red_1}",
                                              str(alliances[d[sf]["red"]]['captain']))
        bracket_sheet = bracket_sheet.replace("#{SF_" + str(sf) + "_Red_2}",
                                              str(alliances[d[sf]["red"]]['pick1']))
        bracket_sheet = bracket_sheet.replace("#{SF_" + str(sf) + "_Red_3}",
                                              str(alliances[d[sf]["red"]]['pick2'])
                                              if alliances[d[sf]["red"]]['pick2'] > 0 else "")

        bracket_sheet = bracket_sheet.replace("#{SF_" + str(sf) + "_Blue_1}",
                                              str(alliances[d[sf]["blue"]]['captain']))
        bracket_sheet = bracket_sheet.replace("#{SF_" + str(sf) + "_Blue_2}",
                                              str(alliances[d[sf]["blue"]]['pick1']))
        bracket_sheet = bracket_sheet.replace("#{SF_" + str(sf) + "_Blue_3}",
                                              str(alliances[d[sf]["blue"]]['pick2'])
                                              if alliances[d[sf]["blue"]]['pick2'] > 0 else "")

    return bracket_sheet


def format_team_data(sheet, team_data):
    team_codes = ['', 'captain', 'pick1', 'pick2']
    for seed in range(1, 5):
        for team in range(1, len(team_codes)):
            sheet = sheet.replace("#{seed_"+str(seed)+"_team_" + str(team) + "_number}",
                                  str(team_data[seed][team_codes[team]]['number']))
            sheet = sheet.replace("#{seed_"+str(seed)+"_team_" + str(team) + "_name}",
                                  str(team_data[seed][team_codes[team]]['name']))
            sheet = sheet.replace("#{seed_"+str(seed)+"_team_" + str(team) + "_affiliation}",
                                  str(team_data[seed][team_codes[team]]['school']))

            country = ", " + str(team_data[seed][team_codes[team]]['country']) \
                if str(team_data[seed][team_codes[team]]['country']) not in ["USA", ""]  \
                else ""
            location = str(team_data[seed][team_codes[team]]['city']) + ", " \
                + str(team_data[seed][team_codes[team]]['state']) + country
            sheet = sheet.replace("#{seed_"+str(seed)+"_team_" + str(team) + "_location}", location)
    return sheet


def get_team_info(url, team_number):
    result = requests.get(url + str(team_number))
    if result.status_code == 500:
        return None
    return result.json()


def make_seed_dict(seed):
    s = seed['seed']
    return {'seed': s, 'captain': get_team_info(alliance_information_url, alliances[s]['captain']),
            'pick1': get_team_info(alliance_information_url, alliances[s]['pick1']),
            'pick2': get_team_info(alliance_information_url, alliances[s]['pick2'])}


if __name__ == "__main__":
    config = ConfigParser()
    config.read("Configuration.ini")

    section = 'Elimination_Alliance_Sheet'

    base_url = "http://" + config.get(section, 'server_ip') + "/"
    base_path = "apiv1/events/" + config.get(section, 'event_code') + "/"

    elimination_alliances_url = base_url + base_path + "elim/alliances/"

    with open(config.get(section, 'elimination_template_file'), "r") as template_file:
        template = template_file.read()

    response = requests.get(elimination_alliances_url)
    response.raise_for_status()
    result = response.json()
    alliances = {d['seed']: d for d in result['alliances']}
    elimination_sheet = format_elimination_bracket_teams(template, alliances)

    if config.getboolean(section, 'include_team_details'):
        with open(config.get(section, 'details_template_file'), "r") as details_file:
            details = details_file.read()

        elimination_sheet = elimination_sheet.replace("#{team_details}", details)

        alliance_information_url = base_url + base_path + "teams/"
        response = requests.get(alliance_information_url)
        result = response.json()
        team_data = {seed['seed']: make_seed_dict(seed) for seed in alliances.values()}
        elimination_sheet = format_team_data(elimination_sheet, team_data)
    else:
        elimination_sheet = elimination_sheet.replace("#{team_details}", "")

    with open(config.get(section, 'elimination_output_file'), "w") as file:
        file.write(elimination_sheet)

    os.system("start " + config.get(section, 'elimination_output_file'))
