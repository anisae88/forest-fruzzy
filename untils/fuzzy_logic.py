import matplotlib
matplotlib.use('Agg')

import numpy as np
import matplotlib.pyplot as plt
import skfuzzy as fuzz
import os


def create_rule_graph():

    x = np.arange(0, 101, 1)

    rendah = fuzz.trimf(x, [0, 0, 40])
    sedang = fuzz.trimf(x, [20, 50, 80])
    tinggi = fuzz.trimf(x, [60, 100, 100])

    plt.figure(figsize=(8,5))

    plt.plot(x, rendah, label='Rendah')
    plt.plot(x, sedang, label='Sedang')
    plt.plot(x, tinggi, label='Tinggi')

    plt.title('Fuzzy Membership Hutan')
    plt.xlabel('Persentase Hutan')
    plt.ylabel('Derajat Keanggotaan')
    plt.legend()

    plt.savefig('static/charts/rule_graph.png')
    plt.close()


def fuzzy_analysis(value, idx):

    x = np.arange(0, 101, 1)

    rendah = fuzz.trimf(x, [0, 0, 40])
    sedang = fuzz.trimf(x, [20, 50, 80])
    tinggi = fuzz.trimf(x, [60, 100, 100])

    low_degree = fuzz.interp_membership(x, rendah, value)
    med_degree = fuzz.interp_membership(x, sedang, value)
    high_degree = fuzz.interp_membership(x, tinggi, value)

    if high_degree >= med_degree and high_degree >= low_degree:
        category = "Hutan Lebat"
    elif med_degree >= low_degree:
        category = "Hutan Sedang"
    else:
        category = "Hutan Jarang"

    aggregated = np.fmax(rendah * low_degree,
                 np.fmax(sedang * med_degree,
                          tinggi * high_degree))

    defuzz = fuzz.defuzz(x, aggregated, 'centroid')

    plt.figure(figsize=(8,5))

    plt.plot(x, rendah, label='Rendah')
    plt.plot(x, sedang, label='Sedang')
    plt.plot(x, tinggi, label='Tinggi')

    plt.fill_between(x, aggregated, alpha=0.4)

    plt.axvline(defuzz, color='red', linestyle='--',
                label=f'Defuzzifikasi = {defuzz:.2f}')

    plt.legend()
    plt.title(f'Defuzzifikasi Gambar {idx+1}')

    chart_path = f'static/charts/defuzz_{idx}.png'

    plt.savefig(chart_path)
    plt.close()

    calculation = f"""
    Derajat Rendah : {low_degree:.2f}
    Derajat Sedang : {med_degree:.2f}
    Derajat Tinggi : {high_degree:.2f}
    """

    return {
        'category': category,
        'defuzz': round(defuzz, 2),
        'calculation': calculation,
        'chart': f'charts/defuzz_{idx}.png'
    }
