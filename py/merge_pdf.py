# merge_pdf.py
# usage: 
#   复制到目标目录，由终端进入，运行 "python3 merge_pdf.py" 命令即可。

import os
from PyPDF2 import PdfFileReader, PdfFileWriter

filenames = []
outfile = '../temp.pdf'

def getfiles(curr_dir='.', ext='.pdf'):
    global filenames
    dir = os.path.abspath(curr_dir)
    files = os.listdir(dir)
    for f in files:
        path = os.path.join(dir,f)
        if os.path.isdir(path):
            getfiles(path, ext)
            continue
        extname = os.path.splitext(f)[1]
        if ext == extname:
            filenames.append(os.path.join(dir,f))

def merge():
    getfiles()
    filenames.sort()
    writer = PdfFileWriter()
    pages = 0
    for f in filenames:
        print(f)
        reader = PdfFileReader(open(f, 'rb'))
        count = reader.getNumPages()
        pages += count
        for i in range(count):
            writer.addPage(reader.getPage(i))
        writer.addBookmark(os.path.basename(f)[:-3],pages - count)
    stream = open(outfile, 'wb')
    writer.write(stream)
    stream.close()
    print("OK!")

if __name__ == '__main__':
    filenames.clear()
    merge()
