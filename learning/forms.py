from django import forms
from django.db import transaction
from .models import UserDeck, Deck

class UserDeckAdminForm(forms.ModelForm):
    word_item = forms.CharField(
        label='Word Items (comma-separated)',
        widget=forms.Textarea(attrs={'rows':5})
    )

    class Meta:
        model = UserDeck
        fields = '__all__'


    def clean(self):
        cleaned_data = super().clean()
        word_items = cleaned_data.get('word_items')
        print(word_items)
        if word_items:
            word_items_list = [word.strip() for word in word_items.split(',') if word.strip()]
            cleaned_data['word_items'] = word_items_list
        # print(cleaned_data)

    # @transaction.atomic
    # def save(self, commit=True):
    #     try:
    #         with transaction.atomic():
    #             deck_name = self.cleaned_data['deck'].name
    #             words_input = self.cleaned_data['word_items']
    #             word_items = [word.strip() for word in words_input.split(',') if word.strip()]
    #             print(f"Words entered:  {word_items}")
    #
    #     except Exception as e:
    #         print("An error occurred:", str(e))
    #         raise e
