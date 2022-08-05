import matplotlib.pyplot as plt
import io

from services import get_dict_of_credits_data


def get_visual_report(labels, cell_text):
    fig, ax = plt.subplots()
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    ax.table(cellText=cell_text, colLabels=labels, loc='center')
    fig.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=600)
    buf.seek(0)
    # plt.show()
    return buf


def get_visual_table_data(report_data: dict):
    cell_text = []
    labels = ['', ]
    for sponsor, consumers in report_data.items():
        for consumer, money in consumers.items():
            if consumer.name not in labels:
                labels.append(consumer.name)

    for sponsor, consumers in report_data.items():
        row = [sponsor.name, ]
        for consumer, money in consumers.items():
            while len(row) < len(labels):
                row.append('0')
            row.insert(labels.index(consumer.name), money)
            row.pop(-1)
        cell_text.append(row)
    return labels, cell_text
