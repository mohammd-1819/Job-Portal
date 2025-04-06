from django.shortcuts import get_object_or_404
from portal.models.job_application_model import JobApplication
from portal.models.job_owner_model import JobOwner
from portal.models.job_seeker_profile_model import JobSeekerProfile
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.job_application_serializer import JobApplicationSerializer
from portal.serializers.create_job_application_serializer import CreateJobApplicationSerializer
from portal.serializers.job_application_status_serializer import JobApplicationStatusSerializer
from rest_framework.permissions import IsAuthenticated
from portal.utility.permissions import IsJobOwner
from portal.utility.pagination import Pagination


class JobApplicationListView(APIView, Pagination):
    permission_classes = [IsJobOwner]
    serializer_class = JobApplicationSerializer

    @extend_schema(
        tags=['Job Applications'],
        summary='Job applications for a specific company',
        responses={200: JobApplicationSerializer}
    )
    def get(self, request):
        owner = get_object_or_404(JobOwner, user=request.user)
        applications = JobApplication.objects.select_related('job__company__owner').filter(job__company__owner=owner)
        result = self.paginate_queryset(applications, request)
        serializer = self.serializer_class(result, many=True)
        return self.get_paginated_response(serializer.data)


class JobApplicationDetailView(APIView):
    permission_classes = [IsJobOwner]
    serializer_class = JobApplicationSerializer

    @extend_schema(
        tags=['Job Applications'],
        summary='Details of a Job Application',
        responses={200: JobApplicationSerializer}
    )
    def get(self, request, application_id):
        try:
            application = JobApplication.objects.get(id=application_id)
        except JobApplication.DoesNotExist:
            return Response({'error': 'Application Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(instance=application)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateJobApplicationRequest(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateJobApplicationSerializer

    @extend_schema(
        tags=['Job Applications'],
        summary='Send a job application request',
        responses={201: CreateJobApplicationSerializer}
    )
    def post(self, request):
        job_seeker = get_object_or_404(JobSeekerProfile.objects.select_related('user'), user=request.user)

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request, 'job_seeker': job_seeker}
        )

        serializer.is_valid(raise_exception=True)
        serializer.save(applicant=job_seeker)

        return Response({
            'message': 'Application sent successfully',
            'result': serializer.data
        }, status=status.HTTP_201_CREATED)


class CancelApplicationRequest(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateJobApplicationSerializer

    @extend_schema(
        tags=['Job Applications'],
        summary='Cancel job application request'
    )
    def delete(self, request, application_id):
        applicant = get_object_or_404(JobSeekerProfile.objects.select_related('user'), user=request.user)
        try:
            application = JobApplication.objects.get(id=application_id, applicant=applicant)
        except JobApplication.DoesNotExist:
            return Response({'error': 'Application Not Found'}, status=status.HTTP_404_NOT_FOUND)

        application.delete()
        return Response({'message': 'Application Canceled'}, status=status.HTTP_200_OK)


class JobApplicationStatusView(APIView):
    permission_classes = [IsJobOwner]
    serializer_class = JobApplicationStatusSerializer

    @extend_schema(
        tags=['Job Applications'],
        summary='Change job application request status',
        responses={200: JobApplicationStatusSerializer}
    )
    def put(self, request, application_id):
        owner = get_object_or_404(JobOwner.objects.select_related('user'), user=request.user)

        application = get_object_or_404(
            JobApplication.objects.select_related('job__company__owner'),
            id=application_id,
            job__company__owner=owner
        )

        serializer = self.serializer_class(instance=application, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'message': 'Application status changed',
            'data': serializer.data
        }, status=status.HTTP_200_OK)
