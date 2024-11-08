from underthesea import sent_tokenize
from googletrans import Translator
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer
from langdetect import detect, LangDetectException

import nltk

nltk.download('punkt')

def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return None

def translate_text(text, dest_language='vi'):
    translator = Translator()
    try:
        translation = translator.translate(text, dest=dest_language)
        translated_text = translation.text.replace('.', '. ')
        return translated_text.strip()
    except Exception as e:
        return f"Không thể dịch văn bản do lỗi: {str(e)}"


def wrap_text(text, max_length=100):
    wrapped_lines = []
    for line in text.split('\n'):
        while len(line) > max_length:
            split_pos = line.rfind(' ', 0, max_length)
            if split_pos == -1:
                split_pos = max_length
            wrapped_lines.append(line[:split_pos])
            line = line[split_pos:].strip()
        wrapped_lines.append(line)
    return '\n'.join(wrapped_lines)





def summarize_vietnamese(text):
    try:

        sentences = sent_tokenize(text)
        if len(sentences) < 1:
            return "Văn bản quá ngắn để tóm tắt."
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = TextRankSummarizer()
        summary = summarizer(parser.document, 2)
        return ' '.join(str(sentence) for sentence in summary)
    except Exception as e:
        return f"Không thể tóm tắt văn bản do lỗi: {str(e)}"


def get_multiline_input(prompt):
    print(prompt)
    lines = []
    while True:
        line = input()
        if line.strip() == "" and lines:
            break
        lines.append(line)
    return '\n'.join(lines)


def is_valid_language_code(code):
    valid_codes = ['en', 'fr', 'zh-cn', 'de', 'es', 'ko', 'ja', 'vi', 'it', 'el', 'tr', 'hi', 'th', 'nl', 'pt', 'ru',
                   'ar']
    return code in valid_codes


def process_translation(summarized_text):
    while True:
        translate_choice = input(
            "\nBạn có muốn chuyển đổi văn bản này sang ngôn ngữ khác không? (yes/no): ").lower().strip()
        if translate_choice == 'yes':
            if not summarized_text:
                print("Không có văn bản nào để dịch. Vui lòng tóm tắt văn bản trước.")
                break
            dest_language = input(
                "Nhập mã ngôn ngữ đích (ví dụ: 'en' cho tiếng Anh, 'fr' cho tiếng Pháp, 'zh-cn' cho tiếng Trung Quốc\n"
                "\t\t\t\t\t\t\t  'de' cho tiếng Đức, 'es' cho tiếng Tây Ban Nha, 'ko' cho tiếng Hàn Quốc\n"
                "\t\t\t\t\t\t\t  'ja' cho tiếng Nhật Bản, 'it' cho tiếng Ý, ...): ").lower()
            if not is_valid_language_code(dest_language):
                print(
                    "Mã ngôn ngữ không hợp lệ. Các mã hợp lệ bao gồm: 'en', 'fr', 'zh-cn', 'de', 'es', 'ko', 'ja', 'vi', 'it', 'el', 'tr', 'hi', 'th', 'nl', 'pt', 'ru', 'ar'. Vui lòng thử lại.")
                continue
            print("Đang dịch văn bản... Vui lòng chờ.")
            translated_text = translate_text(summarized_text, dest_language)
            print(f"\n--- Văn bản đã dịch (sang {dest_language}) ---")
            print(wrap_text(translated_text))

        elif translate_choice == 'no':
            print("Không thực hiện chuyển đổi ngôn ngữ. Thoát chương trình.")
            break  # Thêm lệnh thoát ngay lập tức
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


