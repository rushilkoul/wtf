import zipfile

ZIP_FAMILY = {
    "word/document.xml": {
        "name": "Microsoft Word Document",
        "extensions": [".docx"],
    },

    "xl/workbook.xml": {
        "name": "Microsoft Excel Spreadsheet",
        "extensions": [".xlsx"],
    },

    "ppt/presentation.xml": {
        "name": "Microsoft PowerPoint Presentation",
        "extensions": [".pptx"],
    }
}

def identifyZipFamily(filepath):
    with zipfile.ZipFile(filepath, 'r') as z:
        names = set(z.namelist())
        for filename, filetype in ZIP_FAMILY.items():
            if filename in names:
                return filetype
    return None