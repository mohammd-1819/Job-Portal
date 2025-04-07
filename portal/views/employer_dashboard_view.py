from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, CreateAPIView
from portal.models.job_model import Job
from portal.models.job_owner_model import JobOwner
from portal.models.job_application_model import JobApplication
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.job_serializer import JobSerializer
from portal.serializers.job_application_serializer import JobApplicationSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from portal.utility.permissions import IsJobOwner
from portal.utility.pagination import Pagination


class EmployerJobListView(APIView, Pagination):
    permission_classes = [IsJobOwner]
    serializer_class = JobSerializer

    @extend_schema(
        tags=['Employer Dashboard'],
        summary='List of jobs posted by an employer',
        responses={200: JobSerializer}

    )
    def get(self, request):
        owner = get_object_or_404(JobOwner.objects.select_related('user'), user=request.user)
        jobs = Job.objects.select_related('company', 'company__owner').filter(company__owner=owner)
        result = self.paginate_queryset(jobs, request)
        serializer = self.serializer_class(result, many=True)

        return self.get_paginated_response(serializer.data)


class EmployerJobApplicationRequestView(APIView, Pagination):
    permission_classes = [IsJobOwner]
    serializer_class = JobApplicationSerializer

    @extend_schema(
        tags=['Employer Dashboard'],
        summary='List of all job applications for employer jobs',
        responses={200: JobApplicationSerializer}
    )
    def get(self, request):
        owner = get_object_or_404(JobOwner.objects.select_related('user'), user=request.user)
        applications = JobApplication.objects.select_related('job', 'job__company', 'job__company__owner').filter(
            job__company__owner=owner)
        result = self.paginate_queryset(applications, request)
        serializer = self.serializer_class(result, many=True)

        return self.get_paginated_response(serializer.data)

