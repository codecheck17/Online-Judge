import subprocess,re,os
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .forms import CodeForm
from .models import Problem, Submission, TestCase

Language_Choices = {
    '1':'C++',
    '2':'Java',
    '3':'Python',
    '4':'JavaScript',
    '5':'Haskell',
}

#=====================================================================================#


@login_required
def ProblemSet(request):
    username = None
    problems = Problem.objects.all()
    context = {
        'problems' : problems
    }
    return render(request,'judge/ProblemSet.html',context)




#=====================================================================================#




@login_required
def Description(request,Problem_id):
    CurrentProblem = get_object_or_404(Problem,pk = Problem_id)
    testcases = TestCase.objects.filter(Problem_Name = CurrentProblem)[:1]
    for testcase in testcases:
        Sample_Input_Path = f'C:/OJ/OJ/{testcase.Input_File.url}'
        Sample_Output_Path = f'C:/OJ/OJ/{testcase.Output_file.url}'
        
        with open(Sample_Input_Path) as ip,open(Sample_Output_Path) as op:
            Sample_Input = ip.read()
            Sample_Output = op.read()    
    
    context = {
        'Problem_id' : Problem_id,
        'Title' : CurrentProblem.Title,
        'Description' : CurrentProblem.Description,
        'Input_Format' : CurrentProblem.Input_Format,
        'Output_Format' : CurrentProblem.Output_Format,
        'Constriants' : CurrentProblem.Constraint,
        'Sample_Input': Sample_Input,
        'Sample_Output': Sample_Output,
    }
    return render(request,'judge/Description.html',context)


#===========================================================================================#


def findVerdict(Problem,Submission):
   CodePath = f'C:/OJ/OJ/{Submission.Code.url}'
   Verdict = "AC"
   testcases = TestCase.objects.filter(Problem_Name = Problem)
   subprocess.run(f'g++ {CodePath} -o Output',shell = True)
   for testcase in testcases:
        
        inputFile = f'C:/OJ/OJ/{testcase.Input_File.url}'  
        actual_outputFile = f'C:/OJ/OJ/{testcase.Output_file.url}'   
        outputFile = 'C:/OJ/OJ/Output.txt'

        subprocess.call(f'Output < {inputFile} > C:/OJ/OJ/Output.txt',shell = True)
        
        with open(outputFile, 'r') as file:
            data1 = file.read()
        
        with open(actual_outputFile, 'r') as file:
            data2 = file.read() 
        
        data1 = re.sub('[\n ]','',data1)
        data2 = re.sub('[\n ]','',data2) 
        if(data1!=data2):
            Verdict = "WA"
   
   os.remove('Output.exe')
   os.remove('Output.txt')
   Code = []
   with open(CodePath) as Codes:
      for line in Codes:
        Code.append(line)
   
   Code.append(Verdict)
   return Code





#=====================================================================================#




@login_required
def NewSubmission(request,Problem_id):
    thisProblem = get_object_or_404(Problem,pk = Problem_id)
    if request.method == 'POST': 
        thisSubmission = Submission(Problem = thisProblem)
        UploadedForm = CodeForm(request.POST,request.FILES,instance = thisSubmission)
        if UploadedForm.is_valid():
            Language_Option = request.POST['Language_Select']
            thisSubmission.Language=Language_Choices[Language_Option]
            thisSubmission.save()
            result = findVerdict(thisProblem,thisSubmission)
            thisSubmission.Result = result[-1]
            thisSubmission.save() 
            context = {
                'result': result,
                'Language':thisSubmission.Language
            }
            return render(request,'judge/Verdict.html',context)
        else:
            return HttpResponse("somthing went wrong")       
    else:
        NewForm = CodeForm()
        context = {
            'Problem_Name': thisProblem.Title,
            'NewForm' : NewForm,
            'Problem_id' : Problem_id
        }
    
    return render(request,'judge/NewSubmission.html',context)





#=====================================================================================#




@login_required
def MySubmissions(request,Problem_id):
    thisProblem = get_object_or_404(Problem,pk=Problem_id)
    SubmissionList=Submission.objects.filter(Problem = thisProblem).order_by('-Submission_Time')[:5]
    context = {
        'SubmissionList': SubmissionList
    }
    return render(request,'judge/MySubmissions.html',context)

#======================================================================================#
@login_required
def SubmissionDetail(request,CodePath):
    return HttpResponse(str(CodePath))