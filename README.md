# iNeuron-Internship-Travel-Package-Predictor
Tourism is one of the most rapidly growing global industries and tourism forecasting is becoming an increasingly important activity in planning and managing the industry. Because of high fluctuations of tourism demand, accurate predictions of purchase of travel packages are of high importance for tourism organizations.

The goal is to predict whether the customer will purchase the travel or not.

![image](https://3.imimg.com/data3/TC/AX/MY-15186828/1-500x500.jpg)
# Data Description
We have records of 4888 customers. Below are the description of all features
CustomerID: Unique customer ID

ProdTaken: Whether the customer has purchased a package or not (0: No, 1: Yes)

Age: Age of customer

TypeofContact: How customer was contacted (Company Invited or Self Inquiry)

CityTier: City tier depends on the development of a city, population, facilities, and living standards. The categories are ordered i.e. Tier 1 > Tier 2 > Tier 3

DurationOfPitch: Duration of the pitch by a salesperson to the customer

Occupation: Occupation of customer

Gender: Gender of customer

NumberOfPersonVisiting: Total number of persons planning to take the trip with the customer

NumberOfFollowups: Total number of follow-ups has been done by the salesperson after the sales pitch

ProductPitched: Product pitched by the salesperson

PreferredPropertyStar: Preferred hotel property rating by customer

MaritalStatus: Marital status of customer

NumberOfTrips: Average number of trips in a year by customer

Passport: The customer has a passport or not (0: No, 1: Yes)

PitchSatisfactionScore: Sales pitch satisfaction score

OwnCar: Whether the customers own a car or not (0: No, 1: Yes)

NumberOfChildrenVisiting: Total number of children with age less than 5 planning to take the trip with the customer

Designation: Designation of the customer in the current organization

MonthlyIncome: Gross monthly income of the customer

# Data Pipeline
## Data Processing

Data Processing

Data Exploration

Data visualization

Feature Engineering

Model Selection

Pickle File

Webpage

# Conclusion
1) Tuned XGBoost gives a more generalised model.

2) Most important features that have an impact on Product taken are Desgination, Passport,TierCity,Martialstatus,occupation.

3) Customers monthly income in range of 15000- 25000, and age range 15-30, prefer 5 star properties also have higher chances of taking new package based on EDA.

4) Customers with Designation as Executive should be the target customers for the company .Customers who have passport and are from tier 3 city and are single or unmarried, have large business such customers have higher chances of taking new package.

5) Company should help and promote customers to get a passport , as we see having a passport increases the chances of customer accepting a package.
# User Interface


## Home Page
![image](https://github.com/Gauravgade3/iNeuron-Internship-Travel-Package-Predictor/blob/main/Images/home.jpg)
## Prediction/Result Page



![image](https://github.com/Gauravgade3/iNeuron-Internship-Travel-Package-Predictor/blob/main/Images/predict.jpg)


Documentation Link:

https://drive.google.com/drive/folders/1MYUYE9EPdDnXhwhm1ytXyFxEScmFmbIG?usp=sharing
