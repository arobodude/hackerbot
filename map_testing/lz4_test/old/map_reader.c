#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <lz4.h>

// Function to convert hex string to binary data
int hex_to_bytes(const char* hex_str, unsigned char* output, int output_size) {
    int hex_len = strlen(hex_str);
    if (hex_len % 2 != 0) {
        fprintf(stderr, "Invalid hex string length.\n");
        return -1;
    }
    
    int expected_size = hex_len / 2;
    if (expected_size > output_size) {
        fprintf(stderr, "Output buffer too small for hex conversion.\n");
        return -1;
    }

    for (int i = 0; i < expected_size; i++) {
        sscanf(hex_str + 2 * i, "%2hhx", &output[i]);
    }
    
    return expected_size;
}

int main() {
    // File containing hex string
    const char* filename = "compressed_hex.txt";
    FILE* file = fopen(filename, "r");
    if (file == NULL) {
        fprintf(stderr, "Could not open file %s\n", filename);
        return 1;
    }

    // Read the hex string from the file
    fseek(file, 0, SEEK_END);
    long file_size = ftell(file);
    fseek(file, 0, SEEK_SET);

    char* hex_str = (char*)malloc(file_size + 1);
    if (hex_str == NULL) {
        fprintf(stderr, "Memory allocation failed for hex string\n");
        fclose(file);
        return 1;
    }
    
    fread(hex_str, 1, file_size, file);
    hex_str[file_size] = '\0';  // Null-terminate the string
    fclose(file);

    // Allocate buffer for binary compressed data
    int binary_size = file_size / 2;
    unsigned char* compressed_data = (unsigned char*)malloc(binary_size);
    if (compressed_data == NULL) {
        fprintf(stderr, "Memory allocation failed for compressed data\n");
        free(hex_str);
        return 1;
    }

    // Convert hex string to binary data
    int compressed_size = hex_to_bytes(hex_str, compressed_data, binary_size);
    if (compressed_size < 0) {
        free(hex_str);
        free(compressed_data);
        return 1;
    }

    printf("Compressed size from hex: %d bytes\n", compressed_size);

    // Free hex string as it's no longer needed
    free(hex_str);

    // Decompressed data size (you need to know this size in advance)
    int original_size = 1024;  // Adjust this value to match the actual size of the uncompressed data
    unsigned char* decompressed_data = (unsigned char*)malloc(original_size);
    if (decompressed_data == NULL) {
        fprintf(stderr, "Memory allocation failed for decompressed data\n");
        free(compressed_data);
        return 1;
    }

    // Decompress the data
    int decompressed_size = LZ4_decompress_safe((const char*)compressed_data, (char*)decompressed_data, compressed_size, original_size);
    if (decompressed_size < 0) {
        fprintf(stderr, "Decompression failed! Error code: %d\n", decompressed_size);
        free(compressed_data);
        free(decompressed_data);
        return 1;
    }

    printf("Decompressed size: %d bytes\n", decompressed_size);

    // Optionally, print decompressed data (if it's a string or readable data)
    printf("Decompressed data: %s\n", decompressed_data);

    // Clean up
    free(compressed_data);
    free(decompressed_data);

    return 0;
}
