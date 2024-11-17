import numpy as np
from flask import Flask,request,jsonify,render_template
import pickle

app = Flask(__name__)
clust = pickle.load(open('clustering.pkl','rb'))
regr = pickle.load(open('predictor.pkl','rb'))
scaler = pickle.load(open('scaler1.pkl','rb'))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    form_data = request.form

    features = [
        "yummy", "convenient", "spicy", "fattening", "greasy", "fast",
        "cheap", "tasty", "expensive", "healthy", "disgusting",
        "Like", "Age" , "VisitFrequency", "Gender"
    ]

    data = []
    for feature in features:
        value = form_data.get(feature)
        try:
            
            if value in ['Yes', 'No']:
                value = 1 if value == 'Yes' else 0
                
            elif feature== 'Age':
                if int(value)>=17:
                    value = int(value)
                else:
                    raise ValueError("You must be at least 17 years old")
                
            elif feature == 'Like':
                if value == 'I hate it!-5':
                    value = 0
                elif value == '-4':
                    value = 1
                elif value == '-3':
                    value = 2
                elif value == '-2':
                    value = 3
                elif value == '-1':
                    value = 4
                elif value == 'I love it!+5':
                    value = 10
                elif 0 <= int(value) <= 4:  
                    value = int(value) + 5
                else:
                    raise ValueError("Invalid input for Like")
        
            elif feature == 'VisitFrequency':
                if value == 'Never':
                    value = 0
                elif value == 'Once a year':
                    value = 1
                elif value == 'Every three months':
                    value = 2
                elif value == 'Once a month':
                    value = 3
                elif value == 'Once a week':
                    value = 4
                elif value == 'More than once a week':
                    value = 5
                else:
                    raise ValueError("Invalid input for VisitFrequency")
            
            elif feature == 'Gender':
                if value == 'Female':
                    value = 0
                elif value == 'Male':
                    value = 1
                else:
                    raise ValueError("Invalid input for Gender. Please enter Male or Female")
        
            else:
                raise KeyError("Invalid feature encountered")
        
        except (ValueError, KeyError) as e:
            print(f"Exception occurred: {e}")
    
        data.append(value)

    data = np.array(data)
    data = data.reshape(1,-1)
    
    final = regr.predict(scaler.transform(data))
    
    output = final[0]
    
    return render_template('index.html',prediction_text = 'The predicted cluster is {}'.format(output))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    try:
        data = request.get_json()
        clust_pred = clust.predict(data)
        final = regr.predict(clust_pred)
    
        output = final[0]
        return jsonify({'prediction':output})
    except Exception as e:
        return jsonify({'error':str(e)})
    
if __name__=="__main__":
    app.run(debug=True)
    
