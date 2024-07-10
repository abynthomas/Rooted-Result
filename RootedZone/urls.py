"""
URL configuration for RootedZone project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from root import views
from django.conf.urls.static import static
from django.conf import settings
from root.views import custom_404_view

urlpatterns = [
    path('Admin@ROOTEd.DrishtiNews/', admin.site.urls),

    path('', views.login, name='login'),

    path('logout/', views.logout, name='logout'),

    # < * * * * * * * * * * * * * * * * * * * * ADMIN * * * * * * * * * * * * * * * * * * * * >

    path('password/', views.admin_password, name='password'),

    path('admin_home/', views.admin_home, name='admin_home'),

    path('delete/<int:excel_data_id>/', views.delete_excel_data, name='delete_excel_data'),

    path('admin_profile/', views.admin_profile, name='admin_profile'),

    path('student-activity/', views.student_activity, name='student_activity'),

    path('delete_user_login_activity/', views.delete_user_login_activity, name='delete_user_login_activity'),

    path('add_solution/', views.add_solution, name='add_solution'),

    path('delete_solution/<int:solution_id>/', views.delete_solution, name='delete_solution'),

    path('add_study_plan/', views.add_study_plan, name='add_study_plan'),

    path('study_plan/<int:plan_id>/', views.delete_study_plan, name='delete_study_plan'),

    path('add_current_affairs/', views.add_current_affairs, name='add_current_affairs'),

    path('current_affairs_delete/<int:item_id>/', views.current_affairs_delete, name='current_affairs_delete'),

    path('admin_analysis/', views.admin_analysis, name='admin_analysis'),


    # < * * * * * * * * * * * * * * * * * * * * USER * * * * * * * * * * * * * * * * * * * * >

    path('profile/', views.user_profile, name='profile'),

    path('self_analysis/', views.user_self_analysis, name='self_analysis'),

    path('progress_report/', views.user_progress_report, name='progress_report'),

    path('sectional_chart/', views.user_sectional_chart, name='sectional_chart'),

    path('current_affairs/', views.user_current_affairs, name='current_affairs'),

    path('view_result/<int:mock_test_id>/', views.user_view_result, name='view_result'),

    path('ai_analysis/<int:mock_test_id>/', views.user_ai_analysis, name='ai_analysis'),

    path('download-solution/<int:mock_test_id>/', views.download_mock_test_solution, name='download_solution'),

    path('study_plan/', views.user_study_plan, name='study_plan'),

]

handler404 = custom_404_view

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

