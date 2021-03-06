# -*- coding: utf-8 -*-
"""iNeuron - Travel Package Prediction.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xh46d496nj280xxU8W-0Al6wWesMPIsy

# **Problem Statement**

## Tourism is one of the most rapidly growing global industries and tourism forecasting is becoming an increasingly important activity in planning and managing the industry. Because of high fluctuations of tourism demand, accurate predictions of purchase of travel packages are of high importance for tourism organizations. 
## The goal is to predict whether the customer will purchase the travel or not.
"""

# Mounting drive
# from google.colab import drive
# drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# Importing necessary libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
# %matplotlib inline

from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import accuracy_score, recall_score, precision_score, f1_score, roc_auc_score, confusion_matrix, roc_curve, auc, classification_report
from sklearn import metrics
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier,RandomForestClassifier,StackingClassifier
from sklearn.ensemble import AdaBoostClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix,ConfusionMatrixDisplay,plot_confusion_matrix
import pickle

# Importing the dataset

df = pd.read_csv("/content/drive/MyDrive/iNeuron Internship/Travel.csv",encoding = "ISO-8859-1")

# Check shape of dataset

df.shape

# Checking first 10 rows in dataset

df.head(10)

# Checking last 10 rows in dataset

df.tail(10)

# Checking basic information of our dataset

df.info()

# Exploring descriptive statistical parameters

df.describe()

"""# Features Description

## We have records of 4888 customers. Below are the description of all features

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
"""

# checking the total number of null values in every column

df.isnull().sum()

# plotting heatmap of null values

plt.figure(figsize=(12, 8))
sns.heatmap(df.isnull(), yticklabels = False ,cmap = 'viridis')
plt.show()

# checking for identical rows if present

df.duplicated().sum()

# checking for unique value counts in "TypeofContact"
df['TypeofContact'].value_counts()

# Replace null values (categorical)
df['TypeofContact'].fillna('Self Enquiry', inplace=True)

# Replace null values (numeric)
df['Age'].fillna(df['Age'].median(), inplace=True)
df['DurationOfPitch'].fillna(df['DurationOfPitch'].median(), inplace = True)
df['NumberOfFollowups'].fillna(df['NumberOfFollowups'].median(), inplace=True)
df['PreferredPropertyStar'].fillna(df['PreferredPropertyStar'].median(), inplace=True)
df['NumberOfTrips'].fillna(df['NumberOfTrips'].median(), inplace=True)
df['NumberOfChildrenVisiting'].fillna(df['NumberOfChildrenVisiting'].median(), inplace=True)
df['MonthlyIncome'].fillna(df['MonthlyIncome'].median(), inplace=True)

# Drop 'CustomerID' feature
df.drop(['CustomerID'],axis=1,inplace=True)

# Getting the unique values in categorical features
cat_cols = ['Designation','ProdTaken', 'OwnCar', 'Passport','CityTier','MaritalStatus','ProductPitched','Gender','Occupation','TypeofContact']

for i in cat_cols:
  print('Unique values in', i)
  print(df[i].value_counts())
  print('-'*30)

# Replace Fe Male to Female in Gender feature
df['Gender'] = df['Gender'].apply(lambda x: 'Female' if x == 'Fe Male' else x)
df['Gender'].value_counts()

# Plotting histogram for numeric features
numeric_features= df.select_dtypes(exclude='object')

for col in numeric_features[:]:
  sns.histplot(df[col],color="y")
  plt.axvline(df[col].mean(), color='magenta', linestyle='dashed', linewidth=2)
  plt.axvline(df[col].median(), color='cyan', linestyle='dashed', linewidth=2)  
  sns.despine(top=True,right=True,left=True)
  plt.figure(figsize=(10,7))
  plt.show()

# plotting target feature
print(df['ProdTaken'].value_counts())

plt.pie(df['ProdTaken'].value_counts(),labels=['Not Purchased', 'Purchased'],autopct='%0.2f',colors=['orange','green'],explode=[0.1,0])
plt.title("Product Purchased or Not")
plt.show()

