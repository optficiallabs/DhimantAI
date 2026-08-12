# Assessment Integrity Policy

DhimantAI uses explicit learning modes to separate normal learning support from restricted assessment workflows.

## Reference modes

- `guided_practice`: hints and worked examples are allowed; restricted answer keys are denied.
- `revision`: hints and worked examples are allowed; restricted answer keys are denied.
- `examination`: hints, worked examples, final answers before an attempt, and answer keys are denied.
- `teacher_review`: educator review can access the configured resources in this reference policy.

Unknown modes and unknown resource types fail closed.

The module is a reference implementation for testing, benchmark development, and policy discussion. Production deployments should connect these decisions to authenticated roles, institution policy, assessment state, audit records, and human oversight.

All repository examples must use synthetic or otherwise public-safe material rather than real restricted examination content.
