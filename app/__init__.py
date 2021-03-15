from base64 import standard_b64decode
from random import choice, randint
from time import sleep

from flask import Flask, request
from flasgger import Swagger
from validate_docbr import CPF
from pytesseract import image_to_string
from PIL import Image

cpf = CPF()

swagger_config = {
    'headers': [
    ],
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,
            'model_filter': lambda tag: True,
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/'
}


def create_app():
    app = Flask(__name__)
    Swagger(app, config=swagger_config)

    @app.route('/document-to-text', methods=['POST'])
    def document_to_text():
        """Tira dados de cpf de imagem
        ---
        parameters:
        - name: image
          in: path
          type: string
          required: true
        - name: size
          in: path
          type: json
          required: true
        responses:
          200:
            description: Request de sucesso
          400:
            description: Erro inesperado
          403:
            description: Conteúdo inválido ou sem CPF
        """
        image = request.json.get('image', None)
        size = request.json.get('size', None)
        if image and size:
            return image_to_string(
                Image.frombytes(
                    'RGBA',
                    (size['x'], size['y']),
                    standard_b64decode(bytes(image, encoding='utf8'))
                )
            ), 200
        return 'Error', 400

    @app.route('/check-cpf')
    def check_cpf():
        """Validador de CPF.
        Aqui tudo pode acontecer.
        Seu request pode dar certo ou errado 50% de chances
        Seu request também pode ter delay ou não 50% de chances.
        ---
        parameters:
        - name: cpf
          in: query
          type: string
          required: true
        responses:
          200:
            description: Request de sucesso
          400:
            description: Erro inesperado
          403:
            description: Conteúdo inválido ou sem CPF
        """
        args = request.args

        if 'cpf' not in args:
            return 'Conteudo inválido', 403

        escolha = choice(['error', 'ok', 'ok_delay', 'delay_error'])

        if 'delay' in escolha:
            sleep(randint(1, 10))
        if 'error' in escolha:
            return 'Erro inesperado', 400

        return {'cpf-status': cpf.validate(args['cpf'])}, 200

    return app
