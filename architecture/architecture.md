# Secure AWS Manufacturing Monitoring Architecture

## 1. Purpose

This document describes the implemented architecture of an educational
AWS-based manufacturing monitoring and cloud security project.

The system uses synthetic manufacturing records to demonstrate data
validation, automated processing, cloud storage, audit logging, and
security assessment.

It does not connect to live industrial machinery, plant control networks,
or production systems.

## 2. Implemented Architecture

The deployed workflow uses the following components:

1. Synthetic manufacturing records are stored in Amazon S3.
2. AWS Lambda retrieves the input data using its execution role.
3. Python processing logic validates manufacturing indicators against
   configured thresholds.
4. Lambda generates a structured JSON validation report.
5. The report is stored in the designated S3 reports location.
6. Amazon CloudWatch captures Lambda execution logs.
7. AWS CloudTrail records relevant management and S3 object-level events.
8. Sanitised audit evidence and security findings are documented in GitHub.

The AWS deployment is located in the eu-north-1 region.

## 3. AWS Components and Responsibilities

| Component | Implemented responsibility |
|---|---|
| Amazon S3 | Stores synthetic input records and validation reports |
| AWS Lambda | Executes the manufacturing data-processing workflow |
| AWS IAM | Provides the Lambda execution identity and associated permissions |
| Amazon CloudWatch | Captures Lambda execution logs |
| AWS CloudTrail | Records management and selected S3 object-level activity |
| AWS Budgets | Supports cloud spending awareness and monitoring |
| Python | Performs data validation and evidence processing |
| GitHub | Stores source code, documentation, and sanitised evidence |

## 4. Processing Workflow

1. Manufacturing input records are uploaded to Amazon S3.
2. Lambda retrieves the input object.
3. Python validation logic checks required fields and configured thresholds.
4. The system identifies records requiring further review.
5. A JSON validation report is generated.
6. Lambda writes the report to the S3 reports location.
7. CloudWatch records execution information.
8. CloudTrail provides evidence of relevant AWS API activity.

A representative execution processed 10 records, identified
zero invalid records, and flagged four records for review.

## 5. IAM Roles and Access Boundaries

The application uses a dedicated Lambda execution role:

`ManufacturingMonitorLambdaRole`

The documented IAM design separates application execution,
administrative responsibilities, and audit review.

The Lambda role has documented S3 and CloudWatch logging permissions.

However, the complete effective IAM permissions, trust policy,
and all applicable policy boundaries have not yet been independently
verified.

The architecture therefore distinguishes the implemented execution
identity from the broader proposed separation-of-duties model.

## 6. Data Protection and Storage Security

The manufacturing S3 bucket was inspected on 7 November 2026.

The reviewed evidence established:

- All four bucket-level S3 Block Public Access settings enabled.
- AWS classified the inspected bucket policy as non-public.
- The bucket policy explicitly denies insecure transport.
- Default server-side encryption uses SSE-S3 (AES256).
- SSE-C encryption is blocked.
- S3 bucket versioning is enabled.

A historical version of the validation report was successfully retrieved
and parsed as valid JSON.

These findings apply to the inspected bucket configuration.
Account-level public-access settings and complete effective access
permissions remain subject to further verification.

## 7. Audit and Monitoring

AWS CloudTrail is configured to record management events and selected
S3 object-level data events.

Reviewed audit records include:

- GetObject for the manufacturing input file.
- PutObject for the generated validation report.

Both reviewed operations were attributed to the Lambda execution role.

Amazon CloudWatch provides execution logs supporting the processing
workflow.

CloudTrail log-file integrity validation has not yet been completed.
Alerting coverage also requires further review.

## 8. Security Evidence and Publication

The project maintains a distinction between private AWS audit records
and sanitised public evidence.

The public repository includes a reduced CloudTrail evidence summary.

Raw CloudTrail records, account-specific inspection utilities,
credentials, and sensitive AWS identifiers are excluded from
public publication.

The security assessment documents observed configurations,
verified findings, limitations, and recommended improvements.

## 9. Outstanding Verification

The following activities remain outstanding:

- Verify account-level S3 Block Public Access settings.
- Review the complete IAM execution-role trust policy.
- Establish effective IAM permissions and applicable policy boundaries.
- Perform controlled authorised-access and denied-access tests.
- Validate CloudTrail log-file integrity.
- Review the scope and cost implications of S3 data-event selectors.
- Review DeleteObject activity over a defined audit period.
- Design and test a restoration and disaster-recovery exercise for the project environment.
- Review security monitoring and alerting coverage.

These outstanding activities do not invalidate the demonstrated
application workflow or the security evidence already collected.

## 10. Scope and Limitations

This is an educational cloud architecture and security portfolio project.

It uses synthetic manufacturing records and is not production-ready
industrial control software.

The assessment is evidence-based and does not constitute a penetration
test, independent third-party audit, or formal compliance certification.

Controls are described according to their implementation and
verification status rather than assumed effectiveness.

## 11. Future Development

Potential improvements include:

- Stronger IAM permission verification.
- Automated security evidence collection.
- CloudTrail integrity validation.
- Improved security alerting.
- More comprehensive recovery testing.
- Future AI-assisted security analysis and anomaly investigation.
