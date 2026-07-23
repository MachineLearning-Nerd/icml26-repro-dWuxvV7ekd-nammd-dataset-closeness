# Method

Official code was inspected at SHA
`8aca5dc1ec3804ff3754b3cbc82076f8afde9219`. ImageNet data and generated
features are not included. CIFAR code requires a trained model path and uses
hard-coded CUDA calls in attack generation. Recreating semantically different
features or attacks would be a proxy. The checker therefore emits `BLOCKED`.
