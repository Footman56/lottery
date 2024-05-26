from flask import Flask, request, render_template, send_file
import os
import itertools

app = Flask(__name__)


class Lottery:
    def __init__(self, set1=set(), set2=set(), m=None, n=None, Q=None, M=None):
        self.set1 = set(set1)
        self.set2 = set(set2)
        self.m = m
        self.n = n
        self.Q = Q
        self.M = M

    def find_valid_combinations(self):
        valid_combinations = []

        # Generate all possible combinations of a, b, c, d, e, f in the range [1, 33]
        numbers = [i for i in range(1, 34) if i not in self.set2]

        for combination in itertools.combinations(numbers, 6):
            if self.set1 and not self.set1.issubset(set(combination)):
                continue
            a, b, c, d, e, f = combination
            sum_M = a + b + c + d + e + f
            if self.M is not None and self.M != sum_M:
                continue
            if self.M is None and (sum_M < 50 or sum_M > 150):
                continue
            evens = len([num for num in combination if num % 2 == 0])
            odds = 6 - evens

            if self.m is not None and self.m != evens:
                continue
            if self.n is not None and self.n != odds:
                continue

            differences = [abs(combination[i] - combination[i + 1]) for i in range(5)]
            max_gap = max(differences)

            if self.Q is not None and self.Q != max_gap:
                continue

            valid_combinations.append(combination)

        return valid_combinations

#  默认页面
@app.route("/",methods=["GET"])
def index():
    return render_template('index.html')


@app.route('/lottery', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        set1 = request.form.get('set1')
        set2 = request.form.get('set2')
        m = request.form.get('m')
        n = request.form.get('n')
        Q = request.form.get('Q')
        M = request.form.get('M')

        set1 = set(map(int, set1.split(','))) if set1 else set()
        set2 = set(map(int, set2.split(','))) if set2 else set()
        m = int(m) if m else None
        n = int(n) if n else None
        Q = int(Q) if Q else None
        M = int(M) if M else None

        lottery = Lottery(set1=set1, set2=set2, m=m, n=n, Q=Q, M=M)
        combinations = lottery.find_valid_combinations()

        output_file = 'download.txt'

        if os.path.exists(output_file):
            os.remove(output_file)
        with open(output_file, 'w') as f:
            for combo in combinations:
                f.write(f"{combo}\n")

        return render_template('download.html')

    return render_template('index.html')


@app.route('/download')
def download_file():
    return send_file('download.txt', as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')
