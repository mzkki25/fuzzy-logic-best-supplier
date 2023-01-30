import csv
import matplotlib.pyplot as plt

# proses fuzzifikasi
def kualitas_tinggi(n):
    if n >= 80:
        return 1
    elif n <= 70:
        return 0
    else:
        return (n - 70) / (80 - 70)

def kualitas_sedang(n):
    if 50 <= n <= 70:
        return 1
    elif 30 < n < 50:
        return (n - 30) / (50 - 30)
    elif 70 < n < 80:
        return (80 - n) / (80 - 70)
    else:
        return 0

def kualitas_rendah(n):
    if n <= 30:
        return 1
    elif n >= 50:
        return 0
    else:
        return (50 - n) / (50 - 30)

def nilai_kualitas(n):
    tinggi = kualitas_tinggi(n)
    sedang = kualitas_sedang(n)
    rendah = kualitas_rendah(n)
    return tinggi, sedang, rendah

def harga_mahal(n):
    if n >= 8:
        return 1
    elif n <= 6:
        return 0
    else:
        return (n - 6) / (8 - 6)

def harga_sedang(n):
    if 4 <= n <= 6:
        return 1
    elif 2 < n < 4:
        return (n - 2) / (4 - 2)
    elif 6 < n < 8:
        return (8 - n) / (8 - 6)
    else:
        return 0

def harga_murah(n):
    if n <= 2:
        return 1
    elif n >= 4:
        return 0
    else:
        return (4 - n) / (4 - 2)

def nilai_harga(n):
    mahal = harga_mahal(n)
    sedang = harga_sedang(n)
    murah = harga_murah(n)
    return mahal, sedang, murah


# proses inferensi
def fuzzy_rules(murah, sedang, mahal, R, S, T):
    rules = [[max(murah, R), "Bagus"], [max(murah, S), "Bagus"], [max(murah, T), "Bagus"], 
            [max(sedang, R), "Cukup bagus"], [max(sedang, S), "Cukup bagus"], [max(sedang, T), "Bagus"],
            [max(mahal, R), "Tidak bagus"], [max(mahal, S), "Tidak bagus"], [max(mahal, T), "Cukup"]]
    
    bagus = []
    cukup_bagus = []
    tidak_bagus = []

    for rule in rules:
        if rule[1] == "Bagus":
            bagus.append(rule[0])
        elif rule[1] == "Cukup bagus":
            cukup_bagus.append(rule[0])
        elif rule[1] == "Tidak bagus":
            tidak_bagus.append(rule[0])
    
    return max(bagus), max(cukup_bagus), max(tidak_bagus)


# proses defuzzifikasi model sugeno
def sugeno(bagus, cukup_bagus, tidak_bagus):
    try:
        nilai = (bagus * 100 + cukup_bagus * 75 + tidak_bagus * 50) / (bagus + cukup_bagus + tidak_bagus)
    except ZeroDivisionError:
        nilai = 0
    return nilai
    
# plot grafik fungsi keanggotaan
def plot():
    arange_kualitas = [i for i in range(1, 100)]
    plt.plot(arange_kualitas, [kualitas_tinggi(x) for x in arange_kualitas], color='red')
    plt.plot(arange_kualitas, [kualitas_sedang(x) for x in arange_kualitas], color='green')
    plt.plot(arange_kualitas, [kualitas_rendah(x) for x in arange_kualitas], color='blue')
    plt.title('Kualitas')
    plt.legend(['Tinggi', 'Sedang', 'Rendah'])
    plt.show()

    arange_harga = [i for i in range(1, 10)]
    plt.plot(arange_harga, [harga_mahal(x) for x in arange_harga], color='red')
    plt.plot(arange_harga, [harga_sedang(x) for x in arange_harga], color='green')
    plt.plot(arange_harga, [harga_murah(x) for x in arange_harga], color='blue')
    plt.title('Harga')
    plt.legend(['Mahal', 'Sedang', 'Murah'])
    plt.show()

# main program
def main():
    kualitas = []
    harga = []
    skor_kelayakan = []
    skor_akhir = []

    with open('supplier.csv', 'r') as csv_input:
        reader = csv.reader(csv_input, delimiter=';')
        next(reader)
        for row in reader:
            kualitas.append(row[1])
            harga.append(row[2])
    
    for i in range(len(kualitas)):
        T, S, R = nilai_kualitas(int(kualitas[i]))
        mahal, sedang, murah = nilai_harga(int(harga[i]))
        bagus, cukup_bagus, tidak_bagus = fuzzy_rules(murah, sedang, mahal, S, R, T)
        nilai = sugeno(bagus, cukup_bagus, tidak_bagus)
        skor_kelayakan.append([nilai, (i+1)])

    skor_kelayakan.sort(reverse=True)
    
    for i in range(5):
        skor_akhir.append(skor_kelayakan[i][1])
    
    with open('supplier sorted.csv', 'w') as csv_output:
        writer = csv.writer(csv_output, lineterminator='\n',)
        writer.writerow(['ID', 'Skor kelayakan', 'Kualitas', 'Harga'])
        for i in range(len(skor_kelayakan)):
            writer.writerow([skor_kelayakan[i][1], skor_kelayakan[i][0], kualitas[skor_kelayakan[i][1]-1], harga[skor_kelayakan[i][1]-1]])
    
    print("Skor kelayakan supplier: ")
    for i in range(len(skor_kelayakan)):
        print("Supplier", skor_kelayakan[i][1], ":", skor_kelayakan[i][0])

    print("\nSupplier yang layak untuk dipilih: ")
    for i in range(len(skor_akhir)):
        print("Supplier", skor_akhir[i])

if __name__ == "__main__":
    main()
    plot()