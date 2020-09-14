# import regular expressioon
import re
import requests
from urllib.parse import urlparse, urljoin, ParseResult
from bs4 import BeautifulSoup


def find_valid_url(url_string):
    """
    find and return all the valid urls
    param url_string: string
    return type: array (containing valid urls)
    credit: https://www.geeksforgeeks.org/python-check-url-string/
    """
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, url_string)
    return [x[0] for x in url]


def is_valid_url(url_string):
    """
    check whether the given string is valid url using regex
    param url_string: string
    return type: boolean
    """
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    return bool(re.search(regex, url_string))


def extract_domain(url, remove_http=False):
    """
    extract domain name from given url
    param url_string: string
    param remove_http: boolean
    return type: string (containing domain name with or without http)
    Source: https://pydeep.com/get-domain-name-from-url-python-snippet/
    """
    uri = urlparse(url)
    if remove_http:
        domain_name = f"{uri.netloc}"
    else:
        if uri.netloc == "":
            domain_name = ""
        else:
            if uri.scheme == "":
                domain_name = f"http://{uri.netloc}"
            else:
                domain_name = f"{uri.scheme}://{uri.netloc}"
    return domain_name


def is_alive(valid_url):
    """
    check whether the url given is reachable
    param valid_url: url in string
    return type: boolean, true if respond is 200, false for others
    """
    try:
        r = requests.get(valid_url)
    except Exception:
        return("False")
    return (r.status_code == 200)


def build_absolute_url(url_string, base_url_string):
    """
    if the string is not a valid url with "http" or "https",
    convert the string into one
    param url_string: string (the url to be parsed)
    param base_url_string: string (the base url that contain the domain name)
    return type: string (coverted url)
    Reference: https://docs.python.org/3/library/urllib.parse.html
    """
    if is_valid_url(url_string):
        p = urlparse(url_string, 'http')
        netloc = p.netloc or p.path
        path = p.path if p.netloc else ''
        # if not netloc.startswith('www.'):
        #     netloc = 'www.' + netloc
        p = ParseResult('http', netloc, path, *p[3:])
        return p.geturl()
    else:
        return urljoin(base_url_string, url_string)


def retrieve_html(full_url):
    """
    download the html from the given url
    param full_url: string (an url stating with http)
    return type: string (either a html page or an error message)
    """
    if full_url.startswith('http'):
        response = requests.head(full_url)
        if "text/html" in response.headers["content-type"]:
            response = requests.get(full_url)
            html_page = response.content
            return html_page
        else:
            return('Error: Non html page')
    else:
        return('Error: Please use a full url starting with http')


def is_html(full_url):
    """
    check the type of content of the given url
    param full_url: string (an url stating with http)
    return type: boolean (True is content type is html,
                          False if it's not or error encountered)
    """
    if full_url.startswith('http'):
        response = requests.head(full_url)
        if "text/html" in response.headers["content-type"]:
            return True
        else:
            return False
    else:
        return False


def count_words(full_url):
    """
    count the numbers of words in the given url
    param html_page: html document
    return type: integer (number of words)
                  -1 means error
    """
    if full_url.startswith('http'):
        my_wordlist = []
        html_page = retrieve_html(full_url)
        soup = BeautifulSoup(html_page, 'html.parser')
        text = soup.get_text()
        words = text.lower().split()
        for each_word in words:
            my_wordlist.append(each_word)
        return(len(my_wordlist))
    else:
        return(-1)


def count_images(full_url):
    """
    count the numbers of image in the given url
    param html_page: html document
    return type: integer (number of words)
                  -1 means error
    """
    if full_url.startswith('http'):
        my_imageslist = []
        html_page = retrieve_html(full_url)
        soup = BeautifulSoup(html_page, 'html.parser')
        images = soup.find_all('img')
        for each_image in images:
            my_imageslist.append(each_image.get('src'))
    return (len(images))


def check_for_scripts(full_url):
    """
    check whether there is any script in the given url
    param html_page: html document
    return type: boolean
    """
    if full_url.startswith('http'):
        html_page = retrieve_html(full_url)
        soup = BeautifulSoup(html_page, 'html.parser')
        scripts_found = soup.find_all('script')
        if len(scripts_found) > 0:
            return True
        else:
            return False


def strip_url_string(url_string):
    """
    locate the '#' and remove them along
    with the remainder of the given url string
    param url_string: string
    return type:  string
    """
    try:
        url_string = url_string[:url_string.index('#')]
    except Exception:
        pass
    return url_string


