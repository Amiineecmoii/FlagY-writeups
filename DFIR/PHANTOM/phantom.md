# 🕵️ Windows Thumbnail Cache Forensics – Deleted Image Recovery

## 📌 Challenge Description

> A suspicious image file was deleted from a user's system, but remnants of it may still exist within the Windows cache. Your task is to recover this deleted image and uncover the hidden flag.

- **Flag format:** `FlagY{}`
- **Category:** Forensics (Windows Internals)
- **Technique:** Thumbnail Cache Analysis & Image Carving

---

## 🧠 Forensic Background

Windows Explorer caches thumbnails of images to improve performance.  
These thumbnails persist **even after the original file is deleted** and are stored inside binary databases located at:

***%LocalAppData%\Microsoft\Windows\Explorer\***
```bash
These artifacts are frequently used in **DFIR investigations** to recover deleted images, screenshots, and previews of sensitive files.

---
```
## 📂 Evidence Structure

The provided archive contained the following artifacts:

```text
Local/
└── Microsoft/
    └── Windows/
        └── Explorer/
            ├── thumbcache_32.db
            ├── thumbcache_48.db
            ├── thumbcache_96.db
            ├── thumbcache_256.db
            ├── thumbcache_1920.db
            ├── thumbcache_2560.db
            ├── thumbcache_idx.db
            ├── iconcache_*.db

```
**Relevant Files**

| File                | Description              |
| ------------------- | ------------------------ |
| `thumbcache_*.db`   | Cached image thumbnails  |
| `thumbcache_idx.db` | Index mapping thumbnails |
| `iconcache_*.db`    | Cached application icons |

High-resolution caches (`thumbcache_1920.db`, `thumbcache_2560.db`) are the most valuable targets.

## 🔍 Step 1 – File Identification

Thumbnail cache databases are raw binary files:
```bash
file thumbcache_2560.db
```
Output:
```bash
data
```
This confirms the absence of encryption or compression.

## 🔓 Step 2 – Image Carving from Thumbnail Cache

Windows thumbnail cache databases store complete image blobs, identifiable using standard magic bytes.

**Image Signatures**
| Format | Header                    | Footer        |
| ------ | ------------------------- | ------------- |
| JPEG   | `FF D8 FF`                | `FF D9`       |
| PNG    | `89 50 4E 47 0D 0A 1A 0A` | `49 45 4E 44` |


**Extraction Logic**

>Scan database for image headers

>Extract bytes until matching footer

>Save carved data as image files

## 🛠️ Automated Extraction Script 
```python
def carve_images(data, header, footer):
    images = []
    offset = 0
    while True:
        h = data.find(header, offset)
        if h == -1:
            break
        f = data.find(footer, h)
        if f == -1:
            break
        f += len(footer)
        images.append(data[h:f])
        offset = f
    return images

with open("thumbcache_2560.db", "rb") as f:
    data = f.read()

jpgs = carve_images(data, b'\xff\xd8\xff', b'\xff\xd9')

for i, img in enumerate(jpgs):
    with open(f"recovered_{i}.jpg", "wb") as out:
        out.write(img)
```

## 🖼️ Step 3 – Analysis of Recovered Images

>Total recovered images: 41

>Most images were low-resolution previews

>One image had resolution 902×1280

>High resolution strongly indicates relevance to original content

## 🧾 Step 4 – Flag Extraction

Opening the high-resolution recovered image revealed embedded text:

```csharp
Even when a file is gone, a picture might still hold the truth.
Dig deep into the cache.
```
Below the message:

**FlagY{54ddc3c*******************************}**


> ⚠️ **Note on Responsible Disclosure**
>
> In respect of the **FlagYard platform rules** and the effort invested by its authors to provide **high-quality challenges**, I am **not sharing the flag directly** in this repository.
>
> This write-up is provided **for educational purposes only**.  
> Please take the time to **understand each step**, reproduce the analysis yourself, and **learn from the reversing techniques used**.
>
> Do **not** treat this as a copy-paste solution.
>
> **CTRL+C ❌ CTRL+V ❌**  
> **Reverse, analyze, and learn instead.**
