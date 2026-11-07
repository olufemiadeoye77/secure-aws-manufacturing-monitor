\# Secure AWS Manufacturing Monitoring System



\## Project Overview



The \*\*Secure AWS Manufacturing Monitoring System\*\* is a practical cloud architecture and security portfolio project demonstrating how AWS services and Python automation can support the monitoring and validation of manufacturing production data.



The project uses synthetic manufacturing records inspired by industrial solvent extraction operations. It demonstrates a workflow in which production data is stored in Amazon S3, processed by AWS Lambda, and converted into a structured validation report.



It also explores cloud security through IAM permissions, CloudWatch execution logs, AWS CloudTrail auditing, security documentation, and evidence-based assessment.



This is an educational project. It does not connect to live industrial machinery, production control systems, or operational technology (OT) environments.



\## Project Objectives



\- Build a practical AWS-based manufacturing monitoring workflow.

\- Apply AWS Identity and Access Management (IAM) concepts.

\- Store manufacturing input data and processing reports in Amazon S3.

\- Use AWS Lambda for automated data processing.

\- Monitor execution through Amazon CloudWatch.

\- Audit relevant AWS activity using AWS CloudTrail.

\- Develop Python scripts for data validation and evidence sanitisation.

\- Document security findings, architecture decisions, and outstanding risks.

\- Demonstrate practical cloud architecture and security skills through a public GitHub portfolio.



\## Architecture and AWS Services



The project uses the following AWS services:



| Service | Project role |

|---|---|

| Amazon S3 | Stores synthetic manufacturing input data and validation reports. |

| AWS Lambda | Executes the manufacturing data processing workflow. |

| AWS IAM | Provides the Lambda execution identity and associated permissions. |

| Amazon CloudWatch | Captures Lambda execution logs and operational information. |

| AWS CloudTrail | Records relevant AWS management activity and S3 object-level events. |

| AWS Budgets | Supports cost awareness and budget monitoring. |



\### Processing workflow



1\. Synthetic manufacturing records are uploaded to an Amazon S3 input location.

2\. AWS Lambda retrieves the input data using its execution role.

3\. The processing logic evaluates manufacturing indicators against configured validation thresholds.

4\. The system generates a JSON validation report.

5\. The report is written to the designated S3 reports location.

6\. Amazon CloudWatch captures execution information.

7\. AWS CloudTrail provides an audit trail for relevant account and S3 activity.



The deployed AWS environment is in the `eu-north-1` region.



\## Manufacturing Data and Validation



The synthetic dataset includes the following indicators:



\- Timestamp

\- Production throughput (tonnes per day)

\- Residual oil percentage

\- Moisture percentage

\- Solvent consumption per tonne

\- Production status



The validation logic checks for conditions such as:



\- Residual oil above the configured threshold.

\- Zero production throughput.

\- Moisture above the configured threshold.

\- Solvent consumption above the configured threshold.

\- Invalid or out-of-range input values.



\### Recorded validation result



A representative processing run produced the following result:



| Metric | Result |

|---|---:|

| Records processed | 10 |

| Invalid records | 0 |

| Records flagged for review | 4 |

| Records without exceptions | 6 |



The review flags identify records requiring further operational attention. They should not automatically be interpreted as confirmed equipment failures or process incidents.



\## Cloud Security and Audit Evidence



Security is an important part of this project. The work includes both implementation and evidence-based assessment.



\### IAM



A dedicated Lambda execution role, `ManufacturingMonitorLambdaRole`, is used by the monitoring application.



The documented permission design separates application execution from administrative and audit responsibilities. The application role is intended to have only the access needed to retrieve manufacturing input and write validation reports.



The actual effectiveness of all IAM restrictions remains subject to further policy and trust-policy verification.



\### Amazon S3



S3 provides storage for manufacturing input data and generated reports.



The security assessment identifies the configuration areas requiring verification, including:



\- Block Public Access.

\- Bucket policy restrictions.

\- Encryption configuration.

\- Versioning.

\- Transport security.



\### Amazon CloudWatch



CloudWatch execution logs provide evidence of Lambda processing activity, including record counts, execution duration, and memory usage.



\### AWS CloudTrail



CloudTrail is used to investigate AWS activity, including S3 object-level operations.



The repository includes a sanitised public evidence summary showing two reviewed events:



\- `GetObject` for the manufacturing input.

\- `PutObject` for the generated validation report.



Both events were attributed to the Lambda execution role in the reviewed evidence.



The public summary excludes account identifiers, full resource ARNs, request IDs, source IP addresses, and raw log contents.



