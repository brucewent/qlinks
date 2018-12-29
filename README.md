# qlinks

This is a Python command line script to test the links on a web site.

```
usage: qlinks - test the links on a web site [--help]
                                             [--recurse]
                                             [--output OUTPUT]
                                             url
positional arguments:
  url              Input URL

optional arguments:
  -h, --help       show this help message and exit
  --recurse        Recurse through links on the site
  --output OUTPUT  Output file name (xlsx format)
```

**qlinks** was developed on Windows 10 with Python 3.7. The primary use case is
checking that the external links on a web site remain valid. The recurse 
flag will include linked pages on the specified web site.

Beyond the use case, the purpose was to learn more about and demonstrate:

* Running a Python script on the command line
* Using requests and BeautifulSoup to retrieve and parse web pages
* Using pandas DataFrame and openpyxl to write a spreadsheet

Hopefully there are enough comments in the code to help someone pick up those topics.

Note: I believe this script should run on Linux or MacOS if the libraries are available. I used the following two steps to enable command line execution on Windows:

* assoc .py=Python.File
* ftype Python.File="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Anaconda3_64\python.exe" "%1" %*

where you will want to substitute the path to your Python executable.

### License

See the LICENSE file for license rights and limitations (MIT).
