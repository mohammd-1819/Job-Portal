from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from portal.models.saved_jobs_model import SavedJob
from portal.models.job_seeker_profile_model import JobSeekerProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.saved_job_serializer import SavedJobSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from portal.utility.permissions import IsJobOwner
from portal.utility.pagination import Pagination


class AddSavedJobView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedJobSerializer

    @extend_schema(
        tags=['Saved Jobs'],
        summary='Save a job',
        responses={201: SavedJobSerializer}
    )
    def post(self, request):
        job_seeker = get_object_or_404(JobSeekerProfile.objects.select_related('user'), user=request.user)

        serializer = self.serializer_class(data=request.data, context={'job_seeker': job_seeker})
        serializer.is_valid(raise_exception=True)
        serializer.save(job_seeker=job_seeker)

        return Response({'message': 'Job Saved', 'result': serializer.data}, status=status.HTTP_201_CREATED)


class UserSavedJobListView(APIView, Pagination):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedJobSerializer

    @extend_schema(
        tags=['Saved Jobs'],
        summary='List of user saved jobs',
        responses={200: SavedJobSerializer}
    )
    def get(self, request):
        job_seeker = get_object_or_404(JobSeekerProfile.objects.select_related('user'), user=request.user)
        jobs = SavedJob.objects.filter(job_seeker=job_seeker)
        result = self.paginate_queryset(jobs, request)
        serializer = self.serializer_class(result, many=True)

        return self.get_paginated_response(serializer.data)


class RemoveSaveJobView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SavedJobSerializer

    @extend_schema(
        tags=['Saved Jobs'],
        summary='remove user saved job',

    )
    def delete(self, request, saved_job_id):
        job_seeker = get_object_or_404(JobSeekerProfile.objects.select_related('user'), user=request.user)
        job = get_object_or_404(SavedJob, id=saved_job_id, job_seeker=job_seeker)
        job.delete()

        return Response({'message': 'Saved Job Removed'}, status=status.HTTP_200_OK)
