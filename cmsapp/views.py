from django.shortcuts import render, redirect
from django.views.generic import *
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from .models import *
from .forms import *
from django.http import JsonResponse
import json as simplejson
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
# Create your views here.

# backend ko dai haru ko lagi

# class AjaxableResponseMixin(object):
#     def form_valid(self, form):
#         response = super().form_valid(form)
#         if self.request.is_ajax():
#             data = {
#                 'id': self.object.id,
#             }
#             return JsonResponse(data)
#         else:
#             return response


class AdminMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        else:
            user_group = []
            for group in request.user.groups.all():
                user_group.append(group.name)
            if user_group != ['Admin']:
                return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        return super(AdminMixin, self).dispatch(request, *args, **kwargs)


class ReceptionistMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        else:
            user_group = []
            for group in request.user.groups.all():
                user_group.append(group.name)
                print(user_group)
            if user_group != ['Receptionist']:
                return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        return super(ReceptionistMixin, self).dispatch(request, *args, **kwargs)


class ConsultantMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        else:
            user_group = []
            for group in request.user.groups.all():
                user_group.append(group.name)
            if user_group != ['Consultant']:
                return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        return super(ConsultantMixin, self).dispatch(request, *args, **kwargs)


class TeacherMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        else:
            user_group = []
            for group in request.user.groups.all():
                user_group.append(group.name)
            if user_group != ['Teacher']:
                return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        return super(TeacherMixin, self).dispatch(request, *args, **kwargs)


class LeadMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        else:
            user_group = []
            for group in request.user.groups.all():
                user_group.append(group.name)
            if user_group != ['Lead']:
                return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        return super(LeadMixin, self).dispatch(request, *args, **kwargs)


class StudentMixin(object):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        else:
            user_group = []
            for group in request.user.groups.all():
                user_group.append(group.name)
            if user_group != ['Student']:
                return HttpResponseRedirect(reverse_lazy('cmsapp:login'))
        return super(StudentMixin, self).dispatch(request, *args, **kwargs)


class BaseMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasklist'] = Task.objects.filter(
            assigned_to=self.request.user)
        context['receivedlist'] = Message.objects.filter(
            receiver=self.request.user)
        context['sentlist'] = Message.objects.filter(
            sender=self.request.user)
        context['feedlist'] = Feed.objects.all()
        context['feedform'] = FeedForm
        context['commentform'] = CommentForm
        # context['formset'] = DocumentFormSet
        return context


class ReceptionistRegistrationView(AdminMixin, CreateView):
    template_name = 'receptionisttemplates/receptionistcreate.html'
    form_class = ReceptionistRegistrationForm
    success_url = reverse_lazy('cmsapp:adminpanel')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(username, "", password)
        group = Group.objects.get(name="Receptionist")
        group.user_set.add(user)
        form.instance.user = user
        return super().form_valid(form)


class StudentRegistrationView(ReceptionistMixin, CreateView):
    template_name = 'studenttemplates/studentcreate.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('cmsapp:receptionistpanel')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(username, "", password)
        group = Group.objects.get(name="Student")
        group.user_set.add(user)
        form.instance.user = user
        return super().form_valid(form)


class TeacherRegistrationView(ReceptionistMixin, CreateView):
    template_name = 'teachertemplates/teachercreate.html'
    form_class = TeacherRegistrationForm
    success_url = reverse_lazy('cmsapp:receptionistpanel')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(username, "", password)
        group = Group.objects.get(name="Teacher")
        group.user_set.add(user)
        form.instance.user = user
        return super().form_valid(form)


class ConsultantRegistrationView(AdminMixin, CreateView):
    template_name = 'consultanttemplates/consultantcreate.html'
    form_class = ConsultantRegistrationForm
    success_url = reverse_lazy('cmsapp:adminconsultantlist')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(username, "", password)
        group = Group.objects.get(name="Consultant")
        group.user_set.add(user)
        form.instance.user = user
        return super().form_valid(form)


class ConsultantUpdateView(AdminMixin, UpdateView):
    template_name = 'consultanttemplates/consultantcreate.html'
    form_class = ConsultantRegistrationForm
    success_url = reverse_lazy('cmsapp:adminconsultantlist')
    model = Consultant
    success_message = "Consultant updated succesfully"


class LeadRegistrationView(ConsultantMixin, CreateView):

    template_name = 'leadtemplates/leadcreate.html'
    form_class = LeadRegistrationForm
    success_url = reverse_lazy('cmsapp:receptionistpanel')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(username, "", password)
        group = Group.objects.get(name="Lead")
        group.user_set.add(user)
        form.instance.user = user
        # lead = form.save()
        # documents = self.request.FILES.getlist('documents')
        # for f in documents:
        #     document = Document.objects.create(
        #         title='hello', file=f, lead=lead)
        return super().form_valid(form)


class LeadUpdateView(UpdateView):
    template_name = 'leadtemplates/leadupdate.html'
    model = Lead
    form_class = LeadUpdateForm
    success_url = reverse_lazy("cmsapp:leadlist")
    success_message = "Lead updated succesfully"


class AjaxLeadCourseSelectView(View):
    # def post(self, request, **kwargs):
    #     return
    def get(self, request):
        pk = request.GET.get("id")
        course = Course.objects.get(id=pk)
        university = University.objects.filter(course=course)
        print(university)
        print(pk, "hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh")
        return render()


class VisitorRegistrationView(ReceptionistMixin, CreateView):
    template_name = 'visitortemplates/visitorcreate.html'
    form_class = VisitorRegistrationForm
    success_url = reverse_lazy('cmsapp:receptionistpanel')


class AdminRegistrationView(AdminMixin, CreateView):
    template_name = 'admintemplates/admincreate.html'
    form_class = AdminRegistrationForm
    success_url = reverse_lazy('cmsapp:adminpanel')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(username, "", password)
        group = Group.objects.get(name="Admin")
        group.user_set.add(user)
        form.instance.user = user

        return super().form_valid(form)


