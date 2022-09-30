from django.contrib import admin
from .models import *

admin.site.register([Payment, LanguageCourse, Receptionist, Student, Teacher, University, Lead, StudyMaterials,
                     Admin, Consultant, Course, Visitor, Task, Country, Document, Appointment, Feed, Comment, Message, Qualification])
