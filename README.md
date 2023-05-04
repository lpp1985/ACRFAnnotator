# Instroduction

Automated adding annotation to PDF with json formatted data.

# Install

```pip install -r requirements.txt```
# Usage

```
python3 GenerateJson.py  -p blank.pdf -o Annotation.json
   

```
Then edit the Annotation.json by Hbuilder or Other editor!!
Then generated the annotated.pdf by following command:
```
python3 AddComment.py  -p blank.pdf -j Annotation.json -o Annotated.pdf

```