from django import forms
from django.forms import Select
from .models import *
from django.forms import modelformset_factory

# back end ko dai haru ko lagi


class ReceptionistRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose Username',
    }),)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Receptionist
        fields = ['username', 'password1', 'password2',
                  'name', 'phone', 'address', 'email', 'about', 'image']
        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-validation': 'required',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter your email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),

        }

    def clean(self):
        cleaned_data = super(ReceptionistRegistrationForm, self).clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class VisitorRegistrationForm(forms.ModelForm):
    class Meta:
        model = Visitor
        fields = ['name', 'phone', 'address', 'email',
                  'source', 'purpose', 'about', 'image']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-validation': 'required',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter your email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),
            'source': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),
            'purpose': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),
        }


class LeadUpdateForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    university = forms.ModelChoiceField(queryset=University.objects.all())

    class Meta:
        model = Lead
        fields = ['university',
                  'name', 'email', 'address', 'phone', 'visa_status', 'about', 'image', 'course']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'id': 'name',
                'placeholder': 'Enter Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-validation': 'required',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter your email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
            }),
            'course': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Course',
            }),
            'university': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select university',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),
            'visa_status': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),
        }


# class UniversityUpdateForm(forms.ModelForm):
#     course = forms.ModelChoiceField(queryset=Course.objects.all())
#     university = forms.ModelChoiceField(queryset=University.objects.none())

#     class Meta:
#         model = Lead
#         fields = ['university',
#                   'course']
#         widgets = {
#             'course': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Select Course',
#             }),
#             'university': forms.Select(attrs={
#                 'class': 'form-control',
#                 'placeholder': 'Select university',
#             })
#         }

    # def get(self, request):
    #     course = self.instance.course
    #     course_id = course.id
    #     return course_id


class LeadRegistrationForm(forms.ModelForm):
    course = forms.ModelChoiceField(queryset=Course.objects.all())
    # university = forms.ModelChoiceField(queryset=University.objects.none())
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose Username',
    }),)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))
    # documents = forms.FileField(widget=forms.ClearableFileInput(attrs={
    #     'class': 'form-control',
    #     'multiple': True,
    #     'placeholder': 'Upload Documents',
    # }),
    # )

    class Meta:
        model = Lead
        fields = ['username', 'password1', 'password2',
                  'name', 'email', 'address', 'phone', 'university', 'visa_status', 'about', 'image', 'course']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-validation': 'required',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter your email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
            }),
            'course': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Select Course',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),

            'visa_status': forms.Select(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),
        }

    def clean(self):
        cleaned_data = super(LeadRegistrationForm, self).clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class StudentRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose Username',
    }),)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Student
        fields = ['username', 'password1', 'password2',
                  'name', 'email', 'phone', 'address', 'language_course', 'about', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-validation': 'required',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter Email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),
            'language_course': forms.Select(attrs={
                'class': 'form-control form-control-primary',
                'label': 'Category',

            }),

        }

    def clean(self):
        cleaned_data = super(StudentRegistrationForm, self).clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class ConsultantRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose Username',
    }),)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Consultant
        fields = ['username', 'password1', 'password2',
                  'name', 'phone', 'address', 'email', 'about', 'image']

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-validation': 'required',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter your email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),
        }

    def clean(self):
        cleaned_data = super(ConsultantRegistrationForm, self).clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class TeacherRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose Username',
    }),)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Teacher
        fields = ['username', 'password1', 'password2',
                  'name', 'phone', 'address', 'email', 'experience', 'qualification', 'about', 'image']

        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-validation': 'required',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter your email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),
            'experience': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Experience',
            }),
            'qualification': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Qualification',
            }),
        }

    def clean(self):
        cleaned_data = super(TeacherRegistrationForm, self).clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class AdminRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose Username',
    }),)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Admin
        fields = ['username', 'password1', 'password2',
                  'name', 'phone', 'address', 'email', 'about', 'image']
        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-validation': 'required',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter your email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Address',
            }),

        }

    def clean(self):
        cleaned_data = super(AdminRegistrationForm, self).clean()
        username = cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class LoginForm(forms.Form):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username',
    }),)
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))
    remember_me = forms.BooleanField(
        required=False, widget=forms.CheckboxInput())

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        remember_me = cleaned_data.get('remember_me')
        if remember_me is True:
            SESSION_EXPIRE_AT_BROWSER_CLOSE = False
        else:
            SESSION_EXPIRE_AT_BROWSER_CLOSE = True
        return


class PasswordChangeForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))
    confirm_new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))

    def clean(self):
        cleaned_data = super(PasswordChangeForm, self).clean()
        new_password = cleaned_data.get("new_password")
        confirm_new_password = cleaned_data.get("confirm_new_password")
        if new_password != confirm_new_password:
            raise forms.ValidationError(
                "New password and confirm new password didn't match")
        return confirm_new_password


# front end ko vura haru ko lagi
        # if current_password == form.instance.user.password2:
# back end ko dai haru ko lagi

# front end ko vura haru ko lagi


