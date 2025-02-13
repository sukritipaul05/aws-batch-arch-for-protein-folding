# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from attrs import define
from batchfold.batchfold_job import BatchFoldJob
from datetime import datetime
import logging
import uuid

@define
class OmegaFoldJob(BatchFoldJob):
    """Define omegaFold Job"""
    input_file: str = ""
    output_dir: str = uuid.uuid4().hex
    fasta_s3_uri: str = ""
    output_s3_uri: str = ""
    job_definition_name: str = "OmegaFoldJobDefinition"
    weights_file: str = "/database/omegafold_params/model.pt"
    target_id: str = datetime.now().strftime("%Y%m%d%s")
    
    # OmegaFold command options
    allow_tf32: bool = True
    num_cycle: int = 10
    num_pseudo_msa: int = 15
    pseudo_msa_mask_rate: float = 0.12
    subbatch_size: int = 1000    

    def __attrs_post_init__(self) -> None:
        """Override default BatchFoldJob command"""
        command_list = [f"-i {self.fasta_s3_uri}:{self.output_dir}/fasta/{self.target_id}.fasta"]
        command_list.extend([f"-o {self.output_dir}/predictions/:{self.output_s3_uri}"])
        command_list.extend([
            "omegafold",
            f"{self.output_dir}/fasta/{self.target_id}.fasta",
            f"{self.output_dir}/predictions",
            f"--weights_file={self.weights_file}",
            f"--allow_tf32={self.allow_tf32}",
            f"--num_cycle={self.num_cycle}",
            f"--num_pseudo_msa={self.num_pseudo_msa}",
            f"--pseudo_msa_mask_rate={self.pseudo_msa_mask_rate}",
            f"--subbatch_size={self.subbatch_size}",            
        ])

        logging.info(f"Command is \n{command_list}")
        self.container_overrides["command"] = command_list

        return None
