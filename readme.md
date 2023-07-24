# Fine-tuning from an interview transcript

A project I worked on to fine-tune interview transcripts. Works for 1x interviewer and 1x subject per transcript. Sharing online in case it can help anyone. 

This repository contains a Python package that enables interaction with the OpenAI API and provides functionalities to structure interview transcripts for fine-tuning. The package includes the following files:

1. `openai_functions.py`: This file contains a set of functions that allow easy interaction with the OpenAI API. Functions are available to upload files, retrieve uploaded files, create fine-tuned models, and check the status of ongoing fine-tuning processes.

2. `transcript_functions.py`: This file contains functions specifically designed to structure interview transcripts into a format suitable for fine-tuning. It includes functions to extract interviewer and subject names, remove timestamps and colons, and organize the transcript into utterances by speakers.

## Usage

1. **Set up OpenAI API key**: Before using the package, make sure you have set your OpenAI API key as the `OPENAI_API_KEY` environment variable. If the key is not set, an error message will be displayed.

2. **Interacting with OpenAI API**: To utilize the functions for interacting with the OpenAI API, you can import the `openai_functions` module and call the respective functions. Here's an example of how to use these functions:

```python
import openai_functions

# Upload a file to OpenAI
openai_functions.upload_to_openai("filename.txt")

# Retrieve all uploaded files
openai_functions.get_all_files()

# Retrieve all fine-tuned models
openai_functions.get_all_finetunes()

# Create a fine-tuned model
openai_functions.fine_tune_model("training_file.txt", training_model="davinci", custom_name="my-custom-model")

# Get the status of fine-tuned models
openai_functions.get_finetune_status()
```

3. **Structuring Interview Transcripts**: To structure interview transcripts, import the `transcript_functions` module and utilize the provided functions. Here's an example of how to use them:

```python
import transcript_functions

# Structure the transcript file
df = transcript_functions.structure_transcript("transcript.txt")

# Convert the DataFrame to a JSONL file
transcript_functions.dataframe_to_jsonl(df, "output.jsonl")

# Create fine-tuning data from a transcript file
transcript_functions.create_fine_tuning_data("transcript.txt", "output.jsonl")
```

## Suggested Workflow
1. Get your interview transcript files - I used .txt when testing and it worked well. Make sure to add the following to the top of your transcripts:
```
Interviewer: <Interviewer Label/Name>
Subject: <Subject Label/Name>
```

2. Use the transcript functions to create your fine tuning data (.jsonl file)

3. Upload your file to openai using the provided openai function

4. Once your file is uploaded you can fine-tune a model of your choice using your uploaded file as the training data.

5. Fine-tuning can take some time. The fine-tuning process is queued and eventually executed, you can use the get_finetune_status() function to check the status of your fine-tuned model.


## Note

It is recommended to perform further data cleaning and processing before initiating fine-tuning using the OpenAI CLI. This will help improve the quality and performance of the fine-tuned models.

[OpenAI Fine-Tuning Guide](https://platform.openai.com/docs/guides/fine-tuning)