class AdminUpdateView(AdminMixin, UpdateView):
    template_name = 'admintemplates/admincreate.html'
    model = Admin
    form_class = AdminRegistrationForm
    success_url = reverse_lazy("cmsapp:adminlist")
    success_message = "Admin updated succesfully"


class LoginView(FormView):
    template_name = 'login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(self.request, user)
            if Receptionist.objects.filter(user=user).exists():
                return HttpResponseRedirect(reverse_lazy('cmsapp:receptionistpanel'))
            elif Admin.objects.filter(user=user).exists():
                return HttpResponseRedirect(reverse_lazy('cmsapp:adminpanel'))
            elif Teacher.objects.filter(user=user).exists():
                return HttpResponseRedirect(reverse_lazy('cmsapp:teacherpanel'))
            elif Consultant.objects.filter(user=user).exists():
                return HttpResponseRedirect(reverse_lazy('cmsapp:consultantpanel'))
            elif Lead.objects.filter(user=user).exists():
                return HttpResponseRedirect(reverse_lazy('cmsapp:leadpanel'))
            elif Student.objects.filter(user=user).exists():
                return HttpResponseRedirect(reverse_lazy('cmsapp:studentpanel'))
            return HttpResponseRedirect(reverse_lazy('cmsapp:studentpanel'))
        else:
            return render(self.request, self.template_name, {
                'form': form,
                'errors': "Please correct username or password "
            })
        return super().form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('cmsapp:login')


# Receptionist panel content


class ReceptionistPanelView(ReceptionistMixin, TemplateView):
    template_name = 'receptionisttemplates/receptionistbase.html'


class ReceptionistListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptionistlist.html'
    model = Consultant
    context_object_name = 'receptionistlist'


class ReceptionistLeadListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptionistleadlist.html'
    model = Lead
    context_object_name = 'receptionistleadlist'


class ReceptionistTeacherListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptionistteacherlist.html'
    model = Teacher
    context_object_name = 'receptionistteacherlist'


class ReceptionistConsultantListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptionistconsultantlist.html'
    model = Consultant
    context_object_name = 'receptionistconsultantlist'


class ReceptionistStudentListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptioniststudentlist.html'
    model = Student
    context_object_name = 'receptioniststudentlist'


class ReceptionistVisitorListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptionistvisitorlist.html'
    model = Visitor
    context_object_name = 'receptionistvisitorlist'


class ReceptionistTaskListView(ReceptionistMixin, BaseMixin, ListView):
    template_name = 'receptionisttemplates/receptionisttasklist.html'
    model = Task
    context_object_name = 'tasklist'


class ReceptionistAppointmentListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptionistappointmentlist.html'
    model = Appointment
    context_object_name = 'receptionistappointmentlist'


class ReceptionistUniversityListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptionistuniversitylist.html'
    model = University
    context_object_name = 'receptionistuniversitylist'


class ReceptionistLanguage_courseListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptionistlanguage_courselist.html'
    model = LanguageCourse
    context_object_name = 'receptionistlanguage_courselist'


class ReceptionistCourseListView(ReceptionistMixin, ListView):
    template_name = 'receptionisttemplates/receptionistcourselist.html'
    model = Course
    context_object_name = 'receptionistcourselist'

    # Receptionist panel detail views


class ReceptionistConsultantDetailView(ReceptionistMixin, DetailView):
    template_name = 'receptionisttemplates/receptionistconsultantdetail.html'
    model = Consultant
    context_object_name = 'receptionistconsultantdetail'


class ReceptionistDetailView(ReceptionistMixin, DetailView):
    template_name = 'receptionisttemplates/receptionistdetail.html'
    model = Receptionist
    context_object_name = 'receptionistdetail'


class ReceptionistStudentDetailView(ReceptionistMixin, DetailView):
    template_name = 'receptionisttemplates/receptioniststudentdetail.html'
    model = Student
    context_object_name = 'receptioniststudentdetail'


class ReceptionistLeadDetailView(ReceptionistMixin, DetailView):
    template_name = 'receptionisttemplates/receptionistleaddetail.html'
    model = Lead
    context_object_name = 'receptionistleaddetail'


class ReceptionistTeacherDetailView(ReceptionistMixin, DetailView):
    template_name = 'receptionisttemplates/receptionistteacherdetail.html'
    model = Teacher
    context_object_name = 'receptionistteacherdetail'


class ReceptionistVisitorDetailView(ReceptionistMixin, DetailView):
    template_name = 'receptionisttemplates/receptionistvisitordetail.html'
    model = Visitor
    context_object_name = 'receptionistvisitordetail'


class ReceptionistCourseDetailView(ReceptionistMixin, DetailView):
    template_name = 'receptionisttemplates/receptionistcoursedetail.html'
    model = Course
    context_object_name = 'receptionistcoursedetail'

# Receptionist panel create views

class ReceptionistCourseCreateView(CreateView, ReceptionistMixin):
    template_name = 'receptionisttemplates/receptionistcoursecreate.html'
    form_class = CourseForm
    success_url = reverse_lazy('cmsapp:receptionistpanel')

# Receptionist panel update views

class ReceptionistCourseUpdateView(UpdateView, ReceptionistMixin):
    template_name = 'receptionisttemplates/receptionistcoursecreate.html'
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy("cmsapp:receptionistcourselist")
    success_message = "Course updated succesfully"

# Receptionist panel delete views

class ReceptionistCourseDeleteView(DeleteView, ReceptionistMixin):
    template_name = 'receptionisttemplates/receptionistcoursedelete.html'
    model = Course
    success_url = reverse_lazy('cmsapp:receptionistcourselist')
    success_message = "Course  deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ReceptionistCourseDeleteView, self).delete(request, *args, **kwargs)


