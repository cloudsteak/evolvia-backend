resource "aws_scheduler_schedule_group" "this" {
  name = local.group_name
}

resource "aws_scheduler_schedule" "this" {
  for_each = local.schedules

  name                         = each.value.name
  group_name                   = aws_scheduler_schedule_group.this.name
  schedule_expression          = "rate(${each.value.rate})"
  schedule_expression_timezone = "UTC"

  flexible_time_window {
    mode = "OFF"
  }

  target {
    arn      = local.lambda[each.value.function].qualified_arn
    role_arn = aws_iam_role.this[each.key].arn
  }
}

resource "aws_lambda_permission" "scheduler" {
  for_each = local.schedules

  statement_id  = "AllowScheduler-${each.key}"
  action        = "lambda:InvokeFunction"
  function_name = local.lambda[each.value.function].name
  qualifier     = "live"
  principal     = "scheduler.amazonaws.com"
  source_arn    = aws_scheduler_schedule.this[each.key].arn
}
