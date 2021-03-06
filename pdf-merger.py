#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import io
import os
from argparse import ArgumentParser
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfFileMerger
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

QA = {}
LookupTables = ["PDF-all", 
  "ChangLiao", "Chen", "Cheng", "Chou", "Fan", "Huang", "Kao", "Lai", "Lee", "LinYiChin", "LinYiHua","WangWanYu", "WanMeiLing", "Wu",
  "acc", "biobank", "biotrec", "daais", "dga", "dia", "hro", "iptt", "its", "sec", "southcampus"]

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
	pp = 0
	merger = PdfFileMerger(strict=False)

	output = PdfFileWriter()
	output.addBlankPage(width=595, height=842)
	output.write(open("/tmp/blank.pdf", 'wb'))

	index = 0
	for C in QA:
		index = index + 1
		index10 = ((index-1) // 10) % 10

		str_FILE_Q = q_folder+"/"+C+"-Q.pdf"
		#str_FILE_Q = q_folder+"/"+QA[C]+"-Q.pdf"
		str_FILE_A = a_folder+"/"+QA[C]+"-A.pdf"
		str_TMP_Q = "/tmp/"+C+"-Q.pdf"
		str_TMP_A = "/tmp/"+C+"-A.pdf"

		if p%2==0:
			p = p + 1
			pp = pp + 1
			merger.append("/tmp/blank.pdf")

		if os.path.isfile(str_FILE_Q):
			existing_pdf = PdfFileReader(open(str_FILE_Q, "rb"))
			output = PdfFileWriter()
			for i in range (0,existing_pdf.getNumPages(),1):
				pp = pp + 1
				packet = io.BytesIO()
				can = canvas.Canvas(packet)
				can.setFont('Helvetica', 20)
				can.drawString(15, 800, "#" + str(index) + ": " + C + " (" + QA[C]+")")
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



	merger.write(output_file)
	merger.close()


if __name__ == "__main__":

	parser = ArgumentParser()

	# Add more options if you like
	parser.add_argument("-Q", "--Q_Folder", dest="q_folder", default="./PDF/",
				help="folder to store Questions, default= ./PDF/")
	parser.add_argument("-A", "--A_Folder", dest="a_folder", default="./PDF/",
				help="folder to store Answers, default= ./PDF/")

	args = parser.parse_args()

	for lookup in LookupTables:
		QA.clear()
		lookup_table("input/" + lookup + ".csv")
		merge_QA("output/" +lookup+".pdf", args.q_folder, args.a_folder)
