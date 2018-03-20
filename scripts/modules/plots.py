import matplotlib.pyplot as plt
import numpy as np
import matplotlib._color_data as mcd
import seaborn as sns


def plot_clusters(data, attribute_names, plots_path, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    fig, ax = plt.subplots()

    for experiment in data.keys():
        experiment_type = experiment.split('_')[0]
        for i, attr in enumerate(attribute_names[experiment_type]):
            plt.title('Experiment: %s - attribute: %s' % (experiment, attr))

            plot_data = []
            labels = []
            n = 0
            for cluster in data[experiment]['clusters']:
                cluster = np.array(cluster)
                plot_data.append(cluster[:, i])
                labels.append('Cluster %d' % (n + 1))
                n += 1

            plt.boxplot(plot_data, False, '', labels=labels)
            plot_file = plots_path + experiment + '_' + attr + '.png'
            plt.savefig(plot_file)
            print('Graph %s saved.' % plot_file)
            if show_plots:
                plt.show()
            plt.clf()


def plot_inertia(data, file_name, cluster_list, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    fig, ax = plt.subplots()

    plot_data = []
    labels = []
    colors = []
    pallete = mcd.CSS4_COLORS
    pallete = list(pallete.keys())

    data_sorted = sorted(data.items(), key=lambda x: str(x[0]))

    for iteration, (experiment, value) in enumerate(data_sorted):
        labels.append(experiment)
        plot_data.append(value['inertia'])
        colors.append(
            pallete[len(pallete) - (iteration % len(cluster_list)) - 1])
    groups = np.arange(len(data.keys()))
    width = 0.35

    plt.bar(groups, plot_data, width, tick_label=labels, color=colors)
    plt.xticks(groups, labels, rotation=90)
    plt.title("Inertia for each experiment")
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    if show_plots:
        plt.show()
    plt.clf()


def plot_counts(data, cluster_list, plots_path, show_plots):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 12

    titles = {}

    for experiment in data.keys():
        titles[experiment.split('_')[0]] = "Clusters with the experiment \"" + experiment.split('_')[0] + \
            "\" running the k-means for k = " + str(cluster_list)

    data_sorted = sorted(data.items(), key=lambda x: x[0])

    for iteration, (experiment, value) in enumerate(data_sorted):
        plot_data = []
        labels = []
        i = 1
        for c in value['clusters']:
            plot_data.append(len(c))
            labels.append('Cluster ' + str(i))
            i += 1

        tam = len(cluster_list)
        if iteration % tam == 0:
            fig, axes = plt.subplots(1, tam)
            axes[iteration % tam].pie(plot_data, autopct='%1.1f%%')
            axes[iteration % tam].axis('equal')
            axes[iteration % tam].set_title("k = " + str(len(labels)))
        elif iteration % tam >= 1 and iteration % tam < tam - 1:
            axes[iteration % tam].pie(plot_data, autopct='%1.1f%%')
            axes[iteration % tam].axis('equal')
            axes[iteration % tam].set_title("k = " + str(len(labels)))
        else:
            axes[iteration % tam].pie(plot_data, autopct='%1.1f%%')
            axes[iteration % tam].axis('equal')
            axes[iteration % tam].set_title("k = " + str(len(labels)))
            file_name = plots_path + experiment.split('_')[0] + '_pie.png'
            plt.suptitle(titles[experiment.split('_')[0]], fontsize=20)
            plt.savefig(file_name)
            print('Graph %s saved.' % file_name)
            if show_plots:
                plt.show()
            plt.clf()


def plot_distributions(data, attribute_names, plots_path, show_plots, norm):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18.0

    for attr in attribute_names:
        if norm:
            ax = sns.distplot(data[attr])
        else:
            ax = sns.distplot(data[attr], kde=False)
        title = attr + ' distribution'
        if norm:
            title += ' - normalized'
        plt.suptitle(title, fontsize=20)
        file_name = plots_path + attr + '_dist'
        if norm:
            file_name += '_norm'
        file_name += '.png'
        plt.savefig(file_name)
        print('Graph %s saved.' % file_name)
        if show_plots:
            plt.show()
        plt.clf()


def plot_all_sep_distributions(data, attribute_names, plots_path, show_plots, norm):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18

    f, axarr = plt.subplots(3, 3, sharey=True)

    i = 0
    j = 0

    for attr in attribute_names:
        if norm:
            sns.distplot(data[attr], ax=axarr[i, j])
        else:
            sns.distplot(data[attr], ax=axarr[i, j], kde=False)
        title = attr + ' distribution'
        if norm:
            title += ' - normalized'
        axarr[i, j].set_title(title)
        j += 1
        if j == 3:
            j = 0
            i += 1
    if show_plots:
        plt.show()
    file_name = plots_path + 'all_sep_dist'
    if norm:
        file_name += '_norm'
    file_name += '.png'
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    plt.clf()


def plot_all_distributions(data, attribute_names, plots_path, show_plots, norm):
    # config output images
    plt.rcParams["figure.figsize"] = (25, 16)
    plt.rcParams['font.size'] = 18

    for attr in attribute_names:
        if norm:
            sns.distplot(data[attr], label=attr)
        else:
            sns.distplot(data[attr], label=attr, kde=False)

    title = 'All distributions'
    if norm:
        title += ' - normalized'
    plt.suptitle(title, fontsize=20)
    plt.legend()
    if show_plots:
        plt.show()
    file_name = plots_path + 'all_dist'
    if norm:
        file_name += '_norm'
    file_name += '.png'
    plt.savefig(file_name)
    print('Graph %s saved.' % file_name)
    plt.clf()
