"""
******************************
CS 1026 - Assignment 2 – YouTube Emotions
Code by: Armaan Dhillon
Student ID: adhil28
File created: November 15, 2024
******************************
This Python file asks the user for input and raises the corresponding error. It makes use of the functions created in
emotions.py and is the main file which runs the full program.
"""

import os.path
from emotions import *

VALID_COUNTRIES = ['all','bangladesh', 'brazil', 'canada', 'china', 'egypt',
                   'france', 'germany', 'india', 'iran', 'japan', 'mexico',
                   'nigeria', 'pakistan', 'russia', 'south korea', 'turkey',
                   'united kingdom',  'united states']


def ask_user_for_input():
    #Prompts the user to input for the keyword file, comment file, country, and report file. This function will
    #also raise the corresponding error.
    #Parameters: No parameters
    #Returns: keywords_file (str), comment_file (str), country (str), report_file (str)

    keywords_file = input("Input keyword file (ending in .tsv): ").strip()
    if not keywords_file.endswith(".tsv"):
        raise ValueError("Keyword file does not end in .tsv!")
    if not os.path.exists(keywords_file):
        raise IOError(f"{keywords_file} does not exist!")

    comment_file = input("Input comment file (ending in .csv): ").strip()
    if not comment_file.endswith(".csv"):
        raise ValueError("Comments file does not end in .csv!")
    if not os.path.exists(comment_file):
        raise IOError(f"{comment_file} does not exist!")

    country = input("Input a country to analyze (or 'all' for all countries): ").strip().lower()
    if country not in VALID_COUNTRIES:
        raise ValueError(f"{country} is not a valid country to filter by!")

    report_file = input("Input the name of the report file (ending in .txt): ").strip()
    if not report_file.endswith(".txt"):
        raise ValueError("Report file does not end in .txt!")
    if os.path.exists(report_file):
        raise IOError(f"{report_file} already exists!")

    return keywords_file, comment_file, country, report_file



def main():
    #Main function to execute the YouTube Emotion program. It calls all other functions to successfully run the program.
    #Parameters: No parameters
    #Return: Nothing returned

    while True:
        try:
            keywords_file, comment_file, country, report_file = ask_user_for_input()
            keywords = make_keyword_dict(keywords_file)
            comments = make_comments_list(country, comment_file)
            if not comments:
                raise RuntimeError("Error: No comments in dataset!")
            common_emotion = make_report(comments, keywords, report_file)
            print(f"Most common emotion is: {common_emotion}")
            break
        except (ValueError, IOError, RuntimeError) as e:
            print(e)
            break


if __name__ == "__main__":
    main()
