from rest_framework.views import APIView
from rest_framework.response import Response

class SimpleDataAPI(APIView):
    def get(self, request, *args, **kwargs):
        data = {
            "message": "Hello from Django!"
        }
        return Response(data)
