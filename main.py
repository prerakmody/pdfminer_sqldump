"""
PDFMiner
https://github.com/pdfminer/pdfminer.six
http://www.unixuser.org/~euske/python/pdfminer/programming.html

Blogs:
https://dzone.com/articles/pdf-reading
http://okfnlabs.org/blog/2016/04/19/pdf-tools-extract-text-and-data-from-pdfs.html
https://media.readthedocs.org/pdf/pdfminer-docs/latest/pdfminer-docs.pdf
"""

"""
MySQL
 - https://support.rackspace.com/how-to/installing-mysql-server-on-ubuntu/
 - sudo service mysql status
 - /usr/bin/mysql -u <username> -p

 - SQL Commands
  - "show databases;"
  - "create database zauba;"
  - "use zauba;"
  - "show tables;"
 - Ubuntu MySQL Command
  - /usr/bin/mysql -u root -p  
  - mysqldump -u root -p zauba > data/zauba.sql
  - mysql -u root -p zauba < data/zauba.sql

Python Connectors
 - Repo : https://github.com/PyMySQL/mysqlclient-python

"""

from pdfminer.layout import LAParams 
from pdfminer.pdfpage import PDFPage 
from pdfminer.converter import PDFPageAggregator
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LTTextBoxHorizontal, LTLine
import csv
import pprint
import MySQLdb
import traceback

def extract_pdf(pdf_filename, password = '', print_test = 1):

    # PDF EXTRACTION USING PDFMINER
    document = open(pdf_filename, 'rb') 
    rsrcmgr = PDFResourceManager() 
    laparams = LAParams() 
    device = PDFPageAggregator(rsrcmgr, laparams=laparams) 
    interpreter = PDFPageInterpreter(rsrcmgr, device) 
    
    mypdf_elements = []
    for page in PDFPage.get_pages(document): 
        interpreter.process_page(page) 
        layout = device.get_result()
        for i, element in enumerate(layout): 
            # if i == 0: print (dir(element))
            tmp = { 'type' : element, 'y0' : round(float(element.y0),1), 'y1' : round(float(element.y1),1), 'text': '' }
            if isinstance(element, LTTextBoxHorizontal): 
                tmp['text'] = element.get_text()
                mypdf_elements.append(tmp)
    mypdf_elements = sorted(mypdf_elements, key = lambda x : x['y1'], reverse = True)

    res = {
        'SRN': '', 'Service Request Date': '',
        'Payment Made Into': '',
        'Name': '', 'Address': '',
        'Service Type': '',
        'Service Description': '', 'Type of Fee': '','Amount': '', 'Total' : '',
        'Mode of Payment': '',   'Received Payment Rupees': '',   
    }

    # PARSING LOGIC (SLIGHTLY CONVOLUTED)
    idx_address_max = -1
    idx_total = -1
    idx_amount = -1
    for i, each in enumerate(mypdf_elements):
        if each['text'].find('Service Type: ') > -1:
            idx_address_max = i - 1
        if each['text'].replace('\n','').replace(' ','') == 'Total':
            idx_total = i
        
    for i, each in enumerate(mypdf_elements):
        try:
            # SRN / Service Request Date
            if each['text'].find('Service Request Date : ') > -1:
                res['Service Request Date'] = each['text'].split('Service Request Date : ')[1].replace('\n', '')
                tmp = res['Service Request Date'].split('/')
                res['Service Request Date'] = '/'.join([tmp[2], tmp[1], tmp[0]])
            if each['text'].find('SRN : U') > -1 :
                res['SRN']  = each['text'].split(' ')[2].split('\n')[0]
            
            # Payment Made Into
            if i == 4:
                res['Payment Made Into'] = each['text'].replace('\n', '')
            
            # Name / Address / Service Type
            if i == 6:
                res['Name'] = each['text'].split('\n')[0] 
                res['Address'] = ' '.join(each['text'].split('\n')[1:])
            if i > 6 and i <= idx_address_max:
                res['Address'] += each['text']
            if each['text'].find('Service Type: ') > -1:
                res['Service Type'] = each['text'].split('Service Type: ')[1].replace('\n','')
            
            # Service Description / Type of Fee / Amount / Total
            if i == idx_address_max + 5:
                res['Service Description'] = each['text'].replace('\n', '')
            if i == idx_address_max + 6:
                res['Type of Fee'] = each['text'].replace('\n', '')
            if i == idx_address_max + 7:
                res['Amount'] = each['text'].replace('\n', '').replace(' ','')
                try:
                    tmp = float(res['Amount'])
                    idx_amount = i
                except Exception as e:
                    print ('Error in float conversion')
            if idx_amount > 0 and i > idx_amount and i < idx_total:
                res['Service Description'] = res['Service Description'] + ' ' + each['text'].replace('\n', '')
            if i == idx_total + 1:
                res['Total'] = each['text'].replace('\n', '').replace(' ', '')

            #  Received Payment Rupees / Mode of Payment
            if i == idx_total + 2:
                res['Received Payment Rupees'] = each['text'].split('\n')[1].split(': ')[1]
                res['Received Payment Rupees'] = res['Received Payment Rupees'][1:].replace('\r', '')
            if i == idx_total + 3:
                res['Mode of Payment'] = each['text'].replace('\n','')

        except Exception as e:
            traceback.print_exc()
            print ('Error in file {0} -----> Text: {1}'.format(pdf_filename, each['text']))    
            print_test = 1
        
    if print_test:
        for i, each in enumerate(mypdf_elements):
            tmp_text = each['text'].replace('\n', ' ?? ')
            if i < idx_address_max:
                print (i, '\t\t', tmp_text)
            else:
                print (i, '(',i - idx_address_max, ')', '\t\t', tmp_text)
        pprint.pprint(res)

    return res

