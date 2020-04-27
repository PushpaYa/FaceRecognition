from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('student/<slug:stud_id>/attendance/', views.attendance, name='attendance'),
    path('student/<slug:stud_id>/<slug:course_id>/attendance/', views.attendance_detail, name='attendance_detail'),
    path('teacher/<slug:teacher_id>/<int:choice>/Classes/', views.t_clas, name='t_clas'),
    path('teacher/<int:assign_id>/Students/attendance/', views.t_student, name='t_student'),
    path('teacher/<int:assign_id>/ClassDates/', views.t_class_date, name='t_class_date'),
    path('teacher/<int:ass_c_id>/Cancel/', views.cancel_class, name='cancel_class'),
    path('teacher/<int:ass_c_id>/attendance/', views.t_attendance, name='t_attendance'),
    path('teacher/<int:pk>/attendance/upload/', views.AttendanceClassUpdateView.as_view(), name='att_upload'),
    path('teacher/<int:ass_c_id>/attendance/auto', views.t_attendance_auto, name='t_attendance_auto'),
    path('teacher/<int:ass_c_id>/Edit_att/', views.edit_att, name='edit_att'),
    path('teacher/<int:ass_c_id>/attendance/confirm/', views.confirm, name='confirm'),
    path('teacher/<slug:stud_id>/<slug:course_id>/attendance/', views.t_attendance_detail, name='t_attendance_detail'),
    path('teacher/<int:att_id>/change_attendance/', views.change_att, name='change_att'),
    path('teacher/<int:assign_id>/Report/', views.t_report, name='t_report')
]