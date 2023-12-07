from matplotlib import pyplot as plt


class MetricCalculator:
    def __init__(self, total, relevant_no_relevant, relevant):
        self.total = total
        self.relevant_no_relevant = relevant_no_relevant
        self.relevant = relevant

    def precision(self):
        # Расчет точности
        precision = len(self.relevant) / (len(self.relevant) + len(self.relevant_no_relevant))
        return precision

    def recall(self):
        # Расчет полноты
        recall = len(self.relevant) / (len(self.relevant) + len(self.total))
        return recall

    def accuracy(self):
        # Расчет аккуратности
        true_negative = len(self.relevant_no_relevant) - len(self.relevant)
        accuracy = (len(self.relevant) + true_negative) / (len(self.total) + true_negative)
        return accuracy

    def error(self):
        # Расчет ошибки
        return 1 - self.accuracy()

    def f_measure(self):
        # Расчет F-меры
        precision = self.precision()
        recall = self.recall()
        if precision + recall == 0:
            return 0.0
        f_measure = 2 * (precision * recall) / (precision + recall)
        return f_measure

    def trec_graph(self, num_points=11):
        precision = round(self.precision() * 100)
        recall = round(self.recall() * 100)
        precision_values = [i / precision for i in range(precision)]
        recall_values = [i / recall for i in range(recall)]

        # Построение графика
        plt.scatter(recall_values, recall_values, s=50, c='b', marker='o')

        plt.xlabel('Recall')
        plt.ylabel('Precision')
        plt.title('TREC Precision-Recall Curve')
        plt.grid(True)
        plt.savefig('app/static/trec_graph.png')  # Сохранение графика в файл

        return precision_values, recall_values

    def average_metrics(self):
        # Расчет усредненных метрик
        num_metrics = 5  # Число метрик, которые усредняются
        precision = self.precision()
        recall = self.recall()
        accuracy = self.accuracy()
        error = self.error()
        f_measure = self.f_measure()
        average_metrics = (precision + recall + accuracy + error + f_measure) / num_metrics
        return average_metrics
