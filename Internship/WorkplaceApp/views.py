from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from .models import (
    studentDataTable,
    companyDataTable,
    flyerdata,
    studentfavorite,
    studentapply,
    message,
    ComNotification,
    StuNotification,
    StdntLog,
    lecturerDataTable,
)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import datetime
from itertools import groupby


def selectacctype(request):
    return render(request, "selectacctype.html")


def createstuacc(request):
    if request.method == "POST":
        fname = request.POST["firstname"]
        lname = request.POST["lastname"]
        address = request.POST["address"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        uni = request.POST["uni"]
        degree = request.POST["degree"]
        propic = request.FILES.get("stupropic")
        linkedin = request.POST["acc"]
        username = request.POST["username"]
        password = request.POST["password"]

        if studentDataTable.objects.filter(email=email).exists():
            messages.info(request, "Email already taken! Try with another email")
            return redirect("stuacc")
        elif studentDataTable.objects.filter(username=username).exists():
            messages.info(request, "Username already taken! Try with another username")
            return redirect("stuacc")
        else:
            createu = studentDataTable.objects.create(
                firstname=fname,
                lastname=lname,
                address=address,
                email=email,
                tel=phone,
                university=uni,
                degree=degree,
                linkedin=linkedin,
                username=username,
                password=password,
                profilepic=propic,
            )
            createu.save()
            messages.info(request, "Student user account created successfully!")
            return redirect("stuacc")
    else:
        return render(request, "createstuacc.html")


def createcomacc(request):
    if request.method == "POST":
        comname = request.POST["companyname"]
        regnmbr = request.POST["regnumber"]
        address = request.POST["Address"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        prefield = request.POST["prefield"]
        propic = request.FILES.get("compropic")
        linkedin = request.POST["comlinkedin"]
        username = request.POST["username"]
        password = request.POST["password"]

        if companyDataTable.objects.filter(email=email).exists():
            messages.info(request, "Email already taken!")
            return redirect("comacc")
        elif companyDataTable.objects.filter(username=username).exists():
            messages.info(request, "Username already taken!")
            return redirect("comacc")
        else:
            createu = companyDataTable.objects.create(
                companyname=comname,
                comregno=regnmbr,
                address=address,
                email=email,
                tel=phone,
                preffield=prefield,
                linkedin=linkedin,
                username=username,
                password=password,
                profilepic=propic,
            )
            createu.save()
            messages.info(request, "Company user account created succefully!")
            return redirect("comacc")

    else:
        return render(request, "createcomacc.html")


# login views
def login(request):
    if request.method == "POST":
        acctype = request.POST["acctype"]
        username = request.POST["username"]
        password = request.POST["password"]
        # student login
        if acctype == "student":
            if studentDataTable.objects.filter(username=username).exists():
                studb = studentDataTable.objects.get(username=username)
                if studb.password == password:
                    stuid = studb.stuid
                    return redirect("stufeed", stuid)
                else:
                    messages.info(request, "Wrong password entered!")
                    return redirect("login")
            else:
                messages.info(request, "Invalid Credentials!")
                return redirect("login")
            # company login
        elif acctype == "company":
            if companyDataTable.objects.filter(username=username).exists():
                comdb = companyDataTable.objects.get(username=username)
                if comdb.password == password:
                    comid = comdb.comid
                    return redirect("addpost", comid)
                else:
                    messages.info(request, "Wrong password entered!")
                    return redirect("login")
            else:
                messages.info(request, "Invalid Credentials!")
                return redirect("login")
            # lecturer login
        else:
            if lecturerDataTable.objects.filter(username=username).exists():
                lecdb = lecturerDataTable.objects.get(username=username)
                if lecdb.password == password:
                    lecid = lecdb.lecid
                    return redirect("lec_home", lecid)
                else:
                    messages.info(request, "Wrong password entered!")
                    return redirect("login")
            else:
                messages.info(request, "Invalid Credentials!")
                return redirect("login")
    else:
        return render(request, "login.html")


def comaddpost(request, comid):
    comdb = companyDataTable.objects.get(comid=comid)
    if request.method == "POST":
        jobfield = request.POST["jobfield"]
        jobpost = request.POST["jobpost"]
        salary = request.POST["salary"]
        location = request.POST["location"]
        flyerimg = request.FILES.get("flyerimg")
        current_datetime = datetime.datetime.now()
        dateTime = current_datetime.replace(microsecond=0)

        newflyer = flyerdata.objects.create(
            company=comdb,
            jobfield=jobfield,
            jobpost=jobpost,
            salary=salary,
            location=location,
            flyerimage=flyerimg,
            createtimestamp=dateTime,
            updatetimestamp=dateTime,
        )
        newflyer.save()
        messages.info(request, "New post created successfully!")
        return redirect("addpost", comid)

    return render(request, "company/comaddpost.html", {"comdb": comdb})


def mypost(request, comid):
    comdb = companyDataTable.objects.get(comid=comid)
    flyers = flyerdata.objects.filter(company=comdb)
    return render(request, "company/mypost.html", {"comdb": comdb, "flyers": flyers})


def editpost(request, comid, fid):
    comdb = companyDataTable.objects.get(comid=comid)
    flyer = flyerdata.objects.get(flyerid=fid)
    if request.method == "POST":
        jobfield = request.POST["jobfield"]
        jobpost = request.POST["jobpost"]
        salary = request.POST["salary"]
        location = request.POST["location"]
        flyerimg = request.FILES.get("flyerimg")
        current_datetime = datetime.datetime.now()
        dateTime = current_datetime.replace(microsecond=0)

        flyer.jobfield = jobfield
        flyer.jobpost = jobpost
        flyer.salary = salary
        flyer.location = location
        flyer.flyerimage = flyerimg
        flyer.updatetimestamp = dateTime
        flyer.save()
        messages.info(request, "Post updated successfully!")
        return redirect("editpost", comid, fid)

    return render(request, "company/editpost.html", {"comdb": comdb, "flyer": flyer})


def deletepost(request, comid, fid):
    flyer = flyerdata.objects.get(flyerid=fid)
    flyer.delete()
    messages.info(request, "Post Deleted succesfully!")
    return redirect("mypost", comid)


def ComNotifications(request, comid):
    comdb = companyDataTable.objects.get(comid=comid)
    newNotifications = ComNotification.objects.filter(company=comdb, MarkAsRead="0")
    oldNotifications = ComNotification.objects.filter(company=comdb, MarkAsRead="1")
    return render(
        request,
        "company/comnotification.html",
        {
            "comdb": comdb,
            "newNotifications": newNotifications,
            "oldNotifications": oldNotifications,
        },
    )


def markasreadCom(request, comid, notid):
    notidb = ComNotification.objects.get(ComNotificationId=notid)
    notidb.MarkAsRead = "1"
    notidb.save()
    return redirect("ComNotifications", comid)


def commsg(request, comid):
    comdb = companyDataTable.objects.get(comid=comid)
    newmsgdb = message.objects.filter(ReceiverID=comid, MarkAsRead="0")
    oldmsgdb = message.objects.filter(ReceiverID=comid, MarkAsRead="1")
    return render(
        request,
        "company/commsg.html",
        {"comdb": comdb, "newmsgdb": newmsgdb, "oldmsgdb": oldmsgdb},
    )


def msgseen(request, comid, msgid):
    msgdb = message.objects.get(msgid=msgid)
    msgdb.MarkAsRead = "1"
    msgdb.save()
    return redirect("commsg", comid)


def comchat(request, comid, senderid):
    comdb = companyDataTable.objects.get(comid=comid)
    studb = studentDataTable.objects.get(stuid=senderid)
    chatdb = message.objects.filter(
        ReceiverID__in=[comid, senderid], senderID__in=[senderid, comid]
    )
    if request.method == "POST":
        msg = request.POST["newmsg"]
        current_datetime = datetime.datetime.now()
        dateTime = current_datetime.replace(microsecond=0)
        newmsg = message.objects.create(
            msg=msg,
            student=studb,
            company=comdb,
            sender=comdb.companyname,
            senderID=comdb.comid,
            Receiver=studb.firstname + " " + studb.lastname,
            ReceiverID=studb.stuid,
            MarkAsRead="0",
            createtimestamp=dateTime,
        )
        newmsg.save()
        return redirect("comchat", comid, senderid)

    return render(
        request, "company/commsgbody.html", {"comdb": comdb, "chatdb": chatdb}
    )


def stufeed(request, stuid):
    if request.method == "POST":
        field = request.POST["fieldselect"]
        # salary = request.POST['salaryrange']
        location = request.POST["location"]
        position = request.POST["position"]

        studb = studentDataTable.objects.get(stuid=stuid)
        stufavdb = studentfavorite.objects.filter(student=studb)
        stuapply = studentapply.objects.filter(student=studb)
        flyerdb = flyerdata.objects.filter(
            jobfield__contains=field,
            location__contains=location,
            jobpost__contains=position,
        )
        return render(
            request,
            "student/stufeed.html",
            {
                "studb": studb,
                "flyerdb": flyerdb,
                "stufavdb": stufavdb,
                "stuapply": stuapply,
            },
        )
    else:
        studb = studentDataTable.objects.get(stuid=stuid)
        flyerdb = flyerdata.objects.all()
        stufavdb = studentfavorite.objects.filter(student=studb)
        stuapply = studentapply.objects.filter(student=studb)
        return render(
            request,
            "student/stufeed.html",
            {
                "studb": studb,
                "flyerdb": flyerdb,
                "stufavdb": stufavdb,
                "stuapply": stuapply,
            },
        )


def addtofav(request, stuid, fid):
    studb = studentDataTable.objects.get(stuid=stuid)
    flyrdb = flyerdata.objects.get(flyerid=fid)
    if studentfavorite.objects.filter(student=studb, flyer=flyrdb).exists():
        messages.info(request, "Already added to favorites!")
        return redirect("stufeed", stuid)

    newfavstu = studentfavorite.objects.create(flyer=flyrdb, student=studb)
    newfavstu.save()
    messages.info(request, "Post added to favorites!")
    return redirect("stufeed", stuid)


def stufav(request, stuid):
    studb = studentDataTable.objects.get(stuid=stuid)
    stufav = studentfavorite.objects.filter(student=studb)
    stuapply = studentapply.objects.filter(student=studb)
    return render(
        request,
        "student/stufavorite.html",
        {"studb": studb, "stufav": stufav, "stuapply": stuapply},
    )


def removefrmfav(request, stuid, fid):
    studb = studentDataTable.objects.get(stuid=stuid)
    flyrdb = flyerdata.objects.get(flyerid=fid)
    post = studentfavorite.objects.get(student=studb, flyer=flyrdb)
    post.delete()
    messages.info(request, "Post removed from favorites!")
    return redirect("stufav", stuid)


def apply(request, stuid, fid):
    studb = studentDataTable.objects.get(stuid=stuid)
    flyrdb = flyerdata.objects.get(flyerid=fid)
    current_datetime = datetime.datetime.now()
    dateTime = current_datetime.replace(microsecond=0)

    if studentapply.objects.filter(student=studb, flyer=flyrdb).exists():
        messages.info(request, "You already applied for this!")
        return redirect("stufeed", stuid)

    stuapply = studentapply.objects.create(flyer=flyrdb, student=studb)
    stuapply.save()
    newMsg = message.objects.create(
        msg="I want to apply to the job vacancy on "
        + flyrdb.jobpost
        + " in "
        + flyrdb.jobfield
        + " that you posted at "
        + flyrdb.updatetimestamp,
        student=studb,
        company=flyrdb.company,
        sender=studb.firstname + " " + studb.lastname,
        senderID=studb.stuid,
        Receiver=flyrdb.company.companyname,
        ReceiverID=flyrdb.company.comid,
        MarkAsRead="0",
        createtimestamp=dateTime,
    )
    newMsg.save()
    Comnewnotification = ComNotification.objects.create(
        notification=studb.firstname
        + " "
        + studb.lastname
        + " want to apply to the job vacancy on "
        + flyrdb.jobpost
        + " in "
        + flyrdb.jobfield
        + " that you posted at "
        + flyrdb.updatetimestamp,
        company=flyrdb.company,
        createtimestamp=dateTime,
        MarkAsRead="0",
    )
    Comnewnotification.save()
    Stunewnotification = StuNotification.objects.create(
        notification="You send a apply request for the job vacancy on "
        + flyrdb.jobpost
        + " in "
        + flyrdb.jobfield
        + " that posted by "
        + flyrdb.company.companyname
        + " at "
        + flyrdb.updatetimestamp,
        student=studb,
        createtimestamp=dateTime,
        MarkAsRead="0",
    )
    Stunewnotification.save()
    messages.info(request, "Apply message sent to the company")
    return redirect("stufeed", stuid)


def StuNotifications(request, stuid):
    studb = studentDataTable.objects.get(stuid=stuid)
    newNotifications = StuNotification.objects.filter(student=studb, MarkAsRead="0")
    oldNotifications = StuNotification.objects.filter(student=studb, MarkAsRead="1")
    return render(
        request,
        "student/stunotification.html",
        {
            "studb": studb,
            "newNotifications": newNotifications,
            "oldNotifications": oldNotifications,
        },
    )


def markasreadStu(request, stuid, notid):
    notidb = StuNotification.objects.get(StuNotificationId=notid)
    notidb.MarkAsRead = "1"
    notidb.save()
    return redirect("StuNotifications", stuid)


def stumsg(request, stuid):
    studb = studentDataTable.objects.get(stuid=stuid)
    newmsgdb = message.objects.filter(ReceiverID=stuid, MarkAsRead="0")
    oldmsgdb = message.objects.filter(ReceiverID=stuid, MarkAsRead="1")
    return render(
        request,
        "student/stumsg.html",
        {"studb": studb, "newmsgdb": newmsgdb, "oldmsgdb": oldmsgdb},
    )


def stumsgseen(request, stuid, msgid):
    msgdb = message.objects.get(msgid=msgid)
    msgdb.MarkAsRead = "1"
    msgdb.save()
    return redirect("stumsg", stuid)


def stuchat(request, stuid, senderid):
    comdb = companyDataTable.objects.get(comid=senderid)
    studb = studentDataTable.objects.get(stuid=stuid)
    chatdb = message.objects.filter(
        ReceiverID__in=[stuid, senderid], senderID__in=[senderid, stuid]
    )
    if request.method == "POST":
        msg = request.POST["newmsg"]
        current_datetime = datetime.datetime.now()
        dateTime = current_datetime.replace(microsecond=0)
        newmsg = message.objects.create(
            msg=msg,
            student=studb,
            company=comdb,
            sender=studb.firstname + " " + studb.lastname,
            senderID=studb.stuid,
            Receiver=comdb.companyname,
            ReceiverID=comdb.comid,
            MarkAsRead="0",
            createtimestamp=dateTime,
        )
        newmsg.save()
        return redirect("stuchat", stuid, senderid)

    return render(
        request, "student/stumsgbody.html", {"studb": studb, "chatdb": chatdb}
    )


def viewCompany(request, stuid, comid):
    comdb = companyDataTable.objects.get(comid=comid)
    studb = studentDataTable.objects.get(stuid=stuid)

    return render(request, "student/viewcompany.html", {"studb": studb, "comdb": comdb})


def logout(request):
    auth.logout(request)
    return redirect("login")


# student log, added later
from django.shortcuts import render, get_object_or_404


def stulog(request, stuid):
    studb = get_object_or_404(studentDataTable, stuid=stuid)
    stulogs = StdntLog.objects.filter(stuid=studb.stuid)
    return render(request, "student/stulog.html", {"studb": studb, "logs": stulogs})


def LogCreateView(request):
    if request.method == "POST":
        stuid = request.POST.get("stuid")
        title = request.POST.get("title")
        date = request.POST.get("date")
        summary = request.POST.get("summary")
        description = request.POST.get("description")

        student_log = StdntLog(
            stuid=stuid,
            title=title,
            date=date,
            summary=summary,
            description=description,
        )
        student_log.save()

        studb = get_object_or_404(studentDataTable, stuid=stuid)
        stulogs = StdntLog.objects.filter(
            stuid=studb.stuid
        )  # Assuming stuid is a foreign key in StdntLog
        print(stulogs)
        print(studb)
        return render(request, "student/stulog.html", {"studb": studb, "logs": stulogs})


def LecHome(request, lecid):
    lecturer_student_names = {}
    lecdb = get_object_or_404(lecturerDataTable, lecid=lecid)

    # Get all student IDs linked to the lecturer
    student_ids = lecdb.students.values_list("stuid", flat=True)
    for i in student_ids:
        student_name = studentDataTable.objects.get(stuid=i)
        lecturer_student_names.update({i: student_name})

    for name in lecturer_student_names:
        print(lecturer_student_names[name])

    return render(
        request,
        "lecturer/lec_home.html",
        {"lecdb": lecdb, "student_names": lecturer_student_names},
    )


def lec_student_logs(request, student_id):
    studb = get_object_or_404(studentDataTable, stuid=student_id)
    stulogs = StdntLog.objects.filter(stuid=studb.stuid)
    return render(
        request, "lecturer/student_logs.html", {"studb": studb, "logs": stulogs}
    )


def add_comment(request, student_id):
    if request.method == "POST":
        log_id = request.POST.get("log_id")
        log_entry = get_object_or_404(StdntLog, id=log_id)

        comment = request.POST.get("comment")
        log_entry.lect_comment = comment
        log_entry.save()

        # Redirect to a success page or the log entry page
        studb = get_object_or_404(studentDataTable, stuid=student_id)
        stulogs = StdntLog.objects.filter(stuid=studb.stuid)
        return render(
            request, "lecturer/student_logs.html", {"studb": studb, "logs": stulogs}
        )

    # generate report
    from django.http import HttpResponse


from reportlab.pdfgen import canvas
from io import BytesIO
from django.http import HttpResponse


from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph

def generate_pdf(request, stuid):
    studb = get_object_or_404(studentDataTable, stuid=stuid)
    stulogs = StdntLog.objects.filter(stuid=studb.stuid)
    # Create a file-like buffer to receive PDF data.
    buffer = BytesIO()

    # Create the PDF object, using the buffer as its "file."
    p = canvas.Canvas(buffer, pagesize=letter)

    # Starting position for the first log entry.
    x = 100
    y = 800 # Start from the top of the page.

    # Set the font to bold
    p.setFont("Helvetica-Bold", 14)

    # Draw things on the PDF. Here's where the PDF generation happens.
    # For example, let's say you have a list of logs that you want to print:
    logs = stulogs # Retrieve the logs from the database
    for log in logs:
        # Draw the title in bold
        p.drawString(x, y, f"Title: {log.title}")
        y -= 20 # Move to the next line for the title

        # Reset the font to normal weight
        p.setFont("Helvetica", 12)

        # Draw the date and summary
        p.drawString(x, y, f"Date: {log.date}")
        y -= 20
        p.drawString(x, y, f"Summary: {log.summary}")
        y -= 20 # Move to the next line for the next entry.

        if log.lect_comment:
            p.drawString(x, y, f"Lecturer's comment: {log.lect_comment}")
            y -= 20 # Move to the next line for the next entry.
        else:
            p.drawString(x, y, f"The lecturer/supervisor hasn't  commmented yet !")
            y -= 20 # Move to the next line for the next entry.


        # Add space between entries
        y -= 20

    # Close the PDF object cleanly, and end the page.
    p.showPage()
    p.save()

    # Get the value of the BytesIO buffer and write it to the response.
    pdf = buffer.getvalue()
    buffer.close()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="student_logs.pdf"'
    return response
