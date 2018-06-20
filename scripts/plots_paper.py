from modules.data import read_data
import matplotlib.pyplot as plt

plots_path = "files/plots_paper/"
file_name = plots_path + "players_distribution_per_cluster"
data = read_data("df_w_metrics_all")

clusters = data["cluster"].values
num_occur = [0] * (max(clusters) + 1)

for i in clusters:
    num_occur[i] += 1

labels = []

for i in num_occur:
    labels.append((i / len(clusters)) * 100)

plt.bar(range(1, max(clusters) + 2), labels)
plt.ylabel("Porcentagem")
plt.xlabel("Número do grupo")
plt.xticks(range(1, max(clusters) + 2))
plt.title("Distribuição dos jogadores por grupo")
plt.savefig(file_name)
print('Graph %s saved.' % file_name)
plt.clf()