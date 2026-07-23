# Source audit

The judge names v1 Theorem 4. Its display omits an asymptotic qualifier, but
Appendix D.1 invokes Slutsky's theorem and convergence to a normal law. The v3
display was corrected to say “asymptotically bounded.” The paper's DCT
threshold is `epsilon + sigma_hat*z_(1-alpha)/sqrt(m)`. A permutation test is
not faithful for the composite null `NAMMD<=epsilon`; v3 explicitly notes this.
