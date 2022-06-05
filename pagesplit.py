import sys
from PyPDF2 import PdfFileWriter, PdfFileReader
import pikepdf

def main(args):
    files = args[1:]
    for i, fileName in enumerate(files):
        processFile(fileName)

def processFile(fileName):
    pdf = PdfFileReader(fileName)
    try:
        if pdf.isEncrypted:
            decryptedFileName = decryptPDF(fileName)
            splitPDF(PdfFileReader(decryptedFileName), fileName)
        else:
            splitPDF(pdf, fileName)
    except Exception as e:
        print ("FAILED: Unable to read file: %s" % fileName)

def decryptPDF(fileName):
    try:
        decryptedFileName = 'dcr_'+fileName
        pdf = pikepdf.open(fileName, password='')
        pdf.save(decryptedFileName)
        return decryptedFileName
    except FileNotFoundError as e:
        print("FAILED: Decrypt -> Unable to read file: %s" % fileName)


def splitPDF(pdf, fileName):
    try:
        for i in range(pdf.numPages):
            output = PdfFileWriter()
            output.addPage(pdf.getPage(i))
            with open ("%s_%i.pdf" % (fileName.split('.')[0], i+1),"wb") as outputStream:
                output.write(outputStream)
    except Exception as e:
        print ("FAILED: Unable to write to file")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv)
