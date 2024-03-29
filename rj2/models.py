from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    is_active = models.BooleanField(default=True)
    is_content_manager = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin

    def save(self, *args, **kwargs):
        # if user being demoted from content manager, make sure they are not
        # managing any courses
        super().save(*args, **kwargs)

class Course(models.Model):
    def __str__(self):
        return self.name
    name = models.CharField(unique=True, blank=False, null=False,
                            max_length=100)
    description = models.TextField(blank=False, null=False)
    fee = models.DecimalField(decimal_places=2, max_digits=20)
    is_deprecated = models.BooleanField(blank=False, null=False, default=False)
    is_active = models.BooleanField(blank=False, null=False, default=False)
    instructors = models.CharField(blank=False, null=False, max_length=100)
    content_manager = models.ForeignKey(MyUser, related_name="managed_courses",
            unique=False)



    def deprecate(self):
        """
        Deprecating a course causes the course to display a warning whenever a
        student user tries to view it.
        """
        if self.is_active:
            self.is_deprecated = True
        else:
            raise Exception("Cannot deprecate an inactive course.")

    def delete(self):
        """
        Deleting a course causes it to become invisible to student users by
        making it inactive.
        """
        if self.is_deprecated:
            self.is_active = False
        else:
            raise Exception("Cannot delete a course which has not been"
                            " deprecated.")

    def release(self):
        """
        Releasing a course causes it to be visible (i.e., active) and
        non-deprecated.
        """
        quizzes = Quiz.objects.filter(course=self)
        if quizzes.exists():
            self.is_deprecated = False
            self.is_active = True
        else:
            raise Exception("Cannot release a course with no quizzes.")

class Quiz(models.Model):
    course = models.ForeignKey(Course)
    title = models.CharField(blank=False, null=False, max_length=100)
    
    def __str__(self):
        return self.title

class Question(models.Model):
    quiz = models.ForeignKey(Quiz, related_name="questions")
    text = models.TextField(blank=False, null=False)

    @property
    def correct_answer_id(self):
        for answer in self.answers.all():
            if answer.is_correct:
                return answer.id

    def __str__(self):
        return self.text

class Answer(models.Model):
    is_correct = models.BooleanField(blank=False, null=False, default=False)
    question = models.ForeignKey(Question, related_name="answers")
    text = models.CharField(blank=False, null=False, max_length=100)

    def __str__(self):
        return self.text

class Video(models.Model):
    course = models.ForeignKey(Course)
    URL = models.URLField(blank=False, null=False)

    def __str__(self):
        return self.URL

class PDF(models.Model):
    pdf_file = models.FileField()
    course = models.ForeignKey(Course)

    def __str__(self):
        return self.pdf_file.name


class Score(models.Model):
    user = models.ForeignKey(MyUser)
    quiz = models.ForeignKey(Quiz)
    value = models.PositiveIntegerField()
    completed = models.DateTimeField(auto_now_add=True)
    unique_together = (user, quiz)

class CourseRegistration(models.Model):
    user = models.ForeignKey(MyUser)
    course = models.ForeignKey(Course)
    unique_together = (user, course)

    def is_complete(self):
        """
        Returns True if the user has completed all quizzes for this course.
        Otherwise returns False.
        """
        quizzes = Quiz.objects.filter(course=self.course)
        for quiz in quizzes:
            score = Score.objects.filter(user=self.user, quiz=quiz)
            if not score.exists():
                return False
        return True

    def __str__(self):
        return "<Registration: user={}, course={}>".format(self.user,
                self.course)
