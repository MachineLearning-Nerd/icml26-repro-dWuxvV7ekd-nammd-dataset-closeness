# Method

For each `m=4..8` and each ordered pair of Bernoulli parameters on the interior
0.05 grid, epsilon is set to the exact population NAMMD, placing the
distribution on the least-favourable null boundary. The paper/official-code
statistic and variance formula are ported directly. All `2^(2m)` ordered sample
pairs are aggregated by their exact sufficient cells and weighted by their
Bernoulli probabilities. A second implementation brute-forces every sequence
for the strongest candidate.

The triangular kernel is nonnegative, bounded, shift-invariant, and positive
definite; on the binary support its Gram matrix equals the delta kernel.
