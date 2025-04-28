from flask import Flask, request, jsonify
from PIL import Image
import io
import requests

app = Flask(__name__)

@app.route('/', methods=['POST'])
def analyze_image():
    try:
        data = {}
        
        # Tenta pegar JSON primeiro
        if request.is_json:
            data = request.get_json()
        else:
            # Se não for JSON, tenta pegar como form
            data = request.form.to_dict()

        if 'image_url' in data:
            image_url = data['image_url']
            response = requests.get(image_url)
            image = Image.open(io.BytesIO(response.content))
        elif 'image' in request.files:
            file = request.files['image']
            image = Image.open(io.BytesIO(file.read()))
        else:
            return jsonify({"erro": "Nenhuma imagem enviada."}), 400

        width, height = image.size

        if width > height:
            result = "Folha saudável (exemplo automático)"
        else:
            result = "Possível problema detectado"

        return jsonify({
            "resultado": result
        })
    
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=10000)
