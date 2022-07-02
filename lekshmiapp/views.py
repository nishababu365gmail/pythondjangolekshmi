from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from lekshmiapp.forms import (simpleinputform, 
EmployeeModelForm,SimpleForm,studentmodelform,citymodelform,rdbuttonform,testcustomsvalidators)
from lekshmiapp.models import Employee, State,studentcourse,course,student
from django.core.paginator import Paginator 
from django.db.models import Count
from django.db import connection
import os.path
import sqlite3
from django.conf import settings
#the following function can be used when 
# filter function is called on Employee 
# object along with values function
def ValuesQuerySetToDict(vqs):
    return [item for item in vqs]
# the following function is called when filter
# function is called on Employeee object without values function.
# here we nned to convert each employee object to a dictionarry
#  and add that dict to another dict    
def ValuesQuerySetToDict1(vqs):
    returndic={}
    localdic={}
    for item in vqs:
        localdic["employee_fname"]=item.employee_fname
        localdic["employee_lname"]=item.employee_lname
        localdic["employee_adharnos"]=item.employee_adharnos
        localdic["employee_age"]=item.employee_age
        
        returndic[item.employee_fname]=localdic        
        localdic={}
    return returndic
def CreateCity(request):
    template_name='lekshmiapp/CreateCity.html'
    citymodelformobj= citymodelform()
    context={'citymdlform':citymodelformobj}
    if request.method=="GET":
        return render(request,template_name,context)
    else:
        
       
        citymodelformobj=citymodelform(request.POST)
        if citymodelformobj.is_valid():
            citymodelformobj.save()
          
        context={'citymdlform':citymodelformobj}
        return render(request,template_name,context)

def CreateStudent(request):
    template_name='lekshmiapp/CreateStudent.html'
    studentcourseobj=studentcourse()
    studentobj=student()
    if request.method=="GET":
        studentform=studentmodelform()
        context={'studentform':studentform}
        return render(request,template_name,context)
    else:
        studentform=studentmodelform(request.POST)
        if studentform.is_valid():
           todo_list=studentform.save(commit=False) 
           stobj=student.objects.last()
           idincremented= (stobj.student_id+1)
           todo_list.student_id=idincremented                    
           todo_list.save()
           studentform.save_m2m()
           #The following is another method
            # print('kunjamu')          
            # courselist=studentform.cleaned_data['student_courses']  
                
            # studentobj.student_fname=  studentform.cleaned_data['student_fname']
            # studentobj.student_age=studentform.cleaned_data['student_age']
            # studentobj.student_date_of_birth=studentform.cleaned_data['student_date_of_birth']
            # studentobj.save()
            # instance=student.objects.last()
            # studentinstance=student.objects.get(student_id=instance.student_id)
            # for item in courselist:                
            #     studentinstance.student_courses.add(item)          
        context={'studentform':studentform}      
        return render(request,template_name,context)
        
    return render(request,template_name,context)
        
def search1(request):
    print('i a m in search1')
    template_name='lekshmiapp/search.html'
    searchterm=''
    mydict={}
    if request.method=="GET": 
        emplist=Employee.objects.all()       
        data_dict=ValuesQuerySetToDict1(emplist)      
        context={'searchterm':searchterm,'searchlist':emplist}
        return render(request,template_name,context)  
def iamfromfetch(request):
    print('hello nisha ababu vava')
    foo=request.GET.get('foo')
    bar=request.GET.get('bar')
    print(foo)
    print(bar)
    return JsonResponse('nisha',safe=False)        
def commonfunc(request):
    
    modelname=request.GET.get('objectname')
    columnname=request.GET.get('columnname')
    columnvalue=request.GET.get('columnvalue')
    columnvalue="'"+columnvalue+"'"
    appname='lekshmiapp_'
    # columnvalue='iop'
    print(modelname)
    dbpath=settings.DATABASES['default']['NAME']
    
    IsPresent=False
    with sqlite3.connect(dbpath) as db:
        cursor = db.cursor()
        #cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
       
        # select_stmt = ("SELECT * FROM lekshmiapp_"+modelname+" WHERE "+columnname + " ='"+ columnvalue +"'")
        select_stmt = f"SELECT * FROM {appname}{modelname} WHERE  {columnname}={columnvalue}"
        
        cursor.execute(select_stmt)
        row = cursor.fetchall()
        print(len(row))
        if len(row)>=1:
            IsPresent=True
        else:
            IsPresent=False     
    
    return JsonResponse(IsPresent,safe=False)        
