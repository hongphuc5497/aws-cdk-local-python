from aws_cdk import aws_sns as sns
import aws_cdk as cdk

import aws_cdk.assertions as assertions
from aws_cdk.assertions import Match

from aws_cdk_local_python.aws_cdk_local_python_stack import AwsCdkLocalPythonStack

def test_synthesizes_properly():
    app = cdk.App()

    # Build cross-stack references
    topics_stack = cdk.Stack(
        app, "TopicsStack",
    )
    topics = [sns.Topic(topics_stack, "Topic1")]

    state_machine_stack = AwsCdkLocalPythonStack(
        app,
        "AwsCdkLocalPythonStack",
        topics=topics,
    )

    # Prepare the stack for assesrtion
    template = assertions.Template.from_stack(state_machine_stack)

    # Assert that we have created the function with the correct properties
    template.has_resource_properties(
        "AWS::Lambda::Function",
        {
            "Handler": "start_state_machine.handler",
            "Runtime": "python3.12",
        }
    )

    # Assert that we have created a subscription
    template.resource_count_is("AWS::SNS::Subscription", 1)

    # Fully assert on the state machine's IAM role with matchers.
    EXPECTED_ROLE_PROPERTIES = {
      "AssumeRolePolicyDocument": {
        "Version": "2012-10-17",
        "Statement": [
          {
            "Action": "sts:AssumeRole",
            "Effect": "Allow",
            "Principal": {
              "Service": {
                "Fn::FindInMap": [
                  "ServiceprincipalMap",
                  {
                    "Ref": "AWS::Region"
                  },
                  "states"
                ]
              }
            }
          }
        ]
      }
    }
    template.has_resource_properties(
        "AWS::IAM::Role",
        Match.object_equals(EXPECTED_ROLE_PROPERTIES),
    )


