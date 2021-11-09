from aws_cdk import core as cdk
from aws_cdk import aws_lambda
from aws_cdk.core import Tags


class CdkLambdaMyLayers2Stack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # The code that defines your stack goes here

        layers_path = 'python'
        bundling = cdk.BundlingOptions(
            image=aws_lambda.Runtime.PYTHON_3_8.bundling_docker_image,
            command=[
                '/bin/bash',
                '-c',
                f"""
                pip install -r requirements.txt -t /asset-output/{layers_path} &&
                cp -au . /asset-output/{layers_path}
                """
            ]
        )

        code = aws_lambda.Code.from_asset(
            path='layers/base',
            bundling=bundling
        )

        base_layer = aws_lambda.LayerVersion(
            scope=self,
            id='BaseAppLayer',
            code=code
        )

        fn_base_app = aws_lambda.Function(
            scope=self,
            id='FunctionBaseApp',
            function_name='baseApp',
            description='base App Function with Layers',
            handler='base_app.handler',
            runtime=aws_lambda.Runtime.PYTHON_3_8,
            code=aws_lambda.Code.asset('src/lambda/base'),
            layers=[base_layer]
        )

        Tags.of(fn_base_app).add('AppName', 'Base')
        cdk.CfnOutput(
            scope=self,
            id='lambda_function_name',
            value=fn_base_app.function_name
        )
        cdk.CfnOutput(
            scope=self,
            id='lambda_function_arn',
            value=fn_base_app.function_arn
        )
