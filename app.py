#!/usr/bin/env python3
import os

from aws_cdk import aws_sns as sns
import aws_cdk as cdk

from aws_cdk_local_python.aws_cdk_local_python_stack import AwsCdkLocalPythonStack

app = cdk.App()

topics_stack = cdk.Stack(
    app, "TopicsStack",
    env=cdk.Environment(
      account=os.getenv('CDK_DEFAULT_ACCOUNT'),
      region=os.getenv('CDK_DEFAULT_REGION')
    ),
)
topics = [sns.Topic(topics_stack, "Topic1")]

AwsCdkLocalPythonStack(
    app,
    "AwsCdkLocalPythonStack",
    topics=topics,
    env=cdk.Environment(
        account=os.getenv('CDK_DEFAULT_ACCOUNT'),
        region=os.getenv('CDK_DEFAULT_REGION')
    ),
)

app.synth()
