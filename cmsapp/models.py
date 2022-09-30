from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.


class Organization(models.Model):
    title = models.CharField(max_length=200)
    slogan = models.CharField(max_length=500)
    logo = models.ImageField(upload_to="organization")
    image = models.ImageField(upload_to="organization", null=True, blank=True)
    address = models.CharField(max_length=500)
    location = models.CharField(max_length=20)
    mission = models.TextField(null=True, blank=True)
    phone = models.CharField(max_length=20)
    mobile1 = models.CharField(max_length=20, null=True, blank=True)
    mobile2 = models.CharField(max_length=20, null=True, blank=True)
    email1 = models.EmailField()
    email2 = models.EmailField(null=True, blank=True)
    about = models.TextField()
    established = models.DateField()

    def __str__(self):
        return self.title


class TimeStamp(models.Model):
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=False,auto_now_add=True, null=True, blank=True)
    created_by = models.ForeignKey(
        User, on_delete=models.DO_NOTHING, null=True, blank=True)

    class Meta:
        abstract = True


class Receptionist(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.PROTECT, null=True, blank=True)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(
        upload_to='receptionist/', default="/default.jpg", blank=True, null=True)

    # @receiver(post_save, sender=User)
    # def save_user_profile(sender, instance, **kwargs):
    #     instance.profile.save()

# class FollowUp(models.Model):
#     visitor = models.ForeignKey(Visitor, on_delete=models.PROTECT)
#     summary = models.TextField()
#     by = models.ForeignKey(Staff, on_delete=models.PROTECT)
#     response_through = models.CharField(
#         max_length=200, choices=ENQUIRY_THROUGH)

#     def __str__(self):
#         return self.summary


class Appointment(models.Model):
    subject = models.TextField()
    phone = models.CharField(max_length=10)
    date = models.DateField(null=True, blank=True)
    party1 = models.CharField(max_length=200)
    party2 = models.CharField(max_length=200)

    def __str__(self):
        return self.subject


class Country(models.Model):
    name = models.CharField(max_length=130)
    city = models.CharField(max_length=130)
    about = models.TextField()
    image = models.ImageField(upload_to="countries/",
                              blank=True, null=True, default="/default.jpg")

    def __str__(self):
        return self.name


relation = (("Partnered", "Partnered"),
            ("Non partnered", "Non partnered"))

term = (("fall", "fall"),
        ("spring", "spring"),
        ("summer", "summer"))


class University(models.Model):
    name = models.CharField(max_length=120, blank=True, null=True)
    about = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    country = models.ForeignKey(
        Country, on_delete=models.PROTECT, blank=True, null=True)
    deadline = models.DateField(null=True, blank=True)
    relation = models.CharField(
        choices=relation, max_length=100, null=True, blank=True)
    requirements = models.TextField(blank=True, null=True)
    contact_person = models.TextField(blank=True, null=True)
    term = models.CharField(choices=term, null=True,
                            blank=True, max_length=120)
    phone = models.CharField(max_length=10)
    email = models.EmailField(blank=True, null=True)
    features = models.TextField(blank=True, null=True)
    scholarship = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='university/', null=True, blank=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=120)
    fee_structure = models.CharField(max_length=120)
    about = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


status = (("Completed", "Completed"),
          ("Pending", "Pending"))
priority = (("Urgent", "Urgent"),
            ("High", "High"),
            ("Low", "Low"),
            ("Medium", "Medium"))


class Task(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True, null=True)
    status = models.CharField(
        choices=status, default="Pending", max_length=100)
    priority = models.CharField(
        choices=priority, default="Medium", max_length=100)
    due_date = models.DateField(null=True, blank=True)
    assigned_to = models.ManyToManyField(User)

    def __str__(self):
        return (self.title)


class Teacher(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=100)
    phone = models.PositiveIntegerField()
    address = models.CharField(max_length=100)
    email = models.EmailField()
    qualification = models.CharField(max_length=400, null=True, blank=True)
    experience = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='teacher/',
                              blank=True, null=True, default="/default.jpg")
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


seats = (("Available", "Available"),
         ("Full", "Full"))


class LanguageCourse(models.Model):
    title = models.CharField(max_length=150, null=True)
    fee = models.PositiveIntegerField(null=True, blank=True)
    schedule = models.TextField(blank=True, null=True)
    seats = models.CharField(choices=seats, max_length=150, null=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, related_name='teachers', max_length=150, null=True)
    duration = models.PositiveIntegerField(null=True, blank=True)
    books = models.CharField(max_length=130, null=True)

    def __str__(self):
        return self.title


class StudyMaterials(models.Model):
    language_course = models.ForeignKey(
        LanguageCourse, on_delete=models.SET_NULL, related_name='language_course', max_length=150, null=True, blank=True)
    title = models.CharField(max_length=100, blank=True, null=True)
    study_file = models.FileField(upload_to='study_file/', blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.language_course, self.title)


