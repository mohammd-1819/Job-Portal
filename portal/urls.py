from django.urls import path
from .views import job_category_view

app_name = 'portal'

urlpatterns = [
    path('job/category/all/', job_category_view.JobCategoryListView.as_view(), name='jov-category-list'),
    path('job/category/<str:name>/', job_category_view.JobCategoryDetailView.as_view(), name='jov-category-detail'),
    path('job/category/create', job_category_view.CreateJobCategoryView.as_view(), name='jov-category-create'),
    path('job/category/<str:name>/remove/', job_category_view.RemoveJobCategoryView.as_view(),
         name='jov-category-remove')
]