# Student Panel content


class StudentPanelView(StudentMixin, TemplateView):
    template_name = 'studenttemplates/studentbase.html'


class StudentTeacherListView(StudentMixin, ListView):
    template_name = 'studenttemplates/studentteacherlist.html'
    model = Consultant
    context_object_name = 'studentteacherlist'


class StudentReceptionistListView(StudentMixin, ListView):
    template_name = 'studenttemplates/studentreceptionistlist.html'
    model = Receptionist
    context_object_name = 'studentreceptionistlist'

    # Student panel detail views


class StudentDetailView(StudentMixin, DetailView):
    template_name = 'studenttemplates/studentdetail.html'
    model = Student
    context_object_name = 'studentdetail'

    # Lead panel content


class LeadPanelView(LeadMixin, TemplateView):
    template_name = 'leadtemplates/leadbase.html'


class LeadConsultantListView(LeadMixin, ListView):
    template_name = 'leadtemplates/leadconsultantlist.html'
    model = Consultant
    context_object_name = 'leadconsultantlist'


class LeadReceptionistListView(LeadMixin, ListView):
    template_name = 'leadtemplates/leadreceptionistlist.html'
    model = Receptionist
    context_object_name = 'leadreceptionistlist'


class LeadDocumentListView(LeadMixin, ListView):
    template_name = 'leadtemplates/leaddocumentlist.html'
    model = Document
    context_object_name = 'leaddocumentlist'

    # lead panel detail views


class LeadDetailView(LeadMixin, DetailView):
    template_name = 'leadtemplates/leaddetail.html'
    model = Lead
    context_object_name = 'leaddetail'

    # Visitor Panel content


class VisitorPanelView(TemplateView):
    template_name = 'visitortemplates/visitorpanel.html'

# Teacher Panel content


class TeacherPanelView(TeacherMixin, TemplateView):
    template_name = 'teachertemplates/teacherbase.html'


class TeacherListView(TeacherMixin, ListView):
    template_name = 'teachertemplates/teacherlist.html'
    model = Teacher
    context_object_name = 'teacherlist'


class TeacherConsultantListView(TeacherMixin, ListView):
    template_name = 'teachertemplates/teacherconsultantlist.html'
    model = Consultant
    context_object_name = 'teacherconsultantlist'


class TeacherReceptionistListView(TeacherMixin, ListView):
    template_name = 'teachertemplates/teacherreceptionistlist.html'
    model = Receptionist
    context_object_name = 'teacherreceptionistlist'


class TeacherStudentListView(TeacherMixin, ListView):
    template_name = 'teachertemplates/teacherstudentlist.html'
    model = Student
    context_object_name = 'teacherstudentlist'


class TeacherTaskListView(TeacherMixin, BaseMixin, ListView):
    template_name = 'teachertemplates/teachertasklist.html'
    model = Task
    context_object_name = 'teachertasklist'


class TeacherUniversityListView(TeacherMixin, BaseMixin, ListView):
    template_name = 'teachertemplates/teacheruniversitylist.html'
    model = University
    context_object_name = 'teacheruniversitylist'


# teacherpanel detail views


class TeacherDetailView(TeacherMixin, DetailView):
    template_name = 'teachertemplates/teacherdetail.html'
    model = Teacher
    context_object_name = 'teacherdetail'


class TeacherStudentDetailView(TeacherMixin, DetailView):
    template_name = 'teachertemplates/teacherstudentdetail.html'
    model = Teacher
    context_object_name = 'teacherstudentdetail'

class TeacherStudyMaterialsListView(ListView):
    template_name = 'teachertemplates/teacherstudymaterialslist.html'
    model = StudyMaterials
    context_object_name = 'teacherstudymaterialslist'



# teacherpanel create views

class TeacherStudyMaterialsCreateView(FormView):
    template_name = 'teachertemplates/teacherstudymaterialscreate.html'
    form_class = TeacherStudyMaterialsForm
    success_url = reverse_lazy('cmsapp:teacherpanel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = StudyMaterialsFormset(
            queryset=StudyMaterials.objects.none())
        return context

    def form_valid(self, form):
        studymaterialsformset =StudyMaterialsFormset(self.request.POST, self.request.FILES).save()
        language_course = form.cleaned_data['language_course']
        for studymaterials in studymaterialsformset:
            studymaterials.language_course = language_course
            studymaterials.save()
            print(studymaterials)

        return super().form_valid(form)

# teacherpanel update views
class TeacherStudyMaterialsUpdateView(UpdateView, TeacherMixin):
    template_name = 'teachertemplates/teacherstudymaterialscreate.html'
    model = StudyMaterials
    form_class = StudyMaterialsForm
    success_url = reverse_lazy("cmsapp:teacherstudymaterialslist")
    success_message = "Study Materials updated succesfully"



# teacherpanel delete views
class TeacherStudyMaterialsDeleteView(DeleteView):
    template_name = 'teachertemplates/teacherstudymaterialsdelete.html'
    model = StudyMaterials
    success_url = reverse_lazy('cmsapp:teacherstudymaterialslist')
    success_message = "Study Materials deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TeacherStudyMaterialsDeleteView, self).delete(request, *args, **kwargs)




# consultant panel content


class ConsultantPanelView(ConsultantMixin, TemplateView):
    template_name = 'consultanttemplates/consultantbase.html'

 # consultant list views


class ConsultantListView(ConsultantMixin, ListView):
    template_name = 'consultanttemplates/consultantlist.html'
    model = Consultant
    context_object_name = 'consultantlist'


class ConsultantLeadListView(ConsultantMixin, ListView):
    template_name = 'consultanttemplates/consultantleadlist.html'
    model = Lead
    context_object_name = 'consultantleadlist'


class ConsultantTeacherListView(ConsultantMixin, ListView):
    template_name = 'consultanttemplates/consultantteacherlist.html'
    model = Teacher
    context_object_name = 'consultantteacherlist'


