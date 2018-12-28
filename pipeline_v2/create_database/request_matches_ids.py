import urllib3
import json
import time


def main():
    # Initial request
    http = urllib3.PoolManager()
    r = http.request('GET', 'https://api.opendota.com/api/proMatches')
    data_dict = json.loads(r.data.decode("utf-8"))
    matches_list = []
    for match in data_dict:
        matches_list.append(match["match_id"])

    f = open("matches.txt", "w")
    for match in matches_list:
        f.write(str(match) + "\n")
    f.close()

    count_requests = 100

    while count_requests < 1000000:
        r = http.request('GET', 'https://api.opendota.com/api/proMatches?less_than_match_id=' +
                         str(matches_list[len(matches_list) - 1]))
        data_dict = json.loads(r.data.decode("utf-8"))
        if r.status == 200:
            print("Successful request!")
            matches_list = []
            for match in data_dict:
                matches_list.append(match["match_id"])

            f = open("matches.txt", "a")
            for match in matches_list:
                f.write(str(match) + "\n")
            f.close()
        else:
            print("Request failed! Waiting 10 seconds...")
            time.sleep(10)


if __name__ == "__main__":
    main()
