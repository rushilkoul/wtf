# What The File? (wtf)

A tiny file identification utility that determines file types with binary signatures instead of their extensions.

> **(work in progress)**. 

Example:
```
cat.png -> renamed to -> random.xyz

$ wtf random.xyz

# output:

random.xyz
 PNG image data
```
This project is an extension-ish to [ByteSweep](https://github.com/rushilkoul/bytesweep). ByteSweep works well for what it is, but leans more towards cleanup rather than actual recovery and analysis, which is what i originally intended for ByteSweep to be.

Eventually, I want this project to be able to classify files using a neural network. The cool part would be when a file header is gone but `wtf file.bin` still says: 

*Probably PNG*

by running pattern recognition on the raw byte patterns. This could even potentially find other files embedded in the target file. For example, executables hidden in images.

> The scope for training a model is decent. `scrambler.py` already generates files, with minor changes it is possible to automatically generate large supervised datasets

this could probably be used as a straightforward CLI tool, and also incorporated directly into ByteSweep making it more powerful.

### Roadmap
- [x] classifying using magic headers
- [ ] confidence scoring
- [ ] ZIP family handling (distinguish between `DOCX / XLSX / PPTX / JAR ..etc`)
- [ ] headerless file classification
- [ ] deep probing for files embedded in files
- [ ] some form of corruption analysis (ties into recovery)
- [ ] train a model to classify files from binary patterns.
