import re  # import regular expressioon
import requests
from urllib.parse import urlsplit


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


def get_base_url(url_string):
    """
    split up the url_string to get the base url
    param url_string: string
    return type: string (of the base url)
    """
    parts = urlsplit(url_string)
    base = "{0.netloc}".format(parts)
    strip_base = base.replace("www.", "")
    base_url = "{0.scheme}://{0.netloc}".format(parts)
    path = url_string[:url_string.rfind('/')+1] if '/' in parts.path else url_string
    print("strip_base: " + strip_base)
    print("base_url:" + base_url)
    print("path:" + path)
    return path


def is_alive(valid_url):
    """
    check whether the url given is reachable
    param valid_url: url in string
    return type: boolean, true if respond is 200, false for others
    """
    r = requests.get(valid_url)
    return (r.status_code == 200)


"""
MAIN
"""
# define the starting url string.
# this will be an input from the user
starting_string = 'my homepage is http://resume.donovanlo.sg?all and linkedin profile is www.linkedin.sg'

# place the found urls into urls array
starting_urls = find_valid_url(starting_string)
# initialise an array to keep the url and info
url_list = []

if len(starting_urls) > 0:
    # set the first url found as base url
    base_url = starting_urls[0]
    # if the first url is reachable. start crawling
    if is_alive(starting_urls[0]):
        # add the starting url into the list as dict
        for each_url in starting_urls:
            url_list.append({"url": each_url})
            # check whether the url is a absolute url
            # check whether the url belong to the same site as base url
            # if not a absolute url, prefix with base url
            # check whether the url is a valid url
            # check whether the url is reachable
            # 

        print(url_list)
        print("-----------------")
        print(get_base_url("http://resume.donovan.sg"))
        print("-----------------")
        print(get_base_url("https://resume.donovan.sg"))
        print("-----------------")
        print(get_base_url("resume.donovan.sg"))
        print("-----------------")
        print(get_base_url("/resume.donovan.sg"))
        print("-----------------")

    else:
        print("The first url specified is unreachable.")
else:
    print("No urls found in the string.")





# If it is a valid URL
#     add string into array urls
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
