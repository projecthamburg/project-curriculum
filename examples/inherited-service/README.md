# inherited-service

A small record-processing service. We inherited it; the original authors are gone and no
design discussion survives.

Records are read from a flat file, filtered, and written back out. The format round-trips
cleanly, so an exported file can be fed straight back in.

## Usage

```
python3 -m src.app records.txt
python3 -m src.export out.txt
```
