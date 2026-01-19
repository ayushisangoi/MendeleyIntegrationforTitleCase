from mendeley import Mendeley
import requests
import string


def has_more_than_one_capital_ascii(word):
    if not isinstance(word, basestring):
        raise TypeError("Input must be a string")
    return sum(1 for ch in word if ch in string.ascii_uppercase) > 1

def title_case(text):
    """
    Convert a string to title case, excluding certain small words
    unless they are the first or last word.
    """
    if not isinstance(text, str):
        raise TypeError("Input must be a string")

    # Words to keep lowercase unless first or last
    exceptions = {"a", "an", "and", "as", "at", "but", "by", "for",
                  "in", "nor", "of", "on", "or", "per", "the", "to", "vs", "via"}

    words = text.split()
    if not words:
        return ""

    result = []
    for i, word in enumerate(words):
        # Always capitalize first and last word
        if (i == 0 or i == len(words) - 1 or word not in exceptions ) and not(has_more_than_one_capital_ascii(word)):
            result.append(word.capitalize())
        else:
            result.append(word)

    return " ".join(result)


# import nltk.data

# These values should match the ones supplied when registering your application.
# under https://dev.mendeley.com/myapps.html
redirect_uri = "http://localhost:5000/oauth"
client_id = 99999                    # please update
client_secret = "1p2iendow930"     # please update

mendeley = Mendeley(client_id, redirect_uri=redirect_uri)
auth = mendeley.start_implicit_grant_flow()

# The user needs to visit this URL, and log in to Mendeley.
login_url = auth.get_login_url()

res = requests.post(login_url, allow_redirects = False, data = {
    'username': 'email',    # please update
    'password': 'password'                # please update
})
res.headers
auth_response = res.headers['Location']


# After logging in, the user will be redirected to a URL, auth_response.
session = auth.authenticate(auth_response)
print(session.files.list().items)
counter = 0
# Iterate over every document in your mendeley library
for document in session.documents.iter():
    counter += 1
    # if counter > 50:
    #     break
    # Uncomment below to see all titles and ids
    # print(document.id)
    # print(document.title)
    title = document.title
    # print(type(title))
    # Note I would recommend you doing a backup of old titles by e.g. saving all ID and titles to a dataframe and saving it as .csv file
    oldstring=title.encode('utf-8')
    # print(oldstring)
    newtitle = title_case (oldstring)
    print(newtitle)
    document.update(title=newtitle) #comment to not update mendeley permanently

