import os

DATA_LOC='D:\\PHD\\RA\\Ha\\'
FINAL_OUTPUT='D:\\PHD\\RA\\Ha\\all_pdfs\\big_charities\\'

tally={}

for file in os.listdir(FINAL_OUTPUT):
    if file.endswith(".pdf"):
        abn=file.split('_')[0]
        year=file.split('_')[1].split('.')[0]

        if not abn in tally:
            tally[abn]=['N','N']

        if year=='2014':
            tally[abn][0]='Y'
        elif year=='2015':
            tally[abn][1]='Y'

all_abns=open(DATA_LOC+'all_abns.txt').read().split()
missing_abns=set(all_abns)-set(tally.keys())
#missing_abns
fh_w=open(FINAL_OUTPUT+'missing_abns.txt','w')
for abn in missing_abns:
    fh_w.write(abn+'\n')
fh_w.close()


fh_w=open(FINAL_OUTPUT+'summary.csv','w')
for k,v in tally.items():
    fh_w.write(k+','+v[0]+','+v[1]+'\n')
fh_w.close()