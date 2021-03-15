from random import choice, randint
from time import sleep

from flask import Flask, request
from flasgger import Swagger
from validate_docbr import CPF

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
    swagger = Swagger(app, config=swagger_config)

    @app.route('/check-cpf')
    def check_cpf():
        """Example endpoint returning a list of colors by palette
        This is using docstrings for specifications.
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

        if not 'cpf' in args:
            return 'Conteudo inválido', 403

        escolha = choice(['delay', 'error', 'ok', 'ok_delay', 'delay_error'])

        if 'delay' in escolha:
            sleep(randint(1, 10))
        if 'error' in escolha:
            return 'Erro inesperado', 400

        return {'cpf-status': cpf.validate(args['cpf'])}, 200


    return app
