# DhimantAI

DhimantAI is an open education technology project for guided learning, Socratic tutoring, concept-gap diagnosis, assessment support, educator insights, and secure institution-controlled learning workflows for schools, colleges, coaching centres, and universities.

## Purpose

DhimantAI is designed to support learning without short-circuiting the learner's thinking process. The project focuses on guided reasoning, structured educational workflows, institution-owned content, assessment integrity, and transparent controls for students and educators.

## Core Areas

- Socratic tutoring and guided hints
- Concept-gap diagnosis
- Previous-year question practice
- Feynman-style teach-back workflows
- Debate and argumentation practice
- Guided media and co-watch learning
- Flash-card and recall workflows
- Study planning
- Educator and institution insights
- Secure institution-controlled content and permissions

## Security and Responsible Use

The public repository must not contain identifiable student information, confidential institution records, restricted examination material, passwords, private keys, authentication tokens, production secrets, or proprietary third-party material without permission.

Public examples and benchmarks should use synthetic, independently created, properly licensed, or otherwise public-safe data.

DhimantAI is intended to support educators and learners. It does not replace teachers, academic governance, institutional policy, or professional judgement.

## Open-Source Structure

The project includes reusable components for content validation, access control, assessment-integrity checks, secure logging, benchmark scenarios, benchmark metrics, tests, and developer workflows.

## Getting Started

Clone the repository:

```bash
git clone https://github.com/optficiallabs/DhimantAI.git
cd DhimantAI
```

Install in editable mode:

```bash
python -m pip install -e .
```

Run tests:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

## CLI

After installation, the `dhimantai` command provides public-safe reference utilities.

Scan learning content:

```bash
dhimantai validate-content examples/sample_learning_content.json
```

Evaluate a role/action/scope request:

```bash
dhimantai check-access student view_own_progress --scope self
```

Run the benchmark plumbing and report overall/per-category metrics:

```bash
dhimantai run-benchmark benchmarks/education_cybersecurity_cases.jsonl
```

The benchmark command currently uses a reference evaluator to verify loading, execution, and metric calculation. Future releases can plug in additional defensive evaluators without changing the benchmark format.

## Contributing

Please review `CONTRIBUTING.md`, `SECURITY.md`, and `CODE_OF_CONDUCT.md` before contributing.

## Licence

DhimantAI is released under the Apache License 2.0.

## Maintained By

Optficial Labs Pvt Ltd., Hyderabad, India

Website: https://optficial.ai/
