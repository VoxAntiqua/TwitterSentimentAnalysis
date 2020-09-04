import json
import string
import sys

# This should be a .json file with scraped tweets
TWEETS_FILENAME = sys.argv[1]

def main():    
    
    # Based on the word sentiment scores in the provided text file,
    # 'AFINN-111.txt', we can sum scores for words with emotional content in
    # each tweet and assign a score to that tweet - positive sentiment will
    # result in a positive integer, and vice-versa for negative.
    
    with open('AFINN-111.txt', 'r') as f:
        scores = {}
        for line in f:
            term, score  = line.split("\t")  # The file is tab-delimited.
            scores[term] = int(score)  # Convert the score to an integer.
              
    scores_output = []            
            
    with open(TWEETS_FILENAME, 'r') as f:
        for line in f:
            tweet = json.loads(line)
            if "data" in tweet:
                tweet_text = tweet["data"]["text"]
                tweet_words = remove_punct_lower(tweet_text)
                score = 0
                for word in tweet_words:
                    if word in scores:
                        score += scores[word]
                scores_output.append(score)
            
    with open('tweet_scores.txt', 'w') as f:
        f.writelines("%s\n" % val for val in scores_output)

# Given a string, returns a list of lowercase words without punctuation.

def remove_punct_lower(text):
     words = text.lower().split()
     return [w.rstrip( string.punctuation) for w in words ]

if __name__ == '__main__':
    main()
