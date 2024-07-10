from django.db import models


class ExcelData(models.Model):
    excel_file = models.FileField(upload_to='excel_files/')


class Admin(models.Model):
    email = models.CharField(max_length=25)
    password = models.CharField(max_length=15)


class UserLoginActivity(models.Model):
    email = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    login_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.email} - {self.login_time}"


class MockTestSolution(models.Model):
    mock_test_number = models.IntegerField(unique=True)
    solution_file = models.FileField(upload_to='mock_test_solutions/')

    def __str__(self):
        return f"Mock Test {self.mock_test_number} Solution"


class StudyPlan(models.Model):
    name = models.CharField(max_length=255)
    pdf_file = models.FileField(upload_to='study_plans/')

    def __str__(self):
        return self.name


class CurrentAffairs(models.Model):
    title = models.CharField(max_length=200)
    link = models.URLField(max_length=200)
    text = models.TextField()
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_day(self):
        return self.created_at.day

    def get_month(self):
        return self.created_at.month
