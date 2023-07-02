from flask import Flask, render_template, request, Response, jsonify
import DiaryEntry 
import AddUser 
import time

app = Flask(__name__)

@app.route('/')
def index():
  return render_template('index.html')


@app.route('/entry')
def process_entry():
    start = time.time()
    email = request.args.get('email')
    date = request.args.get('date')
    content = request.args.get('content')
    dates, emotion, sadness_curve, happiness_curve, anger_curve, anxiety_curve = DiaryEntry.main(email,content,date)
    
    if email and date and content:
        output = {
            "dates":dates,
            "emotion":emotion,
            "sadness_curve":sadness_curve,
            "happiness_curve":happiness_curve,
            "anger_curve":anger_curve,
            "anxiety_curve":anxiety_curve
        }
        end = time.time()
        print("The time of execution of above program is :",(end-start) * 10**3, "ms")
        return jsonify(output), 200
    else:
        return Response("Please provide email, date, and content parameters."), 400

@app.route('/user')
def add_user():
    email = request.args.get('email')
    date = request.args.get('date')
    name = request.args.get('name')
    AddUser.main(email,name,date)
    
    if email and date and name:
        entry = Response(f"User Added")
        return entry, 200
    else:
        return Response("Please provide email, date, and name parameters."), 400
if __name__ == '__main__':
  app.run(port=5000)
