import pandas as pd
import re
import json


def structure_transcript(file_path):
        

    with open(file_path, 'r') as f:
        text = f.read()

    # Use regex to find the lines that contain interviewer and subject names
    interviewer_pattern = r'Interviewer:\s*(.*)'
    subject_pattern = r'Subject:\s*(.*)'

    interviewer_match = re.search(interviewer_pattern, text)
    subject_match = re.search(subject_pattern, text)


    if interviewer_match:
                print(f"Interviewer Found: {interviewer_match.group(1).strip()}")
                interviewer = interviewer_match.group(1).strip()
    else:
                raise ValueError("Interviewer not found in the transcript.")

    if subject_match:
                subject = subject_match.group(1).strip()
                print(f"Subject Found: {subject}")
    else:
                raise ValueError("Subject not found in the transcript.")


    # remove any timestamps - that look like [00:36:00]
    timestamp_pattern = r'\[\d+:\d+:\d+\]'
    text = re.sub(timestamp_pattern, '', text)

    # remove any colons
    text = text.replace(':', '')

    # create a list of tuples with each tuple containing the speaker and his/her utterances
    utterances = []
    current_speaker = None  # To keep track of the current speaker

    for line in text.split('\n'):
        if line.startswith(interviewer):
            speaker = interviewer
            line = line.replace(interviewer, '')
        elif line.startswith(subject):
            speaker = subject
            line = line.replace(subject, '')
        else:
            # If the line doesn't start with a speaker, consider it a continuation of the latest speaker's text
            if current_speaker is not None:
                utterances[-1] = (current_speaker, f"{utterances[-1][1]} {line.strip()}")
            continue

        if current_speaker == speaker:
            # If the speaker is the same as the previous line, concatenate the utterances
            utterances[-1] = (current_speaker, f"{utterances[-1][1]} {line.strip()}")
        else:
            # If the speaker is different, add the new utterance as a new tuple
            utterances.append((speaker, line.strip()))

        current_speaker = speaker  # Update the current speaker

    # Separate the utterances of Interviewer and Subject into different lists
    interviewer_utterances = [utterance[1] for utterance in utterances if utterance[0] == interviewer]
    subject_utterances = [utterance[1] for utterance in utterances if utterance[0] == subject]

    print(f"Number of interviewer utterances: {len(interviewer_utterances)}")
    print(f"Number of subject utterances: {len(subject_utterances)}")

    # Create a DataFrame with separate columns for Interviewer and Subject utterances
    df = pd.DataFrame({'Interviewer': interviewer_utterances, 'Subject': subject_utterances})

    # Add a column for question numbers
    df.insert(0, 'Question', range(1, len(df) + 1))

    # Reset the index
    df.reset_index(drop=True, inplace=True)

    return df



def dataframe_to_jsonl(df, output_file_path):
    # Create an array of dictionaries with questions and ideal generated answers
    result_array = []
    for _, row in df.iterrows():
        result_array.append({
            "prompt": row['Interviewer'],
            "completion": row['Subject']
        })

    # Write the array of dictionaries to a JSONL file
    with open(output_file_path, 'w') as f:
        for item in result_array:
            f.write(json.dumps(item) + '\n')




def create_fine_tuning_data(file_path, output_file_path):
    # pass in the path to the transcript file and the path to the output file
    # the transcript file should be a text file with the interviewer and subject names at the top
    # the output file will be a jsonl file that can be used to fine tune the GPT model
    # recommended to use openai cli to do further cleaningon the data before fine-tuning

    df = structure_transcript(file_path)
    dataframe_to_jsonl(df, output_file_path)
    return

