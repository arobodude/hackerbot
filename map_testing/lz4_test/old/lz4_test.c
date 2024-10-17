#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <lz4.h>

int main(){
	const char* original_data = "this is an example string";
	int original_size = strlen(original_data) + 1;
	int max_compressed_size = LZ4_compressBound(original_size);
	char* compressed_data = (char*)malloc(max_compressed_size);
	int compressed_size = LZ4_compress_default(original_data, compressed_data, original_size, max_compressed_size);
	if (compressed_size <= 0) {
		fprintf(stderr, "Compression failed!\n Compressed size: %d\n", compressed_size);
		free(compressed_data);
		return 1;
	}
	printf("Original size: %d, Compressed size = %d\n", original_size, compressed_size);

	char* decompressed_data = (char*)malloc(original_size);
	//Decompress the data
	int decompressed_size = LZ4_decompress_safe(compressed_data, decompressed_data, compressed_size, original_size);
	if (decompressed_size < 0){
		fprintf(stderr, "Decompression failed!\n");
		free(compressed_data);
		free(decompressed_data);
		return 1;
	}
	printf("Decompressed size: %d\n", decompressed_size);
	if (strcmp(original_data, decompressed_data) ==0){
		printf("Decompression sucessful!\n");
	}else{
		printf("Decompressed data does not match original!\n");
	}
	
	free(compressed_data);
	free(decompressed_data);
	return 0;
}