def extract_links(full_url):
    """
    extract all the 'a' links on the page
    param html_page: html document
    return type :  list (a list of url)
    """
    if full_url.startswith('http'):
        starting_base_url = extract_domain(full_url)
        my_a_tags = []
        html_page = retrieve_html(full_url)
        soup = BeautifulSoup(html_page, 'html.parser')
        a_tags = soup.find_all('a')
        for each_a_tag in a_tags:
            href = each_a_tag.attrs.get("href")
            href = strip_url_string(href)
            if href not in ["NULL", "_blank", "None", None, "NoneType"]:
                href = build_absolute_url(href, starting_base_url)
                my_a_tags.append(href)
        return my_a_tags
    return None


def is_url_in_list(my_url, my_list):
    """
    check whether the given url is in the list of dictionaries
    param my_url: sting (the url searching for)
    param my_list: list (of dictionairies containing a key "url")
    return type: Boolean
    """
    for each_dict in my_list:
        if each_dict["url"] == my_url:
            return True
    return False


def remove_duplicates(my_list):
    """
    remove duplicates items in the list
    param my_list: list
    return type: list
    """
    final_list = []
    for item in my_list:
        if item not in final_list:
            final_list.append(item)
    return final_list


def retrieve_info(starting_url):
    """
    retrieve the information from the website of the given url
    param starting_url: sting (the url to start crawling)
    return type: list (of dictionairies)
    """
    # place the found urls into urls array
    starting_urls = find_valid_url(starting_string)
    starting_urls = remove_duplicates(starting_urls)
    # initialise an array to keep the url and info
    url_list = []  # store processed url
    # remove duplicates from the link list
    queue_url_list = starting_urls
    starting_base_url = extract_domain(starting_urls[0])
    for each_url in queue_url_list:
        each_url = strip_url_string(each_url)
        each_url = build_absolute_url(each_url, starting_base_url)
    queue_url_list = remove_duplicates(queue_url_list)
    while len(queue_url_list) > 0:
        current_url = queue_url_list.pop(0)
        current_domain = extract_domain(current_url)
        current_record = {}
        current_record.update({"url": current_url})
        # check whether the url is valid
        current_url = build_absolute_url(current_url, starting_base_url)
        valid_url = is_valid_url(current_url)
        current_record.update({"valid url": valid_url})
        if valid_url:
            # check whether  it's in the same domain
            within_domain = (current_domain == starting_base_url)
            current_record.update({"within domain": within_domain})
            if within_domain:
                # check whether the domain is reachable
                reachable = is_alive(current_url)
                current_record.update({"reachable": reachable})
                if reachable:
                    # check the page has html content
                    html_content = is_html(current_url)
                    current_record.update({"html content": html_content})
                    if html_content:
                        # proceed with web scrapping
                        num_of_words = count_words(current_url)
                        num_of_pages = num_of_words // words_per_page + 1
                        current_record.update({"words": num_of_words})
                        current_record.update({"pages": num_of_pages})
                        num_of_images = count_images(current_url)
                        current_record.update({"images": num_of_images})
                        page_contain_scripts = check_for_scripts(current_url)
                        current_record.update({"contain scripts":
                                              page_contain_scripts})
                        # scrap links on page
                        links_on_page = []
                        # extract links from the page for processing
                        links_on_page = extract_links(current_url)
                        # remove duplicates from the link list
                        links_on_page = remove_duplicates(links_on_page)
                        base_url = current_domain
                        for each_link in links_on_page:
                            each_link = strip_url_string(each_link)
                            each_link = build_absolute_url(each_link, base_url)
                        links_on_page = remove_duplicates(links_on_page)
                        for each_link in links_on_page:
                            to_queue_url = True
                            # check validity of the url
                            try:
                                if not(is_valid_url(each_link)):
                                    to_queue_url = False
                            except Exception:
                                pass
                            # check whether it is within the domain
                            try:
                                if not(base_url == extract_domain(each_link)):
                                    to_queue_url = False
                            except Exception:
                                pass
                            # check whether it exist in the url list
                            try:
                                if (is_url_in_list(each_link, url_list)):
                                    to_queue_url = False
                            except Exception:
                                pass
                            # check whether it exist in the queued url list
                            try:
                                if each_link in queue_url_list:
                                    to_queue_url = False
                            except Exception:
                                pass
                            # check whether it the current url
                            try:
                                if current_url == each_link:
                                    to_queue_url = False
                            except Exception:
                                pass
                            # add records to url list
                            if to_queue_url:
                                queue_url_list.append(each_link)
                            else:
                                to_queue_url = True
        url_list.append(current_record)
    return url_list


"""
MAIN
"""
# setting config variables
words_per_page = 300
basic_overhead_cost_per_project = 500

# define the starting url string.
# this will be an input from the user
starting_string = 'http://resume.donovanlo.sg?all'
'http://resume.donovanlo.sg/index.html http://resume.donovanlo.sg?all'
'linkedin profile is www.linkedin.sg'
' http://resume.donovanlo.sg/some/path'
'//www.example.com/some/path  /some/path'

result = retrieve_info(starting_string)

for x in result:
    print(x)
