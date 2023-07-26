exec(open("./django_settings.py").read())

from user_management.fetchers import fetch_user_info, fetch_words_in_buffer
from learning.services.generate_sentences import from_openai_chat


def main():

    # Page title
    # st.title("LangLearn")

    username = "adrian"
    user_info = fetch_user_info(username)

    def get_user_word_list(user_info):
        word_list = fetch_words_in_buffer(user_info['user_profile'])
        return word_list

    def generate_sentences(user_info):
        words = get_user_word_list(user_info)
        proficiency = user_info['proficiency']
        learning_language = user_info['learning_language']
        native_language = user_info['native_language']

        sentences = from_openai_chat(learning_language, native_language, proficiency, words)

        print(sentences)

    generate_sentences(user_info)

    # user_word_list = get_user_word_list(username)


    # st.write(user_word_list)


if __name__ == "__main__":
    main()
