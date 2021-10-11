#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from argparse import ArgumentParser
import re
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

QA = {}

def lookup_table(fname):
	try:
		with open(fname) as f:
			for line in f:
				items = re.split('\t|,',line.rstrip())
				QA[items[0]] = items[1]
	except IOError:
		print("Could not read file:", fname)

def merge_QA(output_file, q_folder, a_folder):
	p = 0
	merger = PdfFileMerger()

	output = PdfFileWriter()
	output.addBlankPage(width=595, height=842)
	output.write(open("/tmp/blank.pdf", 'wb'))

	for C in QA:
		if p%2==0:
			p = p + 1
			merger.append("/tmp/blank.pdf")

		packet = io.BytesIO()
		can = canvas.Canvas(packet)
		#can.drawString(10, 820, "Final: "+C+"; Original: "+QA[C])
		can.drawString(10, 820, "Case #: "+C)
		can.save()
		packet.seek(0)

		new_pdf = PdfFileReader(packet)
		existing_pdf = PdfFileReader(open(q_folder+"/"+C+"-Q.pdf", "rb"))
		output = PdfFileWriter()
		for i in range (0,existing_pdf.getNumPages(),1):
			page = existing_pdf.getPage(i)
			# add the "watermark" (which is the new pdf) on the existing page
			page.mergePage(new_pdf.getPage(0))
			output.addPage(existing_pdf.getPage(i))
		outputStream = open("/tmp/"+C+"-Q.pdf", "wb")
		output.write(outputStream)
		outputStream.close()

		inputStream = open("/tmp/"+C+"-Q.pdf",'rb')
		p = p + PdfFileReader(inputStream).getNumPages()
		inputStream.close()
		merger.append("/tmp/"+C+"-Q.pdf")

		p = p + PdfFileReader(open(a_folder+"/"+QA[C]+"-A.pdf",'rb')).getNumPages()
		merger.append(a_folder+"/"+QA[C]+"-A.pdf")

	merger.write(output_file)
	merger.close()


if __name__ == "__main__":

	parser = ArgumentParser()

	# Add more options if you like
	parser.add_argument("-Q", "--Q_Folder", dest="q_folder", default="./PDF-Q/",
				help="folder to store Questions, default= ./PDF-Q/")
	parser.add_argument("-A", "--A_Folder", dest="a_folder", default="./PDF-A/",
				help="folder to store Answers, default= ./PDF-A/")
	parser.add_argument("-o", "--output", dest="output_filename", default="output.pdf",
				help="write merged PDF to FILE, default=output.pdf", metavar="FILE")
	parser.add_argument("input_filename", help="the lookup table to merge PDF files")

	args = parser.parse_args()

	lookup_table(args.input_filename)
	merge_QA(args.output_filename, args.q_folder, args.a_folder)
