from modules.AIModel import SentimentClassifier

print("=== BẮT ĐẦU TRAINING MODEL ===")
model = SentimentClassifier()

# Test đọc file
import pandas as pd
df = pd.read_csv("data/train_clean.csv")
print(f"\n✓ Đọc được file train_clean.csv: {len(df)} dòng")
print(f"✓ Columns: {df.columns.tolist()}")
print(f"\n✓ Sample data:")
print(df.head(3))
print(f"\n✓ Label distribution:")
print(df['label'].value_counts())

# Test tokenize
test_text = df['text'].iloc[0]
tokens = model._token(test_text)
print(f"\n✓ Test tokenize: '{test_text[:50]}...'")
print(f"  Tokens: {tokens[:10]}")

# Train model
print("\n=== TRAINING ===")
try:
    # Directly call train without input
    df = pd.read_csv("data/train_clean.csv")
    X = df["text"]
    Y = df["label"]
    
    for sentences, label in zip(X, Y):
        words = model._token(sentences)
        if label == 0:  # Positive
            model.pos_sentences += 1 
            for word in words:
                model.pos_word[word] = model.pos_word.get(word, 0) + 1 
                model.pos_words_count += 1
        elif label == 2:  # Negative
            model.neg_sentences += 1
            for word in words:
                model.neg_word[word] = model.neg_word.get(word, 0) + 1 
                model.neg_words_count += 1 
        elif label == 1:  # Neutral
            model.neu_sentences += 1 
            for word in words:
                model.neu_word[word] = model.neu_word.get(word, 0) + 1 
                model.neu_words_count += 1
    
    model.dictionary = set(list(model.pos_word) + list(model.neu_word) + list(model.neg_word))
    
    print(f"\n✓ Kết quả training:")
    print(f"  - Positive sentences: {model.pos_sentences}")
    print(f"  - Negative sentences: {model.neg_sentences}")
    print(f"  - Neutral sentences: {model.neu_sentences}")
    print(f"  - Total: {model.pos_sentences + model.neg_sentences + model.neu_sentences}")
    print(f"  - Vocabulary size: {len(model.dictionary)}")
    
    # Save model
    model._saveModel()
    print("\n✓ Đã lưu model!")
    
except Exception as e:
    import traceback
    print(f"\n✗ Lỗi: {e}")
    traceback.print_exc()
