import requests
import os

template_name = "html/FIRST_elim_alliance_sheet.austl"
output_name = "html/elim_alliance_sheet.html"


def format_elimination_bracket(json_data):
    alliances = {d['seed']: d for d in json_data['alliances']}

    with open(template_name, "r") as template_file:
        template = template_file.read()

    bracket_sheet = template

    d = {1: {"red": 1, "blue": 4}, 2: {"red": 2, "blue": 3}}

    for sf in range(1, 3):
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Red_1}",
                                              str(alliances[d[sf]["red"]]['captain']))
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Red_2}",
                                              str(alliances[d[sf]["red"]]['pick1']))
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Red_3}",
                                              str(alliances[d[sf]["red"]]['pick2']))

        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Blue_1}",
                                              str(alliances[d[sf]["blue"]]['captain']))
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Blue_2}",
                                              str(alliances[d[sf]["blue"]]['pick1']))
        bracket_sheet = bracket_sheet.replace("#{SF_"+str(sf)+"_Blue_3}",
                                              str(alliances[d[sf]["blue"]]['pick2']))

    with open(output_name, "w") as file:
        file.write(bracket_sheet)

    os.system("start " + output_name)


server_ip = "127.0.0.1"
event_code = "dummy"


base_url = "http://" + server_ip + "/"
base_path = "apiv1/events/" + event_code + "/"

elimination_alliances_url = base_url + base_path + "elim/alliances/"

if __name__ == "__main__":
    response = requests.get(elimination_alliances_url)
    response.raise_for_status()

    result = response.json()

    format_elimination_bracket(result)
