resource "aws_apigatewayv2_api" "this" {
  name          = local.api_name
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = local.cors_allow_origins
    allow_methods = local.cors_allow_methods
    allow_headers = local.cors_allow_headers
    max_age       = 3600
  }
}

resource "aws_apigatewayv2_integration" "backend" {
  api_id                 = aws_apigatewayv2_api.this.id
  integration_type       = "AWS_PROXY"
  integration_uri        = local.backend.qualified_arn
  integration_method     = "POST"
  payload_format_version = "2.0"
}

resource "aws_apigatewayv2_authorizer" "api_key" {
  api_id                            = aws_apigatewayv2_api.this.id
  authorizer_type                   = "REQUEST"
  authorizer_uri                    = local.authorizer.invoke_arn
  identity_sources                  = ["$request.header.x-api-key"]
  name                              = "${local.prefix}-authorizer"
  authorizer_payload_format_version = "2.0"
  enable_simple_responses           = true
  authorizer_result_ttl_in_seconds  = 60
}

resource "aws_lambda_permission" "authorizer" {
  statement_id  = "AllowAPIGatewayAuthorizer"
  action        = "lambda:InvokeFunction"
  function_name = local.authorizer.name
  qualifier     = "live"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.this.execution_arn}/authorizers/${aws_apigatewayv2_authorizer.api_key.id}"
}

resource "aws_apigatewayv2_route" "this" {
  for_each = local.routes

  api_id             = aws_apigatewayv2_api.this.id
  route_key          = each.value.key
  target             = "integrations/${aws_apigatewayv2_integration.backend.id}"
  authorization_type = each.value.auth ? "CUSTOM" : "NONE"
  authorizer_id      = each.value.auth ? aws_apigatewayv2_authorizer.api_key.id : null
}

resource "aws_apigatewayv2_stage" "this" {
  api_id      = aws_apigatewayv2_api.this.id
  name        = local.stage_name
  auto_deploy = true

  default_route_settings {
    throttling_rate_limit  = local.throttle_rate
    throttling_burst_limit = local.throttle_burst
  }

  # $default törlése előtt kell a live + a domain mapping átállítása
  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_lambda_permission" "api" {
  statement_id  = "AllowAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = local.backend.name
  qualifier     = "live"
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.this.execution_arn}/*/*"
}

resource "aws_apigatewayv2_api_mapping" "this" {
  api_id      = aws_apigatewayv2_api.this.id
  domain_name = local.domain
  stage       = aws_apigatewayv2_stage.this.name
}