source = (("Social Media", "Social Media"),
          ("Television", "Television"),
          ("Radio", "Radio"),
          ("Newspaper", "Newspaper"),
          ("Magazines", "Magazines"),
          ("Friends", "Friends"),
          ("Magazines", "Magazines"),
          ("Pamphlets", "Pamphlets"),
          ("Referral", "Referral"),
          )


class Visitor(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    phone = models.PositiveIntegerField()
    email = models.EmailField()
    source = models.CharField(choices=source, max_length=100)
    visited_date = models.DateField(auto_now=True)
    purpose = models.TextField()
    about = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='visitor/',
                              blank=True, null=True, default="/default.jpg")

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=150)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    email = models.EmailField(null=True)
    language_course = models.ForeignKey(
        LanguageCourse, on_delete=models.SET_NULL, null=True, blank=True)
    assigned_to = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(upload_to='student/',
                              blank=True, null=True, default="/default.jpg")
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


visa_status = (("Processing", "Processing"),
               ("Lodged", "Lodged"),
               ("Accepted", "Accepted"),
               ("Rejected", "Rejected"))


class Lead(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    course = models.ForeignKey(
        Course, on_delete=models.SET_NULL, null=True, blank=True)
    university = models.ForeignKey(
        University, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(null=True, blank=True)
    address = models.CharField(max_length=100)
    phone = models.CharField(max_length=10)
    visa_status = models.CharField(
        choices=visa_status, max_length=50, default="Processing", blank=True, null=True)
    image = models.ImageField(
        upload_to='lead/', blank=True, null=True, default="/default.jpg")
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return str(self.address)


class Document(models.Model):
    title = models.CharField(max_length=100)
    file = models.FileField(upload_to='documents')
    lead = models.ForeignKey(
        Lead, on_delete=models.SET_NULL, blank=True, null=True, related_name='lead')

    def __str__(self):
        return str(self.title)


class Consultant(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    image = models.ImageField(upload_to='consultant/',
                              blank=True, null=True, default="/default.jpg")
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Admin(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    address = models.CharField(max_length=200)
    email = models.EmailField()
    image = models.ImageField(
        upload_to='admin/', blank=True, null=True, default="/default.jpg")
    about = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username


qualifications = (("Under-Graduate", "Under-Graduate"),
                  ("Graduate", "Graduate"),
                  ("Post-Graduate", "Post-Graduate"))
year = (("2019", "2019"),
        ("2018", "2018"),
        ("2017", "2017"),
        ("2016", "2016"),
        ("2015", "2015"),
        ("2014", "2014"),
        ("2013", "2013"),
        ("2012", "2012"),
        ("2011", "2011"),
        ("2010", "2010"),
        ("2009", "2009"))


class Qualification(models.Model):
    level = models.CharField(choices=qualifications,
                             max_length=100, null=True, blank=True)
    completed_year = models.CharField(
        choices=year, max_length=100, null=True, blank=True)
    student = models.ForeignKey(
        Student, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.level


relation = (("Partnered", "Partnered"),
            ("Non partnered", "Non partnered"))

method = (("Cash", "Cash"),
          ("Cheque", "Cheque"))


class Payment(models.Model):
    method = models.CharField(
        choices=method, max_length=20, null=True, blank=True)
    amount = models.PositiveIntegerField(null=True, blank=True)
    particulars = models.CharField(max_length=120, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    student = models.ForeignKey(
        Student, on_delete=models.SET_NULL, blank=True, null=True)
    teacher = models.ForeignKey(
        Teacher, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return '%s %s' % (self.amount, "(" + self.method + ")")


class Feed(TimeStamp):
    post = models.TextField()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.post


class Comment(models.Model):
    post = models.ForeignKey(
        Feed, on_delete=models.CASCADE, related_name="comments")
    comment = models.TextField()
    comment_by = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.comment


# class FollowUp(models.Model):
#     visitor = models.ForeignKey(Visitor, on_delete=models.PROTECT)
#     summary = models.TextField()
#     by = models.ForeignKey(Staff, on_delete=models.PROTECT)
#     response_through = models.CharField(
#         max_length=200, choices=ENQUIRY_THROUGH)

#     def __str__(self):
#         return self.summary


# class Appointment(models.Model):
#     subject = models.CharField(max_length=200)
#     date = models.DateTimeField()
#     party1 = models.CharField(max_length=200)
#     party2 = models.CharField(max_length=200)

#     def __str__(self):
#         return self.subject


class Message(models.Model):
    sender = models.ForeignKey(
        User, related_name="sender", on_delete=models.PROTECT)
    receiver = models.ForeignKey(
        User, related_name="receiver", on_delete=models.PROTECT)
    msg_content = models.CharField(max_length=250)
    # created_at = # time field
