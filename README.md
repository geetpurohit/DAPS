<H1 align="center">
    D. A. P. S.
</H1>


<H5 align="center">
    Data Analysis and Predicting System
</H5>

<H5 align="center">
     An automated pipeline that can load a database and perform data-drift analysis, visualize EDA/ETL insights, perform
time-series feature engineering, train an SKLearn machine learning model, and forecast data.
</H5>

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
143  2022-12          432           North                   NaN

```

# What does this program do?
This project forecasts data and is divided into six steps that are all automated:

<details> 
  <summary> Fetch'n Clean </summary>    
    First we take the data and clean it up to only take values of interest. Additionally we will also index it by datetime. For our example, the data will now look like:
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
    2022-12          432  
    </code>
</pre>
    
</details>

<details> 
  <summary> Make Forecasting Frame </summary>    
    Next, we take the time series and using TSFresh's inbuilt feature to roll a time series, we make a forecasting frame. At this point our forecasting frame looks like this:
    
    
</details>
<details> 
  <summary> CMake </summary>    
    Dlib is written in C/C++, and your computer needs to *build* the package, so you need something that can automate that build process. Head over to the download link given above and download the file that is the best for you. I recommend the .msi file since it is much easier (tip - make sure to add the Windows PATH during installation). :

    
</details>
<details> 
  <summary> CMake </summary>    
    Dlib is written in C/C++, and your computer needs to *build* the package, so you need something that can automate that build process. Head over to the download link given above and download the file that is the best for you. I recommend the .msi file since it is much easier (tip - make sure to add the Windows PATH during installation). :

    
</details>
<details> 
  <summary> CMake </summary>    
    Dlib is written in C/C++, and your computer needs to *build* the package, so you need something that can automate that build process. Head over to the download link given above and download the file that is the best for you. I recommend the .msi file since it is much easier (tip - make sure to add the Windows PATH during installation). :

    
</details>
