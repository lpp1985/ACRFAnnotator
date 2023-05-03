import re
from lpp import Ddict
import fitz,os,filetype,argparse,subprocess

BLUE_COLOR = (0,0,1)
border = {"width": 2}

def build_range(rangeval:str):
    """
    Build the range of pages based on the parameter inputted rangeval
    """
    result=set()
    for part in rangeval.split(','):
        x=part.split('-')
        result.update(range(int(x[0]),int(x[-1])+1))
    return list(sorted(result))

def comment_pdf(input_file:str
              , search_text:str
              , comment_title:str
              , comment_info:str
              , output_file:str
              , pages:list=None
              ):
    """
    Search for a particular string value in a PDF file and add comments to it.
    """
    pdfIn = fitz.open(input_file)
    found_matches = 0
    # Iterate throughout the document pages
    for pg,page in enumerate(pdfIn):
        pageID = pg+1
        # If required for specific pages
        if pages:
           if pageID not in pages:
              continue

        # Use the search for function to find the text
        matched_values = page.search_for(search_text,hit_max=20)
        found_matches += len(matched_values) if matched_values else 0

        #Loop through the matches values
        #item will contain the coordinates of the found text
        for item in matched_values:
            # Enclose the found text with a bounding box
            # print( dir( page ) )
            annot= page.add_freetext_annot( item,"Fuck!!!!!",border_color=BLUE_COLOR )
            # annot = page.add_rect_annot(item)
            annot.set_border({"dashes":[1],"width":2,"color":BLUE_COLOR})
            #annot.set_colors({"stroke":BLUE_COLOR})
            # page.add_text_annot( (200 , 200) , "Fuck Xijinping!!" )
            # Add comment to the found match
            # info = annot.info
            # info["title"]   = comment_title
            # info["content"] = comment_info
            #info["subject"] = "Educative subject"
            # annot.set_info(info)
            
            annot.update(border_color=BLUE_COLOR)

    #Save to output file
    pdfIn.save(output_file,garbage=3,deflate=True)
    pdfIn.close()

    #Process Summary
    summary = {
         "Input File": input_file
       , "Matching Instances": found_matches
       , "Output File": output_file
       , "Comment Title": comment_title
       , "Comment Info":  comment_info
    }

    # Print process Summary
    print("## Summary ########################################################")
    print("\n".join("{}:{}".format(i, j) for i, j in summary.items()))
    print("###################################################################")

if __name__ == "__main__":
    pdf_out = fitz.open( )
    name_prefix = re.compile("\[(\S+)\]")
    abbre_prefix = re.compile("\[A\:(\S+)\]")
    #Input PDF file
    input_file_name  = 'see.pdf'
    #Output PDF file
    output_file_name = 'commented.pdf'

    #Selected pages
    pages = '1,2'
    pages_list = build_range(pages) if pages else None
    f1 = ""
    f2 = ""
    endhash= Ddict()
    
    #Commenting the document
    # comment_pdf(input_file     =input_file_name
    #            , search_text   = 'NCBI'
    #            , comment_title = 'Pay Attention'
    #            , comment_info  = 'COVID is dangerous'
    #            , output_file   = output_file_name
    #            , pages         = pages_list
    #             )

    pdfIn = fitz.open( input_file_name )
    pdfIn2 = fitz.open(  )
    record_status = False
    # result = []
    for pg in range(0,pdfIn.page_count) :
        page = pdfIn[pg]
        for annot in page.annots(  ) :
            print(annot)
            page.delete_annot(annot )
            
            # page.update()
            # result.append(page)
            # pdfIn.reload_page(page)
        # pdfIn2.new_page(  )
        # pdfIn2[0] = page
    for pg in range( 0 , pdfIn.page_count ) :
        page = pdfIn[ pg ]
        for annot in page.annots( ) :
            print( annot )
            page.delete_annot( annot )
        
    pdfIn.save("NoAnno.pdf")
    pdfIn.close()

        
    # #Downloading input file
    # subprocess.call(['cp'
    #               , os.path.join('./static',input_file_name)
    #               , os.path.join('/usercode/output',input_file_name)
    #                ])
