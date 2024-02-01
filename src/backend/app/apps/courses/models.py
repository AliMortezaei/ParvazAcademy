from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator

from accounts.users.models import User



class Category(models.Model):
    title = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(unique=True, allow_unicode=True, null=True, blank=True)
    description = models.CharField(max_length=2048, null=True, blank=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

class Course(models.Model):

    title = models.CharField(max_length=65, db_index=True, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='courses'
    )
    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teacher_courses',
        limit_choices_to={'user_type__user_type': 'teacher'},
    )
    is_public = models.BooleanField(default=True)
    is_start = models.BooleanField(default=True)
    date_start = models.DateField(null=True, blank=True)
    date_end = models.DateField(null=True, blank=True)
    students = models.ManyToManyField(
        User,
        related_name='courses',
        limit_choices_to={'user_type__user_type': 'student'},
        through="CourseStudent",
        blank=True,
    )
    numbers = models.PositiveSmallIntegerField(        
        default=0,
        validators=[
            MaxValueValidator(50),
            MinValueValidator(0)
        ]
    )

    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ('-is_start', '-numbers')


class Section(models.Model):
    title = models.CharField(max_length=65, db_index=True, unique=True)
    slug = models.SlugField(unique=True, allow_unicode=True, null=True, blank=True)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    link = models.CharField(max_length=255, blank=True, null=True)
    date_start = models.DateTimeField(null=True, blank=True)
    is_passed = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-is_passed', '-date_start')


class CourseStudent(models.Model):
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='student_course')
    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type__user_type': 'student'},
        related_name='course_student'
    )
    join_date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'course_student'
    


# class Quiz(models.Model):
#     # course = models.OneToOneField(
#     #     Course, on_delete=models.CASCADE, related_name='quez'
#     # )
#     questions = models.ManyToManyField('Question', through='QuizQuestion')




# class Question(models.Model):
#     title = models.CharField(max_length=255)
#     quiz = models.ForeignKey(
#         Quiz, on_delete=models.CASCADE, related_name='questions'
#     )


# class QuizQuestion(models.Model):
#     quez = models.ForeignKey(
#         Quiz, on_delete=models.CASCADE, related_name='questions_quez',
#     )
#     question = models.ForeignKey(
#         Question, on_delete=models.CASCADE, related_name='quiz_question',
#         unique=True
#     )

# class Answer(models.Model):
#     text = models.CharField(max_length=255)
#     question = models.ForeignKey(
#         Question, on_delete=models.CASCADE,related_name='answers'
#     )
#     is_correct = models.BooleanField(default=False)
    