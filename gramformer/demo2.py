from gramformer import Gramformer

gf = Gramformer(models = 1, use_gpu=True) # 1=corrector, 2=detector

influent_sentence = "Matt like fish"

print(gf.correct(influent_sentence))
