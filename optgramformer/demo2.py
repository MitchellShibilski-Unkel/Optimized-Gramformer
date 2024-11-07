from optgramformer import Gramformer

gf = Gramformer(models=1, use_gpu=False) # 1=corrector, 2=detector

influent_sentence = "Matt like fish"

print(gf.correct(influent_sentence))
