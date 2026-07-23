# Method

The search samples 750,000 deterministic centered-Gaussian variance tuples.
All kernel norms, cross moments, MMD², NAMMD, and the asymptotic MMD influence
variance have closed forms. For each tuple, the largest integer no greater than
`C2` is tested after enforcing every theorem premise and `m>=C1`.

The independent checker does not reuse the product-moment formula. It
numerically integrates the influence function under both test Gaussians and
uses `math.erf` for the normal-CDF power difference.
