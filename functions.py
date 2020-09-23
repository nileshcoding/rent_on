import csv

#takes the path of file as argument an returns list of dictinary
def li_dictObject(path):
    li = []
    csv_r = open(path,'r')
    csv_reader = csv.DictReader(csv_r)
    for row in csv_reader:
        li.append(dict(row))
    csv_r.close()
    return li

#takes the path and list of dictionaries and overwrites the file
def overwrite_file(path,li):
    header = li[0].keys()
    csv_w = open(path,'w',newline='\n')
    csv_writer = csv.DictWriter(csv_w,fieldnames=header)
    csv_writer.writeheader()
    csv_writer.writerows(li)
    csv_w.close()

'''takes the path, fieldnames as header and the row to be appended as argument
and appends row into the file'''
def append_row(path,header,value):
    csv_a = open(path,'a',newline = '\n')
    csv_writer = csv.DictWriter(csv_a,fieldnames=header)
    csv_writer.writerow(value)
    csv_a.close()
    