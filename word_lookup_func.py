#%%
import pandas as pd
import re
#%%
def word_lookup(text, words_of_interest):
    """
    Returns a dictionary with the count of each word of interest found in the text.
    args:
        text (str): The text to search within.
        words_of_interest (list): A list of words or lists with words to count in the text.
    returns:
        dict: A dictionary with words as keys and their counts as values.
    """
    word_dict = {}
    for item in words_of_interest:
        if type(item) == list:
            total = 0
            for word in item:
                total += len(re.findall(word, text))
            word_dict[item[0]] = total
        else:
            word_dict[item] = len(re.findall(item, text))
    return word_dict