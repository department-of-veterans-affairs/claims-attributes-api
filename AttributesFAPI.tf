terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.11"
    }
  }
}

data "aws_iam_role" "ecr" {
  name = "ecsTaskExecutionRole"
}

provider "aws" {
  profile = "default"
  region  = "us-east-1"
}

module "ecr" {
  source                 = "git::https://github.com/cloudposse/terraform-aws-ecr.git?ref=master"
  image_names            = toset(["attributes_fastapi"])
  principals_full_access = [data.aws_iam_role.ecr.arn]
}

