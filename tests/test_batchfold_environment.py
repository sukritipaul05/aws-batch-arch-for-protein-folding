# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

import pytest
import boto3
from batchfold.batchfold_environment import BatchFoldEnvironment

@pytest.fixture()
def batch_environment():
    stack = BatchFoldEnvironment(boto_session = boto3.Session())
    return(stack)

def test_get_stack_outputs(batch_environment):
    outputs = batch_environment.get_stack_outputs()
    output_keys = list(outputs)
    assert "AlphaFold2JobDefinition" in output_keys
    assert "JackhmmerJobDefinition" in output_keys
    assert "OpenFoldJobDefinition" in output_keys
    assert "DownloadJobDefinition" in output_keys
    
    assert "CPUOnDemandJobQueue" in output_keys
    assert "CPUSpotJobQueue" in output_keys
    assert "G4dnJobQueue" in output_keys
    assert "GravitonOnDemandJobQueue" in output_keys
    assert "GravitonSpotJobQueue" in output_keys

    assert "JobDefinition" in outputs["AlphaFold2JobDefinition"]
    assert "JobQueue" in outputs["CPUOnDemandJobQueue"]
    assert "JobQueue" in outputs["G4dnJobQueue"]
    assert "batchfolds3bucket" in outputs["S3BucketName"]

def test_get_job_queue_names(batch_environment):
    job_queue_names = batch_environment.list_job_queue_names()
    assert "CPUOnDemandJobQueue" in job_queue_names
    assert "CPUSpotJobQueue" in job_queue_names
    assert "G4dnJobQueue" in job_queue_names
    assert "CPUOnDemandJobQueue" in job_queue_names
    assert "GravitonOnDemandJobQueue" in job_queue_names
    assert "GravitonSpotJobQueue" in job_queue_names

def test_get_job_definition_names(batch_environment):
    job_def_names = batch_environment.list_job_definition_names()
    assert "AlphaFold2JobDefinition" in job_def_names
    assert "DownloadJobDefinition" in job_def_names
    assert "OpenFoldJobDefinition" in job_def_names
    assert "JackhmmerJobDefinition" in job_def_names

def test_get_job_queue_objects(batch_environment):
    assert len(batch_environment.queues) == 5
    assert batch_environment.queues["CPUOnDemandJobQueue"].name == "CPUOnDemandJobQueue"

def test_get_default_bucket(batch_environment):
    assert "batchfolds3bucket" in batch_environment.default_bucket