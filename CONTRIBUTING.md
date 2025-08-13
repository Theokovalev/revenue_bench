# Contributing to Revenue Bench

We welcome contributions to Revenue Bench! This guide will help you get started.

## Ways to Contribute

### 1. Add New Models

Test additional models by:
1. Adding them to `config.yaml`
2. Running evaluation: `python run_evaluation.py --model your-model`
3. Submitting results via PR

### 2. Improve the Benchmark

- Add new evaluation tasks
- Enhance scoring methodology
- Improve verification system
- Add new judge models

### 3. Documentation

- Fix typos or clarify instructions
- Add examples and tutorials
- Translate documentation

### 4. Report Issues

Found a bug or have a suggestion?
- Open an issue on GitHub
- Include model name and error details
- Provide reproduction steps

## Development Setup

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/your-username/revenue-bench.git
   cd revenue-bench
   ```

3. Create a branch:
   ```bash
   git checkout -b feature/your-feature-name
   ```

4. Make your changes and test:
   ```bash
   python test_structure.py
   python run_evaluation.py --list-models
   ```

5. Commit with clear messages:
   ```bash
   git commit -m "Add: New feature description"
   ```

6. Push and create PR:
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Python 3.9+ compatible
- Follow PEP 8 guidelines
- Add docstrings to functions
- Keep code clean and readable

## Testing

Before submitting:
1. Run `test_structure.py` to verify files
2. Test with at least one model
3. Ensure no API keys in code
4. Update documentation if needed

## Pull Request Guidelines

- One feature per PR
- Clear PR title and description
- Link related issues
- Include test results
- Update CHANGELOG if applicable

## Adding a New Task

To add a new evaluation task:

1. Create task file in `benchmark/tasks/`
2. Add prompt in `benchmark/tasks/prompts/`
3. Implement scoring logic
4. Add documentation
5. Test with multiple models

Example structure:
```python
from inspect_ai import Task, task
from inspect_ai.dataset import Sample

@task
def your_task_name():
    """Your task description"""
    # Implementation
```

## Adding a New Judge

To add a new judge model:

1. Update `config.yaml` with model name
2. Test compatibility with scorer
3. Verify cost estimates
4. Document performance

## Community

- Join discussions in Issues
- Share your results and insights
- Help others with setup problems
- Suggest improvements

## License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT).

## Questions?

- Check existing issues first
- Open a new issue with [Question] tag
- Be specific and provide context

Thank you for contributing to Revenue Bench! 🚀