def search2(request,myterm=None,pagenum=None):
     print('helllo')
     if request.method=="GET":
        searchterm=request.GET.get("myterm")
        pagenum=request.GET.get("pagenum")
        if pagenum!=None:
            intpagenum=int(pagenum)
            print(pagenum)
        else:
            intpagenum=2    
        if searchterm!=None:
           print('i am searchterm')
           # emplist=Employee.objects.filter(employee_fname__contains=searchterm).values('employee_fname','employee_lname','pk')
           if intpagenum>0:
                startnum=(intpagenum-1)*2
                endnum=startnum+2
                print(searchterm)
                #emplist=Employee.objects.filter(employee_fname__contains=searchterm).values('employee_fname','employee_lname','pk')[3:2]
                emplist=Employee.objects.filter(employee_fname__contains=searchterm).order_by('employee_fname')[startnum:endnum]
                             
                print(emplist)
                
                data_dict=ValuesQuerySetToDict1(emplist)
                return JsonResponse(data_dict,safe=False)
           else:
                emplist=Employee.objects.filter(employee_fname__contains=searchterm).order_by('employee_fname')
                data_dict=ValuesQuerySetToDict1(emplist)
                     
                return JsonResponse(data_dict,safe=False)  
        else:
            emplist=Employee.objects.all()
            data_dict=ValuesQuerySetToDict1(emplist)                     
            return JsonResponse(data_dict,safe=False)  

        
def search(request):
    print('i a m in search')
    template_name='lekshmiapp/search.html'
    searchterm=''
    mydict={}
    if request.method=="GET":
        searchterm=request.GET.get("myterm")     
          
        if searchterm!=None:         
            totalcount=Employee.objects.filter(employee_fname__contains=searchterm).count()
            emplist=Employee.objects.filter(employee_fname__contains=searchterm).order_by('employee_fname')[0:2]
            data_dict=ValuesQuerySetToDict1(emplist) 
             
            data_dict["totalcount"]={'querysetcount':totalcount}
            print(data_dict)  
            return JsonResponse(data_dict,safe=False)  
        else:

            emplist=Employee.objects.all().order_by('employee_fname')
            data_dict=ValuesQuerySetToDict1(emplist)                     
            return JsonResponse(data_dict,safe=False)  

    if request.method=="POST":
        searchterm=request.POST.get("searchterm") 
        
        if searchterm!=None:
            emplist=Employee.objects.filter(employee_fname__contains=searchterm)
        context={'searchterm':searchterm,'searchlist':emplist}
        return render(request,template_name,context)   

def simpleView(request):
    return HttpResponse("<h1>Hi from Lekshmi</h1>")


def index(request):
    context = {"name": "Nisha", "university": "FIT", "company": "UST"}
    return render(request, "lekshmiapp/base.html", context)


def formwithcontrolsview(request):
    if request.method == "POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        context = {"firstname": fname, "lastname": lname}
        return render(request, "lekshmiapp/simpleform.html", context)
    elif request.method == "GET":
        context = {"method": "GET"}
        return render(request, "lekshmiapp/simpleform.html", context)


def formwithformclass(request):
    form = simpleinputform()
    empmodel = Employee()
    context = {"myform": form}
    if request.method == "POST":
        form = simpleinputform(request.POST)
        if form.is_valid():
            fname = form.cleaned_data["fname"]
            lname = form.cleaned_data["lname"]
            adharno = form.cleaned_data["adharno"]
            age = form.cleaned_data["age"]
            empmodel.employee_fname = fname
            empmodel.employee_lname = lname
            empmodel.employee_adharnos = adharno
            empmodel.employee_age = age
            empmodel.save()
            context = {
                "myform": form,
                "sdfname": fname,
                "sdlname": lname,
                "sdadharno": adharno,
            }
        return render(request, "lekshmiapp/simpleformclass.html", context)
    else:
        return render(request, "lekshmiapp/simpleformclass.html", context)


