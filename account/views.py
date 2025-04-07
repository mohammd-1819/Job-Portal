from rest_framework import status
from .models import User
from .serializers import SignUpSerializer, LogoutSerializer, JobOwnerSignUpSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['email'] = user.email

        return token


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class SignUpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = SignUpSerializer

    @extend_schema(
        tags=['account'],
        summary='Sign up as a regular user',
        responses={200: SignUpSerializer},
        auth=[]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate tokens for the user
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                'message': 'Signup Successful',
                'access_token': str(access),
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class JobOwnerSignUpView(APIView):
    permission_classes = [AllowAny]
    serializer_class = JobOwnerSignUpSerializer

    @extend_schema(
        tags=['account'],
        summary='Sign up as a job owner',
        responses={200: JobOwnerSignUpSerializer},
        auth=[]
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate tokens for the user
            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            return Response({
                'message': 'Job Owner Signup Successful',
                'access_token': str(access),
                'refresh_token': str(refresh)
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        tags=['User'],
        summary='User Profile'
    )
    def get(self, request):
        user = request.user
        serializer = UserSerializer(instance=user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserDetailView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        tags=['User'],
        summary='User Details',

    )
    def get(self, request):
        try:
            serializer = UserSerializer(instance=request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": 'User Not Found'}, status=status.HTTP_404_NOT_FOUND)


class UpdateProfileView(APIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    @extend_schema(
        tags=['User'],
        summary='Update User Profile'
    )
    def put(self, request):
        user = request.user
        serializer = UserSerializer(instance=user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile Updated', 'result': serializer.data}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    @extend_schema(
        tags=['User'],
        summary='Logout user'
    )
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "message": "Successfully logged out."
            })
        except Exception as e:
            return Response({
                "error": "Invalid token or token not provided."
            }, status=status.HTTP_400_BAD_REQUEST)
