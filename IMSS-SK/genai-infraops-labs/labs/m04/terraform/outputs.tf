output "infrastructure_model_file" {
  description = "Path to the generated local infrastructure model."
  value       = local_file.infrastructure_model.filename
}

output "infrastructure_model" {
  description = "Infrastructure definitions modeled for local review."
  value       = local.model
}