class ConsultantReceptionistListView(ConsultantMixin, ListView):
    template_name = 'consultanttemplates/consultantreceptionistlist.html'
    model = Receptionist
    context_object_name = 'consultantreceptionistlist'


class ConsultantStudentListView(ConsultantMixin, ListView):
    template_name = 'consultanttemplates/consultantstudentlist.html'
    model = Student
    context_object_name = 'consultantstudentlist'


class ConsultantVisitorListView(ConsultantMixin, ListView):
    template_name = 'consultanttemplates/consultantvisitorlist.html'
    model = Visitor
    context_object_name = 'consultantvisitorlist'


class ConsultantTaskListView(ConsultantMixin, BaseMixin, ListView):
    template_name = 'consultanttemplates/consultanttasklist.html'
    model = Task
    context_object_name = 'tasklist'


class ConsultantAppointmentListView(ConsultantMixin, ListView):
    template_name = 'consultanttemplates/consultantappointmentlist.html'
    model = Appointment
    context_object_name = 'consultantappointmentlist'


# consultant create views
class ConsultantDocumentCreateView(FormView):
    template_name = 'consultanttemplates/consultantdocumentcreate.html'
    form_class = LeadDocumentForm
    success_url = reverse_lazy('cmsapp:consultantpanel')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['formset'] = DocumentFormset(
            queryset=Document.objects.none())
        return context

    def form_valid(self, form):
        documentformset = DocumentFormset(self.request.POST, self.request.FILES).save()
        lead = form.cleaned_data['lead']
        for document in documentformset:
            document.lead = lead
            document.save()

        return super().form_valid(form)


class ConsultantTaskCreateView(CreateView, BaseMixin):
    template_name = 'consultanttemplates/consultanttaskcreate.html'
    form_class = TaskForm
    success_url = reverse_lazy('cmsapp:consultantlist')


class ConsultantAppointmentCreateView(CreateView, BaseMixin):
    template_name = 'consultanttemplates/consultantappointmentcreate.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('cmsapp:consultantlist')


# consultant update views
class ConsultantTaskUpdateView(UpdateView):
    template_name = 'consultanttemplates/consultanttaskcreate.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("cmsapp:consultanttasklist")
    success_message = "Task updated succesfully"


class ConsultantAppointmentUpdateView(UpdateView):
    template_name = 'consultanttemplates/consultantappointmentcreate.html'
    model = Lead
    form_class = AppointmentForm
    success_url = reverse_lazy("cmsapp:consultantappointmentlist")
    success_message = "Appointment updated succesfully"

class ConsultantLeadUpdateView(UpdateView):
    template_name = 'consultanttemplates/consultantleadupdate.html'
    model = Lead
    form_class = LeadUpdateForm
    success_url = reverse_lazy("cmsapp:consultantpanel")
    success_message = "Lead updated succesfully"


# consultant delete views


class ConsultantTaskDeleteView(DeleteView):
    template_name = 'consultanttemplates/consultanttaskdelete.html'
    model = Task
    success_url = reverse_lazy('cmsapp:consultanttasklist')
    success_message = "Task  deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ConsultantTaskDeleteView, self).delete(request, *args, **kwargs)


class ConsultantAppointmentDeleteView(DeleteView):
    template_name = 'consultanttemplates/consultantappointmentdelete.html'
    model = Appointment
    success_url = reverse_lazy('cmsapp:consultantappointmentlist')
    success_message = "Appointment deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(ConsultantAppointmentDeleteView, self).delete(request, *args, **kwargs)


# cosultant panel detail views


class ConsultantDetailView(ConsultantMixin, DetailView):
    template_name = 'consultanttemplates/consultantdetail.html'
    model = Consultant
    context_object_name = 'consultantdetail'


class ConsultantVisitorDetailView(ConsultantMixin, DetailView):
    template_name = 'consultanttemplates/consultantvisitordetail.html'
    model = Visitor
    context_object_name = 'consultantvisitordetail'


class ConsultantStudentDetailView(ConsultantMixin, DetailView):
    template_name = 'consultanttemplates/consultantstudentdetail.html'
    model = Student
    context_object_name = 'consultantstudentdetail'


class ConsultantLeadDetailView(ConsultantMixin, DetailView):
    template_name = 'consultanttemplates/consultantleaddetail.html'
    model = Lead
    context_object_name = 'consultantleaddetail'


# admin panel content

class AdminPanelView(AdminMixin, TemplateView):
    template_name = 'admintemplates/adminbase.html'


class AdminConsultantListView(AdminMixin, ListView):
    template_name = 'admintemplates/adminconsultantlist.html'
    model = Consultant
    context_object_name = 'adminconsultantlist'


class AdminLeadListView(AdminMixin, ListView):
    template_name = 'admintemplates/adminleadlist.html'
    model = Lead
    context_object_name = 'adminleadlist'


class AdminTeacherListView(AdminMixin, ListView):
    template_name = 'admintemplates/adminteacherlist.html'
    model = Teacher
    context_object_name = 'adminteacherlist'


class AdminReceptionistListView(AdminMixin, ListView):
    template_name = 'admintemplates/adminreceptionistlist.html'
    model = Receptionist
    context_object_name = 'adminreceptionistlist'


class AdminStudentListView(AdminMixin, ListView):
    template_name = 'admintemplates/adminstudentlist.html'
    model = Student
    context_object_name = 'adminstudentlist'


class AdminVisitorListView(AdminMixin, ListView):
    template_name = 'admintemplates/adminvisitorlist.html'
    model = Visitor
    context_object_name = 'adminvisitorlist'


class AdminTaskListView(AdminMixin, BaseMixin, ListView):
    template_name = 'admintemplates/admintasklist.html'
    model = Task
    context_object_name = 'tasklist'


