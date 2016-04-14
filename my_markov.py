import sys
import os
import twitter
from random import choice

def open_and_read_file(file_path1):
    """Takes file path as string; returns text as string.

    Takes a string that is a file path, opens the file, and turns
    the file's contents as one string of text.
    """

    file_one = open(file_path1)
    # file_two = open(file_path2)

    file_text = file_one.read()

    file_one.close()
    # file_two.close()


    #Note the new line characters still exist in super string
    return file_text


def make_chains(text_string, num):
    """Takes input text as string; returns _dictionary_ of markov chains.

    A chain will be a key that consists of a tuple of (word1, word2)
    and the value would be a list of the word(s) that follow those two
    words in the input text.

    For example:

        >>> make_chains("hi there mary hi there juanita")
        {('hi', 'there'): ['mary', 'juanita'], ('there', 'mary'): ['hi'], ('mary', 'hi': ['there']}
    """
    # Initialize empty dictionary
    chains = {}

    words = text_string.split()

    # Iterate over every word in list until there aren't enough words left to fill a tuple of [num] length
    for i in range(len(words) - (num - 1)): 
        n_gram = () #Empty tuple for keys
    
        #Add word at index [i], and all following words, until tuple is [num] words long
        for j in range(num):
            n_gram += (words[i + j],) 

        #If key does not exist in dictionary, initialize key with value = empty list    
        chains[n_gram] = chains.get(n_gram, [])

        #Append word following last word in key, if one exists
        if i + num < len(words): 
            chains[n_gram].append(words[i + num])


    return chains


def make_text(chains):
    """Takes dictionary of markov chains.
        Returns random text beginning with a capitalized letter and ending with a punctuation.

    """

    text = ""
    key = choice(chains.keys()) #Choosing random key from chains dict
    punctuation = ['!', '.', '?'] #Designate final punctuation marks

    # Keep pulling keys at random until you find one whose first item begins with an uppercase letter
    while not key[0][0].isupper():
        key = choice(chains.keys())

    text = text + key[0]

    for i in range(1,len(key)):    
        text = text + " " + key[i]  #Adding first word pair to text 

    #Choosing random word from value list, append to text, generate new key, repeat
    #Repeat until loop reaches end of original file or punctuation in punctuation list 
    while chains[key] != [] and key[-1][-1] not in punctuation and len(text) <= 140: 

        next_word = choice(chains[key])
        text = text + " " + next_word
        key = key[1:] + (next_word,)

    return text


def tweet(chains):
    # Use Python os.environ to get at environmental variables
    # Note: you must run `source secrets.sh` before running this file
    # to make sure these environmental variables are set.

    api = twitter.Api(
        consumer_key = os.environ['TWITTER_CONSUMER_KEY'],
        consumer_secret = os.environ['TWITTER_CONSUMER_SECRET'],
        access_token_key = os.environ['TWITTER_ACCESS_TOKEN_KEY'],
        access_token_secret = os.environ['TWITTER_ACCESS_TOKEN_SECRET'])

    # print api.VerifyCredentials()

    tweet = api.PostUpdate(chains)

    print tweet.text


# #Get variables from command line 
input_path1 = sys.argv[1]
# input_path2 = sys.argv[2]
input_num = int(sys.argv[2]) 

# # Open the file and turn it into one long string
input_text = open_and_read_file(input_path1)

# # Get a Markov chain
chains = make_chains(input_text,input_num)

# # Produce random text
random_text = make_text(chains)

# Your task is to write a new function tweet, that will take chains as input
tweet(random_text)



