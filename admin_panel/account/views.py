from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework import views
from rest_framework.permissions import IsAuthenticated 
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import *
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication


class SignUpView(GenericAPIView):
    # This view is for the creation of a new User account
    # It create the user according to its model User (unique username and email)
    # It create an account which needs to be validated by email (send mail
    # to confirm the user email)
    serializer_class = SignUpSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(request)
        
        return Response("data save", status="200")
     
    
class LoginView(views.APIView):
    
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True) 
        
        user = serializer.validated_data['user']
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        return Response({'error': 'Invalid credentials'}, status=400)
        # serialized_user = self.serializer_class(user).data
        # return Response({'token': serialized_user})
    

class AllUsers(views.APIView):
    # authentication_classes=[JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    def get(self, request): 
        users = User.objects.all()
        serialized_user = UserSerializer(users , many=True).data  # Assuming you have a serializer for your user model
        return Response(serialized_user)
