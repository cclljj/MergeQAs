#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import io
import os
import shutil
from argparse import ArgumentParser
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

QA = {}
LookupTables = ["PDF-all", 
#   "ChangLiao", "Chen", "Cheng", "Chou", "Fan", "Huang", "Kao", "Lai", "Lee", "LinYiChin", "LinYiHua","WangWanYu", "WanMeiLing", "Wu",
#   "acc", "biobank", "biotrec", "daais", "dga", "dia", "hro", "iptt", "its", "sec", "southcampus"
]

def lookup_table(fname):
	try:
		with open(fname) as f:
			for line in f:
				items = re.split('\t|,',line.rstrip())
				QA[items[0]] = items[1]
	except IOError:
		print("Could not read file:", fname)

def merge_QA(output_file, q_folder, a_folder, print_pp = True):
	p = 0
	pp = 0
	merger = PdfFileMerger(strict=False)

	output = PdfFileWriter()
	output.addBlankPage(width=595, height=842)

	blank_pdf_path = os.path.join(os.getcwd(), "tmp", "blank.pdf")
	dirname = os.path.dirname(blank_pdf_path)
	if not os.path.exists(dirname):
		os.makedirs(dirname)

	output.write(open(blank_pdf_path, 'wb'))

	index = 0
	for C in QA:
		index = index + 1
		index10 = ((index-1) // 10) % 10

		str_FILE_Q = os.path.join(os.getcwd(),q_folder, C+"-Q.pdf")
		#str_FILE_Q = q_folder+"/"+QA[C]+"-Q.pdf"
		str_FILE_A = os.path.join(os.getcwd(),a_folder, QA[C]+"-A.pdf")
		str_TMP_Q = os.path.join(os.getcwd(),"tmp", C+"-Q.pdf")
		str_TMP_A = os.path.join(os.getcwd(),"tmp", C+"-A.pdf")

		if p%2==0:
			p = p + 1
			pp = pp + 1
			merger.append(blank_pdf_path)

		if os.path.isfile(str_FILE_Q):
			existing_pdf = PdfFileReader(open(str_FILE_Q, "rb"))
			output = PdfFileWriter()
			for i in range (0,existing_pdf.getNumPages(),1):
				pp = pp + 1
				packet = io.BytesIO()
				can = canvas.Canvas(packet)
				can.setFont('Helvetica', 20)
				can.drawString(15, 800, "#" + str(index) + ": " + C + " (" + QA[C]+")")
				if print_pp:
					can.drawString(250, 20, str(pp))
				#add two black rectangles on the two sides for quick indexing
				can.rect(0,700-40*index10-40,20,40,fill=1,stroke=1)
				can.rect(575,700-40*index10-40,20,40,fill=1,stroke=1)
				can.save()
				packet.seek(0)
				new_pdf = PdfFileReader(packet)
				page = existing_pdf.getPage(i)
				# add the "watermark" (which is the new pdf) on the existing page
				page.mergePage(new_pdf.getPage(0))
				output.addPage(existing_pdf.getPage(i))

			outputStream = open(str_TMP_Q, "wb")
			output.write(outputStream)
			outputStream.close()

			if os.path.isfile(str_TMP_Q):
				inputStream = open(str_TMP_Q,'rb')
				p = p + PdfFileReader(inputStream).getNumPages()
				inputStream.close()
				merger.append(str_TMP_Q)
			else:
				print("Error - file missing: ", str_TMP_Q)
		else:
			print("Error - file missing: ", str_FILE_Q)


		if os.path.isfile(str_FILE_A):
			existing_pdf = PdfFileReader(open(str_FILE_A, "rb"))
			output = PdfFileWriter()
			for i in range (0,existing_pdf.getNumPages(),1):
				pp = pp + 1
				packet = io.BytesIO()
				can = canvas.Canvas(packet)
				can.setFont('Helvetica', 20)
				can.drawString(15, 800, "#" + str(index) + ": " + C + " (" + QA[C]+")")
				if print_pp:
					can.drawString(250, 20, str(pp))
				#add two black rectangles on the two sides for quick indexing
				can.rect(0,700-40*index10-40,20,40,fill=1,stroke=1)
				can.rect(575,700-40*index10-40,20,40,fill=1,stroke=1)
				can.save()
				packet.seek(0)
				new_pdf = PdfFileReader(packet)
				page = existing_pdf.getPage(i)
				# add the "watermark" (which is the new pdf) on the existing page
				page.mergePage(new_pdf.getPage(0))
				output.addPage(existing_pdf.getPage(i))

			outputStream = open(str_TMP_A, "wb")
			output.write(outputStream)
			outputStream.close()

			if os.path.isfile(str_TMP_A):
				inputStream = open(str_TMP_A,'rb')
				p = p + PdfFileReader(inputStream).getNumPages()
				inputStream.close()
				merger.append(str_TMP_A)
			else:
				print("Error - file missing: ", str_TMP_A)
		else:
			print("Error - file missing: ", str_FILE_A)

	output_dir = os.path.join(os.getcwd(), output_file)
	output_dirname = os.path.dirname(output_dir)
	if not os.path.exists(output_dirname):
		os.makedirs(output_dirname)

	merger.write(output_file)
	merger.close()


if __name__ == "__main__":

	parser = ArgumentParser()

	# Add more options if you like
	parser.add_argument("-Q", "--Q_Folder", dest="q_folder", default="PDF",
				help="folder to store Questions, default= PDF")
	parser.add_argument("-A", "--A_Folder", dest="a_folder", default="PDF",
				help="folder to store Answers, default= PDF")
	parser.add_argument("-NP", "--No_Page_Number", dest="no_pp", action="store_true",
				help="do not print page number")

	args = parser.parse_args()

	for lookup in LookupTables:
		QA.clear()
		lookup_table("input/" + lookup + ".csv")
		merge_QA("output/" +lookup+".pdf", args.q_folder, args.a_folder, print_pp = not args.no_pp)

	# Delete tmp directory
	shutil.rmtree(os.path.join(os.getcwd(), "tmp"))