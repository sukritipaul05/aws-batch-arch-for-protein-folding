# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0

from attrs import define
from batchfold.batchfold_job import BatchFoldJob
from datetime import datetime
import logging


@define
class AlphaFold2Job(BatchFoldJob):
    """Define AlphaFold 2 Job"""

    job_definition_name: str = "AlphaFold2JobDefinition"
    target_id: str = datetime.now().strftime("%Y%m%d%s")
    fasta_s3_uri: str = ""
    msa_s3_uri: str = ""
    output_s3_uri: str = ""
    use_precomputed_msas: bool = True
    output_dir: str = "/tmp/alphafold2"
    data_dir: str = "/database"
    template_mmcif_dir: str = "pdb_mmcif/mmcif_files"
    bfd_database_path: str = (
        "bfd/bfd_metaclust_clu_complete_id30_c90_final_seq.sorted_opt"
    )
    mgnify_database_path: str = "mgnify/mgy_clusters_2018_12.fa"
    pdb70_database_path: str = "pdb70/pdb70"
    obsolete_pdbs_path: str = "pdb_mmcif/obsolete.dat"
    pdb_seqres_database_path: str = "pdb_seqres/pdb_seqres.txt"
    small_bfd_database_path: str = "small_bfd/bfd-first_non_consensus_sequences.fasta"
    uniclust30_database_path: str = "uniclust30/uniclust30_2018_08/uniclust30_2018_08"
    uniprot_database_path: str = "uniprot/uniprot.fasta"
    uniref90_database_path: str = "uniref90/uniref90.fasta"
    max_template_date: str = datetime.now().strftime("%Y-%m-%d")
    db_preset: str = "full_dbs"
    model_preset: str = "monomer_ptm"
    benchmark: bool = False
    run_relax: bool = True
    use_gpu_relax: bool = True
    num_multimer_predictions_per_model: int = 1

    def __attrs_post_init__(self) -> None:
        """Override default BatchFoldJob command"""

        download_string = f"aws s3 cp {self.fasta_s3_uri} {self.output_dir}/fasta/"
        if self.use_precomputed_msas:
            download_string += f" && aws s3 cp --recursive {self.msa_s3_uri}/jackhmmer/ {self.output_dir}/{self.target_id}/msas/"

        command_list = [
            "/app/run_alphafold.sh",
            f"--data_dir={self.data_dir}",
            f"--output_dir={self.output_dir}",
            f"--fasta_paths=/tmp/alphafold2/fasta/{self.target_id}.fasta",
            f"--template_mmcif_dir={self.data_dir}/{self.template_mmcif_dir}",
            f"--obsolete_pdbs_path={self.data_dir}/{self.obsolete_pdbs_path}",
            f"--uniref90_database_path={self.data_dir}/{self.uniref90_database_path}",
            f"--mgnify_database_path={self.data_dir}/{self.mgnify_database_path}",
            f"--db_preset={self.db_preset}",
            f"--max_template_date={self.max_template_date}",
            f"--model_preset={self.model_preset}",
            f"--use_precomputed_msas={self.use_precomputed_msas}",
            f"--benchmark={self.benchmark}",
            f"--run_relax={self.run_relax}",
            f"--use_gpu_relax={self.use_gpu_relax}",
        ]

        if self.db_preset == "full_dbs":
            command_list.extend(
                [
                    f"--bfd_database_path={self.data_dir}/{self.bfd_database_path}",
                    f"--uniclust30_database_path={self.data_dir}/{self.uniclust30_database_path}",
                ]
            )
        elif self.db_preset == "reduced_dbs":
            command_list.extend(
                [
                    f"--small_bfd_database_path={self.data_dir}/{self.small_bfd_database_path}"
                ]
            )
        else:
            raise ValueError(
                "db_preset value must be either 'full_dbs' or 'reduced_dbs'"
            )

        if self.model_preset == "multimer":
            command_list.extend(
                [
                    f"--pdb_seqres_database_path {self.data_dir}/{self.pdb_seqres_database_path}",
                    f"--uniprot_database_path {self.data_dir}/{self.uniprot_database_path}",
                    f"--num_multimer_predictions_per_model={self.num_multimer_predictions_per_model}",
                ]
            )
        else:
            command_list.extend(
                [f"--pdb70_database_path {self.data_dir}/{self.pdb70_database_path}"]
            )

        upload_string = f'aws s3 cp {self.output_dir}/{self.target_id}/ {self.output_s3_uri} --recursive --exclude "*.a3m" --exclude "*.sto" --exclude "*.hhr" '

        command_string = (
            download_string + " && " + " ".join(command_list) + " && " + upload_string
        )
        logging.info(f"Command is \n{command_string}")
        self.container_overrides["command"] = [command_string]

        return None
