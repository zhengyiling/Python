#!/usr/bin/env python
# coding: utf-8


#Q1
#A researcher has gathered thousands of news articles. 
#But she wants to focus her attention on articles including a specific word. 
#Complete the function below to help her filter her list of articles.

# Your function should meet the following criteria:

# Do not include documents where the keyword string shows up only as a part of a larger word. 
# For example, if she were looking for the keyword “closed”, you would not include the string “enclosed.”
# She does not want you to distinguish upper case from lower case letters. So the phrase “Closed the case.” 
# would be included when the keyword is “closed”
# Do not let periods or commas affect what is matched. “It is closed.” would be included when the keyword is “closed”. 
# But you can assume there are no other types of punctuation.



#Lin's solution
def word_search(doc_list, keyword):
    """
    Takes a list of documents (each document is a string) and a keyword. 
    Returns list of the index values into the original list for all documents 
    containing the keyword.

    Example:
    doc_list = ["The Learn Python Challenge Casino.", "They bought a car", "Casinoville"]
    >>> word_search(doc_list, 'casino')
    >>> [0]
    """
    res = []
    for i in range(len(doc_list)):
        if keyword.lower() in doc_list[i].lower().strip('.,').split():
                res.append(i)
    return res
            





doc_list = ["The Learn Python Challenge Casino.", "They bought a car", "Casinoville"]
word_search(doc_list, 'casino')





doc_list=['The Learn Python Challenge Casino', 'They bought a car, and a horse', 'Casinoville?']
word_search(doc_list, 'car')





#Kaggle's solution
def word_search(documents, keyword):
    # list to hold the indices of matching documents
    indices = [] 
    # Iterate through the indices (i) and elements (doc) of documents
    for i, doc in enumerate(documents):
        # Split the string doc into a list of words (according to whitespace)
        tokens = doc.split()
        # Make a transformed list where we 'normalize' each word to facilitate matching.
        # Periods and commas are removed from the end of each word, and it's set to all lowercase.
        normalized = [token.rstrip('.,').lower() for token in tokens]
        # Is there a match? If so, update the list of matching indices.
        if keyword.lower() in normalized:
            indices.append(i)
    return indices





doc_list = ["The Learn Python Challenge Casino.", "They bought a car", "Casinoville"]
word_search(doc_list, 'casino')





doc_list=['The Learn Python Challenge Casino', 'They bought a car, and a horse', 'Casinoville?']
word_search(doc_list, 'car')







