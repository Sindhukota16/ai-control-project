# Practice Terraform file. Nothing here is ever deployed.
# In later steps the agent will be asked to fix or change this file.

resource "aws_iam_policy" "app_read_only" {
  name        = "app-read-only"
  description = "Lets the app read from one S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = ["s3:GetObject", "s3:ListBucket"]
        Resource = [
          "arn:aws:s3:::demo-app-bucket",
          "arn:aws:s3:::demo-app-bucket/*"
        ]
      }
    ]
  })
}
