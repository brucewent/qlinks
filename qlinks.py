# qlinks
# Test the links on a web site

import sys, argparse, datetime
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from pandas import DataFrame
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.styles import PatternFill, Font

def query_link (url, recurse):
    global recursion_level, pages_done, urls_checked, data

    # header string derived from a browser session
    headers = {"Pragma" : "no-cache",
           "Cache-Control" : "max-age=0",
           "Upgrade-Insecure-Requests" : "1",
           "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
           "Accept" : "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
           "Referer" : get_base(url),
           "Accept-Encoding" : "gzip, deflate, br",
           "Accept-Language" : "en-US,en;q=0.9"}

    recursion_level = recursion_level + 1
    prefix_space = recursion_level * "   " + str(recursion_level) + " "

    # read the referenced page
    page_status = "OK"
    try:
        r1 = requests.get(url,headers=headers,timeout=10)

    # catch all errors handled by requests
    except requests.exceptions.RequestException as e:
        page_status = "ConnectErr: " + str(e)
        pass

    # should catch the rest
    except Exception as e:
        page_status = "Unhandled: " + str(e)
        pass

    # return if the page was not available
    if page_status != "OK":
        try:
            if pages_done.index(url) >= 0:
                recursion_level = recursion_level - 1
                return
        except ValueError:
            pass
        pages_done.append(url)
        print (prefix_space + "Page", url, page_status)
        recursion_level = recursion_level - 1
        return

    # parse to a BeautifulSoup object
    soup = BeautifulSoup(r1.text, "lxml")
    try:
        page_title = soup.title.text
    except AttributeError:
        page_title = ""
    base_url = r1.url

    # quit if we did this before
    try:
        if pages_done.index(base_url) >= 0:
            recursion_level = recursion_level - 1
            return
    except ValueError:
        pass

    # add it to the list of URLs done
    pages_done.append(base_url)

    print (prefix_space + "Page \"" + page_title + "\"(" + base_url + ")")

    # find all of the links and iterate over them
    links = soup.findAll('a')
    if not links:
        recursion_level = recursion_level - 1
        return

    links_checked = 0

    for a in links:
        try:
            link_href = a['href'].strip()
        except Exception as e:
            continue

        link_url = urljoin(base_url, link_href)

        link_status = 'OK'
        try:
            r2 = requests.head(link_url,headers=headers,timeout=10)

        # catches all errors handled by requests
        except requests.exceptions.RequestException as e:
            link_status = "ConnectErr: " + str(e)
            pass

        # should catch the rest
        except Exception as e:
            link_status = "Unhandled: " + str(e)
            pass

        # add links to increase console verbosity
        #print (prefix_space + "Link \"" + a.text.strip().replace('\n',' ') + "\" (" + link_url + ") " + link_status)

        data.append({ 'Page_Title' : page_title, \
                      'Page_URL'   : base_url, \
                      'Link_Text' : a.text.strip().replace('\n',' '), \
                      'Link_URL'   : link_url, \
                      'Link_Status' : link_status })

        links_checked = links_checked + 1

        # recurse if requested and the link is to the root site

        if recurse and link_status == 'OK' and get_base(base_url) == get_base(link_url):
            query_link(link_url, recurse)

    recursion_level = recursion_level - 1
    return

def get_base(url):
    my_url = url
    if my_url[len(my_url)-1:] != "/":
        my_url = my_url + "/"
    p1 = my_url.find("//")
    p2 = my_url.find("/", p1 + 2) + 1
    return my_url[:p2]

def write_excel(output):
    global data
    if len(data) == 0:
        print ("No data to write to Excel")
        return
    print ("Writing", len(data), "lines to Excel")
    
    # convert data (list of dictionaries) to df (pandas DataFrame) 
    # and then Excel (openpyxl Workbook)

    df = DataFrame(data)[['Page_Title','Page_URL','Link_Text','Link_URL','Link_Status']]
    wb = Workbook()
    ws = wb.active
    for r in dataframe_to_rows(df, index=False, header=True):
        ws.append(r)

    # pretty up the spreadsheet
    name_date = output + " " + str(datetime.datetime.now())[0:10]
    ws.title = name_date
    ws.freeze_panes = ws['A2']
    ws.auto_filter.ref = "A1:E" + str(df.shape[0]+1)

    # column width & label formatting
    cwidth = {'A' : 30, 'B' : 30, 'C' : 30, 'D' : 30, 'E' : 30}
    font = Font(b=True, i=True)
    fill = PatternFill(start_color='cccccc', end_color='cccccc', fill_type='solid')

    for xk in cwidth:
        ws.column_dimensions[xk].width = cwidth[xk]
        ws[xk+'1'].font = font
        ws[xk+'1'].fill = fill

    # set the hyperlinks
    for xr in range(df.shape[0]):
        ws['B'+str(xr+2)].hyperlink = ws['B'+str(xr+2)].value
        ws['B'+str(xr+2)].style = "Hyperlink"
        ws['D'+str(xr+2)].hyperlink = ws['D'+str(xr+2)].value
        ws['D'+str(xr+2)].style = "Hyperlink"

    # save & wrap up 
    # (loops because you don't want to loose your run when you have the target open in Excel)

    trys = 10
    fname = name_date
    fmsg = "finished saving"
    for fnum in range (trys):
        try:
            wb.save(fname + ".xlsx")
        except Exception as e:
            if fnum+1 == trys:
                fmsg = "failed to save"
                print(e)
            else:
                fname = name_date + "-" + str(fnum+1)

def main():
    # Parse the arguments
	
    parser = argparse.ArgumentParser("qlinks - test the links on a web site")
    parser.add_argument("url", help="Input URL")
    parser.add_argument("--recurse", dest='recurse', action='store_const',
                        const=True, default=False, help="Recurse through links on the site")
    parser.add_argument("--output", dest='output', type=str,
                        default="qlinks", help="Output file name (xlsx format)")
    args = parser.parse_args()

    # define the global variables
	
    global recursion_level, pages_done, urls_checked, data
    recursion_level = -1
    pages_done = []
    urls_checked = []
    data = []

    start_time = datetime.datetime.now()
    print(start_time,"- qlinks starting")

    query_link(args.url, args.recurse)
    write_excel(args.output)

    finish_time = datetime.datetime.now()
    print(finish_time, "- qlinks finished")

    elapsed_time = finish_time - start_time
    print("Elapsed time", elapsed_time)

# The following is required to run as a CLI

if __name__ == '__main__':
    main()
