"""
Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
SPDX-License-Identifier: MIT-0

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

# Python3 script
import boto3

profile = input("Enter AWS CLI profile name or leave blank if using instance profile: ")
if profile:
    # use CLI profile specified in input
    session = boto3.Session(profile_name=profile)
else:
    # use instance profile IAM role
    session = boto3.Session()

ec2 = session.client("ec2")
regions = ec2.describe_regions()

for region in regions['Regions']:
    region_name = region['RegionName']
    print(f"{region_name}:")
    athena = session.client("athena", region_name=region_name)
    workgroups = athena.list_work_groups()
    for workgroup in workgroups['WorkGroups']:
        prepared_statements = athena.list_prepared_statements(
            WorkGroup=workgroup['Name']
        )
        for statement in prepared_statements['PreparedStatements']:
            print(f"\t{workgroup['Name']}: {statement['StatementName']}")