from django.forms import ModelForm
from rj2.models import Course

class CourseForm(ModelForm):
    class Meta:
        model = Course
        fields = ['name', 'fee', 'instructors', 'description']
