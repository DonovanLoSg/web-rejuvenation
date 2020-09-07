# input string
# test whether it is a valid URL
# extract domain name portion
# extract domain name source directory
# declare variables an array of urls
# If it is a valid URL
#     add string into array urls
#     proceed with web crawling
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
