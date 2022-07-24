<H1 align="center">
    D. A. P. S.
</H1>


<H5 align="center">
    Data Analysis and Predicting System
</H5>

<H5 align="center">
     An automated pipeline that can load a time series-esque database and perform data-drift analysis, visualize EDA/ETL insights, perform
time-series feature engineering, train an SKLearn machine learning model, and forecast data.
</H5>![Untitled Diagram drawio(1)](https://user-images.githubusercontent.com/68968629/180628463-e09048af-07e2-459e-88e3-8d39888cabfb.png)


# Introduction 

Time series data is a collection of observations obtained through repeated measurements over time. It generally looks like this:
```
       Time         Value      Region_Demarcation       Channel_Type
0    2020-01          112           North                   Agent
1    2020-02          118           South                   International
2    2020-03          132           South                   Retail
3    2020-04          129           West                    Retail
4    2020-05          121           North                   HQ
..       ...          ...
139  2022-08          606           East                    Military
140  2022-09          508           South                   Agent
141  2022-10          461           North                   Retail
142  2022-11          390           East                    Local
143  2022-12          ' '           North                   NaN

```

# What does this pipeline do?
This pipeline forecasts data and is divided into six steps that are all automated.

# Extract Transport Load (ETL)  

First we take the data and clean it up to only take values of interest. Additionally we will also index it by datetime. For our example, the data will now look like (this data below only has 1 column. Do you understand why?):
<pre>
<code>
                    Value 
 Datetime Index       
    2020-01          112  
    2020-02          118  
    2020-03          132  
    2020-04          129  
    2020-05          121  
      ...            ...
    2022-08          606  
    2022-09          508  
    2022-10          461  
    2022-11          390  
    2̶0̶2̶2̶-̶1̶2̶ ̶ ̶ ̶ ̶ ̶ ̶ ̶ ̶ ̶ ̶N̶a̶N                     ... note that NaN removal depends on your end goal + packages you may use
    </code>
</pre>
    

# Exploratory Data Analysis (EDA)  

Now that we have the ETL process completed and streamlined the procees to convert the time series data into a DateTime indexed VoI (value of interest) series, we will now perform Exploratory Data Analysis. For this, the automated pipeline uses two tools. DTale, and Pandas-Profiling. These tools have graphical interfaces that makes data visualization easy and intuitive. Using these two tools, you can automatically create reports that have correlations (if multi-columnar data), distributions, interactions, missing values report, across all the different VoIs within a dataset. DTale helps expedite the manual coding for each visualization to make the proces about 10-20x faster from the 25-30 minutes it typically takes to code each visual. These tools are state-of-the-art free alternatives to expensive tools such as Tableau. All of this is automated in the D.A.P.S. pipeline as shown below:
    

https://user-images.githubusercontent.com/68968629/180626086-7c5849cb-1b07-4f10-9126-f95b02545f03.mp4


    
    
    

# Stability Monitoring  
When we perform analysis on data, it is important that we understand how stable our data is. If we don't account for shifts over time, our forecasting models will not be able to capture variance from new potential market factors, and will eventually degrade in performance. The traditional way of checking for data drfit is tedious and time consuming. So we make the process more efficient and faster using Popmon, a package that generates interactable report analyzing shifts in data over time. The automatic creation of plots within the D.A.P.S. pipeline significantly reduces the amount of time needed to manually generate these plots by over 90% from the 30 minutes it typically takes. Population monitoring to ensure stability is automated in the D.A.P.S. piepline as shown below:

https://user-images.githubusercontent.com/68968629/180626286-9c572539-d4a0-4cac-9f67-91faf87a4574.mp4

    
# Feature Engineering 
With stable data and the EDA completed, we next set our eyes on automating feature engineering from a time series. Basic features such as the mean or the median are normally derived through programming, which is great when looking at the entirety of a data set. However, when looking at a time series and forecasting, we care about features over multiple windows of time, which makes recalculating something as simple as the mean over and over again inefficient. To solve this issue and automate this entirely, we use TSFresh. With TSFresh, the feature enginerring process can be done instantaneously, making the process about 9 times faster from the 45 minutes it took me to extract similar features manually.
    <add TSFresh Gif>
        
        
# Machine Learning

        
Now that we have performed feature engineering, we can leverage the features and train models for predictive analysis. We can use an automatic process that integrates the features calculated in the pipeline and pass it off to an automated function. This function splits the data into test/train. This means we no longer have to manually upload or download data.  :
 <add machine learning gif>
    
# Forecasting 
Lastly we use the trained machine learning model for predictive analysis. Since D.A.P.S. is open source and free (and always will be), it uses the SKLearn modelling feature to predict data based on previous data. A rough high level overview of Training and Forecasting is as follows:

<pre>
<code>

             Train Data:                            Test Data:                              End Result
    
    
                    Value                                   Value                                       Value
 Datetime Index                         Datetime Index                              Datetime Index
    2020-01          112       |            2023-01          ' '    |                  2020-01           112
    2020-02          118       |                                    |                  2020-02           118            
    2020-03          132       |                                    |                  2020-03           132              
    2020-04          129       |                                    |                  2020-04           129              
    2020-05          121       |                                    |                  2020-05           121              
      ...            ...       |                                    |   ------->         ...
    2022-08          606       |                                    |                  2022-08           606              
    2022-09          508       |                                    |                  2022-09           508              
    2022-10          461       |                                    |                  2022-10           461               
    2022-11          390       |                                    |                  2022-11           390
                                                                                       2023-01           ???
    </code>                                                 
</pre>
