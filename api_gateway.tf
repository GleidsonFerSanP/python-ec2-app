resource "aws_apigatewayv2_route" "python_api_route_rag_query" {
  api_id    = var.api_gateway_id
  route_key = "POST /rag-api/query"
  target    = "integrations/${aws_apigatewayv2_integration.ec2_integration_rag_query.id}"
}
resource "aws_apigatewayv2_route" "python_api_route_rag_create_embeddings" {
  api_id    = var.api_gateway_id
  route_key = "POST /rag-api/embeddings"
  target    = "integrations/${aws_apigatewayv2_integration.ec2_integration_rag_create_embeddings.id}"
}
resource "aws_apigatewayv2_route" "python_api_route_rag_delete" {
  api_id    = var.api_gateway_id
  route_key = "DELETE /rag-api/embeddings"
  target    = "integrations/${aws_apigatewayv2_integration.ec2_integration_rag_delete.id}"
}

# Create an HTTP Proxy integration for EC2
resource "aws_apigatewayv2_integration" "ec2_integration_rag_query" {
  api_id           = var.api_gateway_id
  integration_type = "HTTP_PROXY"
  integration_uri  = "http://${aws_instance.python_app.public_ip}/rag-api/query"
  integration_method = "POST"
}
# Create an HTTP Proxy integration for EC2
resource "aws_apigatewayv2_integration" "ec2_integration_rag_create_embeddings" {
  api_id           = var.api_gateway_id
  integration_type = "HTTP_PROXY"
  integration_uri  = "http://${aws_instance.python_app.public_ip}/rag-api/embeddings"
  integration_method = "POST"
}
# Create an HTTP Proxy integration for EC2
resource "aws_apigatewayv2_integration" "ec2_integration_rag_delete" {
  api_id           = var.api_gateway_id
  integration_type = "HTTP_PROXY"
  integration_uri  = "http://${aws_instance.python_app.public_ip}/rag-api/embeddings"
  integration_method = "DELETE"
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