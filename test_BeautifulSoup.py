import re  # import regular expressioon


# this function will find and return all the valid url
# in the given string and return them in an array.
def find_valid_url(url_string):
    regex = r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))"
    url = re.findall(regex, url_string)
    return [x[0] for x in url]


# define the starting url string.
# this will be an input from the user
starting_url = 'my homepage is http://resume.donovanlo.sg?all and linkedin profile is linkedin.sg'

# place the found urls into urls array
urls = find_valid_url(starting_url)
print(urls)


# extract domain name portion
# extract domain name source directory
# declare variables an array of objects urls
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
