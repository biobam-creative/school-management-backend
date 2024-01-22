from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle, Image
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from registration.serializers import UserSerializer



def my_jwt_response_handler(token, user=None, request=None):
    return {
        'token' : token,
        user : UserSerializer(user, context={'request':request}).data
    }

    

pdfmetrics.registerFont(TTFont('Roboto-Black', 'static/fonts/roboto/Roboto-Black.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Bold', 'static/fonts/roboto/Roboto-Bold.ttf'))
pdfmetrics.registerFont(TTFont('Roboto-Regular', 'static/fonts/roboto/Roboto-Regular.ttf'))
def generate_report_card(doc_name, term, student_name, student_class, results):

    freedemia_green = colors.Color(0,72/255,23/255)
    freedemia_yellow = colors.Color(230/255,183/255,17/255)

    logo = 'static/images/school_logo.png'
    warermark = 'static/images/30_transparent.png'
    doc_name = f"media/results/pdfs/{doc_name}.pdf"
    paper_width,paper_height = A4

    doc = canvas.Canvas(doc_name, pagesize=A4)

    table_data = [['S/N','Subject','First C.A', 'Second C.A', 'Third C.A', 'Total C.A', 'Exam', 'Total', 'Remarks', 'Grade']]
    for row in results:
        table_data.append(row)

    doc.drawImage(logo, 0, paper_height-150, width=150, height=150, mask='auto')
    doc.drawImage(warermark, paper_width/2-250, paper_height/2-250, width=500, height=500, mask='auto')

    doc.setFont('Roboto-Black', size=35, leading=None)
    doc.drawCentredString(paper_width/2+50, paper_height-60, 'Freedemia Group of Schools')
    doc.setFont('Roboto-Regular', size=25, leading=None)
    doc.drawCentredString(paper_width/2+50, paper_height-90, 'No. 2 Ayedaade Area')
    doc.drawCentredString(paper_width/2+50, paper_height-120, 'Ogbomoso, Oyo State')

    doc.setFont('Roboto-Black', size=35, leading=None)
    doc.drawCentredString(paper_width/2, paper_height-170, 'Report Card')
    doc.drawCentredString(paper_width/2, paper_height-190, '__________________________________________________________')
    
    doc.setFont('Roboto-Regular', size=15, leading=None)
    doc.drawString(30, paper_height-230, student_name)
    doc.drawString(paper_width/2-50, paper_height-230, f'Term: {term}')
    doc.drawString(500, paper_height-230, student_class)
    
    table = Table(table_data)
    table_style = TableStyle([
        ('GRID',(0,0),(-1,-1),1,freedemia_yellow),
        ('FONT',(1,1),(-1,-1), 'Roboto-Regular', 11),
        ('FONT',(0,0),(-1,0), 'Roboto-Bold', 11),
        ('BACKGROUND',(0,0),(-1,0), freedemia_green),
        ('TEXTCOLOR',(0,0),(-1,0), freedemia_yellow)])
    table.setStyle(table_style)

    table.wrapOn(doc, paper_width-60, paper_height)
    table.drawOn(doc, 20, paper_height-480)

    doc.drawString(30, paper_height-580, 'Class Teacher\'s Remark: __________________________________________________________________________')
    doc.drawString(30, paper_height-620, 'Principal\'s Remark: __________________________________________________________________________')
    doc.drawString(30, paper_height-660, 'Class Teacher\'s Signature: __________________________________________________________________________')
    doc.drawString(30, paper_height-700, 'Principal\'s Signature: __________________________________________________________________________')

    doc.showPage()
    doc.save()

    return doc_name