from careerjet_api_client import CareerjetAPIClient
import requests
import json

cj  =  CareerjetAPIClient("en_GB");
auth_value = "Bearer {{your_api_key}}"
base_url = "{{base_url}}"
debug = 0

def print_line(line):
    if debug:
        print(line)
        
        
def call_careerjet_api(page,keywords,location):

    return cj.search({
                            'page'    : page,
                            'location'    : location,
                            'keywords'    : keywords,
                            'affid'       : '213e213hd12344552',
                            'user_ip'     : '11.22.33.44',
                            'url'         : 'http://www.example.com/jobsearch?q=python&l=london',
                            'user_agent'  : 'Mozilla/5.0 (X11; Linux x86_64; rv:31.0) Gecko/20100101 Firefox/31.0'
                          });


def process_career_jet_results(results,view_for):
    table = "/Jobs"
    url = base_url + table
    headers_dict = {"Authorization": auth_value, "Content-Type": "application/json"}

    jobs = results["jobs"]
    dataObject = {
        "typecast": True,
        "records": [

        ]
    }
    count = 0
    for job in jobs:
        count = count + 1
        record = {
                    "fields": {
                        "title": job['title'],
                        "salary": job['salary'],
                        "description": job['description'],
                        "url": job['url'],
                        "company": job['company'],
                        "locations": job['locations'],
                        "date": job['date'],
                        "view_for":view_for

                    }
                }


        dataObject["records"].append(record)
        print_line("Updating content with values:")
        print_line(dataObject)
        if count == 10:
            response = requests.post(url, json=dataObject, headers=headers_dict)
            print response
            dataObject["records"] = []
            count = 0
            contentJson = json.loads(response.text)
            print_line(contentJson)
            print("Sending to airtable")


def get_jobs_from_career_jet():
    keywords = 'scrum master'
    view_for = "none"
    location = 'united states'
    page_number = 0
    total_pages = 1

    while page_number < total_pages:
        print_line("Calling career jet api for page number: " + str(page_number))
        results = call_careerjet_api(page_number,keywords,location)
        if results:
            print_line(results['pages'])
            process_career_jet_results(results,view_for)
            total_pages = results['pages']
            print("Processing page number: " + str(page_number) + "Total Pages: " + str(total_pages))
            page_number = page_number + 1



def main():
    get_jobs_from_career_jet()


main()
