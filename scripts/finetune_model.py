from datasets import load_dataset
from transformers import (
    DistilBertTokenizerFast,
    DistilBertForSequenceClassification,
    Trainer,
    TrainingArguments,
)


BASE_MODEL_NAME = "distilbert-base-uncased"
FINETUNED_MODEL_NAME = "distilbert-finetuned"
DATASET_NAME = "imdb"
DEVICE = "cuda"

dataset = load_dataset(DATASET_NAME)
tokenizer = DistilBertTokenizerFast.from_pretrained(BASE_MODEL_NAME)
dataset = dataset.map(
    lambda batch: tokenizer(batch["text"], truncation=True, padding=True), batched=True
)
dataset.set_format("torch", columns=["input_ids", "attention_mask", "label"])


model = DistilBertForSequenceClassification.from_pretrained(BASE_MODEL_NAME).to(DEVICE)


training_args = TrainingArguments(
    output_dir="./results",
    per_device_train_batch_size=16,
    num_train_epochs=2,
)


trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset["train"],
    eval_dataset=dataset["test"],
)


trainer.train()
model.save_pretrained(FINETUNED_MODEL_NAME)
tokenizer.save_pretrained(FINETUNED_MODEL_NAME)
