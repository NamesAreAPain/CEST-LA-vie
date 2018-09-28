import csv
import math
import sys
def SigFigFormatter(filename):
    
    with open(filename,'r',newline='') as csvIn, open(filename[:-4]+"Sigfig.csv",'w',newline='') as csvOut:
        reader = csv.DictReader(csvIn)
        writer_fieldnames = []
        sigfig_names = []
        nonfig_names = []
        for fname in reader.fieldnames:
            if len(fname) >= 4 and fname[-4:] == "_BST":
                sigfig_names.append(fname[0:-4])
                writer_fieldnames.append(fname[0:-4])
            elif len(fname) >= 4 and fname[-4:] == "_ERR":
                pass
            else:
                nonfig_names.append(fname)
                writer_fieldnames.append(fname)
        writer = csv.DictWriter(csvOut,fieldnames=writer_fieldnames)
        writer.writeheader()
        for row in reader:
            rowout = {}
            for col in nonfig_names:
                rowout[col] = row[col]
            for col in sigfig_names:
                rowout[col] = BstPlusMinusErr(row[col+"_BST"],row[col+"_ERR"])
            writer.writerow(rowout)
                
def BstPlusMinusErr(bst,err):
    #Work in Progress. Works for errors less 1, less so for others.
    bst = float(bst)
    err = float(err)
    if err == 0:
        return str(bst)
    else:
        errBit = math.floor(math.log10(err))
    errPl = errBit
    if err*10**(-1*errBit) < 2 :
        errOut = formatgButConfigurable(err,2)
    else :
        errOut = formatgButConfigurable(err,1)
    return truncateAtPlace(bst,errBit) + "$\pm$" + errOut
     
def formatgButConfigurable(num2fmt,sigfigs):
    if num2fmt == 0: 
        return '0'
    strnum = '{:.30f}'.format(num2fmt)
    firstsigfig = 0
    for i in strnum :
        if i != '0' and i != '.':
            break;
        firstsigfig += 1
    zneeded = math.floor(math.log10(num2fmt))
    if zneeded < 0:
        zneeded = 0
    return strnum[0:firstsigfig+sigfigs] + (zneeded-1)*'0'

def truncateAtPlace(numIn,pl):
    strnum = '{:.30f}'.format(numIn)
    dpat = 0
    for i in strnum:
        if i == '.':
            break
        dpat += 1
    if pl <= 0:
        pl -= 1
    return strnum[0:dpat-pl]+"0"*(pl if pl > 0 else 0)



if __name__ == "__main__":
    if len(sys.argv) > 1:
        SigFigFormatter(sys.argv[1])
    else :
        SigFigFormatter(input())