class AdminAppointmentListView(AdminMixin, ListView):
    template_name = 'admintemplates/adminappointmentlist.html'
    model = Appointment
    context_object_name = 'adminappointmentlist'


# admin panel create views
class AdminTeacherRegistrationView(CreateView):
    template_name = 'admintemplates/adminteachercreate.html'
    form_class = TeacherRegistrationForm
    success_url = reverse_lazy('cmsapp:adminteacherlist')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(username, "", password)
        group = Group.objects.get(name="Teacher")
        group.user_set.add(user)
        form.instance.user = user
        return super().form_valid(form)


class AdminReceptionistRegistrationView(CreateView):
    template_name = 'admintemplates/adminreceptionistcreate.html'
    form_class = ReceptionistRegistrationForm
    success_url = reverse_lazy('cmsapp:adminreceptionistlist')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(username, "", password)
        group = Group.objects.get(name="Receptionist")
        group.user_set.add(user)
        form.instance.user = user
        return super().form_valid(form)


class AdminStudentRegistrationView(AdminMixin, CreateView):
    template_name = 'admintemplates/adminstudentcreate.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('cmsapp:adminstudentlist')

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password2']
        user = User.objects.create_user(username, "", password)
        group = Group.objects.get(name="Student")
        group.user_set.add(user)
        form.instance.user = user
        return super().form_valid(form)


class AdminTaskCreateView(AdminMixin, CreateView):
    template_name = 'admintemplates/admintaskcreate.html'
    form_class = TaskForm
    success_url = reverse_lazy("cmsapp:admintasklist")

    def form_valid(self, form):
        return super().form_valid(form)


# admin panel detail views
class AdminDetailView(AdminMixin, DetailView):
    template_name = 'admintemplates/admindetail.html'
    model = Admin
    context_object_name = 'admindetail'


class AdminConsultantDetailView(AdminMixin, DetailView):
    template_name = 'admintemplates/adminconsultantdetail.html'
    model = Consultant
    context_object_name = 'adminconsultantdetail'


class AdminReceptionistDetailView(AdminMixin, DetailView):
    template_name = 'admintemplates/adminreceptionistdetail.html'
    model = Receptionist
    context_object_name = 'adminreceptionistdetail'


class AdminStudentDetailView(AdminMixin, DetailView):
    template_name = 'admintemplates/adminstudentdetail.html'
    model = Student
    context_object_name = 'adminstudentdetail'


class AdminLeadDetailView(AdminMixin, DetailView):
    template_name = 'admintemplates/adminleaddetail.html'
    model = Lead
    context_object_name = 'adminleaddetail'


class AdminTeacherDetailView(AdminMixin, DetailView):
    template_name = 'admintemplates/adminteacherdetail.html'
    model = Teacher
    context_object_name = 'adminteacherdetail'


# Admin feed views 


class AdminFeedCreateView(BaseMixin, CreateView):
    template_name = 'admintemplates/adminfeedlist.html'
    form_class = FeedForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.created_by = user
        self.feed_id = form.save().id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cmsapp:adminfeedlist")


class AdminFeedListView(BaseMixin, generic.ListView):
    template_name = 'admintemplates/adminfeedlist.html'
    queryset = Feed.objects.all().order_by('-id')
    # model = Feed
    context_object_name = 'feedlist'


class AdminFeedDeleteView(DeleteView):
    template_name = 'admintemplates/adminfeedlist.html'
    model = Feed
    success_url = '/adminfeed/list/'


class AdminFeedCommentCreateView(BaseMixin, CreateView):
    template_name = 'admintemplates/adminfeedlist.html'
    form_class = CommentForm
    success_url = '/adminfeed/list/'

    def form_valid(self, form):
        feed_id = self.kwargs['pk']
        feed = Feed.objects.get(id=feed_id)
        form.instance.post = feed
        form.instance.comment_by = self.request.user

        return super().form_valid(form)


class AdminFeedCommentDeleteView(DeleteView):
    template_name = 'admintemplates/adminfeedlist.html'
    model = Feed
    success_url = '/adminfeed/list/'



# consultant feed views 


class ConsultantFeedCreateView(BaseMixin, CreateView):
    template_name = 'consultanttemplates/consultantfeedlist.html'
    form_class = FeedForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.feed_by = user
        self.feed_id = form.save().id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cmsapp:consultantfeedlist")


class ConsultantFeedListView(BaseMixin, generic.ListView):
    template_name = 'consultanttemplates/consultantfeedlist.html'
    model = Feed
    context_object_name = 'feedlist'


class ConsultantFeedDeleteView(DeleteView):
    template_name = 'consultanttemplates/consultantfeedlist.html'
    model = Feed
    success_url = '/consultantfeed/list/'


class ConsultantFeedCommentCreateView(BaseMixin, CreateView):
    template_name = 'consultanttemplates/consultantfeedlist.html'
    form_class = CommentForm
    success_url = '/consultantfeed/list/'

    def form_valid(self, form):
        feed_id = self.kwargs['pk']
        feed = Feed.objects.get(id=feed_id)
        form.instance.post = feed
        form.instance.comment_by = self.request.user

        return super().form_valid(form)


class ConsultantFeedCommentDeleteView(DeleteView):
    template_name = 'consultanttemplates/consultantfeedlist.html'
    model = Feed
    success_url = '/consultantfeed/list/'


# # Admin Panel Update Views
# class AdminConsultantUpdateView(AdminMixin, UpdateView):
#     template_name = 'admintemplates/adminconsultantcreate.html'
#     form_class = ConsultantRegistrationForm
#     success_url = reverse_lazy('cmsapp:adminconsultantlist')
#     model = Consultant
#     success_message = "Consultant updated succesfully"


