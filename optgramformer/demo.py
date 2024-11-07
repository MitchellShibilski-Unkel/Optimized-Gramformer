from optgramformer import Gramformer
import torch

def set_seed(seed):
  torch.manual_seed(seed)
  if torch.cuda.is_available():
    torch.cuda.manual_seed_all(seed)

set_seed(1212)


gf = Gramformer(device="cpu") # 1=corrector, 2=detector

influent_sentences = [
    "Matt like fish",
    "the collection of letters was original used the ancient Romans",
    "We enjoys horror movies",
    "Anna and Mike is going skiing",
    "I walk to the store and I bought milk",
    "We all eat the fish and then made dessert",
    "I will eat fish for dinner and drank milk",
    "what be the reason for everyone leave the company",
]   

corrected_sentences = [gf.correct(si, max_candidates=1) for si in influent_sentences]
print(corrected_sentences)