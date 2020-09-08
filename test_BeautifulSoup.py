# import regular expressioon
import re
import requests
from urllib.parse import urlsplit, urlparse, urljoin, ParseResult


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


def get_path(url_string):
    """
    split up the url_string to get the base url
    param url_string: string
    return type: string (of the base url)
    """
    parts = urlsplit(url_string)
    base = "{0.netloc}".format(parts)
    strip_base = base.replace("www.", "")
    starting_base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url_string[:url_string.rfind('/')+1] if '/' in parts.path else url_string
    # print("strip_base: " + strip_base)
    # print("starting_base_url:" + starting_base_url)
    # print("path:" + path)
    return path


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
    r = requests.get(valid_url)
    return (r.status_code == 200)


def build_absolute_url(url_string, base_url_string):
    """
    if the string is not a valid url with "http" or "https",
    convert the string into one
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










"""
MAIN
"""

# define the starting url string.
# this will be an input from the user
starting_string = 'my homepage is http://resume.donovanlo.sg?all and http://resume.donovanlo.sg?all linkedin profile is www.linkedin.sg http://resume.donovanlo.sg/some/path //www.example.com/some/path  /some/path'
# place the found urls into urls array
starting_urls = find_valid_url(starting_string)
# initialise an array to keep the url and info
url_list = []

if len(starting_urls) > 0:
    # set the first url found as base url
    starting_base_url = extract_domain(starting_urls[0])
    # if the first url is reachable. start crawling
    if is_alive(starting_urls[0]):
        # add the starting url into the list as dict
        # note: the starting url are retreived using find_valid_url,
        # therefore, they will be valid url
        for each_url in starting_urls:
            each_url = build_absolute_url(each_url, starting_base_url)
            # add to url list only if it belong to the same domain
            if extract_domain(each_url) == starting_base_url:
                # if it's a duplicate, don't add
                if url_list.count({"url": each_url}) == 0:
                    url_list.append({"url": build_absolute_url(
                        each_url, starting_base_url)})

        print(url_list)
        for idx, val in enumerate(url_list):
            # check whether the url is reachable
            url_reachable = is_alive(url_list[idx]["url"])
            url_list[idx].update({"reachable": url_reachable})
            if url_reachable:
                # proceed with web scrabbing
                print('proceed with '+url_list[idx]["url"])




            # check whether the url belong to the same site as base url




    else:
        print("The first url specified is unreachable.")
else:
    print("No urls found in the string.")






#     proceed with web crawling
#     {add other required operation}
#     word count // detemine pages
#     multimedia file count
#     images count
#     for each links in url array
#          get all the a links
#          check whether it's an absolute url or relative url
#          strip anchor '#'
#          strip query '?'
#          if absolute url
#                check whether it's same domain.
#                if not same domain, check validity of the link
#                   if url is valid, add it to the array urls
#                   else skip
#                else skip
#          else if relative url
#                check whether it start from '\'
#                if start from '\' append domain name
#                if not append domain name and source directory
#                test whether it is a valid url
#                      if it's valid, add it to array urls
#                     if it's not valid, skip
#           else skip
# If it is not a valil URL
#    return error message
