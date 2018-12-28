import requests
import os
from configparser import ConfigParser


def format_elimination_bracket(json_data, input_file_name, output_file_name):
    alliances = {d['seed']: d for d in json_data['alliances']}

    with open(input_file_name, "r") as template_file:
        template = template_file.read()

    bracket_sheet = template

    d = {1: {"red": 1, "blue": 4}, 2: {"red": 2, "blue": 3}}

    for sf in range(1, 3):
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Red_1}",
                                              str(alliances[d[sf]["red"]]['captain']))
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Red_2}",
                                              str(alliances[d[sf]["red"]]['pick1']))
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Red_3}",
                                              str(alliances[d[sf]["red"]]['pick2'])
                                              if alliances[d[sf]["red"]]['pick2'] > 0 else "")

        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Blue_1}",
                                              str(alliances[d[sf]["blue"]]['captain']))
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Blue_2}",
                                              str(alliances[d[sf]["blue"]]['pick1']))
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Blue_3}",
                                              str(alliances[d[sf]["blue"]]['pick2'])
                                              if alliances[d[sf]["blue"]]['pick2'] > 0 else "")

    with open(output_file_name, "w") as file:
        file.write(bracket_sheet)

    os.system("start " + output_file_name)


if __name__ == "__main__":
    config = ConfigParser()
    config.read("Configuration.ini")

    section = 'Elimination_Alliance_Sheet'

    base_url = "http://" + config.get(section, 'server_ip') + "/"
    base_path = "apiv1/events/" + config.get(section, 'event_code') + "/"

    elimination_alliances_url = base_url + base_path + "elim/alliances/"

    response = requests.get(elimination_alliances_url)
    response.raise_for_status()

    result = response.json()

    format_elimination_bracket(result,
                               config.get(section, 'elimination_template_file'),
                               config.get(section, 'elimination_output_file'))
