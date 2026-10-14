"""Imagens escolhidas na curadoria visual (prefixo de 8 caracteres do ImageID do Open Images V7).
Criterio: bovinos domesticos (sem bisao, bufalo, iaque, cabra) e tratores agricolas reais
(sem cortador de grama, brinquedo, retroescavadeira, colheitadeira, foto P&B ou propaganda)."""
VACA = """00474165 04ce0bea 141a89e2 14e28b8e 15ad1a8c 1ded8e6b 24ef2da7 2e8e1310 373eb7cd 37a8b481
3d20ed4e 40cb6009 45b88fb9 4a426770 4e30f758 4f217eee 57711acb 57f06d0f 58100247 6581250a
6c31d5bc 73aa6ef6 74aa413e 78b8edc8 79a5b161 7d41596d 82491249 86463a5a 9085b1c4 91a7534a
934acafa 9832abc7 a242bbc9 a4141375 a4e8f968 b0130d2e b39cbec4 b8e4ff43 bc7bdbdc cea42081
d18c57e2 d48b9940 d4a12f39 e03972d9 e14f9b3b e72baaba ec1ef7a1 f362d980 ff299d79 ffcfb20f
02f3bbf1 0c805afd 0dfb0cb5 0e200491 0ea8215d 1506e28a 177351a9 28c76d0a 450360d4 4c1b97ed""".split()
TRATOR = """0105f82e 072e5b5d 0c055a77 1149bf17 1989f64e 285aa5e5 391b1f3c 3984db3d 3d43ed0f 41549e4c
429ae2ce 42a6138a 45331ccb 494b3eb9 4e5f57bc 52636759 5b51a0ed 600570b9 690801e6 69412ecf
6ceb5e89 6fefdac8 70305da1 7443a59a 74af016e 7fa25536 835f2b52 8b3cbd18 8b995c1d 8cc8c96a
9157341c a670b767 a9295792 aea3c104 b60de56d b7342550 bc6619c5 c97ace44 d81f585f d9d4269b
e2627558 fde4c647 0a50550c 0ac4a16d 0e0821d9 1d11fa97 1eaa73d8 24ae035b 25cd6e7a 3533a590
37086150 5f39626e 6311a25c 657a2cba 66137ba6 694bda72 8a4fde65 8e8663af a79349c8 a9643bc2""".split()
assert len(VACA) == len(set(VACA)) == 60 and len(TRATOR) == len(set(TRATOR)) == 60
