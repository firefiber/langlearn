import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')


def from_openai_chat(learning_language, native_language, proficiency, words, theme=None):
    sentences = []

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are a skilled digital language tutor."
                           "The user will provide you with the following information:"
                           " - The language they are learning (learning language)"
                           " - Their native language (native language)"
                           " - Their proficiency level in the learning language"
                           " - A theme (optional)"
                           " - A list of words they want to use in sentences"
                           "Your primary function is to generate 2 sentences for each of the given words, in the learning language."
                           "Then, translate each sentence into the native language."
                           "Format the response this way: "
                           "word | sentence | translation"
                           "One set per line. Do not include any additional formatting in your response."},
            {
                "role": "user",
                "content":
                    f"learning_language: {learning_language},"
                    f"native_language: {native_language},"
                    f"proficiency: {proficiency},"
                    f"theme: {theme},"
                    f"words: {words}"
            }
        ],
        temperature=0.1
    )

    # Extract the output
    output = response['choices'][0]['message']['content']
    cleaned_output = clean_openai_output(output, learning_language, native_language)
    return cleaned_output


def clean_openai_output(output, learning_language, native_language):
    lines = output.split('\n')  # split the output into lines
    cleaned_output = []
    for line in lines:
        # split each line into word, sentence, and translation
        parts = line.split(" | ")
        if len(parts) == 3:  # check if line was split into 3 parts
            word, sentence, translation = parts
            cleaned_output.append({
                "word": word.strip(),
                "sentence": sentence.strip(),
                "translation": translation.strip(),
            })
    return cleaned_output


def from_openai_completion(learning_language, native_language, proficiency, words, theme=None):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=f"Create 2 {proficiency} level sentences in {learning_language} with each these words: {words}. "
               f"Then, translate these sentences into {native_language}. "
               "Format the response this way: "
               "word | sentence | translation"
               "One set per line. Do not include any additional formatting in your response.",
        temperature=0.1

    )
    output = response['choices'][0]
    cleaned_output = clean_openai_output(output)
    return cleaned_output
