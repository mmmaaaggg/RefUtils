"""
@author  : MG
@Time    : 2020/8/30 9:05
@File    : guo_main.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import sqlite3
import pandas as pd
import numpy as np


class PortConstructor:

    def __init__(self,
                 nsel, nmemory, nalpha, nstyle, risk_tolerance,
                 sector_deviation=0.025, cvar_alpha=0.05, risk_measure="CVaR", cov_estimator="cov"
                 ):
        """

        :param nsel: we select nsel number of stocks
        :param nmemory: window size for Sigma estimation
        :param nalpha: window size for expected return estimation
        :param nstyle: number of style constraints
        :param risk_tolerance: risk tolerance
        :param sector_deviation:
        :param cvar_alpha:
        :param risk_measure: "Risk_Adjusted_Return"/"Risk_Parity"/"Minimum_Tail_Dependent"/"Minimum_Variance"/"CVaR"
        :param cov_estimator: "cov"/"lpmEstimator"/"slpmEstimator"/"kendallEstimator"/"spearmanEstimator"/"shrinkEstimator"
        """
        self.nsel = nsel
        self.nmemory = nmemory
        self.nalpha = nalpha
        self.nstyle = nstyle
        self.risk_tolerance = risk_tolerance
        self.sector_deviation = sector_deviation
        self.cvar_alpha = cvar_alpha
        self.risk_measure = risk_measure
        self.cov_estimator = cov_estimator
        self.wup = 5 / nsel  # upper bound for each stock #
        self.wdown = 1 / nsel / 3  # lower bound for each stock

        self.md = None
        self.fv_df = None
        self.beta_df = None

        self.date_s = None
        self.sector_class2_df = None
        self.sector_unique_list = None

        # 从 DB_FuJuDailybar.db 获取的数据
        self.code_list = None
        self.volume_df = None
        self.cc_df = None
        self.log_cc_df = None

        self.portfolio_weights = None

    def get_md(self, file_path):
        conn = sqlite3.connect(file_path)

        def tables_in_sqlite_db(conn):
            cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = [
                v[0] for v in cursor.fetchall()
                if v[0] != "sqlite_sequence"
            ]
            cursor.close()
            return tables

        tables = tables_in_sqlite_db(conn)
        n = len(tables)
        self.code_list = []
        df = pd.read_sql_query("SELECT * FROM X000001", conn)
        T = df.shape[0]
        Open = np.zeros(shape=(T, n))
        High = np.zeros(shape=(T, n))
        Low = np.zeros(shape=(T, n))
        Close = np.zeros(shape=(T, n))
        LiquidSize = np.zeros(shape=(T, n))
        self.volume_df = np.zeros(shape=(T, n))
        Size = np.zeros(shape=(T, n))
        for i in range(0, (n - 1)):
            df = pd.DataFrame(pd.read_sql_query("SELECT * FROM " + tables[i], conn))
            self.code_list.append(tables[i][1:])
            Open[:, i] = df["Open"]  # A.Open
            High[:, i] = df["High"]
            Low[:, i] = df["Low"]
            Close[:, i] = df["Close"]
            LiquidSize[:, i] = df["LiquidSize"]
            Size[:, i] = df["Size"]
            self.volume_df[:, i] = df["Volume"]

        # CC = np.zeros(shape=(T, n))
        # for i in range(0, (n - 1)):
        #     CC[2:T, i] = Close[2:T, i] / Close[1:(T - 1), i] - 1

        close_df = pd.DataFrame(Close, columns=self.code_list)
        self.cc_df = (close_df.pct_change().iloc[1:, :] / close_df.iloc[:-1, :]).fillna(0)
        log_close_df = np.log(close_df)
        self.log_cc_df = log_close_df.pct_change().iloc[1:, :].fillna(0)

    def load_fv(self, file_path):
        """
        加载 factor value
        :param file_path:
        :return:
        """
        df = pd.read_csv(file_path, index_col=[0])
        self.fv_df = df.fillna(-100)

    def load_beta(self, file_path):
        """
        加载 beta
        :param file_path:
        :return:
        """
        self.beta_df = pd.read_csv(file_path, index_col=[0])

    def load_sector_class_df(self, file_path):
        sector_class_dic = {}
        with sqlite3.connect(file_path) as conn:
            for num, code in enumerate(self.code_list, start=1):
                table_name = f"X{code[:6]}"
                # print(f"{num:4d}) {code} -> {table_name}")
                stock_df = pd.read_sql(f"select * from {table_name}", conn)
                if self.date_s is None:
                    self.date_s = pd.to_datetime(stock_df['Date'])
                sector_class_dic[code] = stock_df["TYPE_ID"]
                # if num > 3:  # 调试使用
                #     break

        sector_class_df = pd.DataFrame(sector_class_dic)
        sector_class_df.fillna(0)
        #          000001.SZ     000002.SZ     000004.SZ     000005.SZ
        # 0     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
        # 1     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
        # 2     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
        # 3     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
        # 4     1.031721e+10  1.031723e+10  1.031718e+10  1.031723e+10
        #             ...           ...           ...           ...
        # 3309  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
        # 3310  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
        # 3311  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
        # 3312  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
        # 3313  1.031721e+10  1.031723e+10  1.031718e+10  1.031704e+10
        # 取前8位
        self.sector_class2_df = sector_class_df.applymap(lambda x: str(int(x))[:8])  # SectorClass2
        self.sector_unique_list = [_ for _ in set(self.sector_class2_df.to_numpy().flatten()) if _ != '0']
        self.sector_unique_list.sort()  # SectorU
        # sector_count = len(sector_unique_list)  # nsector

    def construct(self):
        self.portfolio_weights = np.zeros((self.fv_df.shape[0] + 1, self.fv_df.shape[1]))
        nstart = self.nmemory * 2 + 1
        # H is covariance matrix; Alpha is expected return
        for t in range(nstart, self.fv_df.shape[0]):
            fv_s = self.fv_df.iloc[t, :]
            matched_nsel = fv_s.rank(ascending=False) < self.nsel
            matched_nsel_indexes = np.where(matched_nsel)[0]  # jy
            if self.risk_measure == "Minimum_Tail_Dependent":
                H = np.zeros(1)
                if self.cov_estimator == "cov":
                    pass
                elif self.cov_estimator == "lpmEstimator":
                    pass
                elif self.cov_estimator == "slpmEstimator":
                    pass
                elif self.cov_estimator == "kendallEstimator":
                    pass
                elif self.cov_estimator == "spearmanEstimator":
                    pass
                elif self.cov_estimator == "shrinkEstimator":
                    pass
                else:
                    raise KeyError(f'cov_estimator = {self.cov_estimator} 不合法')

                if np.any(np.isnan(H)):
                    H = self.cc_df.iloc[(t - self.nmemory + 1):(t + 1), matched_nsel_indexes].cov()

                h_diag = np.diag(H)
                if np.any(h_diag == 0):  # min(diag(H))==0
                    # diag(H)[which(diag(H)==0)]=mean(diag(H)[which(diag(H)!=0)])
                    for n in np.where(h_diag == 0)[0]:
                        H[n, n] = np.mean(h_diag[h_diag != 0])

                SD = h_diag ** 0.5

            elif self.risk_measure == "Minimum_Tail_Dependent":
                pass
            else:
                alpha = np.zeros(self.nsel)
                for num, sector in enumerate(self.sector_unique_list):
                    matched_sector = (self.sector_class2_df.iloc[-1, :] == sector) & matched_nsel
                    matched_sector_indexes = np.where(matched_sector)[0]  # jz
                    matched_sector_of_nsel_indexes = np.where(np.isin(matched_nsel_indexes, matched_sector_indexes))
                    if np.sum(matched_sector) > 0:
                        alpha[matched_sector_of_nsel_indexes] = np.sum(
                            self.cc_df.iloc[(t - self.nalpha + 1):(t + 1), matched_sector_indexes]
                        ) / np.sum(
                            self.volume_df[(t - self.nalpha + 1):(t + 1), matched_sector_indexes] > 0
                        )

                    if np.isnan(alpha[matched_sector_of_nsel_indexes]):
                        raise ValueError(
                            f"{num}) {sector} 在 {np.where(np.isnan(alpha[matched_sector_of_nsel_indexes]))[0]} 出现 nan")

                    op = self.Constrained_OneStep_OptimFunc5()
                    self.portfolio_weights[t + 1, matched_nsel_indexes] = op['w_opt']  # Wopt[t+1,jy]=op$w_opt;

    def do_job(self):
        pass
