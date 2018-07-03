FHSGACH3Py<-function(pathdata, pathop, nsimu){

    # pathdata,pathop,nsimu
    # pathdata = "d:/WSR/reseries.csv"
    # pathop = "d:/WSR/VolSimu.csv"
    library(bootstrap);
    library(fGarch);
    library(fArma);
    # reseries=read.csv(pathdata,header=TRUE,sep=",",quote="\"",dec=".")$x;
    reseries=read.csv(pathdata,header=TRUE,sep=",",quote="\"",dec=".")$x;
    # reseries #
    res=armaFit(~arima(2,1,2),reseries);
    fitresult=garchFit(~garch(1,1),data=residuals(res),cond.dist="sstd",trace=FALSE);
    ht=fitresult@h.t;
    et=residuals(res)/ht^0.5;
    T=length(reseries);
    Trajectory=array(0,c(T,nsimu));
    for (i in 1:nsimu){
        etbootstrap=bootstrap(et,1,function(x){x})$"thetastar";
        reseriesSmu=fitted(res)+etbootstrap*ht^0.5;
        Trajectory[,i]=cumprod(1+reseriesSmu);
    }
    write.csv(Trajectory,file=pathop,row.names=F);
    return(Trajectory)

}
