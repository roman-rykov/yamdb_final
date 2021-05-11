from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .permissions import IsAdministrator
from .serializer import EmailSerializer, UserSerializer


@api_view(['POST'])
def email(request):
    """Send confirmation_code by email."""
    email = request.POST['email']
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.get_or_create(
        username=email, email=email, is_active=False)[0]
    confirmation_code = default_token_generator.make_token(user)
    send_mail('Подтверждение регистрации',
              f'Пожалуйста, сохраните этот код : {confirmation_code},'
              ' он Вам понадобиться для получения токена',
              settings.EMAIL_ADDRESS,
              [email], fail_silently=False)
    return JsonResponse(serializer.validated_data)


@api_view(['POST'])
def get_token(request):
    """Generate access token."""
    email = request.POST['email']
    serializer = EmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    confirmation_code = request.POST['confirmation_code']
    user = get_object_or_404(User, email=email)
    if default_token_generator.check_token(user, confirmation_code):
        user.is_active = True
        user.save()
        token = AccessToken.for_user(user)
        return JsonResponse({'token': str(token)})
    return Response({"message": "confirmation_code или email не верны"},
                    status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]
    lookup_field = 'username'
    permission_classes = [IsAuthenticated, IsAdministrator]

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=[IsAuthenticated]
    )
    def me(self, request):
        user = User.objects.filter(username=request.user)[0]
        if request.method == 'GET':
            serializer = self.get_serializer(user)
            return Response(serializer.data)
        if request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data,
                            status=status.HTTP_200_OK)
