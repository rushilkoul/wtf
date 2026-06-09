import zipfile

class Result:

    def __init__(self, file, filetype):
        self.warnings = []
        self.reasons = []
        self.integrity = 0.0;
        self.confidence = 0.0;
        self.file = file
        self.type = filetype
        self.offset = 0;

    def addEvidence(self, points, evidence):
        self.confidence += points
        self.confidence = max(0, min(100, self.confidence))

        if(evidence[0] == "!"):
            self.warnings.append(evidence)
        else: self.reasons.append(evidence)

    def setIntegrity(self, integrity):
        self.integrity = integrity
        # if integrity >= 99: self.confidence += 50 

    def validHeader(self, type=""):
        if type != "": type += " "
        self.confidence += 20.0
        self.reasons.append(f"+ Valid {type}header")

    def setOffset(self, offset):
        self.offset = offset


def analyzeWoff(filepath, offset=0):
    result = Result(filepath, "woff2")
    result.setOffset(offset)
    
    with open(filepath, 'rb') as f:
        data = f.read(4)
    if data == b"wOFF":
        result.type = "Web Open Font Format (WOFF) font"
        result.validHeader("WOFF")
    elif data == b"wOF2":
        result.type = "Web Open Font Format 2 (WOFF2) font"
        result.validHeader("WOFF2")
    
    result.setIntegrity(100) # for now
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

def analyzeZip(filepath, offset=0):
    result = Result(filepath, "ZIP")
    result.setOffset(offset)

    
    with zipfile.ZipFile(filepath, 'r') as z:
        names = set(z.namelist())
        # if filepath.endswith(".apk"): print(z.namelist())
        # if filepath.endswith(".apk"): z.extractall('tmp')
        for filename, filetype in ZIP_FAMILY.items():
            if filename in names:
                result.type = filetype["name"]
                result.validHeader(filetype["name"])
            
    result.setIntegrity(100) # for now
    return result


# -------------------------
# file validators
# -------------------------


# TODO: REPLACE PILLOW, PARSE PNG MANUALLY. 
# remove all dependencies to keep the overlords happy
from PIL import Image

def tryPillowParse(file, result):
    try:
        with Image.open(file) as img:
            img.verify()

        result.addEvidence(100, "+ Successfully parsed image")
        result.setIntegrity(100)
    except Exception as e:
        result.addEvidence(-10, "- Parsing failed: {e}")
        result.setIntegrity(0)


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
    result = Result(file, "PNG image data")
    result.validHeader("PNG")
    result.setOffset(offset)

    with open(file, 'rb') as f:
        data = f.read()[offset:]
        if data[12:16] == b"IHDR":
            result.addEvidence(20, "+ IHDR marker found")
        iend = data.rfind(b"IEND")
        if iend != -1:
            trailing = len(data) - (iend + 8)
            if trailing == 0:
                result.addEvidence(30, "+ IEND marker found near EOF")
            else:
                result.addEvidence(20, "+ IEND marker found")
                result.addEvidence(0, f"! {trailing} trailing bytes found after IEND")
        else:
            result.addEvidence(-20, "+ IEND marker missing")

    tryPillowParse(file, result)

    return result
    
def analyzeJPEG(file, offset=0):
    """
    JPEG
    is a very funky format, JFIF, JPG, EXIF, APP1, help

    wtf will check for:
    ffd8 - Start Of Image
    ffc0 - Start of Frame ~ this is weird, different formats can have different SOFs
                            going to test for ff followed by c0 to cf except reserved ones
    ffda - Start Of Scan
    ffd9 - End Of Image 
    """
    result = Result(file, "JPEG image data")
    result.addEvidence(20, "+ Valid JPEG Header")
    result.setOffset(offset)

    with open(file, 'rb') as f:
        data = f.read()[offset:]
        
    
    eoi = data.rfind(b"\xff\xd9")

    if eoi != -1:
        trailing = len(data) - (eoi + 2)
        if trailing == 0:
            result.addEvidence(30, "+ EOI marker found near EOF")
        else:
            result.addEvidence(20, "+ EOI marker found")
            result.addEvidence(0, f"! {trailing} trailing bytes found after EOI")
    else:
            result.addEvidence(-20, "- EOI marker missing")

    if b'\xff\xda' in data:
        result.addEvidence(20, "+ SOS marker found")
    else: 
        result.addEvidence(-20, "- SOS marker missing")

    sof_markers = [
        b'\xff\xc0', b'\xff\xc1', b'\xff\xc2', b'\xff\xc3',
        b'\xff\xc5', b'\xff\xc6', b'\xff\xc7',
        b'\xff\xc9', b'\xff\xca', b'\xff\xcb',
        b'\xff\xcd', b'\xff\xce', b'\xff\xcf'
    ]

    for marker in sof_markers:
        if marker in data:
            result.addEvidence(20, "+ SOF marker found")
            break;
    else:
        result.addEvidence(-20, "- SOF marker missing")

    tryPillowParse(file, result)


    return result

def parsePE(data, result):
    """
    A naive parser for portable executables.

    checks for the binary sections:
        .text
        .data
        .rdata
        .rsrc
    
    Will improve the parser to actually evaluate the section table
    and navigate the offset chain
    (later :D)
    """

    integ = 0;
    if b".text" in data:
        integ += 25
    if b".data" in data:
        integ += 25
    if b".rdata" in data:
        integ += 25
    if b".rsrc" in data:
        integ += 25
    
    result.setIntegrity(integ)
    if integ == 100:
        result.addEvidence(20, "+ Parsed successfully")

def analyzePE(file, offset=0):
    """
    Windows Portable Executable

    testing for:
    A small DOS stub for legacy compatibility
    PE header at offset 0x3c
    """
    result = Result(file, "Windows Portable Executable data")
    result.addEvidence(20, "+ Valid MZ Header")
    result.setOffset(offset)
    
    with open(file, 'rb') as f:
        data = f.read()[offset:]

        stub = b"This program cannot be run in DOS mode" # cute

        stub_pos = data.find(stub)
    
    if 0 <= stub_pos <= 1024:
        result.addEvidence(50, "+ Found DOS stub")
    else:
        result.addEvidence(-5, "- Missing DOS stub")

    try:
        pe_offset = int.from_bytes(
            data[0x3C:0x40],
            "little"
        )

        if data[pe_offset:pe_offset+4] == b"PE\x00\x00":
            result.addEvidence(
                40,
                "+ Valid PE header"
            )
        else:
            result.addEvidence(
                -40,
                "- Invalid PE header"
            )

    except:
        result.addEvidence(
            -40,
            "- Invalid e_lfanew"
        )

    parsePE(data, result)

    return result




# done to reduce noise during testing --deep mode. 
# will later write proper analyzers
def analyzeBMP(file, offset=0):
    result = Result(file, "Bitmap Image");
    return result

def analyzeTTF(file, offset=0):
    result = Result(file, "TrueType Font");
    return result

def analyzeICO(file, offset=0):
    result = Result(file, "ICO image");
    return result

