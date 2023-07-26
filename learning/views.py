from django.http import JsonResponse, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from LangLearn.services import global_round_manager
from scoring.services import SentenceComparer, ScoreManager
import json


def home(request):
    username = 'adrian'
    user_info = global_round_manager.user_info

    # Pass the first sentence to the template
    context = {
        'username': username,
        'learning_language': user_info['learning_language'],
        'native_language': user_info['native_language'],
        'proficiency': user_info['proficiency'],
        'sentence': global_round_manager.get_sentence(),
    }

    return render(request, 'main/home.html', context)


def next_sentence(request):
    username = 'adrian'

    # Logic to process the user's translation

    # Get the next sentence
    next_sentence = global_round_manager.get_sentence()

    # Pass the next sentence to the template
    context = {
        'username': username,
        'sentence': next_sentence,
    }

    return render(request, 'main/home.html', context)


@csrf_exempt
def compare(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_sentence = data.get('user_sentence')
        correct_sentence = data.get('original_sentence')

        comparer = SentenceComparer('es')
        comparison_results = comparer.compare_sentences(correct_sentence, user_sentence)

        if 'error' not in comparison_results:
            user_profile = global_round_manager.user_info['user_profile']
            scorer = ScoreManager(user_profile)
            scorer.calculate_and_update_scores(comparison_results, correct_sentence, user_sentence, 'es')

        return JsonResponse(comparison_results)
    else:
        return HttpResponseNotAllowed(['POST'])