def formwithmodelandclassichtml(request, fname=None):
    empmodel = Employee()
    inputform = simpleinputform()
    context = {}
    if request.method == "GET":
        if fname == None:
            inputform = simpleinputform()
            context = {"myform": inputform}
        elif fname != None:
            empobj = Employee.objects.get(employee_fname=fname)
            data_dict = {
                "fname": empobj.employee_fname,
                "lname": empobj.employee_lname,
                "age": empobj.employee_age,
                "adharno": empobj.employee_adharnos,
            }
            inputform = simpleinputform(data_dict)
            context = {"myform": inputform}

        return render(request, "lekshmiapp/simpleformwithmodel.html", context)

    elif request.method == "POST":
        empmodel.employee_fname = request.POST.get("fname")
        empmodel.employee_lname = request.POST.get("lname")
        empmodel.employee_adharnos = request.POST.get("adharno")
        empmodel.employee_age = request.POST.get("age")
        empmodel.save()
        context = {
            "myform": inputform,
            "firstname": empmodel.employee_fname,
            "lastname": empmodel.employee_lname,
            "adharno": empmodel.employee_adharnos,
            "age": empmodel.employee_age,
        }
        return render(request, "lekshmiapp/simpleformwithmodel.html", context)


# cmbselect_3:9,cmbselect_1:5,cmbselect_6:5,cmbselect_4:5,
def formwithmodelform(request):
    empmodel = EmployeeModelForm()
    context = {"myform": empmodel}
    if request.method == "GET":
        return render(request, "lekshmiapp/examplewithmodelform.html", context=context)
    elif request.method == "POST":
        empmodel = EmployeeModelForm(request.POST)
        if empmodel.is_valid():
            empmodel.save()
            context = {"myform": empmodel}
            return render(request, "lekshmiapp/examplewithmodelform.html", context)

        else:
            empmodel = EmployeeModelForm()
            context = {"myform": empmodel}
            return render(request, "lekshmiapp/examplewithmodelform.html", context)


def formemplist(request):
    if request.method == "GET":
        emplist = Employee.objects.all()
        context = {"emplist": emplist}
        return render(request, "lekshmiapp/exampleemplist.html", context=context)
def nishafunc(request):
    myform=SimpleForm()
    if request.method=="GET":
        
        context={'myform':myform}
        return render(request, "lekshmiapp/nisha.html", context=context)
    if request.method=="POST":
        print(request.POST)
        myform=SimpleForm(request.POST)
        if myform.is_valid():
            context={'myform':myform}
            return render(request, "lekshmiapp/nisha.html", context=context)
    return render(request, "lekshmiapp/nisha.html", context=context)              

def babu(request):
    if request.method=="GET":
        page_num = request.GET.get('page',1)
        query = request.GET.get('searchterm','') 
        print(query) 
        if query.find('/')!=-1:
           query=query.replace('/','') 
        if query!='':
            books = Employee.objects.filter(employee_fname__contains=query).order_by('employee_fname') 
        else:    
            books = Employee.objects.all().order_by('employee_fname')                      
        print(books)
        book_paginator = Paginator(books, 3)
        page = book_paginator.get_page(page_num)
        book_paginator = Paginator(books, 3)
    context = {
    'count' : book_paginator.count,
    'page' : page,
    'searchterm':query
    }   
    return render(request, 'lekshmiapp/newsearch.html', context)
def manytomanytraversal(request):
    template_name='lekshmiapp/manytomanytraversal.html'
    if request.method=="GET":
        # studentlist=studentcourse.objects.all().values_list('student__student_fname').annotate(total=Count('student__student_fname')).order_by( 'student__student_fname')
        studentlst=studentcourse.objects.distinct().values_list('student__student_id')
        stucoursedict={}
        courselist=[]
        # hi=course.objects.get(course_name='VB').student_course.all().values_list('student__student_fname')
        for obj in studentlst:
            studentname=student.objects.get(student_id=obj[0]).student_fname
            for item in studentcourse.objects.filter(student=student.objects.get(student_id=obj[0])):
                print(item.course)
                courselist.append(item.course.course_name)
            stucoursedict[studentname]=courselist
            courselist=[]
        print(stucoursedict)    
        # for item in studentlist:
        #     print(item)
            # print(student.objects.get(student_id=item[0]))
        context={'mylist':stucoursedict}
        return render(request,template_name,context)
            
def rdbuttonCheck(request):
    template_name='lekshmiapp/radiobuttonmultiple.html'
    myrdfrm=rdbuttonform()
    context={'myform':myrdfrm}
    return render (request,template_name,context)

def testcustomvalidators(request):
    print('hiiiii')
    if request.method=="GET":        
        template_name='lekshmiapp/mycustomvalidators.html'
        myform=testcustomsvalidators()
        context={'myform':myform}    
        return render(request,template_name,context)
    else:
        
        template_name='lekshmiapp/mycustomvalidators.html'
        myform=testcustomsvalidators(request.POST)
        if myform.is_valid():
            print('I am valid')
            context={'myform':myform}    
            return render(request,template_name,context)
        else:
            context={'myform':myform}  
            return render(request,template_name,context)