from django.shortcuts import get_object_or_404
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from portal.models.job_model import Job
from portal.models.job_owner_model import JobOwner
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.job_serializer import JobSerializer
from portal.utility.pagination import Pagination
from rest_framework.permissions import IsAdminUser, AllowAny
from portal.utility.permissions import IsJobOwner


@extend_schema(
    tags=['Job'],
    summary='List of all jobs',
    responses={200: JobSerializer}
)
class JobListView(ListAPIView):
    permission_classes = [AllowAny]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    pagination_class = Pagination


@extend_schema(
    tags=['Job'],
    summary='Detail of a job',
    responses={200: JobSerializer}
)
class JobDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Job.objects.all()
    serializer_class = JobSerializer
    lookup_field = 'title'


class CreateJobView(APIView):
    permission_classes = [IsJobOwner]
    serializer_class = JobSerializer

    @extend_schema(
        tags=['Job'],
        summary='Add a new job',
        responses={201: JobSerializer}
    )
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Job Added', 'result': serializer.data}, status=status.HTTP_201_CREATED)


class UpdateJobView(APIView):
    permission_classes = [IsJobOwner]
    serializer_class = JobSerializer

    @extend_schema(
        tags=['Job'],
        summary='Update existing job',
        responses={200: JobSerializer}
    )
    def put(self, request, job_title):
        owner = get_object_or_404(JobOwner.objects.select_related('user'), user=request.user)
        job = get_object_or_404(Job, company__owner=owner, title=job_title)

        serializer = self.serializer_class(instance=job, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Job Updated', 'result': serializer.data}, status=status.HTTP_200_OK)


class RemoveJobView(APIView):
    permission_classes = [IsJobOwner]
    serializer_class = JobSerializer

    @extend_schema(
        tags=['Job'],
        summary='Remove job',
    )
    def delete(self, request, job_title):
        owner = get_object_or_404(JobOwner.objects.select_related('user'), user=request.user)
        job = get_object_or_404(Job, company__owner=owner, title=job_title)
        job.delete()

        return Response({'message': 'Job Removed'}, status=status.HTTP_200_OK)
