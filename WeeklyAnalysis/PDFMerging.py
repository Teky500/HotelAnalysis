import PyPDF2
import os

infile = PyPDF2.PdfFileReader('PDF.pdf', 'rb')
output = PyPDF2.PdfFileWriter()



merger = PyPDF2.PdfMerger()

for i in range(1, infile.numPages):
    p = infile.getPage(i)
    output.addPage(p)

with open('newfile.pdf', 'wb') as f:
    output.write(f)

os.remove("PDF.pdf")
os.rename('newfile.pdf', 'PDF.pdf')
merger.append('CheckOutPDF.pdf')
merger.append('PDF.pdf')

merger.write("results.pdf")

merger.close()
os.remove('PDF.pdf')
os.remove('CheckOutPDF.pdf')
os.rename('results.pdf', 'CheckOutPDF.pdf')





