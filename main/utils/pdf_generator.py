import datetime
import imghdr
import os 
from django.conf import settings
from reportlab.platypus import *
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.rl_config import defaultPageSize
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas  
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors, pagesizes 
from reportlab.graphics import shapes 
from reportlab.graphics.charts.lineplots import LinePlot 
from reportlab.graphics.widgets.markers import makeMarker 
from reportlab.rl_config import defaultPageSize 
from reportlab.lib import utils
from reportlab.lib.units import cm
from reportlab.pdfgen.canvas import Canvas


def myFirstPage(canvas, doc):
    PAGE_HEIGHT = defaultPageSize[1]
    PAGE_WIDTH = defaultPageSize[0]
    pageinfo = "DIAGNOSIS REPORT"
    canvas.saveState()
    canvas.setFont('Times-Bold', 16)
    canvas.drawCentredString(PAGE_WIDTH / 2.0, PAGE_HEIGHT - 100, "DIAGNOSIS REPORT")
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page 1 / %s" % pageinfo)
    canvas.restoreState()
    
def myLaterPages(canvas, doc):
    pageinfo = "DIAGNOSIS REPORT"
    canvas.saveState()
    canvas.setFont('Times-Roman', 9)
    canvas.drawString(inch, 0.75 * inch, "Page %d / %s" % (doc.page, pageinfo))
    canvas.restoreState()
    
def go(CardiologistName, PatientFirstName, PatientLastName, PatientGender,
       PatientDOB, data_dir, image_list, comments_list, date, styles, pdf_path, diagnosis):
    doc = SimpleDocTemplate(pdf_path)
    Story = [Spacer(1, 2 * inch)]
    styles['h1'].fontSize = 12  
    styles['h1'].leading = 14 
    styles['h1'].alignment = 2 
    styles['h1'].spaceAfter = 0 
    styles['h1'].spaceBefore = 2 
    
    styles['h2'].fontSize = 12  
    styles['h2'].leading = 14 
    styles['h2'].alignment = 0 
    styles['h2'].spaceAfter = 0 
    styles['h2'].spaceBefore = 2
    
    styles['h3'].fontSize = 12  
    styles['h3'].leading = 14 
    styles['h3'].alignment = 1
    styles['h3'].spaceAfter = 0 
    styles['h3'].spaceBefore = 2
#    styles['h2'].bold = 0

    styles['h4'].fontSize = 20  
    styles['h4'].leading = 14 
    styles['h4'].alignment = 1
    styles['h4'].spaceAfter = 10
    styles['h4'].spaceBefore = 2
    
    styleTitle = styles['h4']
    styleSubtitle = styles['h1']
    styleInfo = styles['h2']
    styleParagraph = styles["Normal"]
    styleImageTitle = styles['h3']
    
    im = Image(settings.STATIC_ROOT +"quantmd/images/"+'logo.jpeg', width=11*cm,height = 11*cm)
    Story.append(im)
    
    p = Paragraph('Made Possible By QuantMD<br\><br\><br\><br\><br\>', styleTitle)
    Story.append(p)
    
    p = Paragraph(date, styleSubtitle)
    Story.append(p)
    p = Paragraph("PRODUCED BY: " + CardiologistName, styleSubtitle)
    Story.append(p)
    p = Paragraph("<br\><br\>" , styleInfo)
    Story.append(p)
    
    data = [['PATIENT INFORMATION' + ' '*121, ' ']]
    ts = [('ALIGN', (1, 1), (-1, -1), 'LEFT'),
     ('LINEABOVE', (0, 0), (-1, 0), 1, colors.purple),
     ('LINEBELOW', (0, 0), (-1, 0), 1, colors.purple),
     ('FONT', (0, 0), (-1, 0), 'Times-Bold'),
     ('LINEABOVE', (0, -1), (-1, -1), 1, colors.purple),
     ('LINEBELOW', (0, -1), (-1, -1), 0.5, colors.purple,
      1, None, None, 4, 1),
#     ('LINEBELOW', (0,-1), (-1,-1), 1, colors.red),
     ('FONT', (0, -1), (-1, -1), 'Times-Bold')]
    
    table = Table(data, style=ts)
#    p = Paragraph(table, styleInfo)
    Story.append(table)
    
    p = Paragraph("Name: " + PatientFirstName + " " + PatientLastName, styleInfo)
    Story.append(p)
    
    p = Paragraph("Gender: " + PatientGender, styleInfo)
    Story.append(p)
    
    p = Paragraph("Date of Birth: " + PatientDOB + "<br\><br\>", styleInfo)
    Story.append(p)
    
    data = [['DIAGNOSIS                                                                                                                                                   ', ' ']]
    table = Table(data, style=ts)
    Story.append(table)
    p = Paragraph("<br\><br\>" , styleInfo)
    Story.append(p)
    
    #Append diagnosis
    bogustext = diagnosis
    p = Paragraph(bogustext, styleParagraph)
    Story.append(p)
    Story.append(Spacer(1, 0.2 * inch))
    
    
    for i in xrange(len(comments_list)):
        if imghdr.what(data_dir + "/" + image_list[i]) == "bmp":
            Story.append(Image(data_dir + "/" + image_list[i], width=8 * cm, height=8 * cm))
            p = Paragraph('Figure ' + str(i+1) + "<br\><br\>", styleImageTitle)
            Story.append(p)
            p = Paragraph(comments_list[i], styleParagraph);
            Story.append(p);
    doc.build(Story, onFirstPage=myFirstPage, onLaterPages=myLaterPages)
    
def Report2PDF(CardiologistFirstName, CardiologistLastName, PatientFirstName, PatientLastName,
               PatientGender, PatientDOB, data_dir, image_list, comments_list, pdf_path, diagnosis):
    CardiologistName = CardiologistFirstName + " " + CardiologistLastName
    now = datetime.datetime.today()
    date = now.strftime("%m %d %Y %H:%M:%S")
    
    styles = getSampleStyleSheet()
    go(CardiologistName, PatientFirstName, PatientLastName, PatientGender,
       PatientDOB, data_dir, image_list, comments_list, date, styles, pdf_path, diagnosis) 
