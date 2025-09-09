import numpy as np


class RandomDistribution:
    def __init__(self, elements: list[int], values: list[int], /, even_distribution: bool = True):
        self.elements = np.array(elements)
        self.values = np.array(values)
        self.even_distribution = even_distribution
        self.first_sample_size = len(self.elements) // 2

    def generate(self):
        if len(self.elements) == 0:
            return [], []
        # Normalize the values to convert them into weights
        weights = self.values / self.values.sum()

        # Verify that the weights sum up to 1
        print("Weights:", weights)
        print("Sum of Weights:", weights.sum())
        print(f"first sample size = {self.first_sample_size}")

        # Draw the first sample of half the number of elements
        first_sample_indices = np.random.choice(
            len(self.elements),
            size=self.first_sample_size,
            replace=False,
            p=weights if self.even_distribution else None
        )
        first_sample = self.elements[first_sample_indices]

        # Remove the selected elements and their weights
        remaining_indices = np.setdiff1d(np.arange(len(self.elements)), first_sample_indices)
        remaining_elements = self.elements[remaining_indices]
        remaining_weights = None
        if self.even_distribution:
            remaining_weights = weights[remaining_indices]
            # Normalize remaining weights
            remaining_weights /= remaining_weights.sum()

        # Draw the second sample with the rest of elements
        second_sample_indices = np.random.choice(
            len(remaining_elements),
            size=len(remaining_elements),
            replace=False,
            p=remaining_weights if self.even_distribution else None
        )
        second_sample = remaining_elements[second_sample_indices]

        # Print results
        print("First Sample:", first_sample)
        print("Second Sample:", second_sample)

        return first_sample, second_sample
