   library("data.table");
   path=PasteAll(c(Disk,":/Rwork/AlphaStrategy/Data/DataHis/equal_weighted.csv"),"");
   Data=as.data.frame(read.csv(path,header=TRUE,sep=",",encoding="UTF-8"));
   names(Data)[1]="Date";
   FV=array(0,c(T,n));
   for (i in 1:n){
        FV[1:T,i]=Data[,i+1];
   }
   FV[which(is.na(FV))]=-100;
   CC=array(0,c(T,n));
   LogCC=array(0,c(T,n));
   for (i in 1:n){
        CC[2:T,i]=Close[2:T,i]/Close[1:(T-1),i]-1;
        LogCC[2:T,i]=log(Close[2:T,i])-log(Close[1:(T-1),i]);
   }
   CC[which(is.na(CC))]=0;