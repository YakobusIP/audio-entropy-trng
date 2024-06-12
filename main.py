from record import capture_audio_to_file, read_audio_file
from filter import bandpass_filter
from entropy import extract_entropy

def generate_random_number():
    file_name = 'audios/1minute.wav'
    # capture_audio_to_file(file_name)

    audio_data, rate = read_audio_file(file_name)
    filtered_audio = bandpass_filter(audio_data, fs=rate)
    entropy_bits = extract_entropy(filtered_audio)

    # print("Generated Random Numbers:", entropy_bits)

    # Convert entropy bits to a format suitable for the NIST tests
    binary_sequence = entropy_bits

    # Calculate the length of the binary sequence
    binary_sequence_length = len(binary_sequence)
    print(f"Length of the binary sequence: {binary_sequence_length} bits")

    # Save the binary sequence to a text file
    with open('bs-1min.txt', 'w') as file:
        file.write(binary_sequence)

if __name__ == "__main__":
    generate_random_number()