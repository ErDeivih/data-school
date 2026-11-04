import numpy as np

# Proporciones por bin: la referencia fija los cortes, la actual se compara contra ella
ref = np.array([0.40, 0.30, 0.20, 0.10])
act = np.array([0.25, 0.30, 0.25, 0.20])

psi = ((act - ref) * np.log(act / ref)).sum()          # simetrizado: da igual el orden
kl_act_ref = (act * np.log(act / ref)).sum()           # KL(actual || referencia)
kl_ref_act = (ref * np.log(ref / act)).sum()           # KL(referencia || actual)

print(f"PSI           {psi:.4f}")     # -> 0.1510
print(f"KL(act||ref)  {kl_act_ref:.4f}")  # -> 0.0769
print(f"KL(ref||act)  {kl_ref_act:.4f}")  # -> 0.0741
