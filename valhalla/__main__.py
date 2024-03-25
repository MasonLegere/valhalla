import pulumi
import pulumi_aws as aws
from valhalla.lib.config import stack_config
from pulumi import Input
from typing import Any, Mapping
from dynaconf import Dynaconf


class ValheimEcs(pulumi.ComponentResource):
    def __init__(
        self, name: str, config: Dynaconf, opts: pulumi.ResourceOptions = None
    ):
        super().__init__("custom:resource:ValheimEcs", name, {}, opts)
        self.config = config

        self.vpc = self.create_vpc()
        self.igw = self.create_igw(self.vpc)

    def create_vpc(self) -> aws.ec2.Vpc:
        return aws.ec2.Vpc(
            f"{self.config['vpc']['name']}-vpc",
            cidr_block=self.config["vpc"]["cidr_block"],
            enable_dns_support=True,
            enable_dns_hostnames=True,
            tags={"Name": f"{self.config['vpc']['name']}-vpc"},
        )

    def create_igw(self, vpc: Input[aws.ec2.Vpc]) -> aws.ec2.InternetGateway:
        return aws.ec2.InternetGateway(
            f"{self.config['igw']['name']}-igw",
            vpc_id=vpc.id,
            tags={"Name": f"{self.config['igw']['name']}-igw"},
        )

    def create_efs(self) -> aws.efs.FileSystem:
        return aws.efs.FileSystem(
            f"{self.config['efs']['name']}-efs",
            tags={"Name": f"{self.config['efs']['name']}-efs"},
        )


valheim = ValheimEcs(
    name="valheim-ecs", config=stack_config(), opts=pulumi.ResourceOptions(parent=None)
)
