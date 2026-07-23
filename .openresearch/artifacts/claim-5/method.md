# Method

Official code SHA `8aca5dc1ec3804ff3754b3cbc82076f8afde9219` was audited.
It references absent `HIGGS_TST.pckl`, `Fake_MNIST_data_EP100_N10000.pckl`,
`cifar10_X_adversarial.npy`, and local torchvision datasets. The scripts also
default to CUDA, which this CPU-only campaign cannot use. Blob and HDGM alone
cannot satisfy the five-dataset quantifier, so no partial subset is promoted.
