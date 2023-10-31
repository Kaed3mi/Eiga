from rest_framework.views import APIView
from rest_framework.response import Response
from app.models import User


class UserRegister(APIView):
    def post(self, request):
        user_id = str(request.data.get('user_id'))
        user_name = str(request.data.get('user_name'))
        email = str(request.data.get('email'))
        password = int(request.data.get('password'))
        permission = str(request.data.get('permission'))
        print(request.data)
        try:
            s = User.objects.create(
                user_id=user_id,
                user_name=user_name,
                email=email,
                password=password,
                permission=permission,
            )
            s.save()
        except Exception as e:
            print(e)
            return Response(1)
        return Response(0)
