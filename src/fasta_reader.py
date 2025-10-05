class Seq:
    """
    Класс для работы с биологическими последовательностями.

    Attributes:
        header (str): заголовок FASTA записи
        sequence (str): биологическая последовательность
    """

    # Алфавиты для определения типа последовательности
    NUCLEOTIDE_ALPHABET = set('ATCGUNatcgun-')
    PROTEIN_ALPHABET = set('ACDEFGHIKLMNPQRSTVWYacdefghiklmnpqrstvwy-*')

    def __init__(self, header, sequence):
        """
        Args:
            header (str): заголовок FASTA записи
            sequence (str): биологическая последовательность
        """
        self.header = header.strip()
        self.sequence = sequence.replace('\n', '').replace(' ', '').upper()

    def __str__(self):
        """Красивое строковое представление."""
        return f">{self.header}\n{self.sequence}"

    def __len__(self):
        """Возвращает длину последовательности."""
        return len(self.sequence)

    def get_alphabet(self):
        """
        Определяет тип последовательности (нуклеотидная или белковая).

        Returns:
            str: 'nucleotide', 'protein' или 'unknown'
        """
        seq_chars = set(self.sequence)

        if seq_chars.issubset(self.NUCLEOTIDE_ALPHABET):
            return 'nucleotide'
        elif seq_chars.issubset(self.PROTEIN_ALPHABET):
            return 'protein'
        else:
            return 'unknown'

    def __repr__(self):
        """Представление для отладки."""
        return f"Seq(header='{self.header}', sequence='{self.sequence[:20]}...')"


class FastaReader:
    """
    Класс для чтения и валидации FASTA файлов.

    Использует генераторы для эффективной работы с большими файлами :cite[1]:cite[4].
    """

    def __init__(self, file_path):
        """
        Args:
            file_path (str): путь к FASTA файлу
        """
        self.file_path = file_path

    def is_valid_fasta(self):
        """
        Проверяет базовое соответствие файла формату FASTA.

        Returns:
            bool: True если файл валидный, иначе False
        """
        try:
            with open(self.file_path, 'r') as file:
                first_line = file.readline().strip()
                return first_line.startswith('>')
        except Exception:
            return False

    def read_sequences(self):
        """
        Генератор, который читает файл и возвращает последовательности одну за другой.

        Yields:
            Seq: объекты последовательности

        Raises:
            ValueError: если файл не соответствует формату FASTA
        """
        if not self.is_valid_fasta():
            raise ValueError("Файл не соответствует формату FASTA")

        current_header = None
        current_sequence = []

        with open(self.file_path, 'r') as file:
            for line in file:
                line = line.strip()

                if line.startswith('>'):  # Нашли новый заголовок
                    # Если у нас уже есть собранная последовательность, отдаем ее
                    if current_header is not None:
                        yield Seq(current_header, ''.join(current_sequence))

                    # Начинаем новую последовательность
                    current_header = line[1:]  # Убираем '>' в начале
                    current_sequence = []
                else:
                    # Добавляем строку к текущей последовательности
                    current_sequence.append(line)

            # Не забываем отдать последнюю последовательность
            if current_header is not None:
                yield Seq(current_header, ''.join(current_sequence))