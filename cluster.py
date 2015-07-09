#!/bin/python

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab as pl
import pymysql.cursors
import kmeans
import datetime
# Connect to the database
connection = pymysql.connect(host='',
                             user='',
                             passwd='',
                             db='',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
data = {}
try:
    with connection.cursor() as cursor:
        sql = "SELECT GazeTimestamp,GazeX,GazeY,ReadingSessionId FROM eyeData WHERE TrackingAccuracy>0 AND PageId=1"
        cursor.execute(sql)
        results = cursor.fetchall()

        for res in results:
            if not data.has_key( res['ReadingSessionId'] ):
                #print "Making entry for: ",res['ReadingSessionId']
                data[res['ReadingSessionId']] = []
            data[res['ReadingSessionId']].append( (res["GazeX"], res["GazeY"], res["GazeTimestamp"]) )




finally:
    connection.close()


for key in data.keys()[:1]:
    d0 = datetime.datetime.now()
    k = kmeans.KMeans(30, np.array(data[key]))
    k.Run()
    print "Took: ",(datetime.datetime.now()-d0).total_seconds(),"seconds"
    k.makePlot()
    """
    print k, len(data[k])
    data[k] = np.array( data[k], dtype=float )
    fig = pl.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter( data[k][:,0], data[k][:,1], data[k][:,2])
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Time")
    pl.show()
    """
    #pl.plot( data[k][:,0], data[k][:,1], 'r.')
    #pl.show()
