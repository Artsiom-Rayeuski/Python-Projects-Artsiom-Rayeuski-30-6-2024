import requests
import os


def download_file(url, destination):
    try:
        response = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("No internet connection")
        return None
    with open(destination, 'wb') as f:
        f.write(response.content)


def update_compromised_lists():
    path_to_folder = os.path.dirname(os.path.abspath(__file__))
    # print(path_to_folder)
    ip_live_dest = path_to_folder + "/folder_for_compr_files/compromised_ip_live.txt"
    ip_full_dest = path_to_folder + "/folder_for_compr_files/compromised_ip_full.txt"
    domain_live_dest = path_to_folder + "/folder_for_compr_files/compromised_domains_live.txt"
    domain_full_dest = path_to_folder + "/folder_for_compr_files/compromised_domains_full.txt"
    download_file("https://zonefiles.io/f/compromised/ip/live/", ip_live_dest)
    download_file("https://zonefiles.io/f/compromised/ip/full/", ip_full_dest)
    download_file("https://zonefiles.io/f/compromised/domains/live/", domain_live_dest)
    download_file("https://zonefiles.io/f/compromised/domains/full/", domain_full_dest)


if __name__ == '__main__':
    update_compromised_lists()

