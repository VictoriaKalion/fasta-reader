"""
Демонстрационная программа для работы с FASTA файлами.
"""
import os
import sys

# Добавляем папку src в путь Python
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from fasta_reader import FastaReader, Seq

def demonstrate_small_file():
    """Демонстрация работы с маленьким файлом."""
    print("=== Демонстрация работы с маленьким файлом ===")

    # Создаем тестовый FASTA файл
    test_fasta = """>seq1 protein sequence
MVLSPADKTNVKAAWGKVGAHAGEYGAEALERMFLSFPTTKTYFPHFDLSHGSAQVKGHGKKVADALTNAVAHVDDMPNALSALSDLHAHKLRVDPVNFKLLSHCLLVTLAAHLPAEFTPAVHASLDKFLASVSTVLTSKYR
>seq2 nucleotide sequence
ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG
ATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCGATCG
>seq3 another protein
MKTVETFKLVAASVFLLISLCFSSCSLVSNT"""

    with open('test_small.fasta', 'w') as f:
        f.write(test_fasta)

    # Демонстрируем работу
    reader = FastaReader('test_small.fasta')

    print(f"Файл валидный: {reader.is_valid_fasta()}")
    print("\nПоследовательности:")

    for i, seq in enumerate(reader.read_sequences()):
        print(f"{i+1}. {seq.header}")
        print(f"   Длина: {len(seq)}")
        print(f"   Тип: {seq.get_alphabet()}")
        print(f"   Первые 50 символов: {seq.sequence[:50]}...")
        print()

def demonstrate_large_file_optimization():
    """Демонстрация оптимизации для больших файлов."""
    print("\n=== Демонстрация оптимизации для больших файлов ===")

    # Создаем большой тестовый файл
    print("Создание большого тестового файла...")
    with open('test_large.fasta', 'w') as f:
        for i in range(1000):
            f.write(f">sequence_{i}\n")
            f.write("ATCG" * 50 + "\n")  # 200 символов на последовательность

    reader = FastaReader('test_large.fasta')

    # Используем генератор для эффективной обработки :cite[4]
    total_length = 0
    sequence_count = 0

    for seq in reader.read_sequences():
        total_length += len(seq)
        sequence_count += 1

        # Показываем прогресс каждые 100 последовательностей
        if sequence_count % 100 == 0:
            print(f"Обработано последовательностей: {sequence_count}")

    print(f"Итого: {sequence_count} последовательностей, общая длина: {total_length}")

if __name__ == "__main__":
    demonstrate_small_file()
    demonstrate_large_file_optimization()