# define functio for countplot
def plot(column):
  for i,variable in enumerate(column):
                       plt.subplot(6,3,i+1)
                       sns.set_palette('Set3')
                       ax=sns.countplot(x=df[variable], data=df)
                       sns.despine(top=True,right=True,left=True)                                                # to remove side line from graph
                       for p in ax.patches:
                             percentage = '{:.1f}%'.format(100 * p.get_height()/len(df[variable]))
                             x = p.get_x() + p.get_width() / 2 - 0.05
                             y = p.get_y() + p.get_height()
                             plt.annotate(percentage, (x, y),ha='center')
                       plt.title(cols[i].upper())
                       plt.xticks(rotation=45)
                       plt.subplots_adjust(left=0.1, bottom=0.5, right=1.5, top=5, wspace=0.9, hspace=0.9)

# countplot
cols=['TypeofContact', 'CityTier', 'Occupation', 'Gender',
        'NumberOfPersonVisiting', 'NumberOfFollowups', 'ProductPitched', 
        'PreferredPropertyStar', 'MaritalStatus', 'NumberOfTrips',
        'Passport', 'PitchSatisfactionScore',
        'OwnCar', 'NumberOfChildrenVisiting', 
        'Designation']


plot(cols)

df['Age'].value_counts()

df['Agebin'] = pd.cut(df['Age'], bins = [18,25, 31, 40, 50, 65], labels = ['18-25','26-30', '31-40', '41-50', '51-65'])

df['Agebin'].value_counts()

df['MonthlyIncome'].value_counts()

df['MonthlyIncomebin'] = pd.cut(df['MonthlyIncome'], bins = [0,15000,20000, 25000, 30000,35000,40000,45000,50000,100000], labels = ['<15000', '<20000', '<25000', '<30000','<35000','<40000','<45000','<50000','<100000'])

df['MonthlyIncomebin'].value_counts()

cols1=['Agebin', 'MonthlyIncomebin']
plot(cols1)

# pairplot
sns.set_palette('Set2')
sns.pairplot(df, hue="ProdTaken",corner=True)

# correlation plot
plt.rcParams['figure.figsize'] = (15, 8)
sns.heatmap(df.corr(),annot=True)

X = df.drop(['ProdTaken'],axis=1)
plt.style.use('seaborn-whitegrid')
X.corrwith(df['ProdTaken']).plot.bar(figsize = (20, 10), title = "Correlation with ProdTaken", fontsize = 20,rot = 90, grid = True)

"""Countplot with dependent feature"""

def plot1(column):
  for i,variable in enumerate(column):
                       plt.subplot(6,3,i+1)
                       sns.set_palette('Set1')
                       ax=sns.countplot(x=df[variable],hue=df['ProdTaken'], data=df)
                       sns.despine(top=True,right=True,left=True) # to remove side line from graph
                       for p in ax.patches:
                             percentage = '{:.1f}%'.format(100 * p.get_height()/len(df[variable]))
                             x = p.get_x() + p.get_width() / 2 - 0.05
                             y = p.get_y() + p.get_height()
                             plt.annotate(percentage, (x, y),ha='center')
                     #  plt.tight_layout()
                      #  plt.title(cols[i].upper())
                       plt.xticks(rotation=45)
                       plt.subplots_adjust(left=0.1, bottom=0.5, right=1.3, top=5, wspace=0.9, hspace=0.9)

col=['TypeofContact', 'CityTier', 'Occupation', 'Gender',
        'NumberOfPersonVisiting', 'NumberOfFollowups', 'ProductPitched', 
        'PreferredPropertyStar', 'MaritalStatus', 'NumberOfTrips',
        'Passport', 'PitchSatisfactionScore',
        'OwnCar', 'NumberOfChildrenVisiting', 
        'Designation','Agebin', 'MonthlyIncomebin']


plot1(col)



"""countplot with product category feature"""

def plot2(column):
  for i,variable in enumerate(column):
                       plt.subplot(6,3,i+1)
                       sns.set_palette('Set2')
                       ax=sns.countplot(x=df[variable],hue=df['ProductPitched'], data=df)
                       sns.despine(top=True,right=True,left=True) # to remove side line from graph
                       for p in ax.patches:
                             percentage = '{:.1f}%'.format(100 * p.get_height()/len(df[variable]))
                             x = p.get_x() + p.get_width() / 2 - 0.05
                             y = p.get_y() + p.get_height()
                             plt.annotate(percentage, (x, y),ha='center')
                     #  plt.tight_layout()
                      #  plt.title(cols[i].upper())
                       plt.xticks(rotation=45)
                       plt.subplots_adjust(left=0.1, bottom=0.5, right=1.3, top=5, wspace=0.9, hspace=0.9)

