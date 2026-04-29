from collections import deque, Counter

class PredictionSmoother:
    def __init__(self, window=15, threshold=0.6):
                             #20           #0.75
        self.window = deque(maxlen=window)
        self.threshold = threshold

    def update(self, label):
        if label is None:
            return None

        self.window.append(label)

        if len(self.window) < self.window.maxlen:
            return None

        counts = Counter(self.window)
        dominant, freq = counts.most_common(1)[0]

        if freq / len(self.window) >= self.threshold:
            self.window.clear()
            return dominant

        return None
