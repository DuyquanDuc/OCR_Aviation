from openai import OpenAI
from datetime import datetime
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def send_meta_to_model(meta_content: str):
    """
    Sends a chunk of text to the model and gets a response.
    """ 
    description = ""
    # Assuming `client.chat.completions.create` returns a complete response when not streaming
    response = client.chat.completions.create(
        model="gpt-4-0125-preview",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "assistant", "content": r""" The data provided is the text that extracted from Service Offerring
                   (SOs) files of DXG, a Digital transformation unit (DXG is a division of FPT),  go straight to aswer the following question:
                    1. Based on the metadata (extract the file name and annotate it as the service.for example C:\Users\DuyQD\Desktop\Approved S&O\Data Governance - v2.pptx 
                   so say "DXG Data Governance Service". ) Answer the question what is the service ? and what the component inside it ?
                    2. Summary the content in 3 sentences                   """
                   },
                  {"role": "user", "content": meta_content}
                  ]
    )
    if response.choices and response.choices[0].message.content:
        description += response.choices[0].message.content
        print(f"parsed JSON from model response: {response.choices[0].message.content}")
    return description

import os

# Directory containing the input files
input_directory_path = r'process_documents\process_pptx_separate'
output_file_path = r'service_summarizer_output\service_summarized.txt'

# Ensure any previous output file is cleared or replaced
if os.path.exists(output_file_path):
    os.remove(output_file_path)

# Log start time
logger.info("Starting...")

# Open the output file once and write each response
with open(output_file_path, 'a', encoding='utf-8') as output_file:
    # Process each file in the directory
    for filename in os.listdir(input_directory_path):
        if filename.endswith('.txt'):  # Check if the file is a text file
            input_file_path = os.path.join(input_directory_path, filename)

            # Read the content from the file
            with open(input_file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            # Send content to processing model (assuming send_meta_to_model is defined)
            response = send_meta_to_model(content)

            # Write the processed content to the output file
            output_file.write(f"---{filename}---\n{response}\n\n")

logger.info("All files processed.")