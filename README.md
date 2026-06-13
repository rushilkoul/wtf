# What The File? (wtf)

A file identification and analysis utility. Classifies files using binary signatures, validates structure, and can discover embedded files.

> **in early development**. 

### Features
- Identify files using binary signatures
- Detect corrupted or partially damaged files
- Distinguish between archive-based file formats (DOCX, PPTX, APK, JAR ...)
- Analyze file integrity and report reasoning
- Discover files embedded in files


A long term goal is to train a model capable of identifying files even when their headers are missing or corrupted.

For example:
```
Likely PNG image (82%)
Possible JPEG image (11%)
Possible GIF image (7%)
```

the model would learn patterns directly from raw byte data.

### Quickstart and usage


> Current external dependencies include only Pillow (PNG/JPEG verification). I plan to implement a custom image parser so no pip install is needed. For now:

```bash
git clone https://github.com/rushilkoul/wtf.git
cd wtf

# using uv (recommended)
uv venv
source .venv/bin/activate

uv pip install -r requirements.txt

# or using pip:

python -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```
 

run it:
```bash
./wtf file.bin
./wtf --deep suspicious.png
./wtf -r Downloads/
```
---
### Roadmap
#### Core
- [x] magic header classification
- [x] ZIP family handling
- [x] confidence scoring
- [x] Integrity analysis framework
- [ ] support more formats for integrity analysis
- [ ] corruption diagnosis
- [ ] recovery attempts

#### Embedded files `--deep`
- [x] embedded file discovery
- [ ] embedded file boundary detection & extraction

#### Machine learning
- [x] dataset generation
- [ ] headerless file classification
- [ ] neural network type prediction
- [ ] recovery assistance for damaged files

---
### Examples:

corruption detection:

<img src="https://i.ibb.co/j9ngGPN2/image.png" width="550" alt="image" border="0">

embedded file detection:

<img src="https://i.ibb.co/wrzYHXNm/image.png" width="400" alt="image" border="0">

archive family best candidate classification:

<img src="https://i.ibb.co/xKXSLXwG/image.png" width="350"  alt="image" border="0">