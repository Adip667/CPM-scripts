# main.tf

# Configure the AWS provider
provider "aws" {
  region = "us-east-1"  
  access_key = "123"
  secret_key = "321"
}

# Configure the AWS IAM policies to be used by N2WS IAM role
resource "aws_iam_policy" "my_tf_example_n2ws_policy_1" {
  name = "my_tf_example_n2ws_policy_1"
  description = "IAM Policy for XXX nodes"
  tags = {name="my_tf_demo_n2ws"}
  path = "/"
  policy = file("aws_policy_permissions_Enterprise_BYOL_1.json")
}

resource "aws_iam_policy" "my_tf_example_n2ws_policy_2" {
  name = "my_tf_example_n2ws_policy_2"
  path = "/"
  tags = {name="my_tf_demo_n2ws"}
  policy = file("aws_policy_permissions_Enterprise_BYOL_2.json")
}

resource "aws_iam_policy" "my_tf_example_n2ws_policy_3" {
  name = "my_tf_example_n2ws_policy_3"
  path = "/"
  tags = {name="my_tf_demo_n2ws"}
  policy = file("aws_policy_permissions_Enterprise_BYOL_3.json")
}


# Configure the AWS IAM trust policy to be used by N2WS IAM role
data "aws_iam_policy_document" "example_trust_policy" {
  statement {
    actions = ["sts:AssumeRole"]
    principals {
      type        = "Service"
      identifiers = ["ec2.amazonaws.com"]
    }
  }
}

resource "aws_iam_role" "my_tf_example_iam_role" {
  name = "my_tf_example_iam_role"
  tags = {n2ws_demo=""}
  assume_role_policy = data.aws_iam_policy_document.example_trust_policy.json
  managed_policy_arns = [aws_iam_policy.my_tf_example_n2ws_policy_1.arn,aws_iam_policy.my_tf_example_n2ws_policy_2.arn,aws_iam_policy.my_tf_example_n2ws_policy_3.arn]
}

# Configure the AWS IAM instance profile for the role
resource "aws_iam_instance_profile" "my_instance_profile" {
  name = "${aws_iam_role.my_tf_example_iam_role.name}"
  role = "${aws_iam_role.my_tf_example_iam_role.name}"
}


# Create an N2WS instance with silent config
resource "aws_instance" "my_cpm_tf_testing" {
  ami           = "ami-0a066aa13e3d92643"  
  instance_type = "t3.medium"               
  vpc_security_group_ids =["sg-0338d9b641aa03a0e"]
  subnet_id="subnet-fe51b9df"
  key_name = "CPM_Virginia" 
  
  iam_instance_profile=aws_iam_instance_profile.my_instance_profile.name
  tags = {Name="my_tf_demo_n2ws"}
  
  # Add user data (to configure product)
  user_data =chomp(file("New_Deploy_SilentConfig.txt"))
}

# Output the public IP address of the created instance
output "instance_ip" {
  value = aws_instance.my_cpm_tf_testing.public_ip
}