"""
"""
import sqlite3
import pandas as pd
import numpy as np


def tables_in_sqlite_db(conn):
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
    results = [
        v[0] for v in cursor.fetchall()
        if v[0] != "sqlite_sequence"
    ]
    cursor.close()
    return results


class PortConstructor:

    def __init__(self,
                 n_sel, n_memory, n_alpha, n_style, Lambda=1,
                 sector_deviation=0.025, CVaR_alpha=0.05, RiskMeasure="CVaR", CovEstimator="cov"
                 ):
        """

        :param n_sel: we select nsel number of stocks
        :param n_memory: window size for Sigma estimation
        :param n_alpha: window size for expected return estimation
        :param n_style: number of style constraints
        :param Lambda: risk tolerance
        :param sector_deviation:
        :param CVaR_alpha:
        :param RiskMeasure: "Risk_Adjusted_Return"/"Risk_Parity"/"Minimum_Tail_Dependent"/"Minimum_Variance"/"CVaR"
        :param CovEstimator: "cov"/"lpmEstimator"/"slpmEstimator"/"kendallEstimator"/"spearmanEstimator"/"shrinkEstimator"
        """
        self.n_sel = n_sel
        self.n_memory = n_memory
        self.n_alpha = n_alpha
        self.n_style = n_style
        self.Lambda = Lambda
        self.sector_deviation = sector_deviation
        self.CVaR_alpha = CVaR_alpha
        self.RiskMeasure = RiskMeasure
        self.CovEstimator = CovEstimator
        self.wup = 5 / n_sel  # upper bound for each stock #
        self.wdown = 1 / n_sel / 3  # lower bound for each stock
        # self.load_code FuJuCode2.csv
        self.code_list = None  # Code
        # load_fv
        self.FV = None
        # load_beta
        self.Beta = None
        # load_equity_sector_classification
        self.Date = None
        self.SectorClass2 = None
        self.SectorU = None
        self.n_sector = None
        # load_ohlcv
        self.CC = None
        self.LogCC = None
        # load_equity_index
        self.index_df = None
        self.index_re = None
        # PortfolioOptimization
        self.Wopt = None

    def load_code(self, file_path):
        self.code_list = list(pd.read_csv(file_path)["Code"])

    def load_ohlcv(self, file_path):
        conn = sqlite3.connect(file_path)
        tables = tables_in_sqlite_db(conn)
        n = len(tables)
        df = pd.read_sql_query("SELECT * FROM X000001", conn)
        T = df.shape[0]
        Open = np.zeros(shape=(T, n))
        High = np.zeros(shape=(T, n))
        Low = np.zeros(shape=(T, n))
        Close = np.zeros(shape=(T, n))
        LiquidSize = np.zeros(shape=(T, n))
        self.Volume = np.zeros(shape=(T, n))
        self.CC = np.zeros(shape=(T, n))
        self.LogCC = np.zeros(shape=(T, n))
        Size = np.zeros(shape=(T, n))
        for i in range(0, (n - 1)):
            df = pd.DataFrame(pd.read_sql_query("SELECT * FROM " + tables[i], conn))
            Open[:, i] = df["Open"]  # A.Open
            High[:, i] = df["High"]
            Low[:, i] = df["Low"]
            Close[:, i] = df["Close"]
            LiquidSize[:, i] = df["LiquidSize"]
            Size[:, i] = df["Size"]
            self.Volume[:, i] = df["Volume"]

        LogClose = np.log(Close)
        for i in range(0, (n - 1)):
            self.CC[1:T, i] = Close[1:T, i] / Close[0:(T - 1), i] - 1
            self.LogCC[1:T, i] = LogClose[1:T, i] - LogClose[0:(T - 1), i]

    def load_fv(self, file_path):
        """
        factor value
        :param file_path:
        :return:
        """
        df = pd.read_csv(file_path, index_col=[0])
        self.FV = df.fillna(-100)

    def load_beta(self, file_path):
        """
        beta
        :param file_path:
        :return:
        """
        self.Beta = pd.read_csv(file_path, index_col=[0])

    def load_equity_index(self, file_path):
        self.index_df = pd.read_csv(file_path)
        index_open_s = self.index_df['Open']
        index_high_s = self.index_df['High']
        index_low_s = self.index_df['Low']
        index_close_s = self.index_df['Close']
        self.index_re = index_close_s.pct_change()[1:] / index_close_s[:-1]  # IndexRe

    def load_equity_sector_classification(self, file_path):
        conn = sqlite3.connect(file_path)
        df = pd.read_sql_query("SELECT * FROM X000001", conn)
        self.Date = pd.to_datetime(df.Date)
        tables = tables_in_sqlite_db(conn)
        T = df.shape[0]
        n = len(tables)
        SectorClass = np.zeros(shape=(T, n))
        for i in range(0, (n - 1)):
            data = pd.DataFrame(pd.read_sql_query("SELECT * FROM " + tables[i], conn))
            SectorClass[:, i] = data["TYPE_ID"]  # data.Type_ID

        SectorClass = pd.DataFrame(SectorClass, columns=self.code_list)
        self.SectorClass2 = SectorClass.applymap(lambda x: str(int(x))[:8])
        self.SectorU = [x for x in set(self.SectorClass2.to_numpy().flatten()) if x != '0']
        self.SectorU.sort()
        self.n_sector = len(self.SectorU)

    def PortfolioOptimization(self):
        """
        Run loop for each trading day t:
            1. at time t determine which stocks to hold for t+1: index_jy
            2. compute covariance matrix (corrected for zero diagonal term) and sector-wise expected return
            3. run Portfolio Optimization: Constrained_OneStep_OptimFunc5() and retrieve results for Wopt[t+1,index_jy]
        :return:
        """
        from rpy2.robjects.packages import importr
        FRAPO = importr("FRAPO")
        self.Wopt = np.zeros((self.FV.shape[0] + 1, self.FV.shape[1]))
        nstart = self.n_memory * 2 + 1
        # H is covariance matrix; Alpha is expected return
        for t in range(nstart, self.FV.shape[0]):
            index_jy = np.where(self.FV.iloc[t].rank(ascending=False) <= self.n_sel)[0]
            if self.RiskMeasure != "Minimum_Tail_Dependent":
                H = self.CC.iloc[(t - self.n_memory + 1):(t + 1), index_jy].cov()
                h_diag = np.diag(H)
                if np.any(h_diag == 0):
                    for s in np.where(h_diag == 0)[0]:
                        for s in np.where(h_diag == 0)[0]:
                            H[s, s] = np.mean(h_diag[h_diag != 0])
                SD = np.diag(H) ** 0.5
            elif self.RiskMeasure == "Minimum_Tail_Dependent":
                H = FRAPO.tdc(self.CC[(t - self.n_memory + 1):(t + 1), index_jy])
                SD = self.CC.iloc[(t - self.n_memory + 1):(t + 1), index_jy].cov() ** 0.5
                if np.any(SD == 0):
                    for s in np.where(SD == 0)[0]:
                        SD[s] = np.mean(SD[SD != 0])
            else:  # if (is.element(RiskMeasure, c("Minimum_Tail_Dependent", "Minimum_Variance")) == FALSE)
                H = None
                SD = None
                Alpha = np.zeros(self.n_sel)
                for i in range(0, self.n_sector - 1):
                    index_jz = np.intersect1d(index_jy,
                                              np.where(self.SectorClass2.iloc[t - 1, :] == self.SectorU[i])[0])
                    lz = len(index_jz)
                    index_js = np.where(np.isin(index_jy, index_jz))[0]
                    ls = len(index_js)
                    if lz > 1:
                        Alpha[index_js] = self.CC.iloc[(t - self.n_alpha + 1):(t + 1), index_jz].sum().sum() / np.sign(
                            self.Volume.iloc[(t - self.n_alpha + 1):(t + 1), index_jz]).sum().sum()

            op = self.Constrained_OneStep_OptimFunc5(t, index_jy, H, SD)
            self.Wopt[t + 1, index_jy] = op['w_opt']

    def data_prepare(self):
        """
        EquityIndex Sector Constitutes Info
        """
        pass

    def Constrained_OneStep_OptimFunc5(self, t, index_jy, H, SD):
        """
        1. Prepare for X_sector (sector constraint matrix) and X_style(Size and Beta constraint matrix) at each trading day
        2. Run Optimization according to selected RiskMeasure
            Risk_Adjusted_Return:    Constrained_MultiFactorModel_OptimFunc3()
            Risk_Parity:             Constrained_MultiFactorModel_OptimFunc5()
            Minimum_Tail_Dependent:  Constrained_MultiFactorModel_OptimFunc6()
            Minimum_Variance:        Constrained_MultiFactorModel_OptimFunc3()
            CVaR:                    Constrained_MultiFactorModel_OptimFunc7()
        :param t:
        :param index_jy:
        :param H:
        :param SD:
        :return:
        """
        # some logic here
        op = {}
        return op

    def do_job(self):
        # Load Data
        self.load_code("FuJuCode2.csv")
        self.load_ohlcv(".db")
        self.load_fv(".csv")
        self.load_beta(".csv")
        self.load_equity_sector_classification(".csv")
        self.load_equity_index(".csv")
        # Data Preparation
        self.data_prepare()
        # Run loop for each trading day t
        self.PortfolioOptimization()


obj = PortConstructor(..)
obj.do_job()
