#!/APSshare/anaconda3/x86_64/bin/python

'''
Based on Francesco's script for streaming
This acquires a 180 buffer and returns the array for further processing / writing to disk when complete
'''

import pvaccess as pva
import time
import numpy as np
import matplotlib.pyplot as plt

PVA_prefix = '1idPG1:Pva1:'
width = 1920
height = 1200
nprojs = 100


def grab_scan(buff):
    
    pva_data      = pva.Channel(PVA_prefix + 'Image')
    
    # the detector pv (function addProjection), called inside pv monitor
    #databuffer = np.zeros([buff, height, width], dtype='float32')
    databuffer = np.zeros([buff, height, width], dtype='uint16')
    counter = np.asarray([0])
    def addProjection(pv):
        
        if counter <= buff:
            curid = pv['uniqueId']
            print(curid)
            databuffer[np.mod(curid, buff)] = pv['value'][0]['ushortValue'].reshape(
                height, width).astype('uint16')
            counter[:] = counter + 1
            return
        else:
            return

    pva_data.monitor(addProjection, '')

    while(True):
        if counter == buff:
            datap = databuffer.copy()
        else:
            time.sleep(1.0)
        return datap
        

if __name__ == "__main__":

    
    projs = grab_scan(nprojs)
