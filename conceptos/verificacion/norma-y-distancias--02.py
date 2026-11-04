import numpy as np

# Dos variables con varianza 1 y correlacion 0,9: covarianza escrita a mano.
S = np.array([[1.0, 0.9], [0.9, 1.0]])
S_inv = np.linalg.inv(S)
dif = np.array([[1.0, 0.0], [0.0, 1.0], [1.0, 1.0]])   # diferencias respecto al origen

euclidea = np.linalg.norm(dif, axis=1)
maha = np.sqrt(np.einsum("ij,jk,ik->i", dif, S_inv, dif))

print("S inversa:", np.round(S_inv, 4).tolist())      # -> [[5.2632, -4.7368], [-4.7368, 5.2632]]
print("euclidea :", np.round(euclidea, 3).tolist())   # -> [1.0, 1.0, 1.414]
print("Mahalanobis:", np.round(maha, 3).tolist())     # -> [2.294, 2.294, 1.026]
print("mas cercano euclidea:", int(np.argmin(euclidea)))       # -> 0
print("mas cercano Mahalanobis:", int(np.argmin(maha)))        # -> 2
