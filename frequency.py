import string
import json
import sys

# This should be a .json file with scraped tweets
TWEETS_FILENAME = sys.argv[1]

def main():
    
    """
    For each term in the text of a list of tweets, this returns the frequency
    of each unique term, defined as the number of occurrences of the term in
    all tweets divided by the number of occurrences of all terms in all tweets.
    """ 
    
    term_total = 0
    term_count = {}
    
    with open(TWEETS_FILENAME, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            if "data" in tweet:
                tweet_text = tweet["data"]["text"]
                tweet_words = remove_punct_lower(tweet_text)
                for word in tweet_words:
                    term_total += 1
                    term_count[word] = term_count.get(word, 0) + 1
    
    print(term_total)
    for term in term_count:
        uprint(term, term_count[term]/term_total)

# Given a string, returns a list of lowercase words without punctuation.

def remove_punct_lower(text):
    text.encode("utf-8")
    words = text.lower().split()
    return [w.rstrip( string.punctuation) for w in words ]

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