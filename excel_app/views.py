import zipfile

from django.shortcuts import render
from django.utils.crypto import get_random_string
from django.views.generic.base import TemplateView
# Create your views here.
# excel_app/views.py

import xlwt
from django.http import HttpResponse
from django.contrib.auth.models import User
from zipfile import ZipFile


class ExcelPageView(TemplateView):
    """class for the csv."""
    template_name = "excel_home.html"


def export_users_xls(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="users.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('Users Data') # this will make a sheet named Users Data

    # Sheet header, first row
    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    columns = ['Username', 'First Name', 'Last Name', 'Email Address', ]

    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style) # at 0 row 0 column

    # Sheet body, remaining rows
    font_style = xlwt.XFStyle()

    rows = User.objects.all().values_list('username', 'first_name', 'last_name', 'email')
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, row[col_num], font_style)

    wb.save(response)
    # response = HttpResponse(open('users.xls', 'rb'),
    #                         content_type='application/ms-excel')
    # response['Content-Disposition'] = 'attachment; filename=Reservation.zip'
    # more fine-grained control over ZIP files
    # with ZipFile("file_name.zip", "w") as newzip:
    #     newzip.write("users.xls")
    #
    # with ZipFile("file_name.zip", 'r') as zip:
    #     # setting the pwd to extract files
    #     zip.setpassword("ganofins")
    #     # extracting all contents
    #     zip.extractall()
    #     print('Done!')

    return response


def create_zip_files(list_files):
    """
    Zip files
    """
    files = list_files

    # Create a ZipFile object
    for file in files:
        with zipfile.ZipFile(file, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
            with open(file, 'rb') as f:
                zf.writestr(file, f.read())
        zf.close()

    return zf


def serve_report_zip_file(file):
    """
    Serves the zip file
    """
    random_string = get_random_string(length=15)
    content_type = 'application/zip'
    response = HttpResponse(file, content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename="' + random_string + '.zip"'

    return response