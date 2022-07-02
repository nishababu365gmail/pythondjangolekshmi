from django.db import models
class course(models.Model):
    course_id=models.IntegerField(auto_created=True,primary_key=True)
    course_name=models.CharField(max_length=50)
    def __str__(self):
        return self.course_name

class student(models.Model):
    student_id=models.IntegerField(primary_key=True,auto_created=True)
    student_fname=models.CharField(max_length=50,verbose_name="First Name")
    student_age=models.IntegerField()
    student_date_of_birth=models.DateField()
    student_courses=models.ManyToManyField("course",through ="studentcourse",related_name="student")
    def __str__(self):
        return self.student_fname

class studentcourse(models.Model):
    student_course_id=models.IntegerField(primary_key=True,auto_created=True)
    student=models.ForeignKey(student,related_name="student_course",null=True, on_delete=models.SET_NULL)
    course=models.ForeignKey(course,related_name="student_course",null=True,on_delete=models.SET_NULL)        


class Sweets(models.Model):
    sweet_name = models.CharField(max_length=50)
    sweet_color = models.CharField(max_length=50)
    sweet_shape = models.CharField(max_length=20)


class State(models.Model):
    state_name = models.CharField(max_length=20, null=True)

    def __str__(self):
        return self.state_name


class City(models.Model):
    city_id=models.IntegerField(primary_key=True,auto_created=True)
    city_name = models.CharField(max_length=30, default=1)
    state = models.ForeignKey(State, models.PROTECT)


class Employee(models.Model):
    state_choices = State.objects.values_list("id", "state_name")
    
    employee_fname = models.CharField(
        max_length=50,
        help_text="This is first name of Employee",
        verbose_name="First Name",
    )
    employee_lname = models.CharField(max_length=50)
    employee_adharnos = models.CharField(max_length=20)
    employee_age = models.IntegerField(default=0)
    employee_state = models.ForeignKey(State, models.PROTECT)    
    


class Vendor(models.Model):
    vendorname = models.CharField(max_length=20)

    def __str__(self):
        return self.vendorname


class PurchaseMaster(models.Model):
    purchaseno = models.CharField(max_length=20)
    purchasedate = models.IntegerField()
    invoiceno = models.CharField(max_length=20)
    invoicedate = models.DateField()
    vendor = models.ForeignKey(Vendor, max_length=30, on_delete=models.PROTECT)

    def __str__(self):
        return f"purchaseno for {self.invoiceno}"


class ItemMaster(models.Model):
    itemname = models.CharField(max_length=20)

    def __str__(self):
        return str(self.itemname)


class PurchaseDetail(models.Model):
    purchaseno = models.ForeignKey(
        PurchaseMaster, max_length=20, on_delete=models.PROTECT
    )
    purchaseitem = models.ForeignKey(
        ItemMaster, max_length=30, on_delete=models.PROTECT
    )
    quantity = models.DecimalField(max_digits=7, decimal_places=3)
    rate = models.DecimalField(max_digits=7, decimal_places=3)

    def __str__(self):
        return str(self.purchaseno)
