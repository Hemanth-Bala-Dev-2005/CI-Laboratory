import math
import pandas as pd
from collections import Counter
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ----------------------------------------------------------
# Utility Functions (for Manual Mode)
# ----------------------------------------------------------

def entropy(data):
    total = len(data)
    counts = Counter(data)
    ent = 0
    for count in counts.values():
        p = count / total
        ent -= p * math.log2(p)
    return ent

def gini(data):
    total = len(data)
    counts = Counter(data)
    g = 1
    for count in counts.values():
        p = count / total
        g -= p ** 2
    return g

def gain(dataset, attribute, target, criterion):
    target_values = [row[target] for row in dataset]
    parent = entropy(target_values) if criterion == "entropy" else gini(target_values)
    values = set(row[attribute] for row in dataset)
    weighted_impurity = 0
    for val in values:
        subset = [row for row in dataset if row[attribute] == val]
        subset_targets = [row[target] for row in subset]
        weight = len(subset) / len(dataset)
        impurity = entropy(subset_targets) if criterion == "entropy" else gini(subset_targets)
        weighted_impurity += weight * impurity
    return parent - weighted_impurity

def build_tree(dataset, attributes, target, criterion):
    target_values = [row[target] for row in dataset]
    if len(set(target_values)) == 1: return target_values[0]
    if not attributes: return Counter(target_values).most_common(1)[0][0]
    gains = {attr: gain(dataset, attr, target, criterion) for attr in attributes}
    best_attr = max(gains, key=gains.get)
    tree = {best_attr: {}}
    for val in set(row[best_attr] for row in dataset):
        subset = [row for row in dataset if row[best_attr] == val]
        remaining_attrs = [a for a in attributes if a != best_attr]
        tree[best_attr][val] = build_tree(subset, remaining_attrs, target, criterion)
    return tree

def print_manual_tree(tree, indent=""):
    if not isinstance(tree, dict):
        print(indent + "->", tree)
        return
    for attr, branches in tree.items():
        for val, subtree in branches.items():
            print(f"{indent}{attr} = {val}")
            print_manual_tree(subtree, indent + "   ")

def predict(tree, sample):
    if not isinstance(tree, dict): return tree
    attr = next(iter(tree))
    value = sample.get(attr)
    return predict(tree[attr][value], sample) if value in tree[attr] else "Unknown"

# ----------------------------------------------------------
# CSV Mode (using sklearn for processing)
# ----------------------------------------------------------

def csv_mode(criterion):
    path = input("Enter CSV file path: ")
    target_col = input("Enter target column name: ")

    try:
        df = pd.read_csv(path)
    except FileNotFoundError:
        print("Error: File not found.")
        return

    X = df.drop(columns=[target_col])
    y = df[target_col]

    # Convert categorical text data to numeric for sklearn
    le = LabelEncoder()
    for col in X.columns:
        if X[col].dtype == 'object':
            X[col] = le.fit_transform(X[col].astype(str))

    # Store original class names if categorical
    class_names = None
    if y.dtype == 'object':
        y = le.fit_transform(y.astype(str))
        class_names = [str(c) for c in le.classes_]
    else:
        class_names = [str(c) for v, c in enumerate(sorted(y.unique()))]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

    # Initialize and fit the classifier
    model = DecisionTreeClassifier(criterion=criterion)
    model.fit(X_train, y_train)

    # PRINT TREE IN TEXT FORMAT (Similar to Manual Mode style)
    print("\nFINAL DECISION TREE (CSV Data):")
    # export_text prints a human-readable rule set
    tree_rules = export_text(model, feature_names=list(X.columns), class_names=class_names)
    print(tree_rules)

    # Model Evaluation
    y_pred = model.predict(X_test)
    print("\nTOTAL RECORDS:", len(df))
    print("Accuracy :", accuracy_score(y_test, y_pred))
    print("Precision:", precision_score(y_test, y_pred, average='weighted'))
    print("Recall   :", recall_score(y_test, y_pred, average='weighted'))
    print("F1 Score :", f1_score(y_test, y_pred, average='weighted'))

# ----------------------------------------------------------
# Manual Mode
# ----------------------------------------------------------

def manual_mode(criterion):
    n_attr = int(input("Enter number of attributes (excluding target): "))
    attributes = [a.strip() for a in input("Enter attribute names (comma separated): ").split(",")]
    target = input("Enter target class column name: ")
    n = int(input("Enter number of records: "))

    dataset = []
    print(f"\nEnter data rows (comma-separated):")
    for i in range(n):
        vals = [v.strip() for v in input(f"Row {i+1}: ").split(",")]
        row = {attributes[j]: vals[j] for j in range(n_attr)}
        row[target] = vals[-1]
        dataset.append(row)

    tree = build_tree(dataset, attributes, target, criterion)
    print("\nFINAL DECISION TREE (Manual Data):")
    print_manual_tree(tree)

# ----------------------------------------------------------
# Main Menu
# ----------------------------------------------------------

def main():
    while True:
        print("\n===== DECISION TREE MENU =====")
        print("1. Build Decision Tree (Manual Input)")
        print("2. Build Decision Tree (CSV File)")
        print("3. Exit")
        choice = input("Enter choice: ")

        if choice == '3':
            print("Exiting...")
            break

        print("\nChoose Splitting Criterion:\n1. Entropy\n2. Gini Index")
        c = input("Enter choice: ")
        criterion = "entropy" if c == '1' else "gini"

        if choice == '1':
            manual_mode(criterion)
        elif choice == '2':
            csv_mode(criterion)
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    main()
