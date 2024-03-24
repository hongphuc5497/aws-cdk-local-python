from typing import List
from aws_cdk import (
    Stack,
    aws_lambda as lambda_,
    aws_sns as sns,
    aws_sns_subscriptions as sns_subscriptions,
    aws_stepfunctions as sfn,
)
from constructs import Construct

class AwsCdkLocalPythonStack(Stack):

    def __init__(
        self,
        scope: Construct,
        construct_id: str,
        *,
        topics: List[sns.Topic],
        **kwargs
    ) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Step Functions
        state_machine = sfn.StateMachine(
            self,
            "StateMachine",
            definition_body=sfn.DefinitionBody.from_chainable(
                sfn.Chain.start(
                    sfn.Pass(
                        self, "StartState"
                    )
                )
            )
        )

        # Lambda
        func = lambda_.Function(
            self,
            "LambdaFunction",
            runtime=lambda_.Runtime.PYTHON_3_12,
            code=lambda_.Code.from_asset("lambda"),
            handler="start_state_machine.handler",
            environment={
                "STATE_MACHINE_ARN": state_machine.state_machine_arn,
            }
        )

        state_machine.grant_start_execution(func)

        # SNS
        subscription = sns_subscriptions.LambdaSubscription(func)
        for topic in topics:
            topic.add_subscription(subscription)
