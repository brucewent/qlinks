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
  --output OUTPUT  Output file (default qlinks): "<OUTPUT> YYYY-MM-DD.xlsx"
```

**qlinks** was developed on Windows 10 with Python 3.7. The primary use case is
checking that the links on a web site remain valid. The recurse flag will include 
linked pages on the specified web site. Output is to an Excel xlsx spreadsheet.

Beyond the use case, the purpose was to learn more about and demonstrate:

* Running a Python script on the command line using argparse
* Using requests with BeautifulSoup and lxml to retrieve and parse web pages
* Using pandas DataFrame and openpyxl to write a spreadsheet

Hopefully there are enough comments in the code to help someone pick up those topics. 
Please let me know if you have found this useful, have any questions/suggestions, or 
have found an interesting web site that breaks it.

Note: I believe this script should run on Linux or MacOS if the libraries are available. 
I used the following two steps to enable command line execution on Windows:

* assoc .py=Python.File
* ftype Python.File="C:\Program Files (x86)\Microsoft Visual Studio\Shared\Anaconda3_64\python.exe" "%1" %*

where you will want to substitute the path to your Python executable. Please see the 
file pipshow.txt for information on my environment.

### Some References

http://docs.python-requests.org/  
https://www.crummy.com/software/BeautifulSoup/bs4/doc/  
https://lxml.de/  
http://pandas.pydata.org/pandas-docs/stable/  
https://openpyxl.readthedocs.io/en/stable/  
https://validator.w3.org/checklink  
https://en.wikipedia.org/wiki/List_of_HTTP_status_codes  
https://en.wikipedia.org/wiki/List_of_HTTP_header_fields  
https://en.wikipedia.org/wiki/Meta_refresh  

### License

See the LICENSE file for license rights and limitations (MIT).