plot2(cols)

sns.set_palette('Set2')
plt.rcParams['figure.figsize'] = (10, 7)
sns.stripplot(data=df, x="Occupation", y="MonthlyIncome", hue="ProdTaken",dodge=True, alpha=.25, zorder=1)
sns.despine(top=True,right=True,left=True)
plt.title('Monthly Income vs Occupation')

plt.rcParams['figure.figsize'] = (20, 13)
sns.scatterplot( x="Age", y="MonthlyIncome", hue="ProdTaken",s=100,data=df,alpha=0.8,palette=['orange','green'])
sns.despine(top=True,right=True,left=True)

# plotting boxplot for numerical features to find out outliers
for i, variable in enumerate(numeric_features):
                     plt.subplot(6,3,i+1)
                     plt.boxplot(df[variable])
                     plt.tight_layout()
                     plt.title(variable)

df[(df.MonthlyIncome>40000) | (df.MonthlyIncome<12000)]

df.sort_values(by=["NumberOfTrips"],ascending = False).head()

# drop the outliers
df.drop(index=df[(df.MonthlyIncome>40000) | (df.MonthlyIncome<12000)].index,inplace=True)
df.drop(index=df[df.NumberOfTrips>10].index,inplace=True)

"""Encoding"""

df = pd.get_dummies(df, columns=['ProductPitched','Occupation','Designation','MaritalStatus'],drop_first=True)

df['Gender'] = np.where(df['Gender']=='Male', 1, 0)
df['TypeofContact'] = np.where(df['TypeofContact']=='Self Enquiry', 1, 0)

# drop unnecessary features
df.drop(columns=['Agebin','MonthlyIncomebin'],inplace=True)

# define dependent and independent features
X = df.drop(['ProdTaken'],axis=1)
y = df['ProdTaken']

# train test data split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=1,stratify=y)
X_train.shape, X_test.shape

# define function for confusion matrix
def make_confusion_matrix(y_actual,y_predict,title):
    '''Plot confusion matrix'''
    fig, ax = plt.subplots(1, 1)
    
    cm = confusion_matrix(y_actual, y_predict, labels=[0,1])
    disp = ConfusionMatrixDisplay(confusion_matrix=cm,
                               display_labels=["No","Yes"])
    disp.plot(cmap='Greens',colorbar=True,ax=ax)
    
    ax.set_title(title)
    plt.tick_params(axis=u'both', which=u'both',length=0)
    plt.grid(b=None,axis='both',which='both',visible=False)
    plt.show()

# define function for metrics score
def get_metrics_score(model,X_train_df,X_test_df,y_train_pass,y_test_pass,flag=True):
    '''
    Function to calculate different metric scores of the model - Accuracy, Recall, Precision, and F1 score
   
    '''
    # defining an empty list to store train and test results
    score_list=[] 
    pred_train = model.predict(X_train_df)
    pred_test = model.predict(X_test_df)
    pred_train = np.round(pred_train)
    pred_test = np.round(pred_test)
    train_acc = accuracy_score(y_train_pass,pred_train)
    test_acc = accuracy_score(y_test_pass,pred_test)
    train_recall = recall_score(y_train_pass,pred_train)
    test_recall = recall_score(y_test_pass,pred_test)
    train_precision = precision_score(y_train_pass,pred_train)
    test_precision = precision_score(y_test_pass,pred_test)
    train_f1 = f1_score(y_train_pass,pred_train)
    test_f1 = f1_score(y_test_pass,pred_test)
    score_list.extend((train_acc,test_acc,train_recall,test_recall,train_precision,test_precision,train_f1,test_f1))
    if flag == True: 
          metric_names = ['Train_Accuracy', 'Test_Accuracy', 'Train_Recall', 'Test_Recall','Train_Precision',
                          'Test_Precision', 'Train_F1-Score', 'Test_F1-Score']
          cols = ['Metric', 'Score']
          records = [(name, score) for name, score in zip(metric_names, score_list)]
          display(pd.DataFrame.from_records(records, columns=cols, index='Metric').T)
          plt.rcParams['figure.figsize'] = (7, 7)
          make_confusion_matrix(y_test_pass,pred_test,"Confusion Matrix for Test") 
    return score_list # returning the list with train and test scores

