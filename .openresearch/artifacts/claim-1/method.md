# Method

The main checker discharges the bound from `MMD²=a+b-2c`, `0<=a,b<=K`,
and `c>=0`, and checks the derivative with respect to `a+b` while MMD² is
fixed. It also evaluates 4,000 finite-support RBF cases. The independent
checker uses exact rational arithmetic on a delta kernel. The negative control
replaces `4K-a-b` with `2K-a-b`; opposite Dirac measures then divide by zero.
