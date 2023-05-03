import json

from lpp import *
import sys, fitz
def GenerateJson(input_file_name):
    name_prefix = re.compile("\[(\S+)\]")
    abbre_prefix = re.compile("\[A\:(.+)\]")
    # Input PDF file




    f1 = ""
    f2 = ""
    endhash = Ddict()


    pdfIn = fitz.open(input_file_name)
    # record_status = False
    # for pg, page in enumerate(pdfIn):
    #     width = page.get_text("dict", flags=11)['width']
    #     height = page.get_text("dict", flags=11)['height']
    #     blocks = page.get_text("dict", flags=11)['blocks']
    #     for b in blocks:
    #         for l in b['lines']:
    #             for s in l["spans"]:
    #                 if "Bold" in s['font'] and s['size'] > 9:
    #                     text = s['text']
    #                     if name_prefix.search(text):
    #
    #                         f1 = name_prefix.search(text).group(1)
    #
    #                         record_status = True
    #
    #                     else:
    #                         record_status = False
    #                 elif "Bold" in s['font'] and s['size'] > 6:
    #                     if not record_status:
    #                         continue
    #                     text = s['text']
    #                     if name_prefix.search(text):
    #                         left_coord = s['bbox'][3]
    #
    #                         title = name_prefix.search(text).group(1)
    #                         if left_coord > 1000:
    #                             f2 = title
    #
    #
    #
    #                         elif left_coord > 800:
    #                             f3 = title
    #
    #                         elif left_coord > 550:
    #                             f4 = title
    #
    #                 elif "Italic" in s['font'] and s['size'] > 6:
    #                     text = s['text']
    #                     if abbre_prefix.search(text):
    #                         left_coord = s['bbox'][3]
    #                         content = abbre_prefix.search(text).group(1)
    #                         # print( content )
    #                         if left_coord > 1000:
    #                             pass
    #                             # print( f1 , f2 ,left_coord )
    #                         elif left_coord > 800:
    #
    #                             pass
    #                             # print(f1,f2,f3,left_coord)
    #                         elif left_coord > 550:
    #
    #                             # print(f1,f2,f3,f4,content)
    #                             endhash[f1][f2][f3][f4][content] =""
    #                             # print( f1 , f2 , f3 ,f4, left_coord )
    record_status = False
    title_status = {}
    # print( endhash )
    # print( endhash["frmDRUGTERM"]["sctDRUGTERM"]["lstDRUGCOMP"]["txtRACEOTH"] )
    pdfIn = fitz.open(input_file_name)
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
                            endhash[f1]={}
                            record_status = True
                            f2,f3,f4,content="","","",""

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

                                endhash[f1][f2]={}

                            elif left_coord > 750:
                                f3 = title
                                # print(f1,f2,f3)
                                if f2 not in endhash[f1]:
                                    endhash[f1][f2] = {}
                                # print( endhash[f1] )

                                    endhash[f1][f2][f3]={}
                            elif left_coord > 600:
                                f4 = title
                                if f3 not in endhash[f1][f2]:
                                    endhash[f1][f2][f3]={}
                                endhash[f1][f2][f3][f4] = {}

                    elif "Italic" in s['font'] and s['size'] > 6:
                        text = s['text']
                        if abbre_prefix.search(text):
                            left_coord = s['bbox'][3]
                            content = abbre_prefix.search(text).group(1)
                            # print( content )
                            if left_coord > 1000:
                                endhash[f1][f2][content] = ""
                                # print( f1 , f2 ,left_coord )
                            elif left_coord > 700:
                                # print( f1,f2,f3,content)
                                if f3 not in endhash[f1][f2]:
                                    endhash[f1][f2][f3]={}
                                endhash[f1][f2][f3][content] = ""
                                # print(f1,f2,f3,left_coord)
                            elif left_coord > 550:
                                # print(f1, f2, f3,f4 , content,left_coord)
                                # print( endhash[f1][f2][f3])
                                if not f2:
                                    endhash[f1][f2][f3][f4][content] = ""
                                else:
                                    if f4 not in endhash[f1][f2][f3]:
                                        endhash[f1][f2][f3][f4]={}

                                        endhash[f1][f2][f3][f4][content] = ""
                                # print(endhash[f1][f2][f3][f4])
                                # if
                                # endhash[f1][f2][f3][f4][content] =""
                                # print( f1 , f2 , f3 ,f4, left_coord )
    return endhash
#     # Save to output file
#     pdfIn.save("Out.pdf", garbage=3, deflate=True)
#     pdfIn.close()

if __name__=="__main__":
    endhash = GenerateJson( sys.argv[1] )
    # print(endhash)
    json.dump(endhash,open("see.json",'w'))