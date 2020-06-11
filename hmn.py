import numpy as np
class HMN():
    '''This is a class for constructing hmn networks'''
    def __init__(self,m0,h,b,ln):
        self.b=b
        self.h=h
        self.m0=m0
        self.ln=ln
        self.nm=b**h
        self.n=m0*self.nm
        self.adjM=np.zeros((self.n, self.n))
        self.mc_connected=False
    def mc_all2all(self):
        for i in range(self.nm):
            mo_beg=i*self.m0
            mo_end=(i+1)*self.m0
            for j in range(mo_beg,mo_end):
                for k in range(mo_beg,mo_end):
                    self.adjM[j][k]=1
                self.adjM[j][j]=0
        self.mc_connected=True
    def mc_line(self):
        for i in range(self.nm):
            mo_beg=i*self.m0
            mo_end=(i+1)*self.m0
            for j in range(mo_beg,mo_end-1):
                self.adjM[j][j+1]=1
                self.adjM[j+1][j]=1
        self.mc_connected=True
    def mc_ring(self):
        for i in range(self.nm):
            mo_beg=i*self.m0
            mo_end=(i+1)*self.m0
            for j in range(mo_beg,mo_end-1):
                self.adjM[j][j+1]=1
                self.adjM[j+1][j]=1
            self.adjM[mo_beg][mo_end-1]=1
            self.adjM[mo_end-1][mo_beg]=1
        self.mc_connected=True
    def mc_random(self,avg_con):
        link_num=int(avg_con*self.nm)
        if link_num>0:
            for i in range(self.nm):
                mo_beg=i*self.m0
                mo_end=(i+1)*self.m0
                nc=0
                while nc<link_num:
                    r1=0
                    r2=0
                    while r1==r2:
                        r1=np.random.randint(mo_beg,mo_end)
                        r2=np.random.randint(mo_beg,mo_end)
                    if(self.adjM[r1][r2]==0):
                        self.adjM[r1][r2]=1
                        self.adjM[r2][r1]=1
                        nc+=1
            self.mc_connected=True
        else:
            print('ERROR in avrage connectivity')
    def interMc_hmn1(self):
        if self.mc_connected==True:
            ll=self.h**2
            ip=1
            for i in range(self.h):
                il=ip
                ip=2*ip
                for j in range(0,ll-il,ip):
                    dis1B=j*self.m0
                    dis1E=((j+il)*self.m0)-1
                    dis2B=(j+il)*self.m0
                    dis2E=((j+(2*il))*self.m0)-1
                    #print(i,j,dis1B,dis1E,dis2B,dis2E)
                    nc=0# nubmer of intermodular links
                    while nc<self.ln:
                        r1=np.random.randint(dis1B,dis1E)
                        r2=np.random.randint(dis2B,dis2E)
                        if self.adjM[r1][r2]==0:
                            self.adjM[r1][r2]=1
                            self.adjM[r2][r1]=1
                            nc+=1
        def interMc2_hmn2(self,p):
            if self.mc_connected==True:
                ll=self.h**2
                ip=1
                for i in range(self.h):
                    il=ip
                    ip=2*ip
                    for j in range(0,ll-il,ip):
                        dis1B=j*self.m0
                        dis1E=((j+il)*self.m0)-1
                        dis2B=(j+il)*self.m0
                        dis2E=((j+(2*il))*self.m0)-1
                        print(i,j,dis1B,dis1E,dis2B,dis2E)
                        nc=0# nubmer of intermodular links
                        while nc<1:
                            for r1 in range(dis1B,dis1E,1):
                                for r2 in range(dis2B,dis2E,1):
                                    r=random.random(0.0,1.0)
                                    if r<=p and self.adjM[r1][r2]==0:
                                        self.adjM[r1][r2]=1
                                        self.adjM[r2][r1]=1
                                        nc+=1
                            
    
    def run_hmn1(self):
        self.mc_all2all()
        self.interMc_hmn1()
        return self.adjM
    
    def run_hmn2(self,p):
        self.mc_all2all()
        self.interMc_hmn2()
        return self.adjM
    
    def run_hmn1_line(self):
        self.mc_line()
        self.interMc_hmn1()
        return self.adjM
    
    def run_hmn1_ring(self):
        self.mc_ring()
        self.interMc_hmn1()
        return self.adjM
    
    def run_hmn1_random(self,avgcon):
        self.mc_random()
        self.interMc_hmn1()
        return self.adjM