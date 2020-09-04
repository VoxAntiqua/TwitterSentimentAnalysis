import sys
import json
import string

# This should be a .json file with scraped tweets
TWEETS_FILENAME = sys.argv[1]


def main():
    
    """
    Once we have a list of tweets categorized as either postiive, negative, or
    neutral (their scores being positive, negative, or zero), we can assign a 
    sentiment score to every word that appears in a positive or negative
    tweet, regardless of whether or not it appears in AFINN, the list of
    scored terms.
    
    The sentiment score of each term will be calculated as a ratio of the
    number of instances of that term in a positive tweet to number of
    instances of that term in a negative tweet (starting both counts at 1 to 
    avoid division by zero)
    """
    
    with open('AFINN-111.txt', 'r') as f:
        afinn_scores = {}
        for line in f:
            term, afinn_score  = line.split("\t")  # The file is tab-delimited.
            afinn_scores[term] = int(afinn_score)  # Convert the score to an integer.
      
    # Build two lists of tweets        
      
    positive_tweets = []
    negative_tweets = []            
            
    with open(TWEETS_FILENAME, 'r', encoding="utf-8") as f:
        for line in f:
            tweet = json.loads(line)
            if "data" in tweet:
                tweet_text = tweet["data"]["text"]
                tweet_words = remove_punct_lower(tweet_text)
                score = 0
                for word in tweet_words:
                    if word in afinn_scores:
                        score += afinn_scores[word]
                if score > 0:
                    positive_tweets.append(tweet_words)
                elif score < 0:
                    negative_tweets.append(tweet_words)
                                
    # Build a dictionary of words and their appearances in positive/negative 
    # tweets, with lowercase word as key and a tuple of positive/negative
    # appearances as value

    word_numbers = {}

    for tweet in positive_tweets:
        for word in tweet:
            if word in word_numbers:
                word_numbers[word] = (word_numbers[word][0] + 1, word_numbers[word][1])
            else:
                word_numbers[word] = (2,1)
                
    for tweet in negative_tweets:
        for word in tweet:
            if word in word_numbers:
                word_numbers[word] = (word_numbers[word][0], word_numbers[word][1]+1)
            else:
                word_numbers[word] = (1,2)
                
    # Compute the sentiment score, filtering words that only have one occurrence.
    
    sentiment_scores = {}
    
    for word in word_numbers:
        if word_numbers[word][0] + word_numbers[word][1] != 3:
            sentiment_scores[word] = word_numbers[word][0] / word_numbers[word][1]
    
    for word in sentiment_scores:
        uprint(word,sentiment_scores[word])
    

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


if __name__ == '__main__':
    main()
