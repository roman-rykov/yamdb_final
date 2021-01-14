from rest_framework_simplejwt.serializers import User
from rest_framework.decorators import api_view
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets
from .serializer import UserSerializer
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import filters
from .permissions import IsAdministrator, IsModerator, IsUser
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser

User = get_user_model()

@api_view(['POST'])
def email(requests):
    email = requests.POST['email']
    user = User.objects.get_or_create(username=email, email=email)[0]
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Подтверждение регистрации', f'Пожалуйста, сохраните этот код : {confirmation_code},'
     ' он Вам понадобиться для получения токена', 'ArtembBogatov@yandex.ru',
    [email], fail_silently=False)
    return JsonResponse({'email':email})  

@api_view(['POST'])
def get_token(request):
    email = request.POST['email']
    confirmation_code = request.POST['confirmation_code']
    user = User.objects.filter(email=email)[0]
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return JsonResponse({'token':str(token)})
    return Response(status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username',] 
    lookup_field = 'username'
    permission_classes = [IsAdministrator,]
    

@permission_classes(IsAuthenticated,)
@api_view(['GET', 'PATCH'])
def get_info_me(requests):
    if not requests.user.is_anonymous:
        user = User.objects.filter(username=requests.user)[0]
        if requests.method == 'GET':
            serializer = UserSerializer(user)
            return Response(serializer.data)
        if requests.method == 'PATCH':
            serializer = UserSerializer(user, data=requests.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(status=status.HTTP_401_UNAUTHORIZED)
