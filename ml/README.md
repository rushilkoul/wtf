### wtf's machine learning stuffs

```bash
uv pip install -r requirements.txt
```

dataset directory `ml/dataset`
(not pushing this, way too many files)
```
dataset
├── csv
├── jpg
├── pdf
├── plaintxt
└── png
└── ...etc
```

generate `dataset.csv`:
```
python generate_dataset.py
```
picks a random offset, , reads 1024 bytes, creates a histogram, stores it.

Each dataset row consists of:

`[byte0, byte1, ..byte255, label]`

Example: `137,80,78,71,...,png` or
`255,216,255,...,jpg`

train random forest model:
```
python train_random_forest.py
```

creates `model.joblib`.

test:
```
python random_forest.py <yourfile>
```