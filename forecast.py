import os
import imageio
from matplotlib import pyplot as plt
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

def clean(df, datetime, value):
    """
    """
    if len(df.columns) > 3:
        df = df.loc[:, [datetime, value]]
    df[datetime] = pd.to_datetime(df[datetime], errors = 'coerce', infer_datetime_format="%Y-%m") #change the format inference as you see fit
    df = df.sort_values(by=datetime)
    df = df.groupby(pd.Grouper(key = datetime, axis = 0, freq = 'M', sort = True)).sum(min_count=1).dropna()

    df[value] = [int(i) for i in df[value]]
    return df


def roll_and_extract(df, date, datetime):
    """
    """
    df.loc[pd.to_datetime(date), datetime] = ''
    df_shift, y = make_forecasting_frame(df[datetime], kind = 'Passenger Count', max_timeshift=6, rolling_direction=1)
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

    plt.plot(df.index, df['#Passengers'], color = 'blue', zorder = 1)    
    plt.scatter(df.index, df['#Passengers'], color = 'black', zorder = 2)
    plt.xlabel('Time')
    plt.ylabel('Passenger Count')
    plt.savefig('./images/0.png')
    last = df.reset_index().index[-1]
    for i in range(1, n+1):
        print('Iteration:', i)
        extracted_features, y = roll_and_extract(df, date, '#Passengers')
        print(extracted_features)
        print(extracted_features.dtypes)
        
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
        df.loc[pd.to_datetime(date), '#Passengers'] = float(y_pred)
        date += relativedelta(months=1)
        date = datetime.date(date.year, date.month, calendar.monthrange(date.year, date.month)[-1])
        plt.plot(df.index[last:], df['#Passengers'][last:], color = 'red', zorder = 1)
        plt.scatter(df.index[last:], df['#Passengers'][last:], color = 'black', zorder = 2)
        plt.xlabel('Time')
        plt.ylabel('Passenger Count')
        script_dir = os.path.dirname(__file__)
        results_dir = os.path.join(script_dir, 'images/')
        sample_file_name = "{i}.png".format(i=i)

        if not os.path.isdir(results_dir):
            os.makedirs(results_dir)

        plt.savefig(results_dir + sample_file_name)
    return df


def makegif():
    script_dir = os.path.dirname(__file__)
    png_dir = os.path.join(script_dir, 'images/')
    images = []
    for file_name in sorted(os.listdir(png_dir)):
        if file_name.endswith('.png'):
            file_path = os.path.join(png_dir, file_name)
            images.append(imageio.imread(file_path))
    imageio.mimsave('./images/plot2.gif', images, fps = 2)
    

if __name__ == "__main__":
    df = pd.read_csv("AirPassengers.xls")
    df = clean(df, 'Month', '#Passengers')
    #df2 = forecast(df, 2)
    #print(df2)
    makegif()