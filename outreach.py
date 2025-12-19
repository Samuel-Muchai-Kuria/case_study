# # message_generator.py
# import pandas as pd
# import dotenvt

# from google import genai

# client = genai.Client(api_key= os.dotenv(gemini_api_key))


# def generate_messages(input_csv="validated_jobs.csv", output_csv="jobs_with_messages.csv"):
#     df = pd.read_csv(input_csv)
#     messages = []
#     tones = ["professional", "personalized"]
#     for _, row in df.iterrows():
#         prompt = f"""
#         Write a {tones} outreach message to the hiring manager for the following job:

#         Job Title: {row['Job Title']}
#         Company Name: {row['Company Name']}
#         Location: {row['Location']}
#         Job Description: {row['Job Description']}

#         Message should be concise, engaging, and highlight interest in the role.
#         """
#         response = client.models.generate_content(
#             model="gemini-2.5-flash",
#            contents= prompt,
#         )
#         message = response.text
#         messages.append(message)

#     df['LLM-Generated Message'] = messages
#     df.to_csv(output_csv, index=False)
#     return df

# message_generator.py
import os
import pandas as pd
from dotenv import load_dotenv
from google import genai
import random

# Load environment variables
load_dotenv()

# Initialize Gemini client
client = genai.Client(api_key=os.getenv("gemini_api_key"))

def generate_messages( input_csv="validated_jobs.csv", output_csv="jobs_with_messages.csv"):

    df = pd.read_csv(input_csv)

    messages = []
    tones = ["professional", "personalized"]

    for _, row in df.iterrows():
        tone = random.choice(tones)

        prompt = f"""
        Write a {tone} outreach message to the hiring manager for the following job.

        Job Title: {row['Job Title']}
        Company Name: {row['Company']}
        Location: {row['Location']}
        Job Description: {row['Job Description']}

        Keep the message concise (3–4 sentences), engaging, and express genuine interest.
        """

        response = client.models.generate_content(
            model="gemini-flash-latest",
            contents=prompt
        )

        messages.append(response.text.strip())

    df["LLM-Generated Message"] = messages
    df.to_csv(output_csv, index=False)

    return df

if __name__ == "__main__":
    generate_messages()