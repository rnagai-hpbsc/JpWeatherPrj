import re
import codecs
import argparse

from addparser import getParser

def getData(filename='day1_12.txt'):
    f  = codecs.open(filename,'r','shift_jis')
    line = f.readline()

    title = getTitle(line)

    lat, lon, pre = [], [], []
    prefix = ''
    while line: #各地の天気
        if line.find('ルドナヤプリスタニ')==0: 
            prefix = 'ルドナヤプリスタニ'
            line = f.readline()
            continue
        if line.find('セベロクリリスク')==0:
            prefix = 'セベロクリリスク'
            line = f.readline()
            continue
        if prefix!='': 
            line = f'{prefix}{line}'
            prefix = ''

        if line.find('ウラジオストク')==0: 
            spline = line.split('ストク')
            spline[0] = 'ウラジオストク'
            line = ' '.join(spline)

        if line.find('風向・風力')>=0: 
            spline = line.split('・')
            line = ' '.join(spline)
        
        datalist = line.split()
        if len(datalist) > 6: 
            thistemperature = f2h_temp(datalist[len(datalist)-1])
            thispressure = f2h_pres(datalist[len(datalist)-2])
            thiswstrength = f2h(datalist[len(datalist)-4])
            thislocation = ''.join(datalist[0:len(datalist)-6])
            '''print (datalist[len(datalist)-1]) # temperature
            print (datalist[len(datalist)-2]) # pressure
            print (datalist[len(datalist)-3]) # weather
            print (datalist[len(datalist)-4]) # wind strength
            print (datalist[len(datalist)-6]) # wind direction'''
            #print (f'''City name: {''.join(datalist[0:len(datalist)-6])}''')
            '''print ()
            print (f'Temperature: {f2h_temp(datalist[len(datalist)-1])} degC')
            print (f'Pressure: 10{f2h_pres(datalist[len(datalist)-2])} hPa')
            print (f'Wind strength: {f2h(datalist[len(datalist)-4])}')'''
            locationfile = open('data/locations.txt',encoding="utf-8")
            lline = locationfile.readline()
            thislat = 0
            thislon = 0
            thislatsec = 0
            thislonsec = 0
            while lline:
                lsline = lline.split()
                if len(lsline)==0:
                    break
                if thislocation == lsline[0]:
                    thislat = int(lsline[1])
                    thislon = int(lsline[2])
                    if len(lsline)>3:
                        thislatsec = int(lsline[3])
                    if len(lsline)>4:
                        thislonsec = int(lsline[4])
                    break
                lline = locationfile.readline()
            lat.append(thislat + thislatsec / 60.)
            lon.append(thislon + thislonsec / 60.)
            if thispressure > 100: 
                pre.append(thispressure)
            else: 
                pre.append(thispressure + 1000)
        #print(len(datalist))
        line = f.readline()
        judge = line.split('の船舶の報告をお知らせします\n')
        if len(judge)==2:
            break
    while line: #船舶の報告
        line = f.readline()
        sline = line.split()
        if len(sline)>3: 
            if sline[2]=='北緯': 
                thislat = f2h_temp(sline[3])
        if len(sline)>5:
            if sline[4]=='東経':
                thislon = f2h_temp(sline[5])
        #print(f'N{thislat}deg, E{thislon}deg')
        if len(sline)==4: 
            if sline[2]=='（気圧）':
                thispres = f2h_pres(sline[3]) + 1000
                if thispres > 0: 
                    lat.append(thislat)
                    lon.append(thislon)
                    pre.append(thispres)
                    thislat=0
                    thislon=0
                    thispres=-1000
        judge = line.split('つづいて漁業気象です。')
        if len(judge)==2:
            break
    ispres = 0
    prevline = ''
    peaklat, peaklon, peakpres = 0, 0, 0
    linelat, linelon, linepres = 0, 0, 0 
    plats, plons, ppress = [], [], []
    linedesc = False
    while line: #漁業気象
        sline = line.split('  ')
        f2hline = f2h(line)
        #print(len(sline))
        hline = f2hline.split('北緯')
        if len(hline)>1: 
            peaklat = int((hline[1].split('度'))[0])
            #print(peaklat)
        tline = f2hline.split('東経')
        if len(tline)>1:
            peaklon = int((tline[1].split('度'))[0])
            #print(peaklon)
        kline = f2hline.split('気圧があって')
        if len(kline)>1: 
            if kline[0].find('hPa')==0: 
                prevlist = re.findall(r'\d+',prevline)
                peakpres = int(prevlist[len(prevlist)-1])
            elif kline[0].find('hPa')==-1:
                prevlist = prevline.split('hPa')[0].split('、')
                peakpres = int(prevlist[len(prevlist)-1])
            #print(f'{peaklat},{peaklon},{peakpres}')
            plats.append(peaklat)
            plons.append(peaklon)
            ppress.append(peakpres)
            lat.append(peaklat)
            lon.append(peaklon)
            pre.append(peakpres)

            peaklat, peaklon, peakpres = 0, 0, 0

        if f2hline.find('等圧線は')>=0: 
            linedesc = True
            prescanlist = f2hline.split('hPa')[0].split('通る')
            linepres = int(prescanlist[len(prescanlist)-1])
            #print(linepres)
        if linedesc==True: 
            if f2hline.find('正午')>0: 
                line = f.readline()
                continue
            #print(f2hline)
            if f2hline.find('北緯')>=0: 
                linelat = int(f2hline.split('北緯')[1].split('度')[0])
                #print(linelat)
            if f2hline.find('東経')>=0:
                linelon = int(f2hline.split('東経')[1].split('度')[0])
            if f2hline.find('西経')>=0:
                westslice = f2hline.split('西経')
                if westslice[1].find('度')>=0:
                    linelon = (-1)* int(westslice[1].split('度')[0])
                #print(linelon)
            if linelat > 0 and linelon > 0:
                #print(f'{linelat},{linelon},{linepres}')
                lat.append(linelat)
                lon.append(linelon)
                pre.append(linepres)
                linelat = 0 
                linelon = 0

            braketCoor = f2hline.split('(')
            for i in range(len(braketCoor)):
                #print(braketCoor)
                if i==0:
                    continue
                linelat = int(braketCoor[i].split('、')[0])
                if braketCoor[i].find('西経')>=0:
                    westslice = braketCoor[i].split('西経')
                    linelon = (-1)* int(westslice[1].split(')')[0])
                else: 
                    linelon = int(braketCoor[i].split('、')[1].split(')')[0])
                #print(f'{linelat},{linelon},{linepres}')
                lat.append(linelat)
                lon.append(linelon)
                pre.append(linepres)
                linelat = 0 
                linelon = 0
                
            if f2hline.find('通って')>=0:
                linedesc = False
                linepres = 0 

        prevline = f2hline
        line = f.readline()

    return title, lat, lon, pre

def f2h_temp(tempraw):
    return int(f2h(tempraw.split('度')[0]))    

def f2h_pres(presraw):
    conv = f2h(presraw).split('hPa')
    if len(conv)>1: 
        return int(conv[0])
    else: 
        return -1000

def f2h(raw):
    return raw.translate(str.maketrans({chr(0xFF01 + i): chr(0x21 + i) for i in range(94)}))

def getTitle(line):
    firstllist = f2h(line).split()
    jptitle = firstllist[len(firstllist)-1]
    year  = jptitle.split('年')[0]
    month = jptitle.split('年')[1].split('月')[0]
    day   = jptitle.split('年')[1].split('月')[1].split('日')[0]
    time  = jptitle.split('年')[1].split('月')[1].split('日')[1]
    if time=='正午': 
        time = 'noon'
    titlelist = [year, month, day, time]
    title = '-'.join(titlelist)

    return title

if __name__ == "__main__":
    parser = getParser()
    args = parser.parse_args()
    filename = args.input

    print(getData(filename))
