from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from portal.models.job_seeker_profile_model import JobSeekerProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.job_seeker_profile_serializer import JobSeekerProfileSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny


@extend_schema(
    tags=['Job Seeker'],
    summary='Job seeker Detail',
    responses={200: JobSeekerProfileSerializer}
)
class JobSeekerDetailView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = JobSeekerProfile.objects.all()
    serializer_class = JobSeekerProfileSerializer
    lookup_field = 'user__username'
    lookup_url_kwarg = 'username'


class CreateJobSeekerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSeekerProfileSerializer

    @extend_schema(
        tags=['Job Seeker'],
        summary='Create job seeker profile',
        responses={201: JobSeekerProfileSerializer}
    )
    def post(self, request):
        serializer = JobSeekerProfileSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response({'message': 'Job Seeker Profile Created', 'result': serializer.data},
                            status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UpdateJobSeekerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSeekerProfileSerializer

    @extend_schema(
        tags=['Job Seeker'],
        summary='Update existing job seeker profile',
        responses={200: JobSeekerProfileSerializer}

    )
    def put(self, request):
        profile = get_object_or_404(JobSeekerProfile, user=request.user)
        serializer = JobSeekerProfileSerializer(instance=profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile Updated', 'result': serializer.data}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveJobSeekerProfileView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = JobSeekerProfileSerializer

    @extend_schema(
        tags=['Job Seeker'],
        summary='Remove job seeker profile'
    )
    def delete(self, request):
        profile = get_object_or_404(JobSeekerProfile, user=request.user)
        profile.delete()
        return Response({'message': 'Profile Removed'}, status=status.HTTP_200_OK)
