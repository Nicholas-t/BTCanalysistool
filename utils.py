from blockchain import blockexplorer as blex
import time
import matplotlib.pyplot as plt


#-------------------------- utils
def get_bit(height): 
    blks = blex.get_block_height(height)
    if len(blks) == 1: return blks[0].bits
    else: return None

def get_fee(height): 
    blks = blex.get_block_height(height)
    if len(blks) == 1: return blks[0].fee
    else: return None

def get_no_tx(height):
    blks = blex.get_block_height(height)
    if len(blks) == 1: return blks[0].n_tx
    else: return None

def get_size(height):
    blks = blex.get_block_height(height)
    if len(blks) == 1: return blks[0].size
    else: return None

def return_range(start, end, last):
    if (((start!= 0) & (last != 0))|
        (start>end)):
        print('error')
        return None
    if last != 0:
        return (end-last, end)
    else:
        return (start, end)
#--------------------------------------- 

def plot_block(typ, start =0 , end=blex.get_latest_block().height, last=0):
    functions = {'bit':get_bit,
            'fee':get_fee,
            'no_tx':get_no_tx,
            'size':get_size}
    try:
        funct = functions[typ]
    except:
        print('ERROR TYPE PARAMETER')
        return ''
    Y = []
    rng = return_range(start,end,last)
    if rng == None :
        print('ERROR RANGE')
        return ''
    j = 0
    tot = rng[1]-rng[0]
    for i in range (rng[0], rng[1]):
        Y += [funct(i)]
        time.sleep(0.5)
        j+=1
        print(str(j)+"/"+str(tot)+" import block # "+str(i))
    plt.plot(Y)
    plt.show()

plot_block('no_tx',last = 30)

