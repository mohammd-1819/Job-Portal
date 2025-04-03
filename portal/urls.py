from django.urls import path
from .views import job_category_view, company_view

app_name = 'portal'

urlpatterns = [
    path('job/category/all/', job_category_view.JobCategoryListView.as_view(), name='jov-category-list'),
    path('job/category/<str:name>/', job_category_view.JobCategoryDetailView.as_view(), name='jov-category-detail'),
    path('job/category/create', job_category_view.CreateJobCategoryView.as_view(), name='jov-category-create'),
    path('job/category/<str:name>/remove/', job_category_view.RemoveJobCategoryView.as_view(),
         name='jov-category-remove'),

    path('company/all', company_view.CompanyListView.as_view(), name='company-list'),
    path('company/add/', company_view.AddCompanyView.as_view(), name='company-add'),
    path('company/<str:company_name>/update/', company_view.UpdateCompanyView.as_view(), name='company-update'),
    path('company/<str:company_name>/remove/', company_view.RemoveCompanyView.as_view(), name='company-remove'),

]
