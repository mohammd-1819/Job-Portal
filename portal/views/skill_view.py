from django.core.cache import cache
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView
from portal.models.skill_model import Skill
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from portal.serializers.skill_serializer import SkillSerializer
from ..utility.pagination import Pagination
from rest_framework.permissions import IsAdminUser, AllowAny


@extend_schema(
    tags=['Skill'],
    summary='List of all skills',
    responses={200: SkillSerializer(many=True)},
    auth=[]
)
class SkillListView(ListAPIView):
    permission_classes = [AllowAny]
    serializer_class = SkillSerializer
    pagination_class = Pagination

    def get(self, request, *args, **kwargs):
        page = request.GET.get("page", 1)
        cache_key = f'skill_list_page_{page}'

        cached_data = cache.get(cache_key)
        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        queryset = self.get_queryset()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request, view=self)
        serializer = self.get_serializer(result_page, many=True)

        paginated_response = paginator.get_paginated_response(serializer.data)

        cache.set(cache_key, paginated_response.data, 60 * 15)

        return paginated_response

    def get_queryset(self):
        return Skill.objects.all()


@extend_schema(
    tags=['Skill'],
    summary='Detail of a skills',
    responses={200: SkillSerializer},
    auth=[]
)
class SkillDetailView(RetrieveAPIView):
    permission_classes = [AllowAny]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = 'name'


class AddSkillView(APIView):
    permission_classes = [IsAdminUser]
    serializer_class = SkillSerializer

    @extend_schema(
        tags=['Skill'],
        summary='Add new Skill',
        responses={201: SkillSerializer}
    )
    def post(self, request):
        serializer = SkillSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({'message': 'Skill Added', 'result': serializer.data}, status=status.HTTP_201_CREATED)


@extend_schema(
    tags=['Skill'],
    summary='Remove Skill'
)
class RemoveSkillView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer
    lookup_field = 'name'
