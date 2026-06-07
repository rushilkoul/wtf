SIGNATURES = [
    # images
    {
        "name": "PNG image data",
        "extensions": [".png"],
        "signatures": (
            b"\x89PNG\r\n\x1a\n",
        ),
        "offset": 0
    },
    {
        "name": "JPEG image data",
        "extensions": [".jpg", ".jpeg"],
        "signatures": (
            b"\xff\xd8\xff",
        ),
        "offset": 0
    },
    {
        "name": "GIF image data",
        "extensions": [".gif"],
        "signatures": (
            b"GIF87a",
            b"GIF89a",
        ),
        "offset": 0
    },
    {
        "name": "BMP image data",
        "extensions": [".bmp"],
        "signatures": (b"BM",),
        "offset": 0
    },
    {
        "name": "WEBP image data",
        "extensions": [".webp"],
        "signatures": (b"WEBP",),
        "offset": 8
    },
    {
        "name": "TIFF image data",
        "extensions": [".tif", ".tiff"],
        "signatures": (
            b"II*\x00",
            b"MM\x00*",
        ),
        "offset": 0
    },
    {
        "name": "ICO image data",
        "extensions": [".ico"],
        "signatures": (b"\x00\x00\x01\x00",),
        "offset": 0
    },

    {
        "name": "Adobe Photoshop document",
        "extensions": [".psd"],
        "signatures": (b"8BPS",),
        "offset": 0
    },
    {
        "name": "OpenEXR image",
        "extensions": [".exr"],
        "signatures": (b"\x76\x2F\x31\x01",),
        "offset": 0
    },

    # docs
    {
        "name": "PDF document",
        "extensions": [".pdf"],
        "signatures": (b"%PDF",),
        "offset": 0
    },

    # executables
    {
        "name": "Windows executable",
        "extensions": [".exe", ".dll", ".sys"],
        "signatures": (
            b"MZ",
        ),
        "offset": 0
    },

    {
        "name": "ELF executable",
        "extensions": [".elf"],
        "signatures": (
            b"\x7FELF",
        ),
        "offset": 0
    },

    # audio
    {
        "name": "FLAC audio",
        "extensions": [".flac"],
        "signatures": (
            b"fLaC",
        ),
        "offset": 0
    },
    {
        "name": "OGG container",
        "extensions": [".ogg", ".opus"],
        "signatures": (
            b"OggS",
        ),
        "offset": 0
    },

    {
        "name": "WAV audio",
        "extensions": [".wav"],
        "signatures": (
            b"WAVE",
        ),
        "offset": 8
    },
    {
        "name": "MP3 audio",
        "extensions": [".mp3"],
        "signatures": (
            b"ID3",
        ),
        "offset": 0
    },

    # video 

    {
        "name": "MP4 container",
        "extensions": [".mp4", ".m4v"],
        "signatures": (
            b"ftyp",
        ),
        "offset": 4
    },

    {
        "name": "Matroska container",
        "extensions": [".mkv", ".webm"],
        "signatures": (
            b"\x1A\x45\xDF\xA3",
        ),
        "offset": 0
    },

    {
        "name": "AVI container",
        "extensions": [".avi"],
        "signatures": (
            b"AVI ",
        ),
        "offset": 8
    },

    # fonts
     {
        "name": "TrueType font",
        "extensions": [".ttf"],
        "signatures": (
            b"\x00\x01\x00\x00\x00",
        ),
        "offset": 0
    },

    {
        "name": "OpenType font",
        "extensions": [".otf"],
        "signatures": (
            b"OTTO",
        ),
        "offset": 0
    },
    {
        "name": "Web Open Font Format (WOFF) font",
        "extensions": [".woff"],
        "signatures": (
            b"wOFF",
        ),
        "offset": 0,
    },
    # TODO: figure out how to make this WOFF thing into one. 
    # this is also a problem i will experience with MS Office documents, because
    # they are all also basically zip files. how do i then say if its a .docx or .xlsx
    # or a .pptx if they all have the same headers?
    #   i need some form of further classifier for ambiguous files like these, 
    #   once ive established roughly what kind of file it is.
    {
        "name": "Web Open Font Format 2 (WOFF2) font",
        "extensions": [".woff2"],
        "signatures": (
            b"wOF2",
        ),
        "offset": 0,
    },
    
    # archives
    {
        "name": "ZIP archive",
        "extensions": [".zip"],
        "signatures": (
            b"PK\x03\x04",
        ),
        "offset": 0
    },

    {
        "name": "Microsoft Compound Document",
        "extensions": [".doc", ".xls", ".ppt", ".msi"],
        "signatures": (
            b"\xD0\xCF\x11\xE0\xA1\xB1\x1A\xE1",
        ),
        "offset": 0
    },

    # 3D / graphics
    {
        "name": "Blender file",
        "extensions": [".blend", ".blend1"],
        "signatures": (
            b"BLENDER",
        ),
        "offset": 0
    },
    {
        "name": "FBX model",
        "extensions": [".fbx"],
        "signatures": (
            b"Kaydara FBX Binary",
        ),
        "offset": 0
    },
    
]

def identify(data):
    matches = []

    for filetype in SIGNATURES:
        offset = filetype.get("offset", 0)
        for sig in filetype["signatures"]:
            if data.startswith(sig, offset):
                matches.append(filetype)
                break

    return matches


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