def create_csvfile(csv_filename, pdf_extract_obj_list):
    with open(csv_filename, "w") as fp:
        fp_csv = csv.writer(fp)
        for pdf_extract_obj in pdf_extract_obj_list:
            fp_csv.writerow([
                        pdf_extract_obj['SRN'],
                        pdf_extract_obj['Service Request Date'],
                        pdf_extract_obj['Payment Made Into'],
                        pdf_extract_obj['Name'],
                        pdf_extract_obj['Address'],
                        pdf_extract_obj['Service Type'],
                        pdf_extract_obj['Service Description'],
                        pdf_extract_obj['Type of Fee'],
                        pdf_extract_obj['Amount'],
                        pdf_extract_obj['Total'],
                        pdf_extract_obj['Mode of Payment'],
                        pdf_extract_obj['Received Payment Rupees']
                    ])

def db_check(conn, cursor):
    try:
        query_test = "describe zauba_mca;"
        cursor.execute(query_test)
        data = cursor.fetchall()
        print ('Table Desc: ', data, '\n')
    except:
        query_create = """
            CREATE TABLE zauba_mca(
                srn VARCHAR(16),
                service_request_date DATE,
                payment_made_into VARCHAR(128),
                name VARCHAR(128),
                address VARCHAR(512),
                service_type VARCHAR(128),
                service_description VARCHAR(512),
                fee_type VARCHAR(32),
                amount FLOAT,
                total FLOAT,
                payment_mode VARCHAR(128),
                received_payment_rupees VARCHAR(128)   
            );
        """
        cursor.execute(query_create)
        data = cursor.fetchall()
        print ('Table created')
        conn.commit()

def data_dump(conn, cursor, pdf_extract_obj, csv_filename):
    query_delete = "DELETE FROM zauba.zauba_mca;"
    cursor.execute(query_delete)
    print ('Rows deleted:', cursor.rowcount)
    conn.commit()

    query_insert = """
        LOAD DATA LOCAL INFILE "{0}" 
        INTO TABLE zauba.zauba_mca 
        FIELDS TERMINATED BY ',' 
        OPTIONALLY ENCLOSED BY '"'
        LINES TERMINATED BY '\n'
        """.format(csv_filename)
    print ('\nInsert Query : ', query_insert.replace('\n', ' '))
    cursor.execute(query_insert)
    conn.commit()

    query_select = ("SELECT COUNT(DISTINCT(srn)) FROM zauba.zauba_mca")
    cursor.execute(query_select)
    data = cursor.fetchall()
    print ('\nRows Inserted : ', data[0][0])

    query_select = ("SELECT *, service_request_date FROM zauba.zauba_mca")
    query_select = ("SELECT name, address, service_type,service_description, fee_type, amount, total, payment_mode, received_payment_rupees FROM zauba.zauba_mca")
    cursor.execute(query_select)
    data = cursor.fetchall()
    print ('\nSample Row : ', data[0])

    
if __name__ == "__main__":
    print (' =============== 1. EXTRACTING JSON(s) =============== ')
    pdf_extract_obj_list = []
    pdf_filenames = ['data/U16571275.pdf', 'data/U16572745.pdf', 'data/U16573131.pdf', 'data/PaymentResponseShowReceipt.pdf']
    for pdf_filename in pdf_filenames:
        print (' ---> ', pdf_filename)
        pdf_extract_obj = extract_pdf(pdf_filename, print_test = 0)
        pdf_extract_obj_list.append(pdf_extract_obj)

    csv_filename = 'data/data_zauba.csv'
    create_csvfile(csv_filename, pdf_extract_obj_list)
    conn = MySQLdb.connect(host = '127.0.0.1',user = 'root', passwd = 'root',db = 'zauba')
    cursor = conn.cursor()

    print ('\n =============== 2. DB CHECK =============== ')
    db_check(conn, cursor)

    print ('\n =============== 3. DB INSERT =============== ')
    data_dump(conn, cursor, pdf_extract_obj, csv_filename)
    
"""
{
    'Address': 'No 1/10, II Floor, Near Gate No 9 APMC Yard, Yeshwanthpur '
            'Bangalore , Karnataka India - 00560022 ',
    'Amount': '100.00 ',
    'Mode of Payment': 'Credit Card/Prepaid Card - ICICI Bank',
    'Name': 'Zauba Technologies and Data Services Privat',
    'Payment Made Into': 'ICICI BANK',
    'Received Payment Rupees': ' One Hundred Only',
    'SRN': 'U16571275',
    'Service Description': 'Inspection of Public documents of KEYSTONE REALTORS '
                            'PRIVATE LIMITED ( U45200MH1995PTC094208  )',
    'Service Request Date': '03/08/2017',
    'Service Type': 'Fee for inspection of Public documents',
    'Type of Fee': 'Normal'
}

INSERT INTO zauba.zauba_mca VALUES ('U16571275', '2017/08/03', 'ICICI BANK', 'Zauba Technologies and Data Services Privat', 'No 1/10, II Floor, Near Gate No 9 APMC Yard, Yeshwanthpur Bangalore , Karnataka India - 00560022 ', 'Fee for inspection of Public documents', 'Inspection of Public documents of KEYSTONE REALTORS PRIVATE LIMITED ( U45200MH1995PTC094208  )', 'Normal', 100.00, 'Credit Card/Prepaid Card - ICICI Bank', ' One Hundred Only');
"""