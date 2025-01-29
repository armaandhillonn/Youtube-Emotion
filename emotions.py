"""
******************************
CS 1026 - Assignment 2 – YouTube Emotions
Code by: Armaan Dhillon
Student ID: adhil28
File created: November 15, 2024
******************************
This Python file contains the functions for processing comments and analyzing emotions. These functions are used
together to create a detailed report for the user.
"""


EMOTIONS = ['anger', 'joy', 'fear', 'trust', 'sadness', 'anticipation']


def clean_text(comment):
     #Cleans comments by converting all letters to lowercase and replacing non-alphabet characters with spaces.
     #Parameters: comment (str)
     #Returns: The cleaned comment (comment_cleaned)
    comment_cleaned = ""

    for char in comment:
        if 'a' <= char <= 'z' or 'A' <= char <= 'Z':
            comment_cleaned += char.lower()
        else:
            comment_cleaned += " "
    return comment_cleaned

def make_keyword_dict(keyword_file_name):
    #Reads the keyword file and creates a dictionary mapping keywords to emotion scores.
    #Parameters: keyword_file_name (str)
    #Returns: keyword_dict

    keyword_dict = {}
    with open(keyword_file_name, 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            words = parts[0]
            keyword_dict[words] = {
                'anger': int(parts[1]),
                'joy': int(parts[2]),
                'fear': int(parts[3]),
                'trust': int(parts[4]),
                'sadness': int(parts[5]),
                'anticipation': int(parts[6]),
            }
    return keyword_dict

def classify_comment_emotion(comment, keywords):
    #Classifies the emotion of a comment based on keyword matches.
    #Parameters: comment (str), keywords (dict)
    #Returns: final_emotion (The most common emotion found in the comment.)

    comment_cleaned = clean_text(comment)
    words = comment_cleaned.split()

    emotion_count = {
        'anger': 0,
        'joy': 0,
        'fear': 0,
        'trust': 0,
        'sadness': 0,
        'anticipation': 0
    }

    for word in words:
        if word in keywords:
            for emotion in emotion_count:
                emotion_count[emotion] += keywords[word][emotion]

    max_score = None
    final_emotion = None
    for emotion in emotion_count:
        if max_score is None or emotion_count[emotion] > max_score:
            max_score = emotion_count[emotion]
            final_emotion = emotion

    return final_emotion

def make_comments_list(filter_country, comments_file_name):
    #Reads the comments file and filters comments based on the specified country.
    #Parameters: filter_country (str), comments_file_name (str)
    #Returns: comment_list (list of dictionaries representing filtered comments).

    comments_list = []

    with open(comments_file_name, 'r') as file:
        for line in file:
            parts = line.strip().split(',')

            comment_id = int(parts[0].strip())
            username = parts[1].strip()
            country = parts[2].strip().lower()
            text = ','.join(parts[3:]).strip()

            if filter_country == "all" or country == filter_country:
                comments_list.append({
                    'comment_id': comment_id,
                    'username': username,
                    'country': country,
                    'text': text
                })

    return comments_list

def make_report(comment_list, keywords, report_filename):
    #Computes a report of percent of emotions found in the comments and writes it to a file.
    #Parameters: comment_list (list), keywords (dict), report_filename (str)
    #Returns: final_emotion

    if len(comment_list) == 0:
        raise RuntimeError("No comments in dataset!")

    emotions = ['anger', 'joy', 'fear', 'trust', 'sadness', 'anticipation']
    emotion_count = {}
    for emotion in emotions:
        emotion_count[emotion] = 0

    for comment in comment_list:
        text = comment['text']
        classified_emotion = classify_comment_emotion(text, keywords)
        emotion_count[classified_emotion] += 1

    max_count = 0
    final_emotion = None
    for emotion in emotions:
        if emotion_count[emotion] > max_count:
            max_count = emotion_count[emotion]
            final_emotion = emotion

    total_comments = 0
    for count in emotion_count.values():
        total_comments += count

    emotion_percentages = {}
    for emotion in emotions:
        percentage = (emotion_count[emotion] / total_comments) * 100
        emotion_percentages[emotion] = round(percentage, 2)

    report_lines = []
    report_lines.append(f"Most common emotion: {final_emotion}\n\n")
    report_lines.append("Emotion Totals\n")
    for emotion in emotions:
        count = emotion_count[emotion]
        percentage = emotion_percentages[emotion]
        report_lines.append(f"{emotion}: {count} ({percentage}%)\n")

    with open(report_filename, 'w') as file:
        for line in report_lines:
            file.write(line)

    return final_emotion
