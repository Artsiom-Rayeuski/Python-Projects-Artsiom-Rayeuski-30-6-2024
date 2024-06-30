import os
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin


def check_websocket_creation(url):
    try:
        # Check if the URL points to a JavaScript file
        if url.endswith('.js'):
            # URL points to a JavaScript file, fetch the file content
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch {url}: Status code {response.status_code}")
                return False

            js_code = response.text
        else:
            # URL points to a web page, fetch the web page content
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to fetch {url}: Status code {response.status_code}")
                return False

            # Extract JavaScript code from the web page content
            js_code = re.findall(r'<script.*?>(.*?)</script>', response.text, re.DOTALL)

            # Join multiple JavaScript blocks into a single string
            js_code = '\n'.join(js_code)

        # Check for WebSocket creation
        if re.search(r'new\s+WebSocket\(', js_code):
            return True
        else:
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False


def fetch_internal_links_and_js_reverse(url, visited=None):
    if visited is None:
        visited = set()

    if url in visited:
        return [], []

    visited.add(url)

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url}: Status code {response.status_code}")
            return [], []

        soup = BeautifulSoup(response.content, 'html.parser')
        internal_links = set()
        js_files = set()

        # Extract internal links
        for link in soup.find_all('a'):
            href = link.get('href')
            if href and not href.startswith('#'):  # Skip URLs with fragments
                parsed_url = urlparse(href)
                if parsed_url.netloc == '' or parsed_url.netloc == urlparse(url).netloc:
                    if parsed_url.scheme == '':
                        href = urljoin(url, href)
                    internal_links.add(href)

        # Extract JavaScript files
        for script in soup.find_all('script'):
            src = script.get('src')
            if src:
                parsed_url = urlparse(src)
                if parsed_url.netloc == '' or parsed_url.netloc == urlparse(url).netloc:
                    if parsed_url.scheme == '':
                        src = urljoin(url, src)
                    js_files.add(src)

        internal_links = list(internal_links)
        js_files = list(js_files)

        # Reverse internal links and JavaScript files
        internal_links.reverse()
        js_files.reverse()

        # Fetch resources recursively
        all_links = []
        all_js_files = []
        for link in internal_links:
            fetched_links, fetched_js_files = fetch_internal_links_and_js_reverse(link, visited)
            all_links.extend(fetched_links)
            all_js_files.extend(fetched_js_files)

        return list(set(internal_links + all_links)), list(set(js_files + all_js_files))

    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return [], []


def validate_url(url):
    parsed_url = urlparse(url)
    if parsed_url.scheme and parsed_url.netloc:
        return True
    else:
        return False


def validate_urls_file(file_path):
    if not os.path.isfile(file_path):
        print(f"Error: File {file_path} not found.")
        return False

    try:
        with open(file_path, 'r') as file:
            urls = file.readlines()
            urls = [url.strip() for url in urls]
            for url in urls:
                if not validate_url(url):
                    print(f"Error: Invalid URL in file: {url}")
                    return False
            return True
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return False


def user_input(input_data):
    if input_data.startswith('http://') or input_data.startswith('https://'):
        # Input is a URL
        if validate_url(input_data):
            url = input_data
            internal_links, js_files = fetch_internal_links_and_js_reverse(url)
            return internal_links, js_files
    else:
        # Input is a file containing URLs
        try:
            if validate_urls_file(input_data):
                with open(input_data, 'r') as file:
                    urls = file.readlines()
                    urls = [url.strip() for url in urls]

                    all_internal_links = []
                    all_js_files = []

                    for url in urls:
                        internal_links, js_files = fetch_internal_links_and_js_reverse(url)
                        all_internal_links.extend(internal_links)
                        all_js_files.extend(js_files)

                    return list(set(all_internal_links)), list(set(all_js_files))
        except Exception as e:
            print(f"Error reading file {input_data}: {e}")
            return [], []


def discovery(input_data):
    internal_links, js_files = user_input(input_data)
    websocket_urls = []

    # Check internal links for WebSocket creation
    for link in internal_links:
        if check_websocket_creation(link):
            websocket_urls.append(link)

    # Check JavaScript files for WebSocket creation
    for js_file in js_files:
        if check_websocket_creation(js_file):
            websocket_urls.append(js_file)

    # Sort the URLs by domain name
    websocket_urls.sort(key=lambda url: urlparse(url).netloc)

    return websocket_urls


if __name__ == "__main__":
    input_data = "urls.txt"  # Change this to a file containing URLs or a single URL
    websocket_urls = discovery(input_data)
    print("URLs where WebSocket is being created:")
    print(websocket_urls)
