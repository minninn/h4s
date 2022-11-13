
from fpdf import FPDF
import datetime
import final
import db
import path

connect_database = db.connect_database()
path_dir = path.user_path()

def return_filename():
    finish = datetime.datetime.now()
    today = finish.strftime("%Y%m%d")
    filename = str(today) + ".pdf"

    return filename


def input_data():
    url = connect_database.db_get_urls()
    try:
        dt = str(url[-1])
    except:
        dt = 'http://demo.testfire.net'  # if create new database, use demo.testfire.net site

    return dt


def chkRisk(url):
    results = []
    results.append(final.scan_xss(url, ["a"]))
    return results


class PDF(FPDF):
    global duration
    global data
    start = datetime.datetime.now()

    dt = input_data()

    data = []
    data = chkRisk(dt)

    finish = datetime.datetime.now()
    filename = return_filename()

    title = 'Web Scan Report'
    duration = finish - start

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128)
        self.cell(0, 10, 'Page ' + str(self.page_no()), 0, 0, 'C')

    def chapter_body(self):
        url = connect_database.db_get_urls()
        con = connect_database.db_get_payloads()
        self.set_font("Arial", size=27)
        self.cell(200, 20, txt="XSS Vulnerability Scan",
                  ln=1, align="C")
        self.set_text_color(0, 0, 0)
        self.cell(20, 18, txt="Information", ln=1)
        self.set_line_width(1)
        self.set_draw_color(246, 198, 102)
        self.line(10, 45, 200, 45)
        self.image(name='{0}/info.png'.format( path_dir.get_path() ),
                   w=190, h=20, type='png')
        self.set_font("Arial", size=11.5)
        self.set_text_color(0, 0, 0)
        self.cell(20, 5, txt="Website URL = " + str(url[-1]), ln=1)
        self.cell(10, 5, txt="duration = " + str(duration), ln=1)
        self.set_text_color(255, 0, 0)
        self.set_font("Arial", 'B', size=20)
        self.cell(
            10, 20, txt="                                          RISK", ln=1, align="L")

        self.set_font("Arial", 'B', size=18)
        self.set_draw_color(0, 0)
        self.set_line_width(0.5)
        self.set_text_color(0, 0, 0)
        header = ('Response Data')

        cellwidth = 190
        cellHeight = 10

        self.cell(cellwidth, cellHeight*2, txt=header,
                  border=1, ln=1, align="C")
        self.set_font("Arial", size=12)
        for i in range(1):
            line = 1
            if self.get_string_width(data[i][1]) < cellwidth:
                line = 1
            else:
                textLength = len(data[i][0])
                errMargin = 44
                startChar = 0
                maxChar = 0
                textArray = []
                tmpString = ""
                st = data[i][1]
                while (startChar < textLength):
                    while (self.get_string_width(tmpString) < (cellwidth - errMargin) and (startChar+maxChar) < textLength):
                        maxChar += 1
                        tmpString = st[startChar: maxChar]
                    startChar = startChar + maxChar
                    textArray.append(tmpString)
                    line += 1
                    maxChar = 0
                    tmpString = ""
            self.multi_cell(cellwidth, cellHeight,
                            txt=data[i][1], border=1, align="L")

    def print_chapter(self, name):
        self.add_page()
        self.chapter_body(name)
