import string
import sys
import json

"""
Given a list of tweets in JSON format with hashtag data, this returns the top
ten most frequent hashtags followed by their frequency.
"""

# This should be a .json file with scraped tweets
TWEETS_FILENAME = sys.argv[1]


def main():
    
    hashtags_frequency = {}
    with open(TWEETS_FILENAME, 'r', encoding='utf-8') as f:
        for line in f:
            tweet = json.loads(line)
            if "data" in tweet:
                if "entities" in tweet["data"]:
                    if "hashtags" in tweet["data"]["entities"]:
                        for hashtag in tweet["data"]["entities"]["hashtags"]:
                            hashtags_frequency[hashtag["tag"]] = hashtags_frequency.get(hashtag["tag"],0) + 1
    
    hashtag_list = sorted(hashtags_frequency, key=hashtags_frequency.get, reverse=True)[:10]
    for tag in hashtag_list:
        uprint(tag, hashtags_frequency[tag])
        
# Print helper function so that Windows terminal doesn't freak out about certain
# characters.

def uprint(*objects, sep=' ', end='\n', file=sys.stdout):
    enc = file.encoding
    if enc == 'UTF-8':
        print(*objects, sep=sep, end=end, file=file)
    else:
        f = lambda obj: str(obj).encode(enc, errors='backslashreplace').decode(enc)
        print(*map(f, objects), sep=sep, end=end, file=file)


if __name__ == "__main__":
    main()