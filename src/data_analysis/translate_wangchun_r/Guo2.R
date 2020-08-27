   library("quadprog");
   source("IdentityMatrixFunc.R");
   N=length(Alpha);
   N_sector=dim(X_sector)[2];
   N_style=dim(X_style)[2];

   # #
   Aeq=matrix(1,1,N);
   beq=1;
   Aneq=rbind(t(X_sector),-t(X_sector),t(X_style),-t(X_style));
   bneq=c(alpha_sector_up,-alpha_sector_low,alpha_style_up,-alpha_style_low);
   
   # #
   Amat=Aeq;
   Amat=rbind(Amat,-Aneq);
   Amat=rbind(Amat,matrix(-1,1,N));
   Amat=rbind(Amat,matrix(1,1,N));

   # #
   bvec=beq;
   bvec=c(bvec,-bneq);
   bvec=c(bvec,-wup);
   bvec=c(bvec,wdown);
   bvec=as.matrix(bvec); 

   # #
   Dmat=lambda*H;
   if (corpcor::is.positive.definite(Dmat)==FALSE) Dmat=corpcor::make.positive.definite(Dmat);
   dvec=Alpha;

   # #   
   result=solve.QP(Dmat,dvec,t(Amat),bvec,meq=1,factorized=FALSE);
   w_opt=result$solution/sum(result$solution);
   w_opt[which(w_opt<1e-10)]=0;
   w_opt=w_opt/sum(w_opt);
