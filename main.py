import os
import sys
import json
# Flask
from flask import Flask, redirect, url_for, request, render_template, Response, jsonify, redirect, send_file


# Declare a flask app
app = Flask(__name__)

# Load model

def model_predict(left, right):

    print(f'left right')
    disp = process_image(left, right, model)

    cv2.imwrite('static/disp.png', disp)
    print('done')


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        s1 = json.dumps(request.json)
        data =json.loads(s1)
        img_l = base64_to_pil(data['left']) # Returns pillow image
        img_l = np.array(img_l)[:,:,:3]
        print(f'Left: {img_l.shape}')
        img_r = base64_to_pil(data['right']) # Returns pillow image
        img_r = np.array(img_r)[:,:,:3]
        print(f'Right: {img_r.shape}')
        cv2.imwrite('img_l.png', img_l)
        cv2.imwrite('img_r.png', img_r)
    
        # Make prediction
        disp = model_predict(img_l, img_r)

        # # Process your result for human
        # pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability
        # pred_class = decode_predictions(preds, top=1)   # ImageNet Decode

        # result = str(pred_class[0][0][1])               # Convert to string
        # result = result.replace('_', ' ').capitalize()
        
        # Serialize the result, you can add additional fields
        return jsonify({'image_url': 'static/disp.png'})
        #return send_file('disp.png', mimetype='image/png')
    return None


if __name__ == '__main__':
     app.run(port=5002, threaded=True)

