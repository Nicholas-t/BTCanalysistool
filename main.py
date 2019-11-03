import gzip
import pandas as pd
from urllib.request import urlopen, Request
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import time
import json


URL = 'https://gz.blockchair.com/bitcoin/blocks/blockchair_bitcoin_blocks_{}.tsv.gz'


def date_gen(start, offset):
    d = start
    while True:
        d = d - timedelta(days=offset)
        yield d.strftime("%Y%m%d")

def checkvalid(extra):
    for e in extra:
        for k in e:
            if k not in typs:
                return False
    return True

def lognplot(final,lsdate, extra):
    for title in final.keys():
        data = {'type':title,
                'last_date':lsdate,
                'data':final[title]}
        json.dump(data, open('json/{}.json'.format(title),'w'), sort_keys=True, indent=4)
        plt.title(data['type'])
        plt.plot(data['data'])
        plt.legend((data['type']))
        plt.savefig('png/{}.png'.format(data['type']))
        print('{} PNG SAVED'.format(data['type']))
        plt.clf()
    for ext in extra:
        title = '_'.join(ext)[:10]
        plt.title(title)
        leg = []
        for e in ext:
            leg+=[e]
            plt.plot(final[e])
        plt.legend(leg)
        plt.savefig('png/extra/{}.png'.format(title))
        print('{} PNG SAVED'.format(title))
        plt.clf()

def main(typs,start = datetime.today(), daily = True, offset = 10, extra=[]):
    generator = date_gen(start, offset)
    df = None
    err = 0
    final = {}
    if not checkvalid(extra):
        print('check extras')
        return 0
    for typ in typs:
        final[typ] = []
    try:
        while True:
            if err>4:
                raise Exception
            try :
                date = next(generator)
                req = Request(URL.format(date))
                html = gzip.decompress(urlopen(req).read()).decode('utf-8')
                df = pd.DataFrame([x.split('\t') for x in html.split('\n')])
                df.columns = df.iloc[0]
                for typ in typs:
                    dum = df.drop(df.index[0])[typ].tolist()
                    if daily: final[typ].insert(0,sum(list(map(float, dum)))/len(dum))
                    if not daily: final[typ].insert(0,list(map(float, dum)))
                    print("checking at date {} , {} entry found for {}".format(date, len(final[typ]), typ))
                time.sleep(0.5)
                err = 0
            except Exception as e:
                err+=1
                print(e)
    except KeyboardInterrupt:
        print("stopping for keyboard interrupt")
        time.sleep(1)
        lognplot(final , date, extra)
    except Exception as e:
        print(e)
        print("Interrupted")
        lognplot(final , date, extra)

typs = ['weight','size','stripped_size','nonce',
        'bits', 'difficulty', 'transaction_count', 'witness_count',
        'input_count','output_count','input_total','input_total_usd',
        'output_total','output_total_usd','fee_total','fee_total_usd',
        'fee_per_kb','fee_per_kb_usd','fee_per_kwu','fee_per_kwu_usd',
        'cdd_total','generation','generation_usd','reward','reward_usd']

special = [['weight','size','stripped_size','transaction_count','witness_count']]
            
main(typs,offset = 10, extra=special)





