# Bandit Level 12 → Level 13 Solution

**Objective:**  
Extract the password from `data.txt`, which is a hexdump of a file that was repeatedly compressed.

---

## Steps

### 1. Create a Temporary Working Directory
It’s best practice to work in a scratch directory:
```bash
tmp_dir=$(mktemp -d)
cd $tmp_dir
```

### 2. Copy the Challenge File
```bash
cp ~/data.txt .
```

### 3. Reverse the Hexdump
`xxd -r` converts the hexdump back into its original binary form:
```bash
xxd -r data.txt > data.bin
```

### 4. Identify File Type
Check what kind of compressed file it is:
```bash
file data.bin
```

### 5. Decompress Step by Step
Rename and decompress accordingly:
```bash
mv data.bin data.gz
gunzip data.gz
```

### 6. Continue Extraction
Some files are tar archives, some are gzipped, others bzip2, etc. Use the right tool each time:
```bash
tar xvf data      # for tar
bunzip2 data.bz2  # for bzip2
gunzip data.gz    # for gzip
```

Repeat this process until no further compression layers remain.

### 7. Final File
Eventually, you’ll end up with a file named `data8`. Inspect it:
```bash
cat data8
```

### 8. Result
The file contains the ASCII password for **Bandit Level 13**:
```
[REDACTED]
```