class AdminTeacherUpdateView(AdminMixin, UpdateView):
    template_name = 'teachertemplates/teachercreate.html'
    form_class = TeacherRegistrationForm
    success_url = reverse_lazy('cmsapp:adminteacherlist')
    model = Teacher
    success_message = "Teacher updated succesfully"


class AdminReceptionistUpdateView(AdminMixin, UpdateView):
    template_name = 'admintemplates/adminreceptionistcreate.html'
    form_class = ReceptionistRegistrationForm
    success_url = reverse_lazy('cmsapp:adminreceptionistlist')
    model = Receptionist
    success_message = "Receptionist updated succesfully"


class AdminStudentUpdateView(AdminMixin, UpdateView):
    template_name = 'admintemplates/adminstudentcreate.html'
    form_class = StudentRegistrationForm
    success_url = reverse_lazy('cmsapp:adminstudentlist')
    model = Student
    success_message = "Student updated succesfully"


# Admin Panel Delete Views
class AdminConsultantDeleteView(AdminMixin, DeleteView):
    template_name = 'admintemplates/adminconsultantdelete.html'
    model = Consultant
    success_url = reverse_lazy('cmsapp:adminconsultantlist')
    success_message = "Consultant  deleted successfully."


class AdminLeadDeleteView(AdminMixin, DeleteView):
    template_name = 'admintemplates/adminleaddelete.html'
    model = Lead
    success_url = reverse_lazy('cmsapp:adminleadlist')
    success_message = "Lead deleted successfully."


class AdminTeacherDeleteView(AdminMixin, DeleteView):
    template_name = 'admintemplates/adminteacherdelete.html'
    model = Teacher
    success_url = reverse_lazy('cmsapp:adminteacherlist')
    success_message = "Teacher deleted successfully."


class AdminReceptionistDeleteView(AdminMixin, DeleteView):
    template_name = 'admintemplates/adminreceptionistdelete.html'
    model = Receptionist
    success_url = reverse_lazy('cmsapp:adminreceptionistlist')
    success_message = "Receptionist deleted successfully."


class AdminStudentDeleteView(AdminMixin, DeleteView):
    template_name = 'admintemplates/adminstudentdelete.html'
    model = Student
    success_url = reverse_lazy('cmsapp:adminstudentlist')
    success_message = "Student deleted successfully."


class AdminVisitorDeleteView(AdminMixin, DeleteView):
    template_name = 'admintemplates/adminvisitordelete.html'
    model = Visitor
    success_url = reverse_lazy('cmsapp:adminvisitorlist')
    success_message = "Visitor deleted successfully."


class AdminTaskDeleteView(AdminMixin,DeleteView):
    template_name = 'admintemplates/admintaskdelete.html'
    model = Task
    success_url = reverse_lazy('cmsapp:admintasklist')
    success_message = "Task  deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AdminTaskDeleteView, self).delete(request, *args, **kwargs)


# receptionist feed views 


class ReceptionistFeedCreateView(BaseMixin, CreateView):
    template_name = 'receptionisttemplates/receptionistfeedlist.html'
    form_class = FeedForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.feed_by = user
        self.feed_id = form.save().id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cmsapp:receptionistfeedlist")


class ReceptionistFeedListView(BaseMixin, generic.ListView):
    template_name = 'receptionisttemplates/receptionistfeedlist.html'
    model = Feed
    context_object_name = 'feedlist'


class ReceptionistFeedDeleteView(DeleteView):
    template_name = 'receptionisttemplates/receptionistfeedlist.html'
    model = Feed
    success_url = '/receptionistfeed/list/'


class ReceptionistFeedCommentCreateView(BaseMixin, CreateView):
    template_name = 'receptionistemplates/receptionistfeedlist.html'
    form_class = CommentForm
    success_url = '/receptionistfeed/list/'

    def form_valid(self, form):
        feed_id = self.kwargs['pk']
        feed = Feed.objects.get(id=feed_id)
        form.instance.post = feed
        form.instance.comment_by = self.request.user

        return super().form_valid(form)


class ReceptionistFeedCommentDeleteView(DeleteView):
    template_name = 'receptionistemplates/receptionistfeedlist.html'
    model = Feed
    success_url = '/receptionistfeed/list/'



# teacher feed views 


class TeacherFeedCreateView(BaseMixin, CreateView):
    template_name = 'teachertemplates/teacherfeedlist.html'
    form_class = FeedForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.feed_by = user
        self.feed_id = form.save().id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cmsapp:teacherfeedlist")


class TeacherFeedListView(generic.ListView):
    template_name = 'teachertemplates/teacherfeedlist.html'
    model = Feed
    context_object_name = 'teacherfeedlist'


class TeacherFeedDeleteView(TeacherMixin,DeleteView):
    template_name = 'teachertemplates/teacherfeedlist.html'
    model = Feed
    success_url = '/teacherfeed/list/'


class TeacherFeedCommentCreateView(BaseMixin, CreateView):
    template_name = 'teachertemplates/teacherfeedlist.html'
    form_class = CommentForm
    success_url = '/teacherfeed/list/'

    def form_valid(self, form):
        feed_id = self.kwargs['pk']
        feed = Feed.objects.get(id=feed_id)
        form.instance.post = feed
        form.instance.comment_by = self.request.user

        return super().form_valid(form)


class TeacherFeedCommentDeleteView(DeleteView):
    template_name = 'teachertemplates/teacherfeedlist.html'
    model = Feed
    success_url = '/teacherfeed/list/'



# lead feed views 


class LeadFeedCreateView(BaseMixin, CreateView):
    template_name = 'leadtemplates/leadfeedlist.html'
    form_class = FeedForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.feed_by = user
        self.feed_id = form.save().id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cmsapp:leadfeedlist")


class LeadFeedListView(BaseMixin, generic.ListView):
    template_name = 'leadtemplates/leadfeedlist.html'
    model = Feed
    context_object_name = 'feedlist'


