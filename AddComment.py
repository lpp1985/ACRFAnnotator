import re
from lpp import Ddict
import fitz,os,filetype,argparse,subprocess
from ParseConfig import AnnotationHashLoad
BLUE_COLOR = (1,0,0)
border = {"width": 2}

# def build_range(rangeval:str):
#     """
#     Build the range of pages based on the parameter inputted rangeval
#     """
#     result=set()
#     for part in rangeval.split(','):
#         x=part.split('-')
#         result.update(range(int(x[0]),int(x[-1])+1))
#     return list(sorted(result))

# def Get_all_kv_pairs(hash_map, prefix=None):
#     if prefix is None:
#         prefix = []
#     kv_pairs = []
#     for key, value in hash_map.items():
#         if isinstance(value, dict):
#             kv_pairs.extend(Get_all_kv_pairs(value, prefix + [key]))
#         else:
#             kv_pairs.append((prefix + [key], value))
#     return kv_pairs



# def comment_pdf(input_file:str
#               , search_text:str
#               , comment_title:str
#               , comment_info:str
#               , output_file:str
#               , pages:list=None
#               ):
#     """
#     Search for a particular string value in a PDF file and add comments to it.
#     """
#     pdfIn = fitz.open(input_file)
#     found_matches = 0
#     # Iterate throughout the document pages
#     for pg,page in enumerate(pdfIn):
#         pageID = pg+1
#         # If required for specific pages
#         if pages:
#            if pageID not in pages:
#               continue
#
#         # Use the search for function to find the text
#         matched_values = page.search_for(search_text,hit_max=20)
#         found_matches += len(matched_values) if matched_values else 0
#
#         #Loop through the matches values
#         #item will contain the coordinates of the found text
#         for item in matched_values:
#             # Enclose the found text with a bounding box
#             # print( dir( page ) )
#             print("Coords is !!")
#             print(item)
#             # annot= page.add_freetext_annot( item,"Fuck!!!!!",border_color=BLUE_COLOR )
#             annot = page.add_rect_annot(item)
#             annot.set_border({"dashes":[1],"width":2,"color":BLUE_COLOR})
#             annot.set_colors({"stroke":BLUE_COLOR})
#             page.add_text_annot( (200 , 200) , "Fuck Xijinping!!" )
#             # Add comment to the found match
#             info = annot.info
#             info["title"]   = comment_title
#             info["content"] = comment_info
#             info["subject"] = "Educative subject"
#             annot.set_info(info)
#
#             annot.update(border_color=BLUE_COLOR)
#
#     #Save to output file
#     pdfIn.save(output_file,garbage=3,deflate=True)
#     pdfIn.close()
#
#     #Process Summary
#     summary = {
#          "Input File": input_file
#        , "Matching Instances": found_matches
#        , "Output File": output_file
#        , "Comment Title": comment_title
#        , "Comment Info":  comment_info
#     }
#
#     # Print process Summary
#     print("## Summary ########################################################")
#     print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
#     print("###################################################################")

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
                                coord = [s['bbox'][0], s['bbox'][1] - 20, s['bbox'][2], s['bbox'][1] - 20]

                                coord[1] = coord[1] - 8 *len( Data_Hash[f1]  )

                                annot = page.add_freetext_annot(coord, Data_Hash[f1], 8, border_color=BLUE_COLOR,
                                                                rotate=90, )
                                annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                annot.update(border_color=BLUE_COLOR)

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
                                    coord = [s['bbox'][0], s['bbox'][1] - 100, s['bbox'][2], s['bbox'][1] - 20]
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2], 8, border_color=BLUE_COLOR,
                                                                    rotate=90, )
                                    annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    annot.update(border_color=BLUE_COLOR)


                            elif left_coord > 750:
                                f3 = title

                                if f1 in Data_Hash and f2 in Data_Hash[f1] and f3 in Data_Hash[f1][f2] and isinstance(Data_Hash[f1][f2][f3], str) and len(Data_Hash[f1][f2][f3]) > 0:
                                    coord = [s['bbox'][0], s['bbox'][1] - 100, s['bbox'][2], s['bbox'][1] - 20]
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][f3], 8, border_color=BLUE_COLOR,
                                                                    rotate=90, )
                                    annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    annot.update(border_color=BLUE_COLOR)

                            elif left_coord > 700:
                                f4 = title
                                # print(f4, left_coord)

                                if f1 in Data_Hash and f2 in Data_Hash[f1] and f3 in Data_Hash[f1][f2] and f4 in Data_Hash[f1][f2][f3] and isinstance(Data_Hash[f1][f2][f3][f4], str) and len(Data_Hash[f1][f2][f3][f4]) > 0:

                                    Data_Hash[f1][f2][f3][f4]
                                    coord = [s['bbox'][0], s['bbox'][1] - 100, s['bbox'][2], s['bbox'][1] - 20]
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][f3][f4], 8, border_color=BLUE_COLOR,
                                                                    rotate=90, )
                                    annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    annot.update(border_color=BLUE_COLOR)

                    elif "Italic" in s['font'] and s['size'] > 6:
                        text = s['text']
                        if abbre_prefix.search(text):
                            left_coord = s['bbox'][3]
                            content = abbre_prefix.search(text).group(1)
                            # print(content,left_coord)


                            if left_coord > 1000:


                                if isinstance(Data_Hash[f1][f2][content], str) and len(Data_Hash[f1][f2][content]) > 0:
                                    coord = [s['bbox'][0], s['bbox'][1] - 100, s['bbox'][2], s['bbox'][1] - 20]
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][content], 8,
                                                                    border_color=BLUE_COLOR,
                                                                    rotate=90, )
                                    annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    annot.update(border_color=BLUE_COLOR)

                            elif left_coord > 700:

                                endhash[f1][f2][f3][content] = ""
                                # print(f1, f2, f3, content)
                                # if f3 =="lstDRUGCOMP":
                                #     print( Data_Hash[f1][f2][f3][content] )
                                if f1 in Data_Hash and f2 in Data_Hash[f1] and f3 in Data_Hash[f1][f2]  and isinstance(Data_Hash[f1][f2][f3][content], str) and len(Data_Hash[f1][f2][f3][content]) > 0:
                                    coord = [s['bbox'][0], s['bbox'][1] -200, s['bbox'][2], s['bbox'][1] - 220]
                                    coord[1] = coord[1]- 8 *len( Data_Hash[f1][f2][f3][content] )
                                    # print( f1,f2,f3,content )
                                    # print('I Have!!!')
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][f3][content], 8,
                                                                    border_color=BLUE_COLOR, text_color=1,
                                                                    rotate=90, )
                                    # annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    annot.update(border_color=BLUE_COLOR)

                            elif left_coord > 550:
                                if f1 in Data_Hash and f2 in Data_Hash[f1] and f3 in Data_Hash[f1][f2]   and isinstance(Data_Hash[f1][f2][f3][f4][content],str) and len(Data_Hash[f1][f2][f3][f4][content]) > 0:

                                    # print( f1 , f2 , f3 ,f4, content,left_coord )
                                    coord = [s['bbox'][0], s['bbox'][1] - 300, s['bbox'][2], s['bbox'][1] - 320]
                                    coord[1] = coord[1] - 8 * len(Data_Hash[f1][f2][f3][f4][content])
                                    # print(f1,f2,f3,content)
                                    print('I Have f4!!!')
                                    annot = page.add_freetext_annot(coord, Data_Hash[f1][f2][f3][f4][content], 8,
                                                                    border_color=BLUE_COLOR, text_color=1,
                                                                    rotate=90, )

                                    annot.set_border({"dashes": [1], "width": 1, "color": BLUE_COLOR})
                                    annot.update(border_color=BLUE_COLOR)

    # Save to output file
    pdfIn.save(output_file_name, garbage=3, deflate=True)
    pdfIn.close()
if __name__ == "__main__":
    # Data_Hash = AnnotationHashLoad( "Config.json" )

    #
    # # #Downloading input file
    # # subprocess.call(['cp'
    # #               , os.path.join('./static',input_file_name)
    # #               , os.path.join('/usercode/output',input_file_name)
    # #                ])
    AddAnnotation( 'see.pdf','Out.pdf',"see.json"  )

