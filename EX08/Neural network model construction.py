import math

def get_activation(yin, choice):
    if choice == '1':  # Bipolar Step
        return 1 if yin > 0 else (-1 if yin < 0 else 0)
    elif choice == '2': # Sigmoid
        return 1 / (1 + math.exp(-yin))
    else: # Tanh
        return math.tanh(yin)

def run_perceptron():
    print("--- Multi-Attribute Perceptron with Detailed Table ---")
    print("1. Step | 2. Sigmoid | 3. Tanh")
    choice = input("Select activation (1/2/3): ")

    try:
        max_epochs = int(input("Max epochs: "))
        lr = float(input("Learning rate: "))
    except ValueError:
        max_epochs, lr = 10, 1.0

    dataset = []
    print("\nEnter row: x1 x2 ... xn target (type 'done')")
    while True:
        raw = input("> ").strip().lower()
        if raw == 'done': break
        try:
            dataset.append(list(map(float, raw.split())))
        except ValueError: pass

    if not dataset: return

    num_attr = len(dataset[0]) - 1
    weights = [0.0] * num_attr
    bias = 0.0

    # Header Construction
    x_h = " ".join([f"x{i+1}" for i in range(num_attr)])
    dw_h = " ".join([f"dw{i+1}" for i in range(num_attr)])
    w_h = " ".join([f"w{i+1}" for i in range(num_attr)])
    header = f"{x_h}  t |  yin     y | {dw_h}  db | {w_h}  b"

    for epoch in range(1, max_epochs + 1):
        updates = 0
        print(f"\n--- EPOCH {epoch} ---")
        print(header)
        print("-" * len(header))

        for row in dataset:
            x_vals = row[:-1]
            target = row[-1]

            # 1. Net Input & Prediction
            yin = bias + sum(x * w for x, w in zip(x_vals, weights))
            y = get_activation(yin, choice)

            # 2. Calculate Deltas
            error = target - y
            if abs(error) > 0.001:
                dw = [lr * error * x for x in x_vals]
                db = lr * error
                updates += 1
            else:
                dw = [0.0] * num_attr
                db = 0.0

            # 3. Update Weights (applied before printing to show current state)
            for i in range(num_attr): weights[i] += dw[i]
            bias += db

            # Formatting
            x_str = " ".join([f"{v:3.0f}" for v in x_vals])
            dw_str = " ".join([f"{v:5.1f}" for v in dw])
            w_str = " ".join([f"{v:5.1f}" for v in weights])

# Change this line in the code for better alignment
            print(f"{x_str} {target:4.0f} | {yin:6.1f} {y:6.1f} | {dw_str} {db:5.1f} | {w_str} {bias:5.1f}")


        if updates == 0:
            print(f"\nConverged at Epoch {epoch}!")
            break
