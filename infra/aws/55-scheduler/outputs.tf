output "schedule_group_name" {
  value = aws_scheduler_schedule_group.this.name
}

output "schedules" {
  description = "EventBridge Scheduler names and ARNs"
  value = {
    for k, s in aws_scheduler_schedule.this : k => {
      name       = s.name
      group_name = s.group_name
      arn        = s.arn
    }
  }
}
