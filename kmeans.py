#!/bin/python

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import pylab as pl
from datetime import datetime


class KMeans:


    def __init__(self, K, data):
        self.K = K
        self.data = data
        self.n = self.data.shape[0]
        self.clusterNums = np.zeros( self.n, dtype=int )
        self.lastClusterNums = np.zeros( self.n, dtype=int )
        self.centersIndicies = []
        self.centerPoints = []
        self.points = []
        self.timeout = 50

        np.random.seed(55)

    def EuclideanDistance( self, c, v ):
        a = np.abs( c-v )
        tmp = np.sqrt( np.dot( a,a ) )
        return tmp

    def makePlot(self):
        # Plotting:
        fig = pl.figure()
        ax = fig.add_subplot(111,projection='3d')
        colours = ['b', 'g', 'r', 'c', 'm', 'y', 'k', 'purple', 'brown', "#F00000", "#00F000", "#0000F0"]
        for i,p in enumerate(self.points):
            ax.scatter( [ e[0] for e in p ], [ e[1] for e in p ], [ e[2] for e in p ],  color=colours[i%len(colours)])
        ax.scatter( [ e[0] for e in self.centerPoints ],
            [ e[1] for e in self.centerPoints ],
            [ e[2] for e in self.centerPoints ],
            color='#00FF00', marker='s')
        ax.set_xlabel("X")
        ax.set_ylabel("Y")
        ax.set_zlabel("Z")
        pl.savefig("images/%s_%d.png"%(datetime.now().strftime("%Y-%m-%dT%H:%M:%S"),self.trial))
        pl.clf()
        pl.close()


    def Run(self):
        self.centersIndicies = []

        notUnique = True;

        while notUnique:
            self.centersIndicies = np.array( np.random.rand(self.K)*self.n, dtype=int )
            notUnique = np.array( [ e in self.centersIndicies[i+1:] for i,e in enumerate( self.centersIndicies ) ] ).any()

        self.centersIndicies.sort()

        for i,c in enumerate(self.centersIndicies):
            self.centerPoints.append( self.data[ c ] )

        self.centerPoints = np.array( self.centerPoints )

        self.trial=0
        while( self.trial < self.timeout ):
            self.points = []
            for i in range(self.K):
                self.points.append([])

            self.lastClusterNums[:] = self.clusterNums
            changed = False

            for i,d in enumerate( self.data ):
                dist = [ self.EuclideanDistance(d, c) for c in self.centerPoints ]
                self.clusterNums[i] = dist.index(min(dist))

                if( self.clusterNums[i] != self.lastClusterNums[i]):
                    changed=True

                self.points[ self.clusterNums[i] ].append( d )

            if not changed:
                break

            self.trial += 1

            for i,e in enumerate(self.points):
                if( len(e) ):
                    x = np.average([ z[0] for z in e ])
                    y = np.average([ z[1] for z in e ])
                    z = np.average([ z[2] for z in e ])
                    self.centerPoints[i] = np.array([x,y,z])

        #self.makePlot(trial)
        #print "done in",self.trial,"loops"


if __name__ == '__main__':
    fakeD = []
    K = 10
    maxNumOfPointsInCluster = 250


    np.random.seed(55)
    for i in range( K ):
        # Randomly select a base value to cluster around
        b = int ( np.random.rand()*200 ) - 100
        for i in range(int(np.random.rand()*maxNumOfPointsInCluster)):
            # make a random variance of [-30%, 30%]
            v = (np.random.rand()-0.5)*1.0
            fakeD.append( list((np.random.rand(3)-0.5)*v*b+b) )

    fakeD = np.array(fakeD)
    #print fakeD.shape
    centers = [ np.array([-1.0, -1.0, -1.0]),
        np.array([10.0, 10.0, 10.0]),
        np.array([-55.0, -5.0, -55.0]),
        np.array([1.0, 1.0, 1.0])
    ]



    """
    for f in fakeD:
        print f,"\n\n"
    """
    d0=datetime.now()
    k = KMeans(K, fakeD)
    print "Running:"
    k.Run()
    print "Took: ",(datetime.now()-d0).total_seconds(),"seconds"
