

class StudentMixin:
    def get_student(self):
        id = self.kwargs.get('id')
        student = Student.objects.get(pk=id)
        return get_object_or_404(Student, id=id)