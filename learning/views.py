#TODO: Restructure - either move compare to Scoring, or make a separate api module

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import LimitOffsetPagination
from .models import UserWordBank
from .serializers import UserWordSerializer, LearningViewResponseSerializer
from datetime import datetime
from LangLearn.services import RoundManager
from scoring.services import SentenceComparer, ScoreManager

class LearningView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        print(username)
        round_manager = RoundManager()
        round_manager.initialize_round(username)

        round_info = round_manager.get_round_info()

        # Check if round_info is not None
        if round_info:
            # Prepare the data for the serializer
            data = {
                'username': username,
                'learning_language': {'value': round_info['user_info']['learning_language'].value},
                'native_language': {'value': round_info['user_info']['native_language'].value},
                'proficiency': round_info['user_info']['proficiency'],
                'buffer': round_info['buffer'],  # The entire buffer
                'learned_word_count': round_info['user_info']['learned_word_count'],
            }

            # Use the serializer to format the response data
            serializer = LearningViewResponseSerializer(data=data)
            if serializer.is_valid():
                print(Response(serializer.data).items())
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        else:
            return Response({'error': 'Round information could not be retrieved'}, status=400)

    def post(self, request):
        return Response({"error": "Method not allowed"}, status=405)


class CompareView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_sentence = request.data.get('user_sentence')
        correct_sentence = request.data.get('original_sentence')
        print("user_sentence: " + user_sentence, "correct" + correct_sentence)

        # Use request.user directly, which is the authenticated user
        user_profile = request.user.userprofile

        # Perform sentence comparison
        comparer = SentenceComparer('es')
        comparison_results = comparer.compare_sentences(correct_sentence, user_sentence)

        # Calculate and update scores
        if 'error' not in comparison_results:
            scorer = ScoreManager(user_profile)
            scorer.calculate_and_update_scores(comparison_results, correct_sentence, user_sentence, 'es')

        return Response(comparison_results)

    def get(self, request):
        return Response({"error": "Method not allowed"}, status=405)


class UserWordsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user_profile = request.user.userprofile
        proficiency_min = request.query_params.get('proficiency_min', 0.5)
        proficiency_max = request.query_params.get('proficiency_max', None)
        date_min = request.query_params.get('date_min', None)
        date_max = request.query_params.get('date_max', None)
        return_words = request.query_params.get('return_words', 'false').lower() == 'true'

        # Build the query
        query = Q(user_profile=user_profile, proficiency_level__gte=proficiency_min)
        if proficiency_max:
            query &= Q(proficiency_level__lte=proficiency_max)
        if date_min:
            query &= Q(last_practiced__gte=datetime.fromisoformat(date_min))
        if date_max:
            query &= Q(last_practiced__lte=datetime.fromisoformat(date_max))

        queryset = UserWordBank.objects.filter(query)

        if return_words:
            paginator = LimitOffsetPagination()
            result_page = paginator.paginate_queryset(queryset, request)
            serializer = UserWordSerializer(result_page, many=True)
            return paginator.get_paginated_response(serializer.data)

        # Default behavior: return count
        count = queryset.count()
        return Response({'count': count})

    def post(self, request):
        return Response({"error": "Method not allowed"}, status=405)

class SessionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        username = request.user.username
        round_manager = RoundManager()
        round_manager.initialize_round(username)

        round_info = round_manager.get_round_info()

        if round_info:
            # Structure the response data
            buffer_data = [{'value': item['value'], 'sentence': item['sentence'], 'translation': item['translation']}
                           for item in round_info['buffer']]
            return Response(buffer_data)
        else:
            return Response({'error': 'Session data could not be retrieved'}, status=400)

############################### OLD VIEWS - KEEPING UNTIL TESTED ##################################
#
# @login_required(login_url='/login/')
# @csrf_exempt
# def learning(request):
#     username = request.user.username
#     global_round_manager.set_user(username)
#     user_info = global_round_manager.user_info
#
#     # Pass the first sentence to the template
#     context = {
#         'username': username,
#         'learning_language': user_info['learning_language'],
#         'native_language': user_info['native_language'],
#         'proficiency': user_info['proficiency'],
#         'sentence': global_round_manager.get_sentence(),
#         'learned_word_count': user_info['learned_word_count'],
#     }
#
#     return render(request, 'main/home.html', context)
#
#
# @login_required(login_url='/login/')
# def next_sentence(request):
#     username = request.user.username
#
#     # Logic to process the user's translation
#
#     # Get the next sentence
#     next_sentence = global_round_manager.get_sentence()
#
#     # Pass the next sentence to the template
#     context = {
#         'username': username,
#         'sentence': next_sentence,
#     }
#
#     return render(request, 'main/home.html', context)
#
# @login_required(login_url='/login/')
# @csrf_exempt
# def compare(request):
#     if request.method == 'POST':
#         data = json.loads(request.body)
#         user_sentence = data.get('user_sentence')
#         correct_sentence = data.get('original_sentence')
#
#         comparer = SentenceComparer('es')
#         comparison_results = comparer.compare_sentences(correct_sentence, user_sentence)
#
#         if 'error' not in comparison_results:
#             user_profile = global_round_manager.user_info['user_profile']
#             scorer = ScoreManager(user_profile)
#             scorer.calculate_and_update_scores(comparison_results, correct_sentence, user_sentence, 'es')
#
#         return JsonResponse(comparison_results)
#     else:
#         return HttpResponseNotAllowed(['POST'])
#
# class NextSentenceView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         username = request.user.username
#         next_sentence = global_round_manager.get_sentence()
#
#         response_data = {
#             'username': username,
#             'sentence': next_sentence,
#         }
#
#         return Response(response_data)
#
############################### OLD VIEWS - KEEPING UNTIL TESTED ##################################