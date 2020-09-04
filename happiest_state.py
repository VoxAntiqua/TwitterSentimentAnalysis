import string
import sys
import json

"""
Given a list of tweets in JSON format with location (or, at a minimum, user
data containing location), calculates the average sentiment of tweets from
each US state and returns the state with the highest (happiest) score.
"""

# This should be a .json file with scraped tweets
TWEETS_FILENAME = sys.argv[1]

STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
        'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

def main():
    
    # Initialize dictionary containing tweets for each state
    state_tweets = {}
    for state in STATES:
        state_tweets[state] = []
    
    # Populate above dictionary by searching through tweet location data
    with open(TWEETS_FILENAME, 'r', encoding="utf-8") as f:
        for line in f:
            tweet = json.loads(line)
            if "includes" in tweet:
                if "places" in tweet["includes"]:
                    if tweet["includes"]["places"][0]["country_code"] == "US":
                        for state_abbrev in STATES.keys():
                            if state_abbrev in tweet["includes"]["places"][0]["full_name"] or STATES[state_abbrev] in tweet["includes"]["places"][0]["full_name"]:
                                state_tweets[state_abbrev].append(tweet)
                elif "location" in tweet["includes"]["users"][0]:
                    for state_abbrev in STATES.keys():
                            if ", " + state_abbrev in tweet["includes"]["users"][0]["location"] or STATES[state_abbrev] in tweet["includes"]["users"][0]["location"]:
                                state_tweets[state_abbrev].append(tweet) 
    
    # Create dictionary of word and sentiment scores
    scores = {}
    with open('AFINN-111.txt', 'r') as f:
        for line in f:
            term, score  = line.split("\t")  # The file is tab-delimited.
            scores[term] = int(score)  # Convert the score to an integer.
    
    # Create dictionary containing each state's total sentiment score.
    state_total_scores = {}
    for state in STATES:
        state_total_scores[state] = 0
        for tweet in state_tweets[state]:
            tweet_words = remove_punct_lower(tweet["data"]["text"])
            tweet_score = 0
            for word in tweet_words:
                if word in scores:
                    tweet_score += scores[word]
            state_total_scores[state] += tweet_score
    
    # Compute the average sentiment score for all tweets from each state
    state_average_scores = {}
    for state in STATES:
        if state_tweets[state] != []:
            state_average_scores[state] = state_total_scores[state]/len(state_tweets[state])

    max_value = max(state_average_scores.values())
    max_keys = [k for k, v in state_average_scores.items() if v == max_value]
    
    if len(max_keys) == 1:
        print(max_keys[0], max_value)
    else:
        print(max_keys, max_value)

# Given a string, returns a list of lowercase words without punctuation.
def remove_punct_lower(text):
     words = text.lower().split()
     return [w.rstrip( string.punctuation) for w in words ]                        
                    
if __name__ == "__main__":
    main()