class FeedForm(forms.ModelForm):
    class Meta:
        model = Feed
        fields = ['post']

        widgets = {
            'post': forms.Textarea(attrs={
                'placeholder': 'Write Something...',
                'rows': '5',
                'cols': '50',
                'class': 'form-control',
            }),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']

        widgets = {
            'comment': forms.Textarea(attrs={
                'placeholder': 'Write Something...',
                'rows': '5',
                'cols': '50',
                'class': 'form-control',
            }),
        }


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['msg_content', 'receiver']


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ['party1', 'phone', 'subject', 'party2', 'date']
        widgets = {
            'party1': forms.TextInput(attrs={
                'placeholder': 'Enter Visitor Name',
                'class': 'form-control',
            }),

            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Phone Number',
            }),
            'subject': forms.TextInput(attrs={
                'placeholder': 'Purpose of appointment',
                'class': 'form-control',
            }),
            'party2': forms.TextInput(attrs={
                'placeholder': 'Enter Consultant Name',
                'class': 'form-control',
            }),
            'date': forms.DateInput(attrs={
                'placeholder': 'Enter Appointment Date',
                'class': 'form-control',
                'id': 'id_due_date'
            })
        }


class LeadDocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['lead']


class DocumentForm(forms.ModelForm):

    class Meta:
        model = Document
        fields = ['title', 'file']

        widgets = {
            'file': forms.ClearableFileInput(attrs={
                'placeholder': 'File Title',
                'class': 'form-control',

            }),
        }


DocumentFormset = modelformset_factory(
    Document, form=DocumentForm, max_num=10, extra=2)



class TeacherStudyMaterialsForm(forms.ModelForm):
    class Meta:
        model = StudyMaterials
        fields = ['language_course']

class StudyMaterialsForm(forms.ModelForm):

    class Meta:
        model = StudyMaterials
        fields = ['title','study_file']

        widgets = {
            'study_file': forms.ClearableFileInput(attrs={
                'placeholder': 'File Title',
                'class': 'form-control',

            }),
        }


StudyMaterialsFormset = modelformset_factory(
    StudyMaterials, form=StudyMaterialsForm, max_num=10, extra=2)


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task

        fields = ['title', 'content', 'priority',
                  'due_date', 'assigned_to', 'status']

    widgets = {
        'title': forms.TextInput(attrs={
            'placeholder': 'Enter Your Name',
            'class': 'form-control',
        }),
        'due_date': forms.DateInput(attrs={
            'placeholder': 'Due date',
            'id': 'id_due_date'
        }),

        'assigned_to': forms.SelectMultiple(attrs={
            'class': 'js-example-basic-multiple',
            'placeholder': 'Enter Your Name',
            # 'multiple':'multiple' ,
        })}

    def clean_assigned_to(self):
        assigned_to = self.cleaned_data.get('assigned_to')
        return assigned_to


class LanguageCourseForm(forms.ModelForm):
    class Meta:
        model = LanguageCourse
        fields = ['title', 'fee', 'schedule', 'seats',
                  'teacher', 'duration', 'books']


class UniversityForm(forms.ModelForm):
    class Meta:
        model = University
        fields = ['name', 'about', 'address', 'country', 'deadline', 'relation',
                  'requirements', 'contact_person', 'term', 'phone', 'features', 'scholarship']

        widgets = {
            'name': forms.TextInput(attrs={
                'placeholder': 'Enter University name',
                'class': 'form-control'
            }),
            'about': forms.TextInput(attrs={
                'placeholder': 'Enter Informations of University ',
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'placeholder': 'Enter University address',
                'class': 'form-control'
            }),
            'country': forms.TextInput(attrs={
                'placeholder': 'Enter University country',
                'class': 'form-control'
            }),
            'requirements': forms.TextInput(attrs={
                'placeholder': 'Enter University admission requirement',
                'class': 'form-control'
            }),
            'deadline': forms.TextInput(attrs={
                'placeholder': 'Enter University deadline',
                'class': 'form-control'
            }),
            'relation': forms.Select(attrs={
                'placeholder': 'Enter University name',
                'class': 'form-control'
            }),
            'contact_person': forms.TextInput(attrs={
                'placeholder': 'Enter University name',
                'class': 'form-control'
            }),
            'term': forms.Select(attrs={
                'placeholder': 'Enter University name',
                'class': 'form-control'
            }),
            'phone': forms.TextInput(attrs={
                'placeholder': 'Enter University name',
                'class': 'form-control'
            }),
            'features': forms.TextInput(attrs={
                'placeholder': 'Enter University name',
                'class': 'form-control'
            }),
            'scholarship': forms.TextInput(attrs={
                'placeholder': 'Enter University name',
                'class': 'form-control'
            })

        }


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'fee_structure', 'university', 'about']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter Course title',
                'class': 'form-control'
            }),
            'fee': forms.TextInput(attrs={
                'placeholder': 'Enter Course fee ',
                'class': 'form-control'
            }),
            'University': forms.Select(attrs={
                'placeholder': 'Enter University ',
                'class': 'form-control'
            })
        }
