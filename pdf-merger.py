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
				A = re.split('\t|,',line.rstrip())
				QA[A[1]] = A[0]
	except IOError:
		print("Could not read file:", fname)

def merge_QA(output_file, blank_file, q_folder, a_folder):
	p = 0
	merger = PdfFileMerger()

	for C in QA:
		if p%2==0:
			p = p + 1
			merger.append(blank_file)

		packet = io.BytesIO()
		can = canvas.Canvas(packet)
		can.drawString(10, 820, "Final: "+C+"; Original: "+QA[C])
		can.save()
		packet.seek(0)

		new_pdf = PdfFileReader(packet)
		existing_pdf = PdfFileReader(open(q_folder+"/"+QA[C]+".pdf", "rb"))
		output = PdfFileWriter()
		for i in range (0,existing_pdf.getNumPages(),1):
			page = existing_pdf.getPage(i)
			# add the "watermark" (which is the new pdf) on the existing page
			page.mergePage(new_pdf.getPage(0))
			output.addPage(existing_pdf.getPage(i))
		outputStream = open("/tmp/"+QA[C]+".pdf", "wb")
		output.write(outputStream)
		outputStream.close()

		inputStream = open("/tmp/"+QA[C]+".pdf",'rb')
		p = p + PdfFileReader(inputStream).getNumPages()
		inputStream.close()
		merger.append("/tmp/"+QA[C]+".pdf")

		p = p + PdfFileReader(open(a_folder+"/"+C+".pdf",'rb')).getNumPages()
		merger.append(a_folder+"/"+C+".pdf")

	merger.write(output_file)
	merger.close()


if __name__ == "__main__":

	parser = ArgumentParser()

	# Add more options if you like
	parser.add_argument("-Q", "--Q_Folder", dest="q_folder", default="./PDF-Q/",
				help="folder to store Questions")
	parser.add_argument("-A", "--A_Folder", dest="a_folder", default="./PDF-A/",
				help="folder to store Answers")
	parser.add_argument("-o", "--output", dest="output_filename", default="output.pdf",
				help="write merged PDF to FILE", metavar="FILE")
	parser.add_argument("-b", "--blank", dest="blank_filename", default="blank.pdf",
				help="path to blank PDF file", metavar="FILE")
	parser.add_argument("input_filename", help="the lookup table to merge PDF files")

	args = parser.parse_args()
	print(args.input_filename, args.blank_filename, args.output_filename)

	lookup_table(args.input_filename)
	merge_QA(args.output_filename, args.blank_filename, args.q_folder, args.a_folder)
