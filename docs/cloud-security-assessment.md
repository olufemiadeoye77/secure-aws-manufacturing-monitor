# Cloud Security Assessment
## Secure AWS Manufacturing Monitoring System

**Assessment date:** 7 November 2026
**AWS Region:** `eu-north-1`
**Assessment type:** Evidence-based cloud security review
**Assessment status:** Partial — further verification required
**Project repository:** [secure-aws-manufacturing-monitor](https://github.com/olufemiadeoye77/secure-aws-manufacturing-monitor)

---

## 1. Executive Summary

This assessment reviews selected security controls and audit evidence for the Secure AWS Manufacturing Monitoring System deployed in AWS.

The review focuses on AWS CloudTrail activity, Amazon S3 object access, AWS Lambda execution identity, CloudWatch execution logs, and the handling of security evidence.

The available evidence demonstrates that:

- CloudTrail reported that the audit trail was actively logging.
- CloudTrail reported successful recent log-delivery attempts.
- Management events and S3 object-level data events were selected for recording.
- CloudTrail recorded an S3 `GetObject` event for the manufacturing input file.
- CloudTrail recorded an S3 `PutObject` event for the generated validation report.
- Both object operations were attributed to the `ManufacturingMonitorLambdaRole` assumed-role identity.
- Lambda execution logs corroborated the manufacturing-data processing and report-generation activity.
- A sanitised evidence summary was prepared for public GitHub publication while the original audit files were kept private.

The evidence provides a useful demonstration of cloud auditability and application-level traceability.

However, this is not a complete AWS security audit. Several important controls still require direct verification, including S3 public-access settings, bucket policy, encryption, versioning, IAM permissions, IAM trust policy, and CloudTrail log-integrity validation.

No AWS resource, IAM permission, bucket policy, CloudTrail selector, or encryption setting was changed as part of this assessment.

## 2. Scope and Methodology

The assessment considered the following areas:

1. CloudTrail logging status and delivery.
2. CloudTrail management-event and S3 data-event selectors.
3. S3 object-level access activity.
4. Lambda execution identity and CloudWatch logs.
5. S3 security configuration evidence.
6. IAM execution-role permissions and trust relationship.
7. CloudTrail log-integrity validation.
8. Security evidence sanitisation and publication practices.

The assessment uses evidence supplied from AWS Console, AWS CLI outputs, CloudWatch logs, downloaded CloudTrail records, and the project's local evidence files.

Findings are classified as:

- **Verified:** Directly supported by reviewed evidence.
- **Inferred:** A reasonable interpretation of multiple evidence sources.
- **Not verified:** Evidence was not available to establish the control's current state.
- **Recommendation:** A proposed improvement, not a claim that a change has been implemented.

## 3. Findings and Evidence

### 3.1 CloudTrail logging and delivery

**Status: Verified from supplied CLI output**

The reviewed CloudTrail status output reported:

- Trail logging status: `IsLogging = true`.
- Logging start time: 6 November 2026.
- Latest delivery time reported: 7 November 2026 at approximately 06:43 UTC.
- Latest delivery attempt succeeded: 7 November 2026 at approximately 05:43 UTC.
- Latest digest delivery time reported: 7 November 2026 at approximately 06:03 UTC.

**Assessment**

These results indicate that CloudTrail was reporting active logging and recent successful delivery activity at the time of the supplied status check.

Digest delivery is a positive audit-control indicator, but it does not by itself prove that the delivered log files have passed an integrity validation process.

**Recommendation**

Continue monitoring trail status and delivery. Perform CloudTrail log-file integrity validation and retain the validation output as review evidence.

### 3.2 CloudTrail event selectors

**Status: Verified from supplied event-selector output**

The reviewed configuration contained two advanced event selectors:

- A management-event selector recording events in the `Management` category.
- An S3 object data-event selector recording events in the `Data` category for resources of type `AWS::S3::Object`.

**Assessment**

The configuration demonstrates that both management activity and S3 object-level activity were selected for audit recording.

The S3 object selector, as supplied, did not include additional restrictions for specific resource ARNs or event names.

This suggests that the selector may record a broader set of S3 object data events than this manufacturing-monitoring application requires.

**Security and cost observation**

Broad S3 data-event selection can increase CloudTrail event volume and associated costs. It can also make security reviews more difficult by increasing the quantity of unrelated events.

**Recommendation**

Review whether the S3 data-event selector can be scoped to the required manufacturing bucket and relevant object operations. Any selector changes should be planned, cost-reviewed, authorised, and tested separately.

No selector changes were made during this assessment.

### 3.3 S3 object-level audit activity

**Status: Verified from reviewed CloudTrail records**

Two relevant S3 object events were extracted from the downloaded CloudTrail records.

| Event | Object | Identity | Result |
|---|---|---|---|
| `GetObject` | `manufacturing_records.csv` | `ManufacturingMonitorLambdaRole` | No error code or message recorded |
| `PutObject` | `reports/validation_report.json` | `ManufacturingMonitorLambdaRole` | No error code or message recorded |

Both events were recorded on 7 November 2026 at approximately 02:24:23 UTC in `eu-north-1`.

The records identify the caller as an assumed role associated with the Lambda execution role.

**Assessment**

The records provide direct evidence that CloudTrail captured the Lambda application's read of the manufacturing input object and write of the generated validation report.

No error code or error message was recorded in either extracted event.

The absence of an error field in these records is consistent with successful operations, although the complete application workflow is assessed using the additional CloudWatch evidence below.

**Limitation**

The reviewed extraction contained two matching object events. No `DeleteObject` event was present in that extraction.

This does not establish that no deletion occurred elsewhere or during another period. A wider, date-bounded review is required before drawing that conclusion.

### 3.4 Lambda execution identity and CloudWatch logs

**Status: Verified from supplied CloudWatch execution log**

The reviewed Lambda execution log showed:

- The manufacturing input object was retrieved.
- Ten records were processed.
- Zero records were classified as invalid.
- Four records were flagged for review.
- The validation report was uploaded to the reports location.
- Execution duration was approximately 444 milliseconds.
- Maximum memory used was approximately 96 MB, with 128 MB configured.

The log also contained the message:

`Found credentials in environment variables.`

**Assessment**

The message is consistent with Lambda receiving temporary execution-role credentials through its runtime environment. It is not, by itself, evidence that long-term credentials were exposed.

The CloudWatch activity is consistent with the CloudTrail `GetObject` and `PutObject` records at approximately the same time.

**Recommendation**

Continue using Lambda execution roles rather than embedding long-term AWS credentials in application code or configuration files. Review execution-role permissions and monitor Lambda errors, access-denied events, and unexpected execution activity.

### 3.5 S3 security configuration

**Status: Not verified**

The following configuration evidence was not available for this review:

- S3 Block Public Access settings at bucket level.
- Account-level S3 Block Public Access settings.
- Bucket policy and its effective permissions.
- Default encryption configuration.
- Encryption configuration of the relevant objects.
- Bucket versioning status.

**Assessment**

No conclusion can be made about the current state of these controls from the CloudTrail object-event records alone.

**Recommendations**

Obtain and retain read-only evidence of:

1. Account-level and bucket-level Block Public Access settings.
2. Bucket policy, including any public or cross-account access.
3. Default encryption and relevant object encryption settings.
4. Bucket versioning status.

The intended design should keep manufacturing data private, enforce appropriate encryption, and prevent unauthorised public access.

### 3.6 IAM execution-role permissions and trust policy

**Status: Partially verified**

The CloudTrail records identify `ManufacturingMonitorLambdaRole` as the assumed-role identity associated with the S3 read and write operations.

This confirms the identity attributed to the reviewed operations. It does not establish that the role's complete permissions are least-privilege.

The actual IAM permission policy and role trust policy were not available for this assessment.

**Recommendations**

Review and retain evidence of:

- The Lambda execution-role trust policy.
- Attached managed policies.
- Inline policies.
- Permissions boundaries, if applicable.
- S3 access restricted to the required bucket and object paths.
- CloudWatch logging permissions limited to the required log resources.
- Absence of unnecessary administrative or destructive permissions.

The role should have only the permissions required to retrieve manufacturing input data, write validation reports, and publish necessary execution logs.

### 3.7 CloudTrail log integrity

**Status: Not verified**

The supplied trail status showed digest delivery activity.

However, no completed output from `aws cloudtrail validate-logs` was reviewed.

**Assessment**

Digest delivery is not equivalent to successful log-file integrity validation.

**Recommendation**

Run the CloudTrail log-integrity validation process for a defined period and retain its output. Record any missing, altered, or unverifiable log files for investigation.

### 3.8 Security evidence handling and GitHub publication

**Status: Verified from local Git and push output**

A sanitised CloudTrail evidence file was prepared for public publication.

The published evidence contains:

- UTC event time.
- Event name.
- AWS Region.
- Generic object key.
- Identity type.
- Lambda role name.
- A result description based on the absence of error fields.

The public evidence excludes the account number, bucket name, request IDs, IP addresses, full identity ARN, and original CloudTrail source filenames.

The original compressed CloudTrail files and raw extracted event file were excluded through `.gitignore`.

The account-specific inspection script was not staged for publication.

The Git push output confirmed publication to the existing repository's `main` branch in commit `e83d435`.

**Assessment**

This demonstrates a useful separation between private source audit records and a reduced public evidence summary.

**Recommendation**

Continue reviewing all files before publication. Do not commit raw CloudTrail records, account-specific identifiers, credentials, access keys, private configuration, or unredacted audit data.

## 4. Findings Summary

| Area | Assessment status | Observation |
|---|---|---|
| CloudTrail logging | Verified | Trail reported active logging |
| CloudTrail delivery | Verified | Recent successful delivery attempt reported |
| Event selectors | Verified | Management and S3 object data events selected |
| S3 object activity | Verified | Input read and report write recorded |
| Lambda identity | Verified for observed events | Assumed execution role identified |
| CloudWatch execution | Verified | Processing and report generation recorded |
| S3 public-access block | Not verified | Configuration evidence required |
| Bucket policy | Not verified | Policy review required |
| S3 encryption | Not verified | Configuration evidence required |
| S3 versioning | Not verified | Configuration evidence required |
| IAM permissions | Not verified | Policy documents required |
| IAM trust policy | Not verified | Trust relationship required |
| CloudTrail integrity | Not verified | Validation output required |
| Evidence sanitisation | Verified from reviewed files | Reduced public evidence prepared |

## 5. Security and Cost Observations

The current event selector appears broader than the application's immediate S3 audit requirements.

Broad S3 data-event collection can create additional event volume and increase CloudTrail charges.

A scoped selector may reduce unnecessary collection while retaining visibility over the manufacturing input and validation-report objects.

Any optimisation should preserve the audit requirements and be tested before implementation.

## 6. Recommended Next Actions

The following actions are recommended, in priority order:

1. Verify S3 Block Public Access settings at account and bucket levels.
2. Review the S3 bucket policy for unintended public or cross-account access.
3. Verify S3 default encryption and object encryption.
4. Verify S3 bucket versioning.
5. Review the Lambda execution-role permissions and trust policy.
6. Assess whether the CloudTrail S3 data-event selector can be appropriately scoped.
7. Run CloudTrail log-file integrity validation and preserve the results.
8. Review `GetObject`, `PutObject`, and `DeleteObject` activity over a defined audit period.
9. Continue monthly evidence reviews and maintain a dated evidence record.

## 7. Overall Assessment Conclusion

The evidence reviewed demonstrates that the manufacturing-monitoring workflow has an operational audit trail covering the observed S3 input-read and validation-report-write operations.

CloudTrail records identify the Lambda execution role associated with these operations, while CloudWatch logs provide supporting evidence of data processing and report generation.

The project also demonstrates an important security practice: preserving original audit records privately while publishing a sanitised evidence summary for technical transparency.

Nevertheless, several foundational cloud security controls remain unverified. The available evidence is therefore insufficient to declare the AWS environment fully secure or fully compliant with a particular security standard.

The next review should prioritise S3 access controls, encryption, versioning, IAM policy validation, and CloudTrail integrity validation.

**Final assessment:** Positive evidence of audit logging and application traceability, with additional configuration verification required before a comprehensive security assurance conclusion can be made.

---

## Assessment limitations

This document reflects the evidence supplied and reviewed as of 7 November 2026. It is not a penetration test, formal compliance certification, independent third-party audit, or confirmation that every AWS resource configuration remains unchanged after the evidence was collected.