# define function to append metrics score in list
acc_train = []
acc_test = []
recall_train = []
recall_test = []
precision_train = []
precision_test = []
f1_train = []
f1_test = []

def add_score_model(score):
     '''add score of model to list'''
     acc_train.append(score[0])
     acc_test.append(score[1])
     recall_train.append(score[2])
     recall_test.append(score[3])
     precision_train.append(score[4])
     precision_test.append(score[5])
     f1_train.append(score[6])
     f1_test.append(score[7])

"""# **Decision Tree**"""

dtree=DecisionTreeClassifier(random_state=1, class_weight={0:0.20, 1:0.80})
dtree.fit(X_train,y_train)

dtree_score=get_metrics_score(dtree,X_train,X_test,y_train,y_test)
add_score_model(dtree_score)

"""# **Tuning Decision Tree**"""

#Choose the type of classifier. 
dtree_tuned = DecisionTreeClassifier(class_weight={0:0.20,1:0.80},random_state=1)

# Grid of parameters to choose from
parameters = {'max_depth': [1,4,7,15], 
              'min_samples_leaf': [2,3,5],
              'max_leaf_nodes' : [ 5,7,10,15]}

# Type of scoring used to compare parameter combinations
scorer = metrics.make_scorer(metrics.recall_score)

# Run the grid search
grid_obj = GridSearchCV(dtree_tuned, parameters, scoring=scorer,n_jobs=-1)
grid_obj=grid_obj.fit(X_train, y_train)

# Set the clf to the best combination of parameters
dtree_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data. 
dtree_tuned.fit(X_train, y_train)

score_tune_dt=get_metrics_score(dtree_tuned,X_train,X_test,y_train,y_test)
add_score_model(score_tune_dt) # add score to dataframe

# Feature importance
feature_importances_dt = pd.DataFrame(dtree_tuned.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance_dt']).sort_values('importance_dt',
                                                                        ascending=False)[:10]
                                    
plt.subplots(figsize=(17,6))
plt.title("Feature importances")
plt.bar(feature_importances_dt.index, feature_importances_dt['importance_dt'],
        color="pink",  align="center")
plt.xticks(feature_importances_dt.index, rotation = 85)
plt.show()

# ROC AUC Curve
y_preds_proba_dt = dtree_tuned.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_preds_proba_dt)
auc = metrics.roc_auc_score(y_test, y_preds_proba_dt)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)

"""# **Random Forest**"""

rf_estimator = RandomForestClassifier(random_state=1)
rf_estimator.fit(X_train,y_train)

score_list_rf=get_metrics_score(rf_estimator,X_train,X_test,y_train,y_test)
add_score_model(score_list_rf)

"""# **Tuning Random Forest**"""

rf_tuned = RandomForestClassifier(class_weight={0:0.20,1:0.80},random_state=1)

parameters = { "max_depth":[5,9,15],
               "n_estimators": [150,200,250,500],
               "min_samples_leaf": np.arange(5, 10),
                "max_features": ['auto'],
                "max_samples": np.arange(0.3,0.5, 0.7)
              }
# parameters = {"n_estimators": [50,80,150], 
#               "max_depth": [1,2,3], 
#               "min_samples_split": [3,4,6,7],"max_features": ['auto'],
#              }
# Type of scoring used to compare parameter combinations
scorer = metrics.make_scorer(metrics.recall_score)

# Run the grid search
grid_obj = GridSearchCV(rf_tuned, parameters, scoring=scorer,cv=5,n_jobs=-1)
grid_obj=grid_obj.fit(X_train, y_train)

# Set the clf to the best combination of parameters
rf_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data. 
rf_tuned.fit(X_train, y_train)

score_tune_rt=get_metrics_score(rf_tuned,X_train,X_test,y_train,y_test)
add_score_model(score_tune_rt)

