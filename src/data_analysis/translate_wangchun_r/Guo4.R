    ### Step 3 ###    # 月频率的指数成分，转换日频率的指数成分, 这个月只能用上个月的文件
    Year=year(Date);
    Month=month(Date);
    files=list.files(PasteAll(c(Disk,":/Rwork/AlphaStrategy/Data/DataHis/DataConsDataYes/ZZ500"),""));  # 这个目录下多少个file 
    nfile=length(files);
    Cons=list();
    nfilex=nfile;
    for (i in 24:nfilex){  # 
         pathin=PasteAll(c(Disk,":/Rwork/AlphaStrategy/Data/DataHis/DataConsDataYes/ZZ500/",files[i]),"");
         data=data.table::fread(pathin,fill=TRUE);
         data[,Date:=NULL]; # 去除日期 
         if (i<nfilex)      jx=intersect(which(Year==as.numeric(str_sub(files[i+1],5,8))),which(Month==as.numeric(str_sub(files[i+1],10,11))));
         if (i==nfilex){
             jx=intersect(which(Year==as.numeric(str_sub(files[i],5,8))),which(Month==as.numeric(str_sub(files[i],10,11))));
             jx=c((jx[length(jx)]+1):T);
         }
         for (j in 1:length(jx)) Cons[[jx[j]]]=data;
    }      
    # #
    for (t in 1:T){
         Weight=Cons[[t]]$Weight;
         if (any(is.na(Weight))==TRUE){
             Weight[which(is.na(Weight)==TRUE)]=(100-sum(Weight[which(is.na(Weight)==FALSE)]))/length(which(is.na(Weight)==TRUE));
             Cons[[t]]$Weight=Weight;
         }
    }
    # 取行业的权重 #
    nsector=length(SectorU);
    IndexSector=array(0,c(T,nsector));
    for (t in 1:T){
         for (i in 1:nsector){
              jx=which(is.element(as.character(Cons[[t]]$Code),as.character(Code[which(SectorClass2[t,]==SectorU[i])])))
              if (length(jx)>0) IndexSector[t,i]=sum(Cons[[t]]$Weight[jx]);
         }
    }
    # normalize #
    IndexSector500=array(0,c(T,nsector));
    for (t in 1:T){
         IndexSector500[t,]=IndexSector[t,]/sum(IndexSector[t,]);
    }   
    rowSums(IndexSector500);
    IndexSectorX=IndexSector500;   
    # #
    IndexData=as.data.frame(read.csv("IndexZZ500.csv",header=TRUE,sep=",",encoding="UTF-8"));
    IndexOpen=IndexData$Open;
    IndexHigh=IndexData$High;
    IndexLow=IndexData$Low;
    IndexClose=IndexData$Close;
    IndexRe=array(0,T);
    IndexRe[2:T]=IndexClose[2:T]/Ind