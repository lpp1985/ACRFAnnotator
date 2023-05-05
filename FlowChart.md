# Abstract

Of utmost importance to both sponsor and CRO companies is ensuring high quality and efficiency when generating SDTM aCRFs. This is because SDTM aCRF is a crucial element in the SDTM submission package, and many pharmaceutical MNCs have established their own company-level SDTM aCRF standards in addition to CDISC guidelines. To guarantee success in the highly competitive pharmaceutical industry, it is essential to carefully follow both CDISC and company-level SDTM standards when generating SDTM aCRFs. In this paper, we present a novel way which relies on a meticulously crafted infinite-dimensional and regular expression compatible hashing data structure to automated generated annotated aCRF with quality and efficiency. This method can automatic positioning and locating of comment location and additionally possesses loose coupling capability, making it convenient for multiple collaborators to modularly handle lengthy documents.

```mermaid
flowchart TD;
    A[("Blank CRF PDF File")]
    A--GenerateJson.py-->B(Blank Json)
    F[/"Company SDTM 
    aCRF standard"/]-->
  	 E[["Edit"]]
    B-->E
    G(Annotated Json)
    E-->G
    G====>D[["AddComment.py"]]
    A====>D
    D-->V("Annotated CRF PDF File");
```

# INTRODUCTION  

The genesis of SDTM production lies in the annotation of vacant CRF pages, which must be packaged alongside SDTM datasets as an integral element of the clinical data submission package to the Food and Drug Administration(FDA). For statisticians and programmers, the laborious task of manually annotating CRFs using the Adobe Acrobat comment tool presents a hurdle. They have struggled to mechanize this process, yet, most of the current techniques or packages rely on the use of multiple software. These methods generate Forms Data Format (FDF) files for import substitution into blank CRFs. These approaches record poor annotation performance when applied to unprecedented CRFs or versions of CRFs that undergo radical transformations. To surmount this pitfall, we have developed a Python module that capitalizes on the influential characteristics of Python to author CRF pages automatically. Our package supersedes customary methods and other computerized tools by providing significant attributes, including:

+ Abandoning coordinate systems, EXCEL, or FDF files, we propose utilizing a meticulously designed data structure based on the "infinite dimensional dictionary" to record the entire structure of the CRF form. This data structure will generate a JSON file containing all possible annotation positions. Users can directly modify the JSON file to enable automatic annotation of the desired text. Annotation width and position are automatically calculated by the system and integrated into the generated JSON file without human intervention .

+ There is no need to ensure the correctness of CRF structure parsing. As long as the input parameters are accurate, all possible annotation positions will be traversed, even if the document structure parsing results do not match expectations. The annotation effect will not be affected by any discrepancies.
+ Users do not need to pay attention to the PDF file itself, only edit the parsed JSON file to achieve highly reliable document annotation results and greatly improve efficiency. Furthermore, related editors can format and display the JSON file, facilitating a better understanding of the document by workers and enabling them to work without reference to the source document.
+ This task is highly modular and portable. A large CRF PDF file can be divided into multiple sub-documents and completed collaboratively by multiple personnel. The data structure then combines the annotation results without losing any data integrity. This means that the once cumbersome and labor-intensive work can now be completed by teams working by divide-and-conquer  strategy. Additionally, if necessary, the project can even be open-sourced on Github.
+ Annotation migration becomes possible. Based on Python's build-in functions, annotation updates and comparisons for multiple different versions of the same document can be performed through key-value pair conversion, enabling seamless annotation migration to the required result without data loss.
+ The system supports regular expression matching, and the annotated text can be synchronized based on specific variables. Standard regular expressions can be used to enable the annotated text to change automatically with the matching variables.This greatly simplifies the workload for some tasks.
+ The annotation records are stored in the JSON format file and can be easily dumped into databases such as <i>***MongoDB, Redis, and jsonDB***</i>, enabling remote management and remote work needs at any time. Furthermore, database management can also bring benefits to task management.

+ The system has a complete command-line tool and graphical user interface. Apart from editing the JSON file, all other steps are basically automated.

# WROKFLOW AND PROCESS



