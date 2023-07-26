import streamlit as st

exec(open("./django_settings.py").read())

from django.contrib.auth.models import User
from user_management.models import UserProfile, UserLanguageProficiency
from languages.models import Language


def main():
    st.title("Create User Account")

    with st.form("Create User"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        email = st.text_input("Email")
        learning_languages = st.multiselect("Learning Languages", Language.objects.values_list("name", flat=True))
        native_language = st.selectbox("Native Language", Language.objects.values_list("name", flat=True))
        submit_button = st.form_submit_button("Create")

    if submit_button:
        try:
            # Create User
            user = User.objects.create_user(username, email, password)

            # Create UserProfile
            native_language_obj = Language.objects.get(name=native_language)
            user_profile = UserProfile.objects.create(
                user=user,
                native_language=native_language_obj,
            )

            # Create UserLanguageProficiency for each selected learning language
            for learning_language_name in learning_languages:
                learning_language_obj = Language.objects.get(name=learning_language_name)
                UserLanguageProficiency.objects.create(
                    user_profile=user_profile,
                    language=learning_language_obj,
                    proficiency_level=0,
                )

            st.success("User account created successfully.")
        except Exception as e:
            st.error(f"Error creating user account: {str(e)}")


if __name__ == "__main__":
    main()
