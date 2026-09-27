# Delivery boundaries / 交付边界

## Included in a typical customization

- Requirement clarification using synthetic or sanitized examples
- Field mapping, labels, business rules, output format, and visual branding
- Automated tests for agreed workflows and edge cases
- Deployment instructions and one documented acceptance flow

## Quoted separately

- Authentication, roles, audit logs, database retention, multi-tenant isolation
- Live Shopify/WooCommerce/ERP integrations and historical data migration
- Production monitoring, backups, high availability, ongoing hosting, or SLA
- Paid model/API usage and provider-specific compliance work
- Windows packaging, native mobile apps, OCR, or platform automation

## Not offered

- Bypassing login, paywalls, rate limits, store controls, or platform risk systems
- Unsolicited bulk messaging or automated replies without human oversight
- Processing data without the owner's permission
- Guarantees of model accuracy, conversion lift, platform penalty avoidance, or factual correctness

Client data must be minimized and sanitized before testing. Secrets belong in environment variables or a secret manager, never source control.