class LeadFeedDeleteView(DeleteView):
    template_name = 'leadtemplates/leadfeedlist.html'
    model = Feed
    success_url = '/leadfeed/list/'


class LeadFeedCommentCreateView(BaseMixin, CreateView):
    template_name = 'leadtemplates/leadfeedlist.html'
    form_class = CommentForm
    success_url = '/leadfeed/list/'

    def form_valid(self, form):
        feed_id = self.kwargs['pk']
        feed = Feed.objects.get(id=feed_id)
        form.instance.post = feed
        form.instance.comment_by = self.request.user

        return super().form_valid(form)


class LeadFeedCommentDeleteView(DeleteView):
    template_name = 'leadtemplates/leadfeedlist.html'
    model = Feed
    success_url = '/leadfeed/list/'


# student feed views 


class StudentFeedCreateView(BaseMixin, CreateView):
    template_name = 'studenttemplates/studentfeedlist.html'
    form_class = FeedForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.feed_by = user
        self.feed_id = form.save().id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cmsapp:studentfeedlist")


class StudentFeedListView(BaseMixin, generic.ListView):
    template_name = 'studenttemplates/studentfeedlist.html'
    model = Feed
    context_object_name = 'feedlist'


class StudentFeedDeleteView(DeleteView):
    model = Feed
    success_url = '/studentfeed/list/'


class StudentFeedCommentCreateView(BaseMixin, CreateView):
    template_name = 'studenttemplates/studentfeedlist.html'
    form_class = CommentForm
    success_url = '/studentfeed/list/'

    def form_valid(self, form):
        feed_id = self.kwargs['pk']
        feed = Feed.objects.get(id=feed_id)
        form.instance.post = feed
        form.instance.comment_by = self.request.user

        return super().form_valid(form)


class StudentFeedCommentDeleteView(DeleteView):
    template_name = 'studenttemplates/studentfeedlist.html'
    model = Feed
    success_url = '/studentfeed/list/'


class AdminPasswordChangeView(FormView):
    template_name = 'admintemplates/adminpasswordchange.html'
    form_class = PasswordChangeForm
    success_url = '/adminpanel'

    def form_valid(self, form):
        confirm_new_password = form.cleaned_data['confirm_new_password']
        user = self.request.user
        user.set_password(confirm_new_password)
        user.save()
        return super().form_valid(form)


class ConsultantPasswordChangeView(FormView):
    template_name = 'consultanttemplates/consultantpasswordchange.html'
    form_class = PasswordChangeForm
    success_url = '/consultantpanel'

    def form_valid(self, form):
        confirm_new_password = form.cleaned_data['confirm_new_password']
        user = self.request.user
        user.set_password(confirm_new_password)
        user.save()
        return super().form_valid(form)


class LeadPasswordChangeView(FormView):
    template_name = 'leadtemplates/leadpasswordchange.html'
    form_class = PasswordChangeForm
    success_url = '/leadpanel'

    def form_valid(self, form):
        confirm_new_password = form.cleaned_data['confirm_new_password']
        user = self.request.user
        user.set_password(confirm_new_password)
        user.save()
        return super().form_valid(form)


class ReceptionistPasswordChangeView(FormView):
    template_name = 'passwordchange.html'
    form_class = PasswordChangeForm
    success_url = 'receptionistpanel/'

    def form_valid(self, form):
        confirm_new_password = form.cleaned_data['confirm_new_password']
        user = self.request.user
        user.set_password(confirm_new_password)
        user.save()
        return super().form_valid(form)


class TeacherPasswordChangeView(FormView):
    template_name = 'teachertemplates/teacherpasswordchange.html'
    form_class = PasswordChangeForm
    success_url = '/teacherpanel'

    def form_valid(self, form):
        confirm_new_password = form.cleaned_data['confirm_new_password']
        user = self.request.user
        user.set_password(confirm_new_password)
        user.save()
        return super().form_valid(form)


class StudentPasswordChangeView(FormView):
    template_name = 'studenttemplates/studentpasswordchange.html'
    form_class = PasswordChangeForm
    success_url = '/studentpanel'

    def form_valid(self, form):
        confirm_new_password = form.cleaned_data['confirm_new_password']
        user = self.request.user
        user.set_password(confirm_new_password)
        user.save()
        return super().form_valid(form)

        # Front end ko vura haru ko lagi


# Create your views here.

# backend ko dai haru ko lagi


# Front end ko vura haru ko lagi

class FeedCreateView(BaseMixin, CreateView):
    template_name = 'feedlist.html'
    form_class = FeedForm

    def form_valid(self, form):
        user = self.request.user
        form.instance.feed_by = user
        self.feed_id = form.save().id
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("cmsapp:feedlist")


class FeedListView(BaseMixin, generic.ListView):
    template_name = 'feedlist.html'
    model = Feed
    context_object_name = 'feedlist'


class FeedDetailView(DetailView):
    template_name = 'feeddetail.html'
    model = Feed
    context_object_name = 'feeddetail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['commentform'] = CommentForm
        return context


class CommentCreateView(BaseMixin, CreateView):
    template_name = 'feedlist.html'
    form_class = CommentForm
    success_url = '/feed/list/'

    def form_valid(self, form):
        feed_id = self.kwargs['pk']
        feed = Feed.objects.get(id=feed_id)
        form.instance.post = feed
        form.instance.comment_by = self.request.user

        return super().form_valid(form)


# class MessageCreateView(BaseMixin, CreateView):
#     template_name = 'messagecreate.html'
#     form_class = MessageForm
#     success_url = '/'

#     def form_valid(self, form):
#         user = self.request.user
#         form.instance.sender = user
#         return super().form_valid(form)

# Task


class TaskCreateView(BaseMixin, CreateView):
    template_name = 'taskcreate.html'
    form_class = TaskForm
    success_url = reverse_lazy("cmsapp:tasklist")

    def form_valid(self, form):
        return super().form_valid(form)


