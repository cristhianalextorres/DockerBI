import numpy as np
import pandas as pd
from pandas.tseries.offsets import DateOffset
import statsmodels.api as sm
from pmdarima import auto_arima

class ModeloPredictivoARIMA:
    def __init__(self, df, meses_prediccion):
        self.df = df
        self.meses_prediccion = meses_prediccion

    def entrenar_y_predecir(self):
        ListColumName = list(self.df.columns.values)

        for i in ListColumName:
            self.df[i] = self.df[i].astype('float64')

        pred_date=[self.df.index[-1] + DateOffset(months=x)for x in range(0,self.meses_prediccion)]
        pred_date=pd.DataFrame(index=pred_date[1:],columns=self.df.columns)

        
        count = 0
        df = self.df
        df=pd.concat([df,pred_date])
        for i in ListColumName:

            model = auto_arima(self.df[i],start_P=1,start_q=1,max_P=6,max_q=6,m=12,start_p=0,d=1,D=1,trace=True,error_action='ignore',suppress_warnings=True,stepwise=True)
            results = model.fit(self.df[i])
            
            parametrosModelo = str(model)

            p = int(parametrosModelo[7])
            d = int(parametrosModelo[9])
            q = int(parametrosModelo[11])

            ModeloAutoArima = np.round(results.predict(n_periods = self.meses_prediccion))

            model= sm.tsa.arima.ARIMA(self.df[i],order=(p,d,q))
            results=model.fit()
            ModeloArima = np.round(results.predict())

            valorPred = pd.concat([ModeloArima,ModeloAutoArima])

            columna = self.df.columns.values[count] + 'Pred'
            
            df[columna] = valorPred.astype('int64')
            count += 1

        return df