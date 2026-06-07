import zipfile

def createResult(file, filetype):
    return {
        "file": file,
        "type": filetype,
        "integrity": 100,
        "reasons": ["+ Valid header"],
        "warnings": [],
    }

def analyzeWoff(filepath):
    result = createResult(filepath, "woff2");
    with open(filepath, 'rb') as f:
        data = f.read(4)
    if data == b"wOFF":
        result["type"] = "Web Open Font Format (WOFF) font"
    elif data == b"wOF2":
        result["type"] = "Web Open Font Format 2 (WOFF2) font"
    
    return result

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
    },
    "AndroidManifest.xml": {
        "name": "Android Application Package",
        "extensions": [".apk"], 
    },
    "META-INF/MANIFEST.MF": {
        "name": "Java Archive",
        "extensions": [".jar"], 
    },
}

# TODO: Begin confidence scoring as a single file can satisfy multiple probes. 
# create a potential files list and return the most confident file.
# eg: apk also has MANIFEST.MF same as jar files. rn it works because i've put it above the JAR so it
# detects it first naturally and exits. Later, it should recognize that the file 
# passes the check for both a jar and an apk, and further probing like the presence of androidManifest and
# other similar files should increase confidence that it is an apk rather than a jar, returning the 
# apk as the MOST probable file :p

def analyzeZip(filepath):
    result = createResult(filepath, "zip")
    with zipfile.ZipFile(filepath, 'r') as z:
        names = set(z.namelist())
        # if filepath.endswith(".apk"): print(z.namelist())
        # if filepath.endswith(".apk"): z.extractall('tmp')
        for filename, filetype in ZIP_FAMILY.items():
            if filename in names:
                result["file"] = filetype["name"]
    return result


# -------------------------
# file validators
# -------------------------

# each analyzer begins with a preset confidence and reason, 
# we got here in the first place cuz the magic header matches


from PIL import Image
# TODO: REPLACE PILLOW, PARSE PNG MANUALLY. 
# remove all dependencies to keep the overlords happy

def analyzePNG(file, offset=0):
    """
    PNG STRUCTURE:
    \x89 P N G - 8 bytes, header

    xx xx xx xx - 4 bytes, chunk length
    I H D R - 4 bytes. IHDR marker.

    ... CHUNKS ...

    00 00 00 00 - 4 bytes, chunk length
    I E N D - 4 bytes. IEND marker.
    xx xx xx xx - 4 bytes, CRC
    4 bytes
    """
    integrity = 20.0
    reasons = ["+ Valid PNG header"]
    warnings = []

    with open(file, 'rb') as f:
        data = f.read()
        if data[offset + 12:offset + 16] == b"IHDR":
            integrity += 20
            reasons.append("+ IHDR marker found")
        iend = data.rfind(b"IEND")
        if iend != -1:
            integrity += 20

            trailing = len(data) - (iend + 8)
            if trailing == 0:
                reasons.append("+ IEND marker found near EOF")
                integrity += 10
            else:
                reasons.append("+ IEND marker found")
                warnings.append(f"- {trailing} trailing bytes found after IEND")
        else:
            integrity -= 20
            reasons.append("- IEND marker missing")

    try:
        with Image.open(file) as img:
            img.verify()

        integrity = 100
        reasons.append("+ Successfully parsed image")

    except Exception as e:
        integrity -= 40
        reasons.append(f"- Parsing failed: {e}")


    integrity = min(integrity, 100)
    return {
            "file": file, 
            "type": "PNG image data",
            "reasons": reasons,
            "integrity": integrity,
            "warnings": warnings,
    }
    