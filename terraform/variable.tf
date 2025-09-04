variable "ami_id" {
  description = "The AMI ID for the EC2 instance"
  type        = string
  default     = "ami-02d26659fd82cf299" 
}

variable "instance_type" {
  description = "The type of instance to use"
  type        = string
  default     = "t2.micro"
}

variable "volume_size" {
  description = "The size of the root EBS volume in GB"
  type        = number
  default     = 20
  
}