# Feature importance
feature_importances_rf = pd.DataFrame(rf_tuned.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance_rf']).sort_values('importance_rf',
                                                                        ascending=False)[:10]
                                    
plt.subplots(figsize=(17,6))
plt.title("Feature importances")
plt.bar(feature_importances_rf.index, feature_importances_rf['importance_rf'],
        color="pink",  align="center")
plt.xticks(feature_importances_rf.index, rotation = 85)
plt.show()

# ROC AUC Curve
y_pred_proba_rf = rf_tuned.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba_rf)
auc = metrics.roc_auc_score(y_test, y_pred_proba_rf)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)

"""# **Gradient Boost**"""

gbc = GradientBoostingClassifier(random_state=1)
gbc.fit(X_train,y_train)

gbc_score=get_metrics_score(gbc,X_train,X_test,y_train,y_test)
add_score_model(gbc_score)

"""# **Tuning Gradient Boost**"""

# Choose the type of classifier. 
gbc_tuned = GradientBoostingClassifier(init=AdaBoostClassifier(random_state=1),random_state=1)

# Grid of parameters to choose from
## add from article
parameters = {
    "n_estimators": [100,150,200,250],
    "subsample":[0.8,0.9,1],
    "max_features":[0.7,0.8,0.9,1]
}

# Type of scoring used to compare parameter combinations
acc_scorer = metrics.make_scorer(metrics.recall_score)

# Run the grid search
grid_obj = GridSearchCV(gbc_tuned, parameters, scoring=acc_scorer,cv=5)
grid_obj=grid_obj.fit(X_train, y_train)

# Set the clf to the best combination of parameters
gbc_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data.
gbc_tuned.fit(X_train, y_train)

gbc_tuned_score=get_metrics_score(gbc_tuned,X_train,X_test,y_train,y_test)
add_score_model(gbc_tuned_score)

# Feature importance
feature_importances_gbc = pd.DataFrame(gbc_tuned.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance_gbc']).sort_values('importance_gbc',
                                                                        ascending=False)[:10]
                                    
plt.subplots(figsize=(17,6))
plt.title("Feature importances")
plt.bar(feature_importances_gbc.index, feature_importances_gbc['importance_gbc'],
        color="pink",  align="center")
plt.xticks(feature_importances_gbc.index, rotation = 85)
plt.show()

# ROC AUC Curve
y_pred_proba_gbc = gbc_tuned.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba_gbc)
auc = metrics.roc_auc_score(y_test, y_pred_proba_gbc)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)

"""# **XGBoost**"""

xgb = XGBClassifier(random_state=1,eval_metric='logloss')
xgb.fit(X_train,y_train)

xgb_score=get_metrics_score(xgb,X_train,X_test,y_train,y_test)
add_score_model(xgb_score)

"""# **Tuning XGBoost**"""

# Choose the type of classifier. 
xgb_tuned = XGBClassifier(random_state=1,eval_metric='logloss')

# Grid of parameters to choose from
## add from

parameters = {
    "n_estimators": np.arange(10,100,20),
    "scale_pos_weight":[0,5],
    "colsample_bylevel":[0.5,1],
    "learning_rate":[0.001,0.01,0.1,0.5]
}
# Type of scoring used to compare parameter combinations
acc_scorer = metrics.make_scorer(metrics.recall_score)

# Run the grid search
grid_obj = GridSearchCV(xgb_tuned, parameters,scoring=acc_scorer,cv=5,n_jobs=-1)
grid_obj=grid_obj.fit(X_train, y_train)

# Set the clf to the best combination of parameters
xgb_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data.
xgb_tuned.fit(X_train, y_train)

xgb_tuned_score=get_metrics_score(xgb_tuned,X_train,X_test,y_train,y_test)
add_score_model(xgb_tuned_score)

# Feature importance
feature_importances_xgb = pd.DataFrame(xgb_tuned.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance_xgb']).sort_values('importance_xgb',
                                                                        ascending=False)[:10]
                                    
plt.subplots(figsize=(17,6))
plt.title("Feature importances")
plt.bar(feature_importances_xgb.index, feature_importances_xgb['importance_xgb'],
        color="pink",  align="center")
