<div align="center">
    <h1>Yellow Taxi demand predictor service🚕📊</h1>
</div>

<br />

![365917218-244c75d2-dfb2-4f4f-aaa3-a50d39b35c44](https://github.com/user-attachments/assets/cb4e596e-90cd-43f9-bd3a-c0e11528f6b9)









## Demand Predictor
1. This project is focused on predicting the demand for yellow taxis across New York City.

2. What is a taxi-demand predicting system? Understanding and predicting demand is vital for efficient taxi fleet management. By anticipating areas and times with high demand, taxi companies can position their vehicles more effectively, reducing idle time and increasing profitability. The goal is to balance the supply of taxis to meet the predicted demand, minimizing the chances of unmet demand or an oversupply of taxis.

3. How? Based on demand data from the previous hours, we will try to predict demand for the next 1 hour.

* For this purpose, I used the dataset of the official website of the New York City Taxi and Limousine Commission (TLC), which is updated monthly to achieve this purpose.

* It is worth mentioning that I used "poetry" to create a virtual environment and to have more comfort in managing libraries. I also used a feature store called "hopsworks" with which I store historical data, the created model and the predictions.

* I also used github actions to automate the script to download features from the New York City Taxi and Limousine Commission (TLC)  website and upload them to hopsworks. I also did the same with the predictions, that is, a script that predicts every hour and uploads that prediction to hopsworks. This was done so that the dashboard only has to consume the data that is stored and is faster.

* What model🤖 was used for this? XGBoost-based models are very useful for predicting time series (and also much less complex than a neural network) but for them to work correctly, the data must be given in a certain way that facilitates learning.




# Code Summary
1. In notebook 1, 2, 3, 4 and 5 basically what was done was:

- Download the data and unzip it.
- Perform a cleanup and convert them to parquet format since it is a format that is useful for the purpose we seek and has several advantages.
- Eliminate the minutes and seconds and approximate them to the previous hour.
- Add the hours in which there were no trips with the value "zero" and graph.
- Create a function in which we obtain the indexes of the different rows and then give the most appropriate shape to the dataset so that the model learns.
- Create the dataset that the model will use to learn. (The way we transform the dataset is that it goes from 3 columns with time, trip and station, to one column for each hour, along with the information of the station and the reference time. That is, from the original dataset we take a number of rows (previous and following hours) and perform a transposition, then - - we go down one row and repeat the process. In this case we used 672 previous hours, that is, 28 days and 36 following hours.)
- Finally, a function was created to graph the previous and following records.
2. In notebook 6, 7, 8, 9 and 10:

- The data was split into train and test.
- Base models were created (without applying Machine Learning) on ​​which to later compare more complex models.
- Then it was tested with XGBoost and LightGBM, the latter giving better results.
- The next step was to continue with LightGBM and apply feature engineering to improve the model. To do this, the following were added: the average of the last 4 weeks, latitude and longitude, time and day of the week.
- Optuna was used to perform hyperparameter tuning of the model.
3. In notebook 11, 12, 13 and 14:

- The project was created in Hopsworks (feature store). This allows us to save the different records that are downloaded. To do this, a feature group must be created in which to save it and then to be able to consume it, it is more convenient through a feature view. To do this, these types of figures are created to be able to save the data.
- Notebook 12 basically downloads data from the Buenos Aires Government website, cleans it up, and uploads it to the feature store. To automate this, a GitHub action was used that runs every hour.
- In notebook 13, the model is obtained, saved and uploaded to CometML (which will then be used to make predictions).
- In notebook 14, the different data from the feature store are read, the model is loaded, the predictions are created and saved in the feature store. To automate this, another github action was created that runs immediately after the other github action finishes.
- We also have other files in the src folder. There are different functions in them that are used in different notebooks so that we don't have to repeat the function. Therefore, just by importing it, it can be used. Also within that folder are the two boards that I will now discuss:

- The first dashboard is the frontend dashboard which queries the feature store and loads the previous data and the corresponding predictions. In addition, a map is displayed showing the station that will have the highest demand in the next 1 hour (the description shows the expected demand and the time). Then, below, you will find the graphs showing the top places with the highest demand.
- The second dashboard is the frontend monitoring one, where you can see the overall error and the error of the places with the highest demand.

## Tableros
- [Dashboard with model predictions📈](https://mlsystemtopredicthourlytaxidemand-ds986dxk6gyn6kkcukt225.streamlit.app/)

<p align="center">
<img src="" width="500" align="center">
</p>
<br />

- [Dashboard with model predictions🔍](https://bike-sharing-mae-error-monitoring.streamlit.app/)

<p align="center">
<img src="" width="500" align="center">
</p>

 <br />
PD1: It should be noted that there is no access to the real data for the last hour. Therefore, to overcome this, a query simulation is performed in which data from another year is obtained that simulates being the last hour, to then include it in the database.


 PS2: If an error appears when opening the boards, reload the page to fix it.


<br />
<div align="center">
    <i>Thanks for reading. Let's keep in touch🙌🏻🙌🏻</i>
    <br />
    * <a href="https://www.linkedin.com/in/sameer-ahmad-569501227/">LinkedIn</a>
<br />
</div>

 