class TaskListView(BaseMixin, ListView):
    template_name = 'tasklist.html'
    model = Task
    context_object_name = 'tasklist'


class TaskBoardView(BaseMixin, ListView):
    template_name = 'taskboard.html'
    model = Task
    context_object_name = 'tasklist'


class TaskDetailView(DetailView):
    template_name = 'taskdetail.html'
    model = Task
    context_object_name = 'taskdetail'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['commentform'] = CommentForm
    #     return context


class TaskUpdateView(UpdateView):
    template_name = 'taskcreate.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy("cmsapp:tasklist")
    success_message = "Task updated succesfully"


class TaskDeleteView(DeleteView):
    template_name = 'taskdelete.html'
    model = Task
    success_url = reverse_lazy('cmsapp:tasklist')
    success_message = "Task  deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(TaskDeleteView, self).delete(request, *args, **kwargs)


class AppointmentCreateView(BaseMixin, CreateView):
    template_name = 'appointmentcreate.html'
    form_class = AppointmentForm
    success_url = reverse_lazy("cmsapp:appointmentlist")

    def form_valid(self, form):
        return super().form_valid(form)


class AppointmentListView(BaseMixin, ListView):
    template_name = 'appointmentlist.html'
    model = Appointment
    context_object_name = 'appointmentlist'


class AppointmentDetailView(DetailView):
    template_name = 'appointmentdetail.html'
    model = Appointment
    context_object_name = 'appointmentdetail'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['commentform'] = CommentForm
    #     return context


class AppointmentUpdateView(UpdateView):
    template_name = 'appointmentcreate.html'
    model = Appointment
    form_class = AppointmentForm
    success_url = reverse_lazy("cmsapp:appointmentlist")
    success_message = "Appointment updated succesfully"


class AppointmentDeleteView(DeleteView):
    template_name = 'appointmentdelete.html'
    model = Appointment
    success_url = reverse_lazy('cmsapp:appointmentlist')
    success_message = "Appointment deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(AppointmentDeleteView, self).delete(request, *args, **kwargs)


# class MessageListView(BaseMixin, ListView):
#     template_name = 'messagelist.html'
#     model = Message
#     context_object_name = 'messagelist'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['commentform'] = CommentForm
    #     return context


class LanguageCourseCreateView(CreateView):
    template_name = 'languagecoursecreate.html'
    form_class = LanguageCourseForm
    success_url = reverse_lazy("cmsapp:languagecourselist")


class LanguageCourseListView(BaseMixin, ListView):
    template_name = 'languagecourselist.html'
    model = LanguageCourse
    context_object_name = 'languagecourselist'

# University


class UniversityCreateView(BaseMixin, CreateView):
    template_name = 'universitycreate.html'
    form_class = UniversityForm
    success_url = reverse_lazy("cmsapp:universitylist")


class UniversityListView(ListView):
    template_name = 'universitylist.html'
    model = University
    context_object_name = 'universitylist'


class UniversityDetailView(DetailView):
    template_name = 'universitydetail.html'
    model = University
    context_object_name = 'universitydetail'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['commentform'] = CommentForm
    #     return context


class UniversityUpdateView(UpdateView):
    template_name = 'universitycreate.html'
    model = University
    form_class = UniversityForm
    success_url = reverse_lazy("cmsapp:universitylist")
    success_message = "University updated succesfully"


class UniversityDeleteView(DeleteView):
    template_name = 'universitydelete.html'
    model = University
    success_url = reverse_lazy('cmsapp:universitylist')
    success_message = "University  deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(UniversityDeleteView, self).delete(request, *args, **kwargs)

# class OrganizationCreateView(BaseMixin, CreateView):
#     template_name = 'organizationcreate.html'
#     form_class = OrganizationForm
#     success_url = '/'


class StudentListView(ListView):
    template_name = 'studenttemplates/studentlist.html'
    model = Student
    context_object_name = 'studentlist'


class TeacherListView(ListView):
    template_name = 'teachertemplates/teacherlist.html'
    model = Teacher
    context_object_name = 'teacherlist'


class ReceptionListView(ListView):
    template_name = 'receptionisttemplates/receptionistlist.html'
    model = Receptionist
    context_object_name = 'receptionistlist'


class LeadListView(ListView):
    template_name = 'leadtemplates/leadlist.html'
    model = Lead
    context_object_name = 'leadlist'


class ConsultantListView(ListView):
    template_name = 'consultanttemplates/consultantlist.html'
    model = Consultant
    context_object_name = 'consultantlist'


class AdminListView(AdminMixin, ListView):
    template_name = 'admintemplates/adminlist.html'
    model = Admin
    context_object_name = 'adminlist'


class VisitorListView(ListView):
    template_name = 'visitortemplates/visitorlist.html'
    model = Visitor
    context_object_name = 'visitorlist'

# Course


class CourseCreateView(BaseMixin, CreateView):
    template_name = 'coursecreate.html'
    form_class = CourseForm
    success_url = reverse_lazy("cmsapp:courselist")


class CourseListView(ListView):
    template_name = 'courselist.html'
    model = Course
    context_object_name = 'courselist'


class CourseDetailView(DetailView):
    template_name = 'coursedetail.html'
    model = Course
    context_object_name = 'coursedetail'

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['commentform'] = CommentForm
    #     return context


class CourseUpdateView(UpdateView):
    template_name = 'coursecreate.html'
    model = Course
    form_class = CourseForm
    success_url = reverse_lazy("cmsapp:courselist")
    success_message = "Course updated succesfully"


class CourseDeleteView(DeleteView):
    template_name = 'coursedelete.html'
    model = Course
    success_url = reverse_lazy('cmsapp:courselist')
    success_message = "Course deleted successfully."

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, self.success_message)
        return super(CourseDeleteView, self).delete(request, *args, **kwargs)
