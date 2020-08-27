    ### Step 2 ###
    load("D:\\Rwork\\AlphaStrategy\\Rfiles\\FuJu2.RData");
    Code=read.csv("FuJuCode2.csv",header=TRUE,sep=",",encoding="UTF-8")$Code;
    dbName=PasteAll(c(Disk,":/Rwork/AlphaStrategy/Data/DataBase/DB_SectorClassification.db"),"");
    conn=dbConnect(dbDriver("SQLite"),dbname=dbName);
    TableX=dbListTables(conn);  
    dbListFields(conn,TableX[1]); 
    StockX=dbReadTable(conn,TableX[1]);     # 日期，行业代码(前8位代表一级)
    Date=StockX$Date;   
    T=dim(StockX)[1];
    n=length(Code);
    SectorClass=array(0,c(T,n));            # 列一下行业，不止8位
    for (i in 1:n){
         cat("i",i,"\n");
         codex=PasteAll(c("X",str_sub(Code[i],1,6)),"")
         StockX=dbReadTable(conn,TableX[which(TableX==codex)]);
         SectorClass[,i]=StockX$"TYPE_ID"; 
    }
    SectorClass[which(is.na(SectorClass))]=0;
    dbDisconnect(conn);      
    # 取前8位 #
    xfunc<-function(x) as.numeric(stringr::str_sub(x,1,8))     # 取前8位
    SectorClass2=array(0,c(T,n));  # 和 SectorClass2 是 取SectorClass前8位的结果
    for (i in 1:n) SectorClass2[,i]=apply(as.matrix(SectorClass[,i]),1,xfunc);
    for (i in 1:n){ 
         if (i==1) SectorU=unique(SectorClass2[,i]);
         if (i>1)  SectorU=sort(unique(c(SectorU,unique(SectorClass2[,i]))));
    }
    if (SectorU[1]==0) SectorU=SectorU[-1];
    nsector=length(SectorU);