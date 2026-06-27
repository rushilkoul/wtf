# What The File? (wtf)

A file identification and analysis utility. Classifies files using binary signatures, validates structure, explains its reasoning, and discovers embedded files.

> **in early development**. 

### Features
- Identify files using binary signatures
- Detect corrupted or partially damaged files
- Distinguish between archive-based file formats (DOCX, PPTX, APK, JAR ...)
- Analyze file integrity and report reasoning
- Discover files embedded in files
- Experimental machine learning classifier for headerless file identification


### Machine Learning
`wtf` includes an experimental machine learning model capable of classifying supported file types using statistical features extracted from the file's byte patterns, instead of relying on magic headers.

> what?

File type identification depends on a small sequence of bytes at the very beginning of the file that identifies what format it is, called the header or magic number. If this header were missing, corrupted or intentionally modified, most traditional tools would immediately fail to identify the file type.

The current implementation uses a Random Forest trained on byte frequency histograms and entropy, which lets it make an informed prediction on the file type even when the header is not present. It is intended as a fallback for files that have missing or corrupted headers. For more information about the model setup and performance, go to `ml/README.md`

In the long term i would like to replace this statistical model with a Transformer-based classifier.

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
- [x] headerless file classification
- [ ] integrate into CLI
- [ ] recovery assistance for damaged files
- [ ] transformer classifier

---
### Examples:

corruption detection:

<img src="https://i.ibb.co/j9ngGPN2/image.png" width="550" alt="image" border="0">

embedded file detection:

<img src="https://i.ibb.co/wrzYHXNm/image.png" width="400" alt="image" border="0">

archive family best candidate classification:

<img src="https://i.ibb.co/xKXSLXwG/image.png" width="350"  alt="image" border="0">