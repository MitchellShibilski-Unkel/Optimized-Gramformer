import gc


class Gramformer:
  def __init__(self, models: int = 1, use_gpu: bool = False):
    import torch
    import errant
    from transformers import AutoTokenizer
    from transformers import AutoModelForSeq2SeqLM
    from torch.quantization import quantize_dynamic
    #from lm_scorer.models.auto import AutoLMScorer as LMScorer
    
    self.annotator = errant.load('en')
    
    if use_gpu:
        device = "cuda"
    else:
        device = "cpu"
        
    #batch_size = 1    
    #self.scorer = LMScorer.from_pretrained("gpt2", device=device, batch_size=batch_size)    
    self.device = device
    correction_model_tag = "prithivida/grammar_error_correcter_v1"
    self.model_loaded = False

    if models == 1:
        self.correction_tokenizer = AutoTokenizer.from_pretrained(correction_model_tag, token=False)
        self.correction_model     = AutoModelForSeq2SeqLM.from_pretrained(correction_model_tag, token=False)
        if use_gpu:
          self.correction_model.to(device)
        else:
          self.correction_model = quantize_dynamic(self.correction_model.to(device), {torch.nn.Linear}, dtype=torch.qint8)  # Reduces the model's size to run faster
        self.model_loaded = True
        print("[Gramformer] :: Sucess :: Grammar Error Correction/Highlight Model Loaded...")
    elif models == 2:
        # TODO
        print("TO BE IMPLEMENTED!!!")

  def correct(self, input_sentence: str, max_candidates=1):
      if self.model_loaded == True:
        correction_prefix = "gec: "
        input_sentence = correction_prefix + input_sentence
        input_ids = self.correction_tokenizer.encode(input_sentence, return_tensors='pt')
        input_ids = input_ids.to(self.device)

        # top_k=50, top_p=0.95
        # Get predictions from the model to use to correct the grammar
        preds = self.correction_model.generate(
            input_ids,
            do_sample=True, 
            max_length=128, 
            num_beams=7,
            early_stopping=True,
            num_return_sequences=max_candidates)

        corrected = set()
        for pred in preds:  
          corrected.add(self.correction_tokenizer.decode(pred, skip_special_tokens=True).strip())
          
        # Free up RAM after the model has ran
        # Helps when running the model multiple times on lower end machines
        gc.collect()

        #corrected = list(corrected)
        #scores = self.scorer.sentence_score(corrected, log=True)
        #ranked_corrected = [(c,s) for c, s in zip(corrected, scores)]
        #ranked_corrected.sort(key = lambda x:x[1], reverse=True)
        return corrected
      else:
        return "Model is not loaded"

  def highlight(self, orig, cor):
      edits = self._get_edits(orig, cor)
      orig_tokens = orig.split()

      ignore_indexes = []

      for edit in edits:
          edit_type = edit[0]
          edit_str_start = edit[1]
          edit_spos = edit[2]
          edit_epos = edit[3]
          edit_str_end = edit[4]

          # if no_of_tokens(edit_str_start) > 1 ==> excluding the first token, mark all other tokens for deletion
          for i in range(edit_spos+1, edit_epos):
            ignore_indexes.append(i)

          if edit_str_start == "":
              if edit_spos - 1 >= 0:
                  new_edit_str = orig_tokens[edit_spos - 1]
                  edit_spos -= 1
              else:
                  new_edit_str = orig_tokens[edit_spos + 1]
                  edit_spos += 1
              if edit_type == "PUNCT":
                st = "<a type='" + edit_type + "' edit='" + \
                    edit_str_end + "'>" + new_edit_str + "</a>"
              else:
                st = "<a type='" + edit_type + "' edit='" + new_edit_str + \
                    " " + edit_str_end + "'>" + new_edit_str + "</a>"
              orig_tokens[edit_spos] = st
          elif edit_str_end == "":
            st = "<d type='" + edit_type + "' edit=''>" + edit_str_start + "</d>"
            orig_tokens[edit_spos] = st
          else:
            st = "<c type='" + edit_type + "' edit='" + \
                edit_str_end + "'>" + edit_str_start + "</c>"
            orig_tokens[edit_spos] = st

      for i in sorted(ignore_indexes, reverse=True):
        del(orig_tokens[i])

      return(" ".join(orig_tokens))

  def detect(self, input_sentence):
        # TO BE IMPLEMENTED
        pass

  def _get_edits(self, orig, cor):
        orig = self.annotator.parse(orig)
        cor = self.annotator.parse(cor)
        alignment = self.annotator.align(orig, cor)
        edits = self.annotator.merge(alignment)

        if len(edits) == 0:  
            return []

        edit_annotations = []
        for e in edits:
            e = self.annotator.classify(e)
            edit_annotations.append((e.type[2:], e.o_str, e.o_start, e.o_end,  e.c_str, e.c_start, e.c_end))
                
        if len(edit_annotations) > 0:
            return edit_annotations
        else:    
            return []

  def get_edits(self, orig, cor):
      return self._get_edits(orig, cor)