def main_menu():
    summarized_texts = []  # Danh sách lưu các tóm tắt đã thực hiện
    translated_texts = []  # Danh sách lưu các văn bản đã dịch
    final_summary = ""  # Biến lưu tóm tắt hoàn chỉnh hoặc tóm tắt đơn lẻ

    while True:
        print("\n--- Menu ---")
        print("1: Tóm tắt văn bản")
        print("2: Dịch văn bản sang tiếng Việt")
        print("0: Thoát")
        choice = input("Chọn một tùy chọn: ")

        if choice == '1':
            while True:
                text_to_summarize = get_multiline_input("Nhập văn bản cần tóm tắt (nhấn Enter để kết thúc): ")
                if text_to_summarize.strip() == "":
                    print("Văn bản trống, vui lòng nhập lại.")
                    continue

                print("Đang tóm tắt văn bản... Vui lòng chờ.")
                summarized_text = summarize_vietnamese(text_to_summarize)
                summarized_texts.append(summarized_text)  # Lưu tóm tắt vào danh sách
                print("\n--- Văn bản gốc ---")
                print(wrap_text(text_to_summarize))
                print("\n--- Tóm tắt văn bản ---")
                print(wrap_text(summarized_text))

                another_summary = input("\nBạn có muốn tóm tắt văn bản khác không? (yes/no): ").lower().strip()
                if another_summary == 'no':
                    print("\nChuyển sang chức năng tổng hợp văn bản.")
                    break
                elif another_summary != 'yes':
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

            if summarized_texts:
                while True:
                    # Phát hiện ngôn ngữ của các đoạn văn đã tóm tắt
                    detected_languages = [detect_language(text) for text in summarized_texts]
                    unique_languages = set(detected_languages)

                    if len(unique_languages) > 1:
                        print(f"Các đoạn văn đã tóm tắt có nhiều ngôn ngữ khác nhau: {unique_languages}")
                        while True:
                            dest_language = input(
                                "Chọn ngôn ngữ đích để chuyển đổi tất cả các đoạn văn (ví dụ: 'en' cho tiếng Anh, 'vi' cho tiếng Việt): ").lower()
                            if not is_valid_language_code(dest_language):
                                print("Mã ngôn ngữ không hợp lệ, vui lòng thử lại.")
                            else:
                                print('Đang chuyển đổi ngôn ngữ')
                                # Chuyển tất cả các đoạn văn sang ngôn ngữ đích
                                summarized_texts = [translate_text(text, dest_language) for text in summarized_texts]
                                print(f"Tất cả các đoạn văn đã được dịch sang {dest_language}.")
                                break
                    else:
                        print("Tất cả các đoạn văn đã cùng ngôn ngữ.")

                    combine_choice = input(
                        "\nBạn có muốn tổng hợp các đoạn văn đã tóm tắt thành một đoạn văn hoàn chỉnh không? (yes/no): ").lower().strip()
                    if combine_choice == 'yes':
                        final_summary = ' '.join(summarized_texts)
                        print("\n--- Tóm tắt hoàn chỉnh ---")
                        print(wrap_text(final_summary))
                        break
                    elif combine_choice == 'no':
                        print("\nKhông tổng hợp các tóm tắt, sử dụng tóm tắt cuối cùng để chuyển đổi ngôn ngữ.")
                        final_summary = summarized_texts[-1]
                        break
                    else:
                        print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
                # Sau khi tóm tắt hoặc tổng hợp, hỏi về việc chuyển đổi ngôn ngữ
                process_translation(final_summary)




        elif choice == '2':
            while True:
                text_to_translate = get_multiline_input("Nhập văn bản cần dịch (nhấn Enter để kết thúc): ")
                if text_to_translate.strip() == "":
                    print("Văn bản trống, vui lòng nhập lại.")
                    continue

                print("Đang dịch văn bản... Vui lòng chờ.")
                translated_text = translate_text(text_to_translate)
                translated_texts.append(translated_text)  # Lưu văn bản đã dịch vào danh sách
                print("Văn bản gốc: ", wrap_text(text_to_translate))
                print("\n--- Kết quả dịch ---")
                print("Văn bản đã dịch (sang tiếng Việt):", wrap_text(translated_text))
                another_translation = input("\nBạn có muốn dịch văn bản khác không? (yes/no): ").lower().strip()
                if another_translation == 'no':
                    print("\nChuyển sang chức năng tổng hợp văn bản đã dịch.")
                    break
                elif another_translation != 'yes':
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            # Vòng lặp hỏi người dùng có muốn tổng hợp các văn bản đã dịch
            if translated_texts:
                while True:
                    combine_translated_choice = input(
                        "\nBạn có muốn tổng hợp các văn bản đã dịch thành một đoạn văn hoàn chỉnh không? (yes/no): ").lower().strip()
                    if combine_translated_choice == 'yes':
                        final_summary = ' '.join(translated_texts)  # Ghép các đoạn dịch thành một văn bản
                        print("\n--- Văn bản đã tổng hợp ---")
                        print(wrap_text(final_summary))
                        break  # Thoát vòng lặp sau khi hoàn thành
                    elif combine_translated_choice == 'no':
                        print("\nKhông tổng hợp các văn bản đã dịch.")
                        final_summary = translated_texts[-1]  # Sử dụng văn bản đã dịch cuối cùng
                        break
                    else:
                        print("Lựa chọn không hợp lệ. Vui lòng thử lại.")
            # Hỏi người dùng có muốn tóm tắt văn bản vừa tổng hợp không
            while final_summary:
                summarize_choice = input("\nBạn có muốn tóm tắt văn bản trên không? (yes/no): ").lower().strip()
                if summarize_choice == 'yes':
                    print(f"\nĐang tóm tắt văn bản: {wrap_text(final_summary)}")
                    summarized_text = summarize_vietnamese(final_summary)
                    summarized_texts.append(summarized_text)  # Lưu tóm tắt vào danh sách
                    print("\n--- Tóm tắt văn bản ---")
                    print(wrap_text(summarized_text))
                    process_translation(final_summary)
                    break
                elif summarize_choice == 'no':
                    print("\nChuyển đổi ngôn ngữ với văn bản đã tổng hợp.")
                    process_translation(final_summary)  # Chuyển đổi ngôn ngữ với văn bản đã tổng hợp
                    break
                else:
                    print("Lựa chọn không hợp lệ. Vui lòng thử lại.")

        elif choice == '0':
            print("Cảm ơn bạn đã sử dụng chương trình! Tạm biệt.")
            break
        else:
            print("Lựa chọn không hợp lệ. Vui lòng thử lại.")


if __name__ == "__main__":
    main_menu()
