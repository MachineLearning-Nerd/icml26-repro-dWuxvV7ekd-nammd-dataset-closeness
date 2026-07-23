# Method

The verifier evaluates the displayed sufficient bound on 41 logarithmically
spaced positive gaps, tests the exact `m*gap²` invariant, and regresses
`log(m)` on `log(gap)`. The independent checker uses a different 73-point grid
and SciPy regression. Replacing the inverse-square by inverse-linear is the
negative control and must produce slope -1.
