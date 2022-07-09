from dataclasses import dataclass
from numpy import add
import pandas as pd
from tsfresh.utilities.dataframe_functions import make_forecasting_frame
from tsfresh import extract_features
from tsfresh.utilities.dataframe_functions import impute
from tsfresh import select_features
from datetime import datetime
import calendar
import datetime
from dateutil.relativedelta import relativedelta
from sklearn import datasets, ensemble, linear_model


def clean(df, value):
    """
    """
    if len(df.columns > 3):
        df = df.loc[:, ['datetime', value]]
    df['datetime'] = pd.to_datetime(df['datetime'], errors = 'coerce', infer_datetime_format="%Y/%m")
    df = df.sort_values(by='datetime')
    df = df.groupby(pd.Grouper(key = 'datetime', axis = 0, freq = 'M', sort = True)).sum(min_count=1).dropna()

    df[value] = [int(i) for i in df[value]]
    return df


def roll_and_extract(df, date):
    """
    """
    df.loc[pd.to_datetime(date), 'Passengers']
    df_shift, y = make_forecasting_frame(df['Passengers'], kind = 'Passenger Count', column_sort = 'time', column_value = 'value')
    df_shift['value'] = [float(i)for i in df_shift['value']]
    extracted_features = extract_features(df_shift, column_id = 'id', column_sort = 'time', column_value = 'value', impute_function=impute, n_jobs=7)
    extracted_features.dropna(axis = 1, how = 'all', thresh = None, subset = None, inplace = True)
    extracted_features = extracted_features.loc[:, extracted_features.any()] #drop 0 columns
    return extracted_features, y

def add_dummy(df):
    """
    """
    df['month'] = pd.Categorical.from_codes(
        pd.to_datetime([x[1] for x in df.index.tolist()[:]]).month,
        categories = list(calendar.month_name),
        ordered = True
        )
    df = pd.get_dummies(df, columns = ['month'], prefix_sep='', prefix='')
    return df


def train(df, y, method):
    """
    """
    x_train = df.iloc[:-1]
    y_train = y.iloc[:-1]
    y_train = y_train.astype(float)

    if method == "linear":
        regr = linear_model.LinearRegression()
        regr.fit(x_train, y_train)
    
    if method == "gradient":
        params = {
            "n_estimators": 500, 
            "max_depth": 4,
            "min_samples_split": 5,
            "learning_rate": 0.01,
            "loss": "huber",
        }
        regr = ensemble.GradientBoostingRegressor(**params)
        regr.fit(x_train, y_train)
    
    return regr


def forecast(df, n):
    """
    """
    
    d = pd.to_datetime(df.index[-1])
    d += relativedelta(months = 1)
    date = datetime.date(d.year, d.month, calendar.monthrange(d.year, d.month)[-1])
    for i in range(1, n+1):
        print('Iteration:', i)
        extracted_features, y = roll_and_extract(df, date)w
        
        if i == 1:
            selected_features = select_features(extracted_features, y, n_jobs = 7, fdr_level = 0.99)
            cols = selected_features.columns
            selected_features = add_dummy(selected_features)
            x_test = selected_features.iloc[-1:]
            regr = train(selected_features, y, "gradient")
        else:
            selected_features = extracted_features[cols]
            selected_features = add_dummy(selected_features)
            x_test = selected_features.iloc[-1:]
        
        
        y_pred = regr.predict(x_test)
        df.loc[pd.to_datetime(date), 'Passengers'] = int(y_pred)
        date += relativedelta(months=1)
        date = datetime.date(date.year, date.month, calendar.monthrange(date.year, date.month[-1]))
    return df

if __name__ == "__main__"":
    df = pd.read_csv("airline.xls")
    df = clean(df)
    df2 = forecast(df, 2)
    print(df2)