\*\*Important:\*\* The published events are evidence from the reviewed log files. They do not establish that every possible access event has been reviewed or that no other events occurred.



\### Security assessment



The assessment is documented in:



`docs/cloud-security-assessment.md`



It records observed evidence, limitations, outstanding verification work, and recommended security improvements.



The project is not presented as a completed security audit, penetration test, compliance certification, or production-ready deployment.



\## Repository Structure



```text

secure-aws-manufacturing-monitor/

│

├── architecture/

│   └── architecture.md

│

├── data/

│   ├── README.md

│   └── manufacturing\_records.csv

│

├── docs/

│   ├── cloud-security-assessment.md

│   └── security-plan.md

│

├── evidence/

│   └── public/

│       └── cloudtrail\_s3\_object\_events.json

│

├── results/

│   ├── validation\_report.json

│   └── validation\_report.txt

│

├── scripts/

│   ├── README.md

│   ├── create\_public\_cloudtrail\_evidence.py

│   └── validate\_manufacturing\_data.py

│

├── tests/

│   ├── README.md

│   └── test\_validate\_manufacturing\_data.py

│

├── .gitignore

└── README.md

```



Private raw CloudTrail files and the account-specific inspection utility are intentionally excluded from the public repository.



\## Running the Local Validation



The project includes a local Python validation script and automated tests.



\### Requirements



\- Python 3

\- pytest for running the automated tests



\### Run the validation script



From the repository root:



```bash

python scripts/validate\_manufacturing\_data.py

```



\### Run the automated tests



```bash

python -m pytest -v

```



The local validation script and automated tests demonstrate the data-validation logic. They should be distinguished from the separately deployed AWS Lambda workflow.



\## Security Principles



The project follows these security principles:



\- Least-privilege access.

\- Separation of application and administrative responsibilities.

\- Protection of credentials and sensitive information.

\- Restricted access to stored data.

\- Encryption and secure transport configuration.

\- Logging and auditability.

\- Input validation and automated testing.

\- Sanitisation of evidence before public release.

\- Cost awareness and controlled cloud resource usage.



\## Current Project Status



\*\*Implemented and documented\*\*



\- \[x] GitHub repository and project structure.

\- \[x] Synthetic manufacturing dataset.

\- \[x] Python manufacturing data validation.

\- \[x] Automated validation tests.

\- \[x] AWS S3 input and report storage.

\- \[x] AWS Lambda processing workflow.

\- \[x] Dedicated Lambda execution role.

\- \[x] CloudWatch execution logging.

\- \[x] CloudTrail audit trail and S3 object-level event collection.

\- \[x] Sanitised public CloudTrail evidence.

\- \[x] IAM security design documentation.

\- \[x] Evidence-based cloud security assessment.



\*\*Further hardening and verification\*\*



\- \[ ] Verify S3 Block Public Access and bucket policy configuration.

\- \[ ] Verify S3 encryption and versioning settings.

\- \[ ] Review the complete Lambda IAM trust policy and permissions.

\- \[ ] Validate CloudTrail log-file integrity.

\- \[ ] Review and assess the scope of CloudTrail data-event selectors.

\- \[ ] Perform controlled permitted-access and denied-access tests.

\- \[ ] Review monitoring and alerting coverage.

\- \[ ] Update the security assessment with new verification evidence.



The checklist distinguishes documented implementation from controls that still require independent verification.



\## Safety and Cost Considerations



This project is educational and is not production-ready industrial control software.



It uses synthetic data and does not connect to live machinery, production systems, or operational technology.



AWS resources may incur charges. Deployment and testing should be carried out with cost monitoring, budget awareness, and appropriate resource cleanup.



AWS Budgets notifications are monitoring aids and do not guarantee that spending will stop at a specified amount.



\## Future Development



Potential next stages include:



\- Stronger IAM and S3 security verification.

\- CloudTrail integrity validation.

\- Improved security monitoring and alerting.

\- Automated security evidence collection.

\- Cloud security posture assessment.

\- Future exploration of AI-assisted security analysis and anomaly investigation.



\## Skills Demonstrated



\- AWS cloud architecture.

\- AWS IAM and access-control design.

\- Amazon S3.

\- AWS Lambda.

\- Amazon CloudWatch.

\- AWS CloudTrail.

\- Python automation.

\- Manufacturing data validation.

\- Cloud security assessment.

\- Audit evidence handling.

\- Git and GitHub project development.



\## Author



Developed as a practical cloud architecture, automation, and security learning project focused on manufacturing monitoring use cases.

