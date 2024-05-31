import requests
import json
import pprint
import csv


def check_DA(domain):
    # myFile = open('src/assets/input.csv','r')
    # reader = csv.reader(myFile)

    # row_count = sum(1 for row in myFile)
    # row_count = int(row_count)
    # print ("row_count in file: ",row_count)

    # myFile.close()

    # myFile = open('src/assets/input.csv','r')
    # reader = csv.reader(myFile)

    # outputFile = open('src/DataAnalysis/data/DA_output.csv', 'w')
    # outputWriter = csv.writer(outputFile)

    # outputWriter.writerow(["URL","DA"])

    url = "https://lsapi.seomoz.com/v2/url_metrics"
    """
    headers = {
        'Authorization': 'Basic bW96c2NhcGUtOTQ0ODRiYjI0OTplZTFkOTFhMGJjYWQ2YmNmZThlMWZhNDU5ZDEzNWZiYQ==',
        'Content-Type': 'application/json',
        'Cookie': '__cfduid=d5e605fe6b4077577761980e84856815f1600710127',
    }
    """
    headers = {
        "Authorization": "Basic bW96c2NhcGUtYjJmMmI3NGEwYzo1YTQwOGEzMDZkYWJhM2JhZmUxNThmNzhhMjcyMTllYw==",
        "Content-Type": "application/json",
        "Cookie": "__cfduid=d57137e530cb8830a86dd3966c0e852891609019976",
    }
    response = requests.post(url, headers=headers, json={"targets": [domain]})
    for results in response.json()["results"]:
        root_domain = results["root_domain"]
        domain_authority = results["domain_authority"]
        return {"domain": root_domain, "da": domain_authority}

    # headers = {
    #     'Authorization': 'Basic bW96c2NhcGUtZDE0MTgyMmYyMDpmZGIzYWFiYTBlZTkyMThjNDUzNTk2MjlmNzlmMzZmNQ==',
    #     'Content-Type': 'application/json',
    #     'Cookie': '__cfduid=d57137e530cb8830a86dd3966c0e852891609019976',
    # }

    # pages = []
    # which_row = 0

    # for row in reader:
    #     which_row += 1
    #     pages.append(row[0])
    #     if (len(pages) == 50) or (which_row == row_count):
    #         response = requests.post(url, headers=headers, json={"targets": pages})
    #         for results in response.json()["results"]:
    #             root_domain = results["root_domain"]
    #             domain_authority = results["domain_authority"]
    #             outputWriter.writerow([root_domain,domain_authority])
    #         #print(response.json())
    #         pages = []

    # myFile.close()
    # outputFile.close()
