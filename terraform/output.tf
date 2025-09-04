output "aws_default_vpc_id" {
  value = aws_default_vpc.default.id
}

output "aws_security_group_id" {
  value = aws_security_group.my_sg.id
}

output "aws_instance_public_ip" {
  value = aws_instance.web_server.public_ip
}

output "aws_instance_public_dns" {
  value = aws_instance.web_server.public_dns
}

output "aws_instance_id" {
  value = aws_instance.web_server.id
}

output "aws_key_pair_name" {
  value = aws_key_pair.deployer_key.key_name
}

