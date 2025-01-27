resource "aws_apigatewayv2_route" "python_api_route" {
  api_id    = var.api_gateway_id
  route_key = "ANY /rag-api"
  target    = "integrations/${aws_apigatewayv2_integration.ec2_integration.id}"
}

# Create an HTTP Proxy integration for EC2
resource "aws_apigatewayv2_integration" "ec2_integration" {
  api_id           = var.api_gateway_id
  integration_type = "HTTP_PROXY"
  integration_uri  = "http://${aws_instance.python_app.public_ip}/"
  integration_method = "ANY"
}

# Deploy API Gateway changes
resource "aws_apigatewayv2_stage" "existing_stage" {
  api_id      = var.api_gateway_id
  name        = "v1"  # Reuse your existing stage
  auto_deploy = true
}

# Output API Gateway URL
output "api_gateway_url" {
  value = "https://${var.api_gateway_id}.execute-api.us-east-1.amazonaws.com/v1/rag-api"
}