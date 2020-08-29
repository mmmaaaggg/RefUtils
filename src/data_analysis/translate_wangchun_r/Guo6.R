CodeX=Cons[[t-1]]$Code;
jx=which(is.element(Code,CodeX));
N=length(jx);
# #
X_sector=matrix(0,nsel,nsector);
for (i in 1:nsector){
    js=which(is.element(SectorClass2[t-1,jy],SectorU[i]));
    X_sector[js,i]=1;
}
alpha_sector_up=matrix(0,nsector,1);
alpha_sector_low=matrix(0,nsector,1);
for (i in 1:nsector){
    alpha_sector_up[i]=IndexSector500[t-1,i]+sectorDeviation;
    alpha_sector_low[i]=max(IndexSector500[t-1,i]-sectorDeviation,0);
    if (sum(X_sector[,i])==0) alpha_sector_low[i]=0;
}
wb=matrix(0,N,1);     # HS500 Cons #
for (i in 1:N){
    js=which(is.element(Code[jx],Cons[[t-1]]$Code[i]));
    wb[js]=Cons[[t-1]]$Weight[i]/100;
}
wb=wb/sum(wb);
logsize=log(Size[t-1,jx]);
logsize[which(logsize==-Inf)]=mean(logsize[which(logsize!=-Inf)]);
Index_Style=sum(logsize*wb);
alpha_style_up=array(0,nstyle);
alpha_style_low=array(0,nstyle);
X_sxtyle=array(0,c(nsel,nstyle));
# Size #
alpha_style_up[1]=Index_Style*1.05;
alpha_style_low[1]=Index_Style*0.95;
logsize=log(Size[t-1,jy]);
logsize[which(logsize==-Inf)]=mean(logsize[which(logsize!=-Inf)]);
X_style[,1]=as.matrix(logsize);
# Beta #
alpha_style_up[2]=1.2;
alpha_style_low[2]=0.8;
X_style[,2]=as.matrix(Beta[t,jy]);