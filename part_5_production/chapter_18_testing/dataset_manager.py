# From: AI Agents Book, Chapter 18, Section 18.4
# File: dataset_manager.py
# Description: Manage test datasets - load, validate, filter, and analyze

import json
from pathlib import Path
from datetime import datetime
from collections import Counter


class TestDataset:
    """Manage a test dataset for agent evaluation."""
    
    def __init__(self, path: str | None = None):
        """
        Initialize dataset, optionally loading from a file.
        
        Args:
            path: Path to JSON dataset file
        """
        self.cases = []
        self.metadata = {
            "dataset_version": "1.0",
            "created": datetime.now().isoformat(),
            "description": ""
        }
        
        if path:
            self.load(path)
    
    def load(self, path: str) -> None:
        """Load dataset from JSON file."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.metadata = {k: v for k, v in data.items() if k != 'cases'}
        self.cases = data.get('cases', [])
        
        print(f"Loaded {len(self.cases)} cases from {path}")
    
    def save(self, path: str) -> None:
        """Save dataset to JSON file."""
        data = {**self.metadata, "cases": self.cases}
        
        with open(path, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Saved {len(self.cases)} cases to {path}")
    
    def add_case(self, case: dict) -> None:
        """Add a single test case."""
        # Ensure required fields
        required = ['id', 'query']
        for field in required:
            if field not in case:
                raise ValueError(f"Case missing required field: {field}")
        
        # Check for duplicate IDs
        existing_ids = {c['id'] for c in self.cases}
        if case['id'] in existing_ids:
            raise ValueError(f"Duplicate case ID: {case['id']}")
        
        self.cases.append(case)
    
    def get_case(self, case_id: str) -> dict | None:
        """Get a case by ID."""
        for case in self.cases:
            if case['id'] == case_id:
                return case
        return None
    
    def filter(
        self,
        category: str | None = None,
        difficulty: str | None = None,
        source: str | None = None,
        tags: list[str] | None = None
    ) -> list[dict]:
        """
        Filter cases by criteria.
        
        Args:
            category: Filter by category
            difficulty: Filter by difficulty (easy, medium, hard)
            source: Filter by source (golden, real_user, synthetic, adversarial)
            tags: Filter by tags (case must have ALL specified tags)
        
        Returns:
            List of matching cases
        """
        results = self.cases
        
        if category:
            results = [c for c in results if c.get('category') == category]
        
        if difficulty:
            results = [c for c in results if c.get('difficulty') == difficulty]
        
        if source:
            results = [c for c in results if c.get('source') == source]
        
        if tags:
            results = [c for c in results 
                      if all(t in c.get('tags', []) for t in tags)]
        
        return results
    
    def get_statistics(self) -> dict:
        """Get dataset statistics."""
        stats = {
            "total_cases": len(self.cases),
            "by_category": Counter(c.get('category', 'unknown') for c in self.cases),
            "by_difficulty": Counter(c.get('difficulty', 'unknown') for c in self.cases),
            "by_source": Counter(c.get('source', 'unknown') for c in self.cases),
            "all_tags": Counter(tag for c in self.cases for tag in c.get('tags', []))
        }
        return stats
    
    def print_summary(self) -> None:
        """Print a summary of the dataset."""
        stats = self.get_statistics()
        
        print(f"\n{'='*50}")
        print(f"Dataset Summary")
        print(f"{'='*50}")
        print(f"Version: {self.metadata.get('dataset_version', 'unknown')}")
        print(f"Total Cases: {stats['total_cases']}")
        
        print(f"\nBy Category:")
        for cat, count in stats['by_category'].most_common():
            print(f"  {cat}: {count}")
        
        print(f"\nBy Difficulty:")
        for diff, count in stats['by_difficulty'].most_common():
            print(f"  {diff}: {count}")
        
        print(f"\nBy Source:")
        for src, count in stats['by_source'].most_common():
            print(f"  {src}: {count}")
        
        print(f"\nTop Tags:")
        for tag, count in stats['all_tags'].most_common(5):
            print(f"  {tag}: {count}")
    
    def validate(self) -> list[str]:
        """
        Validate dataset integrity.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        ids_seen = set()
        
        for i, case in enumerate(self.cases):
            # Check required fields
            if 'id' not in case:
                errors.append(f"Case {i}: missing 'id' field")
            elif case['id'] in ids_seen:
                errors.append(f"Case {i}: duplicate id '{case['id']}'")
            else:
                ids_seen.add(case['id'])
            
            if 'query' not in case:
                errors.append(f"Case {case.get('id', i)}: missing 'query' field")
            
            # Check expected_response structure
            if 'expected_response' in case:
                exp = case['expected_response']
                if not isinstance(exp, dict):
                    errors.append(f"Case {case.get('id', i)}: 'expected_response' should be a dict")
        
        if errors:
            print(f"Validation found {len(errors)} errors")
        else:
            print("Dataset validation passed!")
        
        return errors
    
    def to_evaluation_cases(self) -> list[dict]:
        """
        Convert to format suitable for evaluation pipeline.
        
        Returns:
            List of cases formatted for EvaluationPipeline
        """
        eval_cases = []
        for case in self.cases:
            eval_case = {
                "id": case["id"],
                "question": case["query"],
                "expected_response": case.get("expected_response", {}).get("reference_answer"),
                "criteria": self._infer_criteria(case),
                "metadata": {
                    "category": case.get("category"),
                    "difficulty": case.get("difficulty"),
                    "source": case.get("source"),
                    "tags": case.get("tags", [])
                }
            }
            eval_cases.append(eval_case)
        return eval_cases
    
    def _infer_criteria(self, case: dict) -> list[str]:
        """Infer evaluation criteria from case properties."""
        criteria = ["accuracy", "helpfulness"]
        
        tags = case.get("tags", [])
        if "complaint" in tags:
            criteria.append("empathy")
        if "needs_clarification" in tags or "ambiguous" in tags:
            criteria.append("appropriateness")
        
        return criteria


# Example usage
if __name__ == "__main__":
    # Load the sample dataset
    dataset = TestDataset("sample_dataset.json")
    
    # Print summary
    dataset.print_summary()
    
    # Validate
    errors = dataset.validate()
    if errors:
        for error in errors:
            print(f"  - {error}")
    
    # Filter examples
    print("\n=== Adversarial Cases ===")
    adversarial = dataset.filter(source="adversarial")
    for case in adversarial:
        print(f"  {case['id']}: {case['query'][:50]}...")
    
    print("\n=== Easy Cases ===")
    easy = dataset.filter(difficulty="easy")
    for case in easy:
        print(f"  {case['id']}: {case['query'][:50]}...")
    
    # Convert to evaluation format
    print("\n=== First 3 as Evaluation Cases ===")
    eval_cases = dataset.to_evaluation_cases()[:3]
    for ec in eval_cases:
        print(f"  {ec['id']}: criteria={ec['criteria']}")
