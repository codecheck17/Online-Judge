from tkinter import CASCADE
from django.db import models
from django.core.files import File
import re
class Problem(models.Model):
    Problem_id = models.PositiveBigIntegerField(default = 0)
    Title = models.CharField(max_length = 50)
    Description = models.TextField()
    Input_Format = models.TextField()
    Output_Format = models.TextField()
    Constraint = models.CharField(max_length = 50)
    
    def __str__(self):
        return self.Title

class TestCase(models.Model):
    
    def upload_file_name_input(self, filename):
        FolderName = re.sub('[;:,. -+]','_',self.Problem_Name.Title)
        return f'testfiles/{FolderName}/input/{filename}'
    
    def upload_file_name_output(self,filename):
        FolderName = re.sub('[;:,. -+]','_',self.Problem_Name.Title)
        return f'testfiles/{FolderName}/output/{filename}'
    
    Problem_Name = models.ForeignKey(Problem,on_delete = models.CASCADE)
    Input_File = models.FileField(upload_to = upload_file_name_input)
    Output_file = models.FileField(upload_to = upload_file_name_output)
    
    def __str__(self):
        return self.Problem_Name.Title 

class Submission(models.Model):
      
      def upload_code_name(self,filename):
        ext = filename.split('.')[-1]
        filename = str(self.Submission_Time)
        filename = re.sub('[;:,. -+]', '_',filename)
        filename = "%s.%s" % (filename,ext)
        FolderName = re.sub('[;:,. -+]','_',self.Problem.Title)
        return f'codes/mycodes/{FolderName}/{filename}'
      
      Problem = models.ForeignKey(Problem, on_delete = models.CASCADE)
      Submission_Time = models.DateTimeField(auto_now_add = True)
      Language = models.CharField(max_length = 10)
      Code = models.FileField(upload_to = upload_code_name) 
      Result = models.CharField(max_length = 20,default = "None")
      
      def __str__(self):
        return self.Problem.Title


