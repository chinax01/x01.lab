import os

def md2pdfs(currdir='.'):
    dir = os.path.abspath(currdir)
    files = os.listdir(dir) 
    for f in files:
        path = os.path.join(dir, f)
        if os.path.isdir(path):
            md2pdfs(path)
            dir = os.path.dirname(path)
            continue
        name = os.path.splitext(f)[0]
        ext = os.path.splitext(f)[1]
        if ext == '.md':
            mdfile = f
            pdffile = name + '.pdf'
            os.chdir(dir)
            print(os.getcwd() + '/' + f)
            cmd = "pandoc '{0}' -o '{1}' --latex-engine=xelatex -V mainfont='PingFang SC' --template=template.tex".format(mdfile, pdffile)
            os.system(cmd)
        
        

if __name__ == '__main__':
    md2pdfs()