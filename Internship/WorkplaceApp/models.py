from django.db import models
import uuid



# class UnassignedStudentsManager(models.Manager):
#     def get_queryset(self):
#         # Get all students who are not assigned to any lecturers
#         return super().get_queryset().exclude(lecturers__isnull=False)


class studentDataTable(models.Model):
    stuid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=200)
    tel = models.CharField(max_length=50)
    university = models.CharField(max_length=200)
    degree = models.TextField(blank=True, null=True)
    linkedin = models.CharField(blank=True, null=True, max_length=1000)
    createtimestamp = models.DateTimeField(auto_now_add=True)
    updatetimestamp = models.DateTimeField(auto_now_add=True)
    profilepic = models.ImageField(null=True, blank=True)
    username = models.CharField(unique=True, max_length=200)
    password = models.CharField(max_length=100)

    # objects = UnassignedStudentsManager()

    def __str__(self):
        return self.firstname + " " + self.lastname


class lecturerDataTable(models.Model):
    lecid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    email = models.CharField(max_length=200)
    tel = models.CharField(max_length=50)
    createtimestamp = models.DateTimeField(auto_now_add=True)
    updatetimestamp = models.DateTimeField(auto_now_add=True)
    username = models.CharField(unique=True, max_length=200)
    password = models.CharField(max_length=100)
    address = models.CharField(max_length=100, blank=True, null=True)
    profilepic = models.ImageField(null=True, blank=True)
    students = models.ManyToManyField(
        "studentDataTable", blank=True, related_name="lecturers"
    )

    def __str__(self):
        return self.username


# student log, added later
class StdntLog(models.Model):
    stuid = models.CharField(max_length=200, default=None)
    title = models.CharField(max_length=200)
    date = models.DateField()
    summary = models.TextField()
    description = models.TextField()
    lect_comment = models.TextField(default=None, null=True)

    def __str__(self):
        return self.date.strftime("%Y-%m-%d") + " -> " + self.title


# ends here


class companyDataTable(models.Model):
    comid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    companyname = models.CharField(max_length=100)
    comregno = models.CharField(max_length=500)
    address = models.TextField(blank=True, null=True)
    email = models.CharField(max_length=200)
    tel = models.CharField(max_length=50)
    preffield = models.CharField(max_length=300)
    linkedin = models.CharField(blank=True, null=True, max_length=1000)
    createtimestamp = models.DateTimeField(auto_now_add=True)
    updatetimestamp = models.DateTimeField(auto_now_add=True)
    profilepic = models.ImageField(null=True, blank=True)
    username = models.CharField(unique=True, max_length=200)
    password = models.CharField(max_length=100)


# lecturer table


class flyerdata(models.Model):
    flyerid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    company = models.ForeignKey(
        companyDataTable, on_delete=models.CASCADE, null=True, blank=True
    )
    jobfield = models.CharField(max_length=100)
    jobpost = models.CharField(max_length=100)
    salary = models.CharField(max_length=50)
    location = models.CharField(max_length=1000)
    flyerimage = models.ImageField()
    createtimestamp = models.CharField(max_length=30)
    updatetimestamp = models.CharField(max_length=30)


class studentfavorite(models.Model):
    flyer = models.ForeignKey(
        flyerdata, on_delete=models.CASCADE, null=True, blank=True
    )
    student = models.ForeignKey(
        studentDataTable, on_delete=models.CASCADE, null=True, blank=True
    )


class studentapply(models.Model):
    flyer = models.ForeignKey(
        flyerdata, on_delete=models.CASCADE, null=True, blank=True
    )
    student = models.ForeignKey(
        studentDataTable, on_delete=models.CASCADE, null=True, blank=True
    )


class message(models.Model):
    msgid = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    msg = models.TextField(blank=True, null=True)
    student = models.ForeignKey(
        studentDataTable, on_delete=models.CASCADE, null=True, blank=True
    )
    company = models.ForeignKey(
        companyDataTable, on_delete=models.CASCADE, null=True, blank=True
    )
    sender = models.CharField(max_length=200)
    senderID = models.CharField(max_length=200, blank=True, null=True)
    Receiver = models.CharField(max_length=200)
    ReceiverID = models.CharField(max_length=200, blank=True, null=True)
    MarkAsRead = models.CharField(max_length=5, blank=True, null=True)
    createtimestamp = models.CharField(max_length=30)


class StuNotification(models.Model):
    StuNotificationId = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    notification = models.TextField(blank=True, null=True)
    student = models.ForeignKey(
        studentDataTable, on_delete=models.CASCADE, null=True, blank=True
    )
    createtimestamp = models.CharField(max_length=30, blank=True, null=True)
    MarkAsRead = models.CharField(max_length=5, blank=True, null=True)


class ComNotification(models.Model):
    ComNotificationId = models.UUIDField(
        default=uuid.uuid4, primary_key=True, editable=False, unique=True
    )
    notification = models.TextField(blank=True, null=True)
    company = models.ForeignKey(
        companyDataTable, on_delete=models.CASCADE, null=True, blank=True
    )
    createtimestamp = models.CharField(max_length=30, blank=True, null=True)
    MarkAsRead = models.CharField(max_length=5, blank=True, null=True)
