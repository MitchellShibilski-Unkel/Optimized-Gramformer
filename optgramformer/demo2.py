from optgramformer import Gramformer

gf = Gramformer(device="cpu") # 1=corrector, 2=detector

influent_sentence = "Matt like fish"

print(gf.correct(influent_sentence))