plt.xticks(feature_importances_xgb.index, rotation = 85)
plt.show()

# ROC AUC Curve
y_pred_proba_xgb = xgb_tuned.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba_xgb)
auc = metrics.roc_auc_score(y_test, y_pred_proba_xgb)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)

"""# **Adaboost**"""

adaboost = AdaBoostClassifier(random_state=1)
adaboost.fit(X_train,y_train)

adaboost_score=get_metrics_score(adaboost,X_train,X_test,y_train,y_test)
add_score_model(adaboost_score)

"""# **Tuning Adaboost**"""

# Choose the type of classifier. 
abc_tuned = AdaBoostClassifier(random_state=1)

# Grid of parameters to choose from
## add from article
parameters = {
    #Let's try different max_depth for base_estimator
    "base_estimator":[DecisionTreeClassifier(max_depth=1),DecisionTreeClassifier(max_depth=2)],
    "n_estimators": np.arange(10,50,100),
    "learning_rate":np.arange(0.1,1,0.1)
}

# Type of scoring used to compare parameter combinations
acc_scorer = metrics.make_scorer(metrics.recall_score)

# Run the grid search
grid_obj = GridSearchCV(abc_tuned, parameters, scoring=acc_scorer,cv=5)
grid_obj=grid_obj.fit(X_train, y_train)

# Set the clf to the best combination of parameters
abc_tuned = grid_obj.best_estimator_

# Fit the best algorithm to the data.
abc_tuned.fit(X_train, y_train)

abc_tuned_score=get_metrics_score(abc_tuned,X_train,X_test,y_train,y_test)
add_score_model(abc_tuned_score)

# Feature importance
feature_importances_abc = pd.DataFrame(abc_tuned.feature_importances_,
                                   index = X_train.columns,
                                    columns=['importance_abc']).sort_values('importance_abc',
                                                                        ascending=False)[:10]
                                    
plt.subplots(figsize=(17,6))
plt.title("Feature importances")
plt.bar(feature_importances_abc.index, feature_importances_abc['importance_abc'],
        color="pink",  align="center")
plt.xticks(feature_importances_abc.index, rotation = 85)
plt.show()

# ROC AUC Curve
y_pred_proba_abc = abc_tuned.predict_proba(X_test)[::,1]
fpr, tpr, _ = metrics.roc_curve(y_test,  y_pred_proba_abc)
auc = metrics.roc_auc_score(y_test, y_pred_proba_abc)
plt.plot(fpr,tpr,label="data 1, auc="+str(auc))
plt.legend(loc=4)

# dataframe to compare all the models
comparison_frame = pd.DataFrame({'Model':['Decision Tree','Tuned Decision Tree',
                                          'Random Forest','Tuned Random Forest',
                                          'Gradient Boost','Tuned Gradient Boost',
                                          'XGboost','Tuned XGboost',
                                          'AdaBoost','Tuned AdaBoost',],
                                          'Train_Accuracy': acc_train,'Test_Accuracy': acc_test,
                                          'Train_Recall':recall_train,'Test_Recall':recall_test,
                                          'Train_Precision':precision_train,'Test_Precision':precision_test,
                                          'Train_F1':f1_train,'Test_F1':f1_test}) 
                                                       
                                
#Sorting models in decreasing order of test recall
comparison_frame.sort_values(by='Test_Recall',ascending=False)

# dump tuned XGBoost model
pickle.dump(df,open('df.pkl','wb'))
pickle.dump(grid_obj,open('Travel_tuned_XGBoost.pkl','wb'))

"""# **Conclusion**

1) Tuned XGBoost gives a more generalised model.

2) Most important features that have an impact on Product taken are Desgination, Passport,TierCity,Martialstatus,occupation.

3) Customers monthly income in range of 15000- 25000, and age range 15-30, prefer 5 star properties also have higher chances of taking new package based on EDA.

4) Customers with Designation as Executive should be the target customers for the company .Customers who have passport and are from tier 3 city and are single or unmarried, have large business such customers have higher chances of taking new package.

5) Company should help and promote customers to get a passport , as we see having a passport increases the chances of customer accepting a package.
"""