import dtale
import pandas as pd

if __name__ == '__main__':
      dtale.show(pd.read_csv('covid.csv'), subprocess=False)
