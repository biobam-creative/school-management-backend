from rest_framework.views import APIView
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response

from django.http import HttpResponse

from django.db import IntegrityError

import random
import string
import csv

from admin_tools.models import *
from students.models import Student
from teacher.models import Subject
from .models import Result, TermlyReportCard, ResultPdf, Csv
from .serializers import ResultSerializer

from utilities import generate_report_card

class UploadResultView(APIView):

    def post(self, request, format=None):
        data = self.request.data
        user = request.user
        csv_file = request.FILES['csv_file']

        if csv_file:
            term_id = data['term_id']
            session = data['session']
            student_class = data['student_class']
            subject = data['subject']

            obj = Csv.objects.create(csv=csv_file) 
            with open(obj.csv.path, 'r')as f:
                reader = csv.reader(f)
                for index, row in enumerate(reader):
                    if index != 0:
                        registration_number = row[1]
                        first_ca = int(row[2])
                        second_ca = int(row[3])
                        third_ca = int(row[4])
                        exam = int(row[5])

                        student = Student.objects.get(registration_number=registration_number)
                        term = Term.objects.get(id=term_id)
                        session = AcademicSession.objects.get(year=session)
                        student_class = StudentClass.objects.get(name=student_class)
                        subject = Subject.objects.get(name=subject)

                        total = first_ca + second_ca + third_ca + exam
        else:
            term_id = data['term_id']
            session = data['session']
            student_class = data['student_class']
            subject = data['subject']
            first_ca = int(data['first_ca'])
            second_ca = int(data['second_ca'])
            third_ca = int(data['third_ca'])
            exam = int(data['exam'])
            registration_number = data['registration_number']

            student = Student.objects.get(registration_number=registration_number)
            term = Term.objects.get(id=term_id)
            session = AcademicSession.objects.get(year=session)
            student_class = StudentClass.objects.get(name=student_class)
            subject = Subject.objects.get(name=subject)

            total = first_ca + second_ca + third_ca + exam

        if total >= 70:
            remark = 'Excellent'
            grade = 'A1'
        elif total >= 60:
            remark = 'Very Good'
            grade = 'B2'
        elif total >= 50:
            remark = 'Good'
            grade = 'C4'
        elif total >= 45:
            remark = 'CREDIT'
            grade = 'C5'
        elif total >= 40:
            remark = 'CREDIT'
            grade = 'C6'
        elif total >= 35:
            remark = 'PASS'
            grade = 'D7'
        elif total >= 30:
            remark = 'PASS'
            grade = 'E8'
        else:
            remark = 'FAIL'
            grade = 'F9'

        # Create Termly report card model
        code_characters = string.ascii_letters + string.digits
        term_report_card_title = f'{term} result for {student}'
        code = ''.join((random.choice(code_characters)
                                for i in range(20)))

        if user.is_staff:
            try:
                term_report_card = TermlyReportCard.objects.create(
                    title=term_report_card_title, code=code)
                print(term_report_card)
            except IntegrityError:
                term_report_card = TermlyReportCard.objects.get(
                    title=term_report_card_title)

            try:
                Result.objects.create(student=student, term=term, session=session, student_class=student_class,
                                    subject=subject, first_ca=first_ca, second_ca=second_ca,
                                    third_ca=third_ca, exam=exam, total=total, remark=remark,
                                    grade=grade, term_report_card=term_report_card)
                return Response({'success': 'Result uploaded successfully!'})
            except IntegrityError:
                return Response({'error': 'Result Already uploaded !'})
        else:
            return Response({'error': 'You are not allowed'})


class ResultView(APIView):
    def post(self, request, format=None):
        data = self.request.data
        student = request.user.student

        term_id = data['term_id']
        # session = data['session']

        term = Term.objects.get(id=term_id)
        # session = AcademicSession.objects.get(year=session)
        term_report_title = f'{term} result for {student}'
        term_report = TermlyReportCard.objects.get(title=term_report_title)

        results = Result.objects.filter(term_report_card=term_report)
        result_data=[]
        serial_number = 1

        #all first cas, second cas, third cas, total cas, exams, totals into lists
        first_cas = []
        second_cas = []
        third_cas =[]
        total_cas = []
        exams = []
        totals = []

        if results:
            for result in results:
                subject=result.subject
                first_ca=result.first_ca
                second_ca=result.second_ca
                third_ca=result.third_ca
                exam=result.exam
                total=result.total
                remark=result.remark
                grade=result.grade

                total_ca = sum([first_ca, second_ca, third_ca])
                
                #append to first cas, second cas, third cas, total cas, exams, totals into lists
                first_cas.append(first_ca)
                second_cas.append(second_ca)
                third_cas.append(third_ca)
                total_cas.append(total_ca)
                exams.append(exam)
                totals.append(total)

                subject_data = [[serial_number, subject, first_ca, second_ca, third_ca, total_ca, exam, total, remark, grade]]
                for data in subject_data:
                    result_data.append(data)
                serial_number+=1
            #grand total of the colums
            first_cas_total = sum(first_cas)
            second_cas_total = sum(second_cas)
            third_cas_total = sum(third_cas)
            total_cas_total = sum(total_cas)
            exams_totals = sum(exams)
            grand_total = total_cas_total + exams_totals

            #total row into a list
            total_row = ['','TOTAL',first_cas_total,second_cas_total,third_cas_total,total_cas_total,exams_totals,grand_total,'','']
            #append total row to result data
            result_data.append(total_row)

            result = generate_report_card(doc_name=term_report_title, term=term,
                                student_name=f'{student.last_name} {student.first_name}', student_class=student.student_class.name, results=result_data)
            result = result.replace('media/','')
            try:
                result=ResultPdf.objects.create(title=term_report_title, pdf_file=result)
            except IntegrityError:
                ResultPdf.objects.get(title=term_report_title).delete()
                result=ResultPdf.objects.create(title=term_report_title, pdf_file=result)

            response = HttpResponse(result, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment ; filemane="%s"' f'{term_report_title}.pdf'

            return response
        else:
            return Response({'message': 'no result found'})
