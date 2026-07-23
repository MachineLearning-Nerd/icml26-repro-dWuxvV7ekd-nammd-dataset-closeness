# Source audit

The ImageNet-variant study uses ResNet-50 features and sample size 150. The
confidence-margin study partitions ten class intervals around a reference gap
of 0.186 and also samples 150. The adversarial study uses a CIFAR-10 ResNet-18,
PGD perturbations `i/255`, reference `4/255`, and sample size 1,500. The claim
is a conjunction over all three studies.
