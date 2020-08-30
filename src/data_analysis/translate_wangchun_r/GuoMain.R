   ### ###
   library("data.table");
   path=PasteAll(c(Disk,":/Rwork/AlphaStrategy/Graph/StrategyResult/EquityCurve_Beta.csv"),"");
   Beta=data.table::fread(path,header=TRUE,fill=TRUE);
   path=PasteAll(c(Disk,":/Rwork/AlphaStrategy/Data/DataHis/equal_weighted.csv"),"");  
   Data=as.data.frame(read.csv(path,header=TRUE,sep=",",encoding="UTF-8"));
   names(Data)[1]="Date";
   # Factor Values #
   FV=array(0,c(T,n));
   for (i in 1:n){
        FV[1:T,i]=Data[,i+1];
   }
   FV[which(is.na(FV))]=-100;
   CC=array(0,c(T,n));        # Close-to-Close return #
   LogCC=array(0,c(T,n));     # Log return #
   for (i in 1:n){
        CC[2:T,i]=Close[2:T,i]/Close[1:(T-1),i]-1;
        LogCC[2:T,i]=log(Close[2:T,i])-log(Close[1:(T-1),i]);
   }                          
   CC[which(is.na(CC))]=0;
   Wopt=array(0,c(T+1,n));    # optimal portfolio weight, T=number of trading days, n=number of stocks #
   nsel=300;                  # we select nsel number of stocks 
   nmemory=90;                # window size for Sigma estimation 
   nalpha=10;                 # window size for expected return estimation 
   nstyle=2;                  # number of style constraints #
   wup=5/nsel;                # upper bound for each stock #
   wdown=1/nsel/3;            # lower bound for each stock
   lambda=1;                  # risk tolerance 
   sectorDeviation=0.025;     # 
   CVaR_alpha=0.05;
   nstart=nmemory*2+1;
   RiskMeasure="CVaR";       # "Risk_Adjusted_Return"/"Risk_Parity"/"Minimum_Tail_Dependent"/"Minimum_Variance"/"CVaR";
   CovEstimator="cov";                   # "cov"/"lpmEstimator"/"slpmEstimator"/"kendallEstimator"/"spearmanEstimator"/"shrinkEstimator";
   source("NeweyWestFunc.R");
   Beta=rbind(array(0,c(2*nmemory+1,n)),as.matrix(Beta[,2:(n+1)]));  # rbind is row combine, cbind is column combine; rbind(array(1,c(2,2)),array(2,c(3,2)))
   Beta[nstart,]=Beta[nstart+1,];
   source("Constrained_OneStep_OptimFunc5.R");
   # H is covariance matrix; Alpha is expected return 
   for (t in nstart:T){
        cat("t",t,"\n");
        jy=which(rank(-FV[t,])<=nsel);   # factor value 排序取最大值 
        if (RiskMeasure!="Minimum_Tail_Dependent"){
            if (any(is.na(H)))   H=cov(CC[(t-nmemory+1):t,jy]);
            if (min(diag(H))==0) diag(H)[which(diag(H)==0)]=mean(diag(H)[which(diag(H)!=0)]);
            SD=diag(H)^0.5;
        } 
        if (RiskMeasure=="Minimum_Tail_Dependent"){
            H=FRAPO::tdc(CC[(t-nmemory+1):t,jy],method="EmpTC",lower=TRUE);
            SD=diag(cov(CC[(t-nmemory+1):t,jy]))^0.5;
            if (any(SD==0)) SD[which(SD==0)]=mean(SD[which(SD!=0)]);
        }
        Alpha=matrix(0,nsel,1);
        if (is.element(RiskMeasure,c("Minimum_Tail_Dependent","Minimum_Variance"))==FALSE){
            for (i in 1:nsector){
                 jz=intersect(jy,which(is.element(SectorClass2[t-1,],SectorU[i])));
                 lz=length(jz);
                 js=which(is.element(jy,jz));
                 if (lz>1) Alpha[js]=sum(CC[(t-nalpha+1):t,jz])/length(which(Volume[(t-nalpha+1):t,jz]>0));
                 if (any(is.na(Alpha[js]))) stop("Alpha[js]");
            } 
        }
        op=Constrained_OneStep_OptimFunc5(RiskMeasure,t,jy,CC,IndexRe,Cons,Code,nmemory,nalpha,nstyle,H,SD,nsector,Alpha,SectorClass2,SectorU,IndexSector500,Size,nsel,w0,wup,wdown,lambda,sectorDeviation,Beta,CVaR_alpha);
        Wopt[t+1,jy]=op$w_opt;
   }






   
   PortRe=array(0,T);
   PortRe2=array(0,T);
   PortRe[1:nstart]=IndexRe[1:nstart];
   PortRe[(nstart+1):T]=rowSums(Wopt[(nstart+1):T,]*CC[(nstart+1):T,]);
   PortRe2[(nstart+1):T]=PortRe[(nstart+1):T]-IndexRe[(nstart+1):T];
   PortV=cumprod(1+PortRe[(nstart+1):T]);
   PortV2=cumprod(1+PortRe2[(nstart+1):T]);
   plot(x=as.Date(Date)[(nstart+1):T],y=PortV,type="l",col="red",xlab="Trading Day",ylab="Value");
   grid();
   plot(x=as.Date(Date)[(nstart+1):T],y=PortV2,type="l",col="red",xlab="Trading Day",ylab="Value");
   grid();
   plot(x=as.Date(Date)[(nstart+1):T],y=log(PortV),type="l",col="red",xlab="Trading Day",ylab="Value");
   grid();
   plot(x=as.Date(Date)[(nstart+1):T],y=log(PortV2),type="l",col="red",xlab="Trading Day",ylab="Value");
   grid();
