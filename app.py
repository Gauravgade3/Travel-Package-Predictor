from flask import Flask, render_template, request
import pickle

app = Flask(__name__)  # creating the Flask class object

model = pickle.load(open('df.pkl', 'rb'))
model2 = pickle.load(open('XGBoost.pkl', 'rb'))



@app.route("/", methods=['GET', 'POST'])
# @cross_origin()
def home ():
    return render_template("home.html")

@app.route('/predict', methods=['POST'])
# @cross_origin()
def predict():
    if request.method == "POST":
        # Age = int(request.form['Age'])
        Age = request.form.get('Age', type=int)
        TypeofContact = int(request.form['TypeofContact'])
        if TypeofContact=='Self Enquiry':
            TypeofContact==1
        else:
            TypeofContact==0

        CityTier = int(request.form['CityTier'])
        DurationOfPitch = request.form.get('DurationOfPitch', type=int)
        Occupation = int(request.form['Occupation'])
        if Occupation == 'Salaried':
            Occupation == 2
        elif Occupation == 'Free Lancer':
            Occupation == 0
        elif Occupation == 'Small Business':
            Occupation == 3
        else:
            Occupation == 1
        Gender = int(request.form['Gender'])
        NumberOfPersonVisiting = int(request.form['NumberOfPersonVisiting'])
        NumberOfFollowups = int(request.form['NumberOfFollowups'])
        ProductPitched = int(request.form['ProductPitched'])
        if ProductPitched == 'Deluxe':
            ProductPitched == 1
        elif ProductPitched == 'Basic':
            ProductPitched == 0
        elif ProductPitched == 'Standard':
            ProductPitched == 3
        elif ProductPitched == 'Super Deluxe':
            ProductPitched == 4
        else:
            ProductPitched == 2
        PreferredPropertyStar = int(request.form['PreferredPropertyStar'])
        MaritalStatus = int(request.form['MaritalStatus'])
        if MaritalStatus == 'Single':
            MaritalStatus == 2
        elif MaritalStatus == 'Divorced':
            MaritalStatus == 0
        elif MaritalStatus == 'Married':
            MaritalStatus == 1
        else:
            MaritalStatus == 3
        NumberOfTrips = request.form.get('NumberOfTrips', type=int)
        Passport = int(request.form['Passport'])
        if Passport == 'Yes':
            Passport == 1
        else:
            Passport == 0
        PitchSatisfactionScore = int(request.form['PitchSatisfactionScore'])
        OwnCar = int(request.form['OwnCar'])
        if OwnCar == 'Yes':
            OwnCar == 1
        else:
            OwnCar == 0
        NumberOfChildrenVisiting = int(request.form['NumberOfChildrenVisiting'])
        Designation = int(request.form['Designation'])
        if Designation == 'Manager':
            Designation == 2
        elif Designation == 'Executive':
            Designation == 1
        elif Designation == 'Senior Manager':
            Designation == 3
        elif Designation == 'VP':
            Designation == 4
        else:
            Designation == 0
        MonthlyIncome = request.form.get('MonthlyIncome',type=int)

        value = model.predict([[Age, TypeofContact, CityTier, DurationOfPitch, Occupation, Gender, NumberOfPersonVisiting,
                                  NumberOfPersonVisiting, NumberOfFollowups, ProductPitched, PreferredPropertyStar,
                                  MaritalStatus, NumberOfTrips, Passport, PitchSatisfactionScore, OwnCar,
                                  NumberOfChildrenVisiting, Designation, MonthlyIncome]])

        prediction = model2.predict(value)

        if prediction == 0:
            label = 'not purchase'
        else:
            label = 'purchase'

    return render_template('result.html', prediction_text=" Hurray, Customer may {}".format(label))
if __name__ == '__main__':
    app.run(debug=True)
