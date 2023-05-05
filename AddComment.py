#!/usr/bin/env python3
import re
from optparse import OptionParser

from lpp import Ddict
import fitz,os,filetype,argparse,subprocess
from ParseConfig import AnnotationHashLoad
BLUE_COLOR = (1,0,0)
border = {"width": 2}
textcolor=(0,0,0)
color = (0, 0.7, 0.8)
def AddAnnotation(input_file_name,output_file_name,jsonfile="Config.json"):
    endhash = Ddict()
    Data_Hash = AnnotationHashLoad(jsonfile)
    # print( Data_Hash )
    name_prefix = re.compile("\[(\S+)\]")
    abbre_prefix = re.compile("\[A\:(.+)\]")
    f1 = ""
    f2 = ""
    pdfIn = fitz.open(input_file_name)


    record_status = False
    title_status = {}
    displ = fitz.Rect(0, 50, 0, 50)
    for pg, page in enumerate(pdfIn):

        width = page.get_text("dict", flags=11)['width']
        height = page.get_text("dict", flags=11)['height']
        blocks = page.get_text("dict", flags=11)['blocks']
        for b in blocks:
            for l in b['lines']:
                for s in l["spans"]:
                    if "Bold" in s['font'] and s['size'] > 9:
                        text = s['text']
                        if name_prefix.search(text):

                            f1 = name_prefix.search(text).group(1)

                            record_status = True


                            if isinstance(Data_Hash[f1],str) and len(Data_Hash[f1])>0 :
                                coord = [s['bbox'][0], s['bbox'][1] - 420, s['bbox'][2], s['bbox'][1] - 20]

                                coord[1] = coord[1] - 8 *len( Data_Hash[f1]  )

                                annot = page.add_freetext_annot(coord, Data_Hash[f1], 8, border_color=BLUE_COLOR,
                                                                rotate=90,fill_color   = color,align = 1 )
                                #annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                #annot.update(border_color=BLUE_COLOR)

                        else:
                            record_status = False
                    elif "Bold" in s['font'] and s['size'] > 6:
                        if not record_status:
                            continue
                        text = s['text']
                        if name_prefix.search(text):
                            left_coord = s['bbox'][3]
                            title = name_prefix.search(text).group(1)
                            if left_coord > 1000:
                                f2 = title

                                if f1 in Data_Hash and f2 in Data_Hash[f1] and  isinstance(Data_Hash[f1][f2], str) and len(Data_Hash[f1][f2]) > 0:
                                    coord = [s['bbox'][0], s['bbox'][1] - 150, s['bbox'][2], s['bbox'][1] - 20]
                                    coord[1] = coord[1] - 9 *len(Data_Hash[f1][f2])
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2], 8, border_color=BLUE_COLOR,
                                                                    rotate=90,fill_color  = color,align = 1 )
                                    # annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    # annot.update(border_color=BLUE_COLOR)


                            elif left_coord > 750:
                                f3 = title

                                if f1 in Data_Hash and f2 in Data_Hash[f1] and f3 in Data_Hash[f1][f2] and isinstance(Data_Hash[f1][f2][f3], str) and len(Data_Hash[f1][f2][f3]) > 0:
                                    coord = [s['bbox'][0], s['bbox'][1] - 150, s['bbox'][2], s['bbox'][1] - 20]
                                    coord[1] = coord[1] - 9 *len(Data_Hash[f1][f2][f3])
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][f3], 8, border_color=BLUE_COLOR,
                                                                    rotate=90,fill_color  = color,align = 1 )
                                    # annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    # annot.update(border_color=BLUE_COLOR)

                            elif left_coord > 700:
                                f4 = title
                                # print(f4, left_coord)

                                if f1 in Data_Hash and f2 in Data_Hash[f1] and f3 in Data_Hash[f1][f2] and f4 in Data_Hash[f1][f2][f3] and isinstance(Data_Hash[f1][f2][f3][f4], str) and len(Data_Hash[f1][f2][f3][f4]) > 0:

                                    Data_Hash[f1][f2][f3][f4]
                                    coord = [s['bbox'][0], s['bbox'][1] - 150, s['bbox'][2], s['bbox'][1] - 20]
                                    coord[1] = coord[1] - 9 *len(Data_Hash[f1][f2][f3][f4])
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][f3][f4], 8, border_color=BLUE_COLOR,
                                                                    rotate=90,fill_color  = color ,align = 1  )
                                    # annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    # annot.update(border_color=BLUE_COLOR)

                    elif "Italic" in s['font'] and s['size'] > 6:
                        text = s['text']
                        if abbre_prefix.search(text):
                            left_coord = s['bbox'][3]
                            content = abbre_prefix.search(text).group(1)
                            # print(content,left_coord)


                            if left_coord > 1000:


                                if isinstance(Data_Hash[f1][f2][content], str) and len(Data_Hash[f1][f2][content]) > 0:
                                    coord = [s['bbox'][0], s['bbox'][1] - 150, s['bbox'][2], s['bbox'][1] - 20]
                                    coord[1] = coord[1] - 9 *len(Data_Hash[f1][f2][content])
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][content], 8,
                                                                    border_color=BLUE_COLOR,
                                                                    rotate=90,fill_color  = color,align = 1 )
                                    # annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    # annot.update(border_color=BLUE_COLOR)

                            elif left_coord > 700:

                                endhash[f1][f2][f3][content] = ""
                                # print(f1, f2, f3, content)
                                # if f3 =="lstDRUGCOMP":
                                #     print( Data_Hash[f1][f2][f3][content] )
                                if f1 in Data_Hash and f2 in Data_Hash[f1] and f3 in Data_Hash[f1][f2]  and isinstance(Data_Hash[f1][f2][f3][content], str) and len(Data_Hash[f1][f2][f3][content]) > 0:
                                    coord = [s['bbox'][0], s['bbox'][1] -200, s['bbox'][2], s['bbox'][1] - 220]
                                    coord[1] = coord[1]- 9 *len( Data_Hash[f1][f2][f3][content] )
                                    # print( f1,f2,f3,content )
                                    print('I Have!!!')
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][f3][content], 8,
                                                                    border_color=BLUE_COLOR, text_color=textcolor,
                                                                    rotate=90,fill_color  = color,align = 1, )

                                    # annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    # annot.update(border_color=BLUE_COLOR)

                            elif left_coord > 550:
                                if f1 in Data_Hash and f2 in Data_Hash[f1] and f3 in Data_Hash[f1][f2]   and isinstance(Data_Hash[f1][f2][f3][f4][content],str) and len(Data_Hash[f1][f2][f3][f4][content]) > 0:

                                    #print( f1 , f2 , f3 ,f4, content,left_coord )

                                    coord = [s['bbox'][0], s['bbox'][1] - 300, s['bbox'][2], s['bbox'][1] - 320]
                                    coord[1] = coord[1] - 9 *len(Data_Hash[f1][f2][f3][f4][content])
                                    # print(f1,f2,f3,content)
                                    #print('I Have f4!!!')
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][f3][f4][content], 8,
                                                                    border_color=BLUE_COLOR, text_color=1,
                                                                    rotate=90,fill_color =color,align = 1 )

                                    # annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    # annot.update(border_color=BLUE_COLOR)

    # Save to output file
    pdfIn.save(output_file_name, garbage=3, deflate=True)
    pdfIn.close()
if __name__ == "__main__":
    usage = "python3 %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option("-p", "--PDF", action="store",
                      dest="Pdf",

                      help="Input PDF File")

    parser.add_option("-j", "--Json", action="store",
                      dest="Json",

                      help="Json File Describe Annotation Template!!")
    parser.add_option("-o", "--Output", action="store",
                      dest="Output",

                      help="Pdf Output File for Annotationed PDF!!")
    (options, args) = parser.parse_args()
    Pdf = options.Pdf
    Json = options.Json
    Output  = options.Output
    AddAnnotation( Pdf,